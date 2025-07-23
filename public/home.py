import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta
import yfinance as yf 
from MCCEFfuncs import *

@st.fragment
def Partners():
    #st.divider()
    st.header((":blue[Partneři]" if not language_on else ":blue[Partners]"))
    ibkr_path =  "assets/company_icons/Interactive_Brokers.svg"
    ibkrsrc = "https://upload.wikimedia.org/wikipedia/commons/c/ca/Interactive_Brokers_Logo_%282014%29.svg"
    deloitte = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Deloitte.svg/1280px-Deloitte.svg.png"
    richfox = "./assets/company_icons/RichFoxLogo.webp" 
    colpar = st.columns([3, 3, 2],)
    with colpar[0]:
        st.markdown(
        f"""
        <div style='display: flex; justify-content: center; align-items: flex-end; height: 80px'>
            <a href="https://www.interactivebrokers.com/">
                <img src="https://upload.wikimedia.org/wikipedia/commons/c/ca/Interactive_Brokers_Logo_%282014%29.svg" width="250" height="50" style="border-radius:0px;">
            </a>
        </div>
        """,
        unsafe_allow_html=True, help=("Obchodní platforma" if not language_on else "Trading Platform")
        )
    with colpar[1]:
        st.markdown(
        """
        <div style='display: flex; justify-content: center; align-items: flex-end; height: 80px'>
            <a href="https://www2.deloitte.com/cz/cs.html">
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Deloitte.svg/1280px-Deloitte.svg.png" width="250" height="50" style="border-radius:0px;">
            </a>
        </div>
        """,
        unsafe_allow_html=True, help=("Revizor účtů" if not language_on else "Auditor")
        )
    with colpar[2]:
        st.markdown(
        """
        <div style='display: flex; justify-content: top; align-items: flex-end; height: 80px'>
            <a href="https://www.richfox.com/assets-management/">
                <img src="https://www.richfox.com/_next/image/?url=%2F_next%2Fstatic%2Fmedia%2Flogo.e7e91d55.png&w=1920&q=75" width="150" height="150" style="border-radius:0px; margin-bottom: -40px;">
            </a>
        </div>
        """,
        unsafe_allow_html=True, help=("Investiční manažer" if not language_on else "Investment Manager")
        )

option_map = {
    0: 'CZ',
    1: 'ENG',
}
time_options = {
    0: "2020",
    1: "2021",
    2: "2022",
    3: "2023",
    4: "2024",
    5: "2025",
    6: "All"
}
cz_c = {
     0: "Kumulativní",
     1: "Sčítací"
}
eng_c = {
     0: "Cumulative",
     1: "Summation"
}

if "language" not in st.session_state:
    st.session_state["language"] = min(option_map.keys())
if "time_sel" not in st.session_state:
    st.session_state["time_sel"] = max(time_options.keys())
if "cumul_sel" not in st.session_state:
    st.session_state["cumul_sel"] = max(cz_c.keys())

coltop = st.columns([14, 2],)
with coltop[0]:
    st.title(":blue[Market Center Concordia Equity Fund]")
with coltop[1]:
    st.markdown(' ')
    language_on = st.pills(label=('Select language' if st.session_state["language"] else 'Vyberte jazyk'), 
                           options = option_map.keys(),
                           format_func = lambda option: option_map[option],
                           selection_mode='single',
                           key='language', 
                           help=("Změna jazyka obsahu: Čeština ⇄ Angličtina." if not st.session_state["language"] else "Change the language of the content Czech ⇄ English."))

 
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

motto_eng = ' *"Success is not about perfection: Just avoid big mistakes and favorable results will naturally follow."* '
title_1_eng = 'About'
text_1_eng = '''The MC Concordia Equity Fund is administrated by Richfox Capital, a long-standing partner based in Switzerland.
                 It is audited by Deloitte and overseen by the Dutch central bank, offering clients reassurance about its management and security.
                 The fund's investment strategy is primarily mathematical, utilizing a proprietary model developed over 15 years to value selected companies. 
                 This approach has earned accolades, including recognition from Bloomberg as one of the top three funds globally in its category.'''
text_2_eng = '''The team, led by mathematical strategist and technical analysts focuses on long-term asset management with holdings often exceeding 10 years.
                The fund emphasizes risk management, using advanced systems to determine safe trading volumes and minimize risk. 
                Their strategy, developed in collaboration with Interactive Brokers since 2007, has navigated through financial crises, 
                demonstrating resilience and profitability. The fund's goal is consistent, rational analysis, focusing on risk reduction 
                rather than chasing short-term gains.'''
text_3_eng = '''You can find more information about us on the website [mcviva.com](https://www.mcviva.com/).'''

