import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta
import pytz
import yfinance as yf 
from MCCEFfuncs import *


link_positions = 'data/Positions.csv'
link_trades = 'data/AllTrades.csv'

@st.cache_data
def CSV_data(trades_link: str, position_link: str):
    trades = pd.read_csv(trades_link, parse_dates=['TradeDate'], date_format='%m/%d/%y')
    portfolio = pd.read_csv(position_link)
    return trades, portfolio

trades, portfolio = CSV_data(link_trades, link_positions)
uniq_ticks = np.unique(portfolio['labels'])

@st.cache_data
def tick_OHLC_GEN(tick):
    stock = yf.Ticker(tick)
    ohlc = stock.history(start='2021-01-15', auto_adjust=False)
    return ohlc

@st.fragment
def plot_candlestick(df: pd.DataFrame, trades: pd.DataFrame, portfolio: pd.DataFrame, tick, time):
    df_trades_ticker = trades[trades["Symbol"] == tick]
    df_trades = df_trades_ticker.copy()
    df_trades["TradeDate"] = df_trades["TradeDate"].dt.tz_localize('America/New_York')
    df_trades = df_trades.set_index("TradeDate")
    df_trades = df_trades[~df_trades.index.duplicated(keep="last")]
    df_trades = df_trades.reindex(df.index, method="ffill").fillna(0)

    currency = portfolio[portfolio['labels']==tick]['currency'].values[0]

    df['1wma'] = df['Close'].rolling(window=7).mean()
    df['1mma'] = df['Close'].rolling(window=30).mean()
    
    now_ny = datetime.now(pytz.timezone("America/New_York"))
    today = now_ny.date()
    if time == 0:
        n_days = 90
        start_date = today - timedelta(days=n_days)
    elif time == 1:
        n_days = 182
        start_date = today - timedelta(days=n_days)
    elif time == 2:
        n_days = 365
        start_date = today - timedelta(days=n_days)
    elif time == 3:
        n_days = (today - date(today.year, 1, 1)).days
        start_date = datetime(today.year, 1, 1)
    elif time == 4:
        n_days = (today - df.index.min().date()).days
        start_date = df.index.min()
    if time == 4:
        visible_df = df.copy()
    else:
        visible_df = df[(df.index >= (now_ny-timedelta(n_days))) & (df.index <= now_ny)]
    visible_min = visible_df["Low"].min()
    visible_max = visible_df["High"].max()
    dashing = 'dot' #'solid' #'dot'

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        row_heights=[0.8,0.2],
        vertical_spacing = 0.1,
    )

    fig.add_trace(
        go.Candlestick(
                x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'], 
                name='OHLC', 
                increasing_line_color= '#3D9970',
                increasing_fillcolor='#3D9970',
                decreasing_line_color='#FF4136',
                decreasing_fillcolor='#FF4136',
                ),
                row=1,
                col=1
                )

    fig.add_trace(go.Scatter(
        x=df_trades_ticker[df_trades_ticker["Buy/Sell"]=='BUY']["TradeDate"],
        y=df_trades_ticker[df_trades_ticker["Buy/Sell"]=='BUY']["TradePrice"],
        mode="markers",
        marker=dict(color="green", size=12, symbol="triangle-up", 
                    line=dict(width=1, color='darkblue')),
        name="Buy Trades",
        #hovertemplate=f"<b> BUY %{{x}} :</b>  "+f"<b> %{{y:.2f}} {currency}</b><extra></extra>"
        hovertemplate=f"<span style='color:green'><b>BUY</b></span>: " \
            f"<span style='color:blue'><b>%{{x}}</b></span>: " \
            f"<span style='color:green'><b>%{{y:.2f}} {currency}</b></span><extra></extra>"
    ),
    row=1,
    col=1
    )

    fig.add_trace(go.Scatter(
        x=df_trades_ticker[df_trades_ticker["Buy/Sell"]=='SELL']["TradeDate"],
        y=df_trades_ticker[df_trades_ticker["Buy/Sell"]=='SELL']["TradePrice"],
        mode="markers",
        marker=dict(color="red", size=12, symbol="triangle-down", 
                    line=dict(width=1, color='darkblue')),
        name="Sell Trades",
        #hovertemplate="<b> SELL %{x} :</b>  "+"<b> %{y:.2f}<extra></extra>"
        hovertemplate=f"<span style='color:red'><b>SELL</b></span>: " \
            f"<span style='color:blue'><b>%{{x}}</b></span>: " \
            f"<span style='color:red'><b>%{{y:.2f}} {currency}</b></span><extra></extra>"
    ),
    row=1,
    col=1)

    fig.add_trace(
        go.Scatter(x=df.index,
                y=df['1wma'],
                line = dict(color = 'blue', dash=dashing), name = '1-week MA', opacity=0.6,
                hovertemplate=f"<b> WMA %{{x}} :</b>  "+f"<b> %{{y:.2f}} {currency}<extra></extra>",
                visible='legendonly',
                ),
                row=1,
                col=1,
    )

    fig.add_trace(
        go.Scatter(x=df.index,
                y=df['1mma'],
                line = dict(color = 'magenta', dash=dashing), name = '1-month MA', opacity=0.6,
                hovertemplate=f"<b> MMA %{{x}} :</b>  "+f"<b> %{{y:.2f}} {currency}<extra></extra>",
                visible='legendonly',
                ),
                row=1,
                col=1,
    )

    fig.add_trace(go.Bar(x=df_trades.index, 
                        y=df_trades['QuantityVisual'], 
                        opacity=0.6, 
                        name='Position',
                        hovertemplate="<b>%{x} :</b>  "+"<b> %{y:.2f} <extra></extra>"
                        ),
                        row=2,
                        col=1
                    )
    
    fig.update_layout(
        margin=dict(t=40, b=40, l=50, r=20), 
        showlegend=True, 
        height=650,
        plot_bgcolor='white',
        xaxis2=dict(title=("Date" if language_on else "Období"), side='bottom', type="date",
                range=[start_date, (today + timedelta(days=3))],
                ),
        xaxis_rangeslider_visible=False,
        yaxis=dict(title=("Price ({})".format(currency) if language_on else "Cena ({})".format(currency)),
                range=[visible_min * 0.98, visible_max * 1.02],
                ),
        yaxis2=dict(title=("Position / Max Position (%)" if language_on else "Pozice / Max Pozice (%)"),
                    ),
    ) 
    return fig


