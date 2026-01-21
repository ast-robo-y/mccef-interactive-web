import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta
import yfinance as yf 
from MCCEFfuncs import *
import base64


@st.fragment
def Partners():
    #st.divider()
    st.header(":blue[Partneři]")
    ibkr = "assets/company_icons/Interactive_Brokers.svg"
    deloitte = "assets/company_icons/Logo_of_Deloitte.png"
    richfox = "assets/company_icons/RichFoxLogo.webp" 
    bolder = "assets/company_icons/bolder.webp" 

    colpar = st.columns([3, 3, 2, 3],)
    with colpar[0]:
        with open(ibkr, "r", encoding='utf-8') as im_ib:
            ibkr_svg = im_ib.read()
        ibkr_base64 = base64.b64encode(ibkr_svg.encode('utf-8')).decode()
        ib_hover_text = "Obchodní platforma"
        st.markdown(
            f"""
            <style>
            .img-wrap {{
                position: relative;
                display: inline-block;
            }}
            .img-wrap:hover::after {{
                content: attr(data-tooltip);
                position: absolute;
                bottom: 100%;
                left: 50%;
                transform: translateX(-50%);
                background: #333;
                color: white;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 12px;
                white-space: nowrap;
                margin-bottom: 6px;
                z-index: 1000;
            }}
            </style>
            <div style='display: flex; justify-content: center; align-items: flex-end; height: 80px'>
                <div class="img-wrap" data-tooltip="Obchodní platforma">    
                    <a href="https://www.interactivebrokers.com/">
                    <img src="data:image/svg+xml;base64,{ibkr_base64}"
                        width="250" height="50"
                        style="border-radius:0px; "
                    </a>
                </div>
            </div>
            """,
            unsafe_allow_html=True, #help = ib_hover_text
        )
    with colpar[1]:
        with open(deloitte, "rb") as im_del:
            del_png = im_del.read()
        del_base64 = base64.b64encode(del_png).decode()
        del_hover_text = "Revizor účtů"
        st.markdown(
            f"""
            <style>
            .img-wrap {{
                position: relative;
                display: inline-block;
            }}
            .img-wrap:hover::after {{
                content: attr(data-tooltip);
                position: absolute;
                bottom: 100%;
                left: 50%;
                transform: translateX(-50%);
                background: #333;
                color: white;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 12px;
                white-space: nowrap;
                margin-bottom: 6px;
                z-index: 1000;
            }}
            </style>
            <div style='display: flex; justify-content: center; align-items: flex-end; height: 80px'>
                <div class="img-wrap" data-tooltip="Revizor účtů">    
                    <a href="https://www2.deloitte.com/cz/cs.html">
                    <img src="data:image/png;base64,{del_base64}"
                        width="250" height="50"
                        style="border-radius:0px; "
                    </a>
                </div>
            </div>
            """,
            unsafe_allow_html=True, #help = del_hover_text
        )
    with colpar[2]:
        with open(richfox, "rb") as rich:
            rich_bytes = rich.read()
        rich_base64 = base64.b64encode(rich_bytes).decode()
        rf_hover_text = "Investiční manažer"
        st.markdown(
            f"""
            <style>
            .img-wrap {{
                position: relative;
                display: inline-block;
            }}
            .img-wrap:hover::after {{
                content: attr(data-tooltip);
                position: absolute;
                bottom: 100%;
                left: 50%;
                transform: translateX(-50%);
                background: #333;
                color: white;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 12px;
                white-space: nowrap;
                margin-bottom: 6px;
                z-index: 1000;
            }}
            </style>
            <div style='display: flex; justify-content: center; align-items: flex-end; height: 80px'>
                <div class="img-wrap" data-tooltip="Investiční manažer">    
                    <a href="https://www.richfox.com/assets-management/">
                        <img src="data:image/webp;base64,{rich_base64}"
                            width="150" height="150"
                            style="border-radius:0px; margin-bottom:-40px;"
                    </a>
                </div>
            </div>
            """,
            unsafe_allow_html=True, #help = rf_hover_text
        )
    with colpar[3]:
        with open(bolder, "rb") as b:
            b_bytes = b.read()
        b_base64 = base64.b64encode(b_bytes).decode()
        b_hover_text = "Administrátor fondu"
        st.markdown(
            f"""
            <style>
            .img-wrap {{
                position: relative;
                display: inline-block;
            }}
            .img-wrap:hover::after {{
                content: attr(data-tooltip);
                position: absolute;
                bottom: 100%;
                left: 50%;
                transform: translateX(-50%);
                background: #333;
                color: white;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 12px;
                white-space: nowrap;
                margin-bottom: 6px;
                z-index: 1000;
            }}
            </style>
            <div style='display: flex; justify-content: center; align-items: flex-end; height: 80px'>
                <div class="img-wrap" data-tooltip="Administrátor fondu">    
                    <a href="https://boldergroup.com/">
                        <img src="data:image/webp;base64,{b_base64}"
                            width="225" height="125"
                            style="border-radius:0px; margin-bottom:-50px; "
                    </a>
                </div>
            </div>
            """,
            unsafe_allow_html=True, #help = b_hover_text
        )
    st.markdown(' ')
    st.markdown(' ')