cumul_text_cz = (
    "📌 **Kumulativní metoda**: založena na složeném úročení.\n\n"
    "$$1+R_{\\mathrm{c}} = \\prod_{i}(1+R_{\\mathrm{d}, i})$$\n\n"
    "📌 **Sčítací metoda**: jednoduše sčítá denní návratnosti.\n\n"
    "$$R_{\\mathrm{s}} = \\sum_{i}R_{\\mathrm{d}, i}$$"
)
cumul_text_eng = (
    "📌 **Cumulative Method**: Based on compound interest.\n\n"
    "$$1+R_{\\mathrm{c}} = \\prod_{i}(1+R_{\\mathrm{d}, i})$$\n\n"
    "📌 **Summation Method**: Simply sums up daily returns.\n\n"
    "$$R_{\\mathrm{s}} = \\sum_{i}R_{\\mathrm{d}, i}$$"
)
funds_text = """
- **MCCEF: Market Center Concordia Equity Fund**
- **INDU: Dow Jones Industrial Average**
- **SPX: S&P 500**  
- **RUT: Russell 2000 Index**
- **VT: Vanguard Total World Stock**
"""

cumul_help_text = cumul_text_eng if language_on else cumul_text_cz

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

link_positions = 'data/Positions.csv'
#symbs = Portfolio_tickers(link_positions)

#@st.fragment
def Gen_Compare_Funds_Plots(df1, time, cumul):
    is_cumulative = cumul == 0
    df1 = Make_Growth_or_Cumulative_Return(df1, Cumulative=is_cumulative)
    fig = go.Figure()
    times = [2020, 2021, 2022, 2023, 2024, 2025, 'all']
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
                    "<br>Date: %{x}<br>"
                    "Value: %{y:,.2f}%<br>"
                ),
                name=ticker,
                hoverlabel= {'namelength': 0},
                visible=True if (i==0 or i==4) else 'legendonly'
            )
        )
        fig.update_layout(
            xaxis=dict(
                title=("Date" if language_on else "Období"),
                title_font=dict(size=16, #family="Source Sans Pro Bold", 
                                ),
                showgrid=True,
                gridcolor="rgba(200, 200, 200, 0.3)", 
                zeroline=False,
                showline=True,
                linewidth=1,
                tickfont=dict(size=12, #family="Source Sans Pro",
                              ),
                rangeslider = dict(visible=False)
                ),
            yaxis=dict(
                title=("Return" if language_on else "Návratnost"),
                title_font=dict(size=16, #family="Source Sans Pro Bold",
                                ),
                showgrid=True,
                gridcolor="rgba(200, 200, 200, 0.3)",
                zeroline=False,
                showline=True,
                linewidth=1,
                tickfont=dict(size=12, #family="Source Sans Pro",
                              ),
                ticksuffix="%",
                autorange = True
                ),
        )
    return fig

colmotto = st.columns([7, 1],)
with colmotto[0]:
    if not st.session_state['language']:
        st.markdown(''':grey[{}]'''.format(motto_cz))
    else:
        st.markdown(''':grey[{}]'''.format(motto_eng))
with colmotto[0]:
    st.markdown('')

coltext = st.columns([11, 1, 3],)
coltext = st.columns([11],)
with coltext[0]:
    if not st.session_state['language']:
        st.title(title_1_cz)
        st.markdown(text_1_cz)
        st.markdown(text_2_cz)
        st.markdown(text_3_cz)
        st.header('Srovnání s jinými fondy', #help=funds_text
                  )
    else:
        st.title(title_1_eng)
        st.markdown(text_1_eng)
        st.markdown(text_2_eng)
        st.markdown(text_3_eng)
        st.header('Comparison with other Funds', #help=funds_text
                  )
    st.markdown(' ')
    buttons_cols = st.columns([2,1])
    with buttons_cols[0]:
        time_sel = st.segmented_control(
            ("📆 Vyberte časové období" if not language_on else "📆 Select Time Period" ),
            options=time_options.keys(),
            format_func = lambda option: time_options[option],
            selection_mode='single',
            key='time_sel'
        )
    with buttons_cols[1]:
        cumul_sel = st.pills(label=("📈 Vyberte metodu návratnosti" if not language_on else "📈 Select Return Method"),
                             options=cz_c.keys(),
                             format_func=lambda option: eng_c[option] if language_on else cz_c[option],
                             selection_mode='single',
                             key='cumul_sel',
                             help=cumul_help_text
        )
    with st.container(border=True, #height=500
                      ):
        st.plotly_chart(Gen_Compare_Funds_Plots(df, time_sel, cumul_sel), use_container_width=True, #config=config
                    )

    if not st.session_state['language']:
        st.markdown('<span style="font-size:9pt; color: grey;">Poslední aktualizace: 22. července 2025</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span style="font-size:9pt; color: grey;">Last Update: 07/22/2025</span>', unsafe_allow_html=True)
    with st.expander(label=("💬 Vysvětlení zkratek fondů" if not language_on else "💬 Explanation of Fund abbreviations")):
        st.markdown(funds_text)
    Partners()
    
