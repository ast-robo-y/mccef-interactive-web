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
link_sectors = 'data/sectors.csv'
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
def plot_candlestick(df: pd.DataFrame, trades: pd.DataFrame, tick):
    df_trades_ticker = trades[trades["Symbol"] == tick]
    df['1wma'] = df['Close'].rolling(window=7).mean()
    df['1mma'] = df['Close'].rolling(window=30).mean()

    df_trades = df_trades_ticker.copy()
    df_trades["TradeDate"] = df_trades["TradeDate"].dt.tz_localize('America/New_York')
    df_trades = df_trades.set_index("TradeDate")
    df_trades = df_trades[~df_trades.index.duplicated(keep="last")]
    df_trades = df_trades.reindex(df.index, method="ffill").fillna(0)

    ohlc_last_365 = df.loc[(datetime.now(pytz.timezone("America/New_York"))-timedelta(days=365)):]
    ohlc_min = ohlc_last_365["Low"].min()
    ohlc_max = ohlc_last_365["High"].max()

    df_trades_365 = df_trades.loc[(datetime.now(pytz.timezone("America/New_York"))-timedelta(days=365)):]
    tr_min = df_trades_365["QuantityVisual"].min()
    tr_max = df_trades_365["QuantityVisual"].max()

    today = date.today()
    one_y_ago = today - timedelta(days=365)

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        row_heights=[0.7,0.3],
        vertical_spacing = 0.1,
    )
    dashing = 'dot' #'solid' #'dot'
    fig.add_trace(
        go.Scatter(x=df.index,
                y=df['1wma'],
                line = dict(color = 'blue', dash=dashing), name = '1-week MA', opacity=0.6,
                hovertemplate="<b>%{x} :</b>  "+"<b> $%{y:.2f}<extra></extra>"
                ),
                row=1,
                col=1
    )

    fig.add_trace(
        go.Scatter(x=df.index,
                y=df['1mma'],
                line = dict(color = 'magenta', dash=dashing), name = '1-month MA', opacity=0.6,
                hovertemplate="<b>%{x} :</b>  "+"<b> $%{y:.2f}<extra></extra>"
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
        hovertemplate="<b>%{x} :</b>  "+"<b> $%{y:.2f}<extra></extra>"
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
        hovertemplate="<b>%{x} :</b>  "+"<b> $%{y:.2f}<extra></extra>"
    ),
    row=1,
    col=1)

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
                #yaxis='y',
                ),
                row=1,
                col=1)

    fig.add_trace(go.Bar(x=df_trades.index, 
                        y=df_trades['QuantityVisual'], 
                        opacity=0.6, 
                        name='Position',
                        hovertemplate="<b>%{x} :</b>  "+"<b> %{y:.2f} <extra></extra>"
                        ),
                        row=2,
                        col=1
                    )
    fig.data = (
        fig.data[0:2] +   # lines
        fig.data[2:4] +   # scatters
        fig.data[4:]      # candlestick
    )
    fig.update_layout(
        showlegend=True, 
        height=600,
        plot_bgcolor='white',
        xaxis=dict(title='Date', side='bottom', 
                range=[one_y_ago.strftime("%Y-%m-%d"), 
                        (today + timedelta(days=3)).strftime("%Y-%m-%d")],
                        type="date", 
                        rangeselector=dict(buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(step="all")])),
            ),
        xaxis_rangeslider_visible=False,
        yaxis=dict(title="Price", #scaleanchor="x", #overlaying='y2',
                #range=[(2*ohlc_min - ohlc_max), 1.05*ohlc_max],
                ),
        #yaxis2=dict(title="{}".format('% of Max Position'), #side="right",
                    #range=[tr_min-2, 2.2*tr_max]
        #            ),
        yaxis2=dict(title="{}".format('Position Quantity'), #side="right",
                    #range=[tr_min-2, 2.2*tr_max]
                    ),
    ) 
    #fig.layout.yaxis2.showgrid=False

    #fig.update_xaxes(mirror=True, ticks='outside', showline=True, linecolor='black', )
    #fig.update_yaxes(mirror=True, ticks='outside', showline=True, linecolor='black',
    #                gridcolor='lightgrey', fixedrange=False, minor_ticks="outside", ) 
    
    return fig





st.header('Candlestick Plot')
sel_ticker = st.selectbox("Select a Ticker",
                          list(uniq_ticks))

ohlc = tick_OHLC_GEN(sel_ticker)
st.plotly_chart(plot_candlestick(ohlc, trades, sel_ticker))
st.markdown('<span style="font-size:9pt; color: grey;">Last Update: 04/30/2025</span>', unsafe_allow_html=True)
st.divider()


st.header('Actual Positions Held')

@st.fragment
def Treemap_fig(df, colors):
    return My_Treemap(df, colors)

st.plotly_chart(Treemap_fig(portfolio, 'balance'))
st.markdown('<span style="font-size:9pt; color: grey;">Last Update: 04/30/2025</span>', unsafe_allow_html=True)