time_options = {
    0: "2020",
    1: "2021",
    2: "2022",
    3: "2023",
    4: "2024",
    5: "2025",
    6: "2026",
    7: "All"
}
cz_c = {
     0: "Kumulativní",
     1: "Sčítací"
}
if "time_sel" not in st.session_state or st.session_state['time_sel'] == None:
    st.session_state['time_sel'] = list(time_options.keys())[-1]
if "cumul_sel" not in st.session_state:
    st.session_state["cumul_sel"] = max(cz_c.keys())


st.title(":blue[Market Center Concordia Equity Fund]")

 
motto_cz = ' *„Úspěch není o dokonalosti: Stačí se vyhnout velkým chybám a příznivé výsledky přirozeně následují."* '
title_1_cz = 'O nás'
text_1_cz = '''Akciový fond MC Concordia spravuje společnost Richfox Capital, dlouholetý partner se sídlem ve Švýcarsku. 
               Je auditována společností Deloitte a pod dohledem nizozemské centrální banky, což klientům nabízí ujištění o jejím řízení a zabezpečení.
               Investiční strategie fondu je primárně matematická a využívá proprietární model vyvíjený během 15 let pro oceňování vybraných společností. 
               Tento přístup si vysloužil uznání, včetně uznání od Bloomberg jako jednoho ze tří největších fondů na světě ve své kategorii.'''
text_2_cz = '''Tým vedený matematickým stratégem a technickými analytiky se zaměřuje na dlouhodobou správu aktiv s podíly často přesahujícími 10 let.
               Fond klade důraz na řízení rizik pomocí pokročilých systémů k určení bezpečných objemů obchodů a minimalizaci rizika.
               Jejich strategie, vyvíjená ve spolupráci s Interactive Brokers od roku 2007, prošla finančními krizemi,
               demonstrující odolnost a ziskovost. Cílem fondu je konzistentní, racionální analýza se zaměřením na snižování rizik
               spíše než honit se za krátkodobými zisky.'''
text_3_cz = '''Další informace můžete najít na stránce [mcviva.com](https://www.mcviva.com/).'''

cumul_text_cz = (
    "📌 **Kumulativní metoda**: založena na složeném úročení.\n\n"
    "$$1+R_{\\mathrm{c}} = \\prod_{i}(1+R_{\\mathrm{d}, i})$$\n\n"
    "📌 **Sčítací metoda**: jednoduše sčítá denní návratnosti.\n\n"
    "$$R_{\\mathrm{s}} = \\sum_{i}R_{\\mathrm{d}, i}$$"
)
funds_text = """
- **MCCEF: Market Center Concordia Equity Fund**
- **INDU: Dow Jones Industrial Average**
- **SPX: S&P 500**  
- **RUT: Russell 2000 Index**
- **VT: Vanguard Total World Stock**
"""

cumul_help_text = cumul_text_cz

@st.cache_data
def load_data(l1: str, l2: str):
    return BM_Comparison_Daily(l1, l2)

@st.cache_data
def Portfolio_tickers(l1: str):
    df = Read_pd_csv_Pos(l1, do_date_parse=False)
    eu_ticks = df[df['currency'] == 'EUR'].nlargest(3, 'values')['labels'].tolist()
    us_ticks = df[df['currency'] == 'USD'].nlargest(3, 'values')['labels'].tolist()
    return dict(EU=eu_ticks, US=us_ticks, FX=['EURCZK=X', 'USDCZK=X', 'EURUSD=X'])

link_1 = 'data/1fund.csv'
link_2 = 'data/3funds.csv'
df = load_data(link_1, link_2)
df1 = load_data(link_1, link_2)
df2 = load_data(link_1, link_2)

link_positions = 'data/Positions.csv'