option_map = {
    0: 'CZ',
    1: 'ENG',
}
time_options = {
    0: "3M",
    1: "6M",
    2: "1Y",
    3: "YTD",
    4: "All",
}

range_text_cz = """
- **1M**: Poslední 3 měsíce
- **6M**: Poslední půl rok
- **1Y**: Poslední rok 
- **YTD**: Od začátku aktuálního roku
- **All**: Od začátku (2020)
"""
range_text_eng = """
- **1M**: Last 3 Months
- **6M**: Last Half a Year
- **1Y**: Last Year
- **YTD**: Year To Date
- **All**: From the Start (2020)
"""


if "language2" not in st.session_state:
    st.session_state["language2"] = min(option_map.keys())
if "sel_date" not in st.session_state:
    st.session_state["sel_date"] = 2

coltop = st.columns([14, 2],)
with coltop[0]:
    st.header('Candlestick Plot & Trades' if st.session_state["language2"] else 'Svíčkový graf a vykonané obchody')
with coltop[1]:
    st.markdown(' ')
    language_on = st.pills(label=('Select language' if st.session_state["language2"] else 'Vyberte jazyk'), 
                           options = option_map.keys(),
                           format_func = lambda option: option_map[option],
                           selection_mode='single',
                           key='language2', 
                           help=("Změna jazyka obsahu: Čeština ⇄ Angličtina." if not st.session_state["language2"] else "Change the language of the content Czech ⇄ English."))
colsel = st.columns([2,2])
with colsel[0]:
    sel_date = st.segmented_control(
            ("📆 Vyberte časové období" if not language_on else "📆 Select Time Period" ),
            options=time_options.keys(),
            format_func = lambda option: time_options[option],
            selection_mode='single',
            key='sel_date',
            help=(range_text_cz if not language_on else range_text_eng)
        )
with colsel[1]:
    sel_ticker = st.selectbox(("Select a Ticker" if language_on else "Vyberte Ticker"), list(uniq_ticks))

ohlc = tick_OHLC_GEN(sel_ticker)
with st.container(border=True, #height=500
                      ):
    st.plotly_chart(plot_candlestick(ohlc, trades, portfolio=portfolio, tick = sel_ticker, time=sel_date))
if not st.session_state['language2']:
    st.markdown('<span style="font-size:9pt; color: grey;">Poslední aktualizace: 15. srpna 2025</span>', unsafe_allow_html=True)
else:
    st.markdown('<span style="font-size:9pt; color: grey;">Last Update: 08/15/2025</span>', unsafe_allow_html=True)
st.divider()

st.header('Actual Positions Portfolio' if language_on else 'Portfolio aktuálních pozic')

@st.fragment
def Treemap_fig(df, colors):
    return My_Treemap(df, colors)
with st.container(border=True, #height=500
                      ):
    st.plotly_chart(Treemap_fig(portfolio, 'balance'))
if not st.session_state['language2']:
    st.markdown('<span style="font-size:9pt; color: grey;">Poslední aktualizace: 15. srpna 2025</span>', unsafe_allow_html=True)
else:
    st.markdown('<span style="font-size:9pt; color: grey;">Last Update: 08/15/2025</span>', unsafe_allow_html=True)