@st.cache_data
def return_mccef_last(df2, time, cumul):
    is_cumulative = cumul == 0
    df2 = Make_Growth_or_Cumulative_Return(df2, Cumulative=is_cumulative)
    times = [2020, 2021, 2022, 2023, 2024, 2025, 2026, 'all']
    return df2[times[time]]['MCCEF'].iloc[-1]

@st.fragment
def Gen_Compare_Funds_Plots(df1, time, cumul):
    is_cumulative = cumul == 0
    df1 = Make_Growth_or_Cumulative_Return(df1, Cumulative=is_cumulative)
    fig = go.Figure()
    times = [2020, 2021, 2022, 2023, 2024, 2025, 2026, 'all']
    tickers = df1[times[time]].columns[1:]
    for i, ticker in enumerate(tickers): 
        fig.add_trace(
            go.Scatter(
                x=df1[times[time]]["Date"],
                y=df1[times[time]][ticker],
                mode="lines",
                hovertext='',
                hoverinfo='text',
                hovertemplate=(
                    f"<b>{ticker}</b>"
                    "<br>Datum: %{x}<br>"
                    "Hodnota: %{y:,.2f}%<br>"
                ),
                name=ticker,
                hoverlabel= {'namelength': 0},
                visible=True if (i==0 or i==4) else 'legendonly'
            )
        )
        fig.update_layout(
            #autosize=True,
            height=550,
            xaxis=dict(
                title="Období",
                title_font=dict(size=16,                                ),
                showgrid=True,
                gridcolor="rgba(200, 200, 200, 0.3)", 
                zeroline=False,
                showline=True,
                linewidth=1,
                tickfont=dict(size=12,                              ),
                rangeslider = dict(visible=False)
                ),
            yaxis=dict(
                title="Návratnost",
                title_font=dict(size=16,                                ),
                showgrid=True,
                gridcolor="rgba(200, 200, 200, 0.3)",
                zeroline=False,
                showline=True,
                linewidth=1,
                tickfont=dict(size=12,                               ),
                ticksuffix="%",
                autorange = True
                ),
        )
    return fig

colmotto = st.columns([7, 1],)
with colmotto[0]:
    st.markdown(''':grey[{}]'''.format(motto_cz))

with colmotto[0]:
    st.markdown('')

#coltext = st.columns([11, 1, 3],)
coltext = st.columns([11],)
with coltext[0]:
    st.title(title_1_cz)
    st.markdown(text_1_cz)
    st.markdown(text_2_cz)
    st.markdown(text_3_cz)
    st.header('Srovnání s jinými fondy',
                )
    st.markdown(' ')
    buttons_cols = st.columns([2,1])
    with buttons_cols[0]:
        time_sel = st.segmented_control(
            "📆 Vyberte časové období" ,
            options=list(time_options.keys()),
            format_func = lambda option: time_options[option],
            selection_mode='single',
            key='time_sel',
        )
    with buttons_cols[1]:
        cumul_sel = st.pills(label="📈 Vyberte metodu návratnosti",
                             options=cz_c.keys(),
                             format_func=lambda option: cz_c[option],
                             selection_mode='single',
                             key='cumul_sel',
                             help=cumul_help_text
        )
    with st.container(border=True, height=600
                      ):
        st.plotly_chart(Gen_Compare_Funds_Plots(df1, time_sel, cumul_sel), #width='stretch',
                    )
        ret_mccef = return_mccef_last(df2, time_sel, cumul_sel)
        st.markdown(
        f"""
        <style>
        .hover-wrap {{
            position: relative;
            display: inline-block;
        }}

        .hover-wrap:hover::after {{
            content: attr(data-tooltip);
            position: absolute;
            bottom: 100%;
            left: 0;
            background: #333;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            white-space: nowrap;
            margin-bottom: 2px;
            z-index: 1000;
        }}
        </style>
        <div style="position: relative;">
            <div class="hover-wrap"
                data-tooltip="Návratnost MCCEF pro zvolené období"
                style="
                    position: absolute;
                    top: -535px;
                    left: 20px;
                    font-size: 24px;
                    font-weight: bold;
                    color: rgba(25,50,100,1);
                    background-color: rgba(255,255,255,0.5);
                    padding: 5px;
                ">
                Návratnost: {round(ret_mccef, 2)} %
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<span style="font-size:9pt; color: grey;">Poslední aktualizace: 21. leden 2026</span>', unsafe_allow_html=True)
    with st.expander(label="💬 Vysvětlení zkratek fondů"):
        st.markdown(funds_text)
    Partners()
