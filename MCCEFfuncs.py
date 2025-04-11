import pandas as pd
import numpy as np
from datetime import datetime
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go

def Read_pd_csv_BM(link: str, skiprows: int = 0, do_date_parse: bool = True):
    if do_date_parse:
        return pd.read_csv(link, 
                           skiprows=skiprows,
                           parse_dates=['Date'], 
                           date_format='%m/%d/%y',
                           )
    else:
        return pd.read_csv(link,
                           skiprows=skiprows,
                           )
    
def Read_pd_csv_Pos(link: str, skiprows: int = 0, do_date_parse: bool = True):
    if do_date_parse:
        return pd.read_csv(link, 
                           skiprows=skiprows,
                           parse_dates=['ReportDate'], 
                           date_format='%Y%m%d',
                           )
    else:
        return pd.read_csv(link, 
                           skiprows=skiprows,
                           )

def BM_Comparison_Daily(link_1BM: str, link_3BM: str, ) -> dict:
    df_1 = Read_pd_csv_BM(link_1BM, skiprows=7,)
    df_2 = Read_pd_csv_BM(link_3BM, skiprows=7,)
    if len(df_1.columns.values)==7 and len(df_2.columns.values)==11:
        pass
    else:
        temp = df_1.copy()
        df_2 = df_1.copy()
        df_1 = temp
    date = df_2['Date'].values[:-1]
    BM_1 = df_2['BM1Return'].values[:-1]
    BM_2 = df_2['BM2Return'].values[:-1]
    BM_3 = df_2['BM3Return'].values[:-1]
    BM_4 = df_1['BM1Return'].values[:-1]
    MCCEF = df_2['ConsolidatedReturn'].values[:-1]

    list_of_tuples = list(zip(date, BM_1, BM_2, BM_3, BM_4, MCCEF))
    df = pd.DataFrame(list_of_tuples, columns=['Date', 
                                                      np.unique(df_2['BM1'].values[:-1])[0], 
                                                      np.unique(df_2['BM2'].values[:-1])[0], 
                                                      np.unique(df_2['BM3'].values[:-1])[0], 
                                                      np.unique(df_1['BM1'].values[:-1])[0], 'MCCEF' ])
    dataframes_by_year={year: group.reset_index(drop=True) for year, group in df.groupby(df['Date'].dt.year)}
    dataframes_by_year['all'] = df
    return dataframes_by_year

def Cumul_Return_Calculation(l: list) -> float:
    CRet = 1
    for i in range(len(l)):
        CRet = (1+l[i]*10**(-2))*CRet
    return 100*CRet-100

def Make_Growth_or_Cumulative_Return(d: dict, Cumulative: bool = False, ) -> dict:
    if not Cumulative:
        for frame in d:
            d[frame].iloc[:, 1:] = d[frame].iloc[:, 1:].cumsum()
        return d
    else:
        for frame in d:
            for tick in d[frame].columns[1:]:
                d[frame][tick] = 100*((1+d[frame][tick]*10**(-2)).cumprod()-1)
        return d
    
def Repair_EU_Tickers(df: pd.DataFrame) -> pd.DataFrame:
    ticks = list(df['Symbol'].values)
    bad_ticks = ['8TRA', 'DBK', 'HAG', 'R3NK', 'RHM', 'SAP', 'VOW3', 'BARC', 'ETL', #aktualne tickre
                 'ALVd', 'ATVI', 'BASd', 'BRK B', 'CHF.USD', 'EUR.USD', 'ROG', 'VAR1d', 'WIZZ', 'ZALd']
    good_ticks = ['8TRA.DE', 'DBK.DE', 'HAG.F', 'R3NK.DE', 'RHM.DE', 'SAP.DE', 'VOW3.DE', 'BARC.L', 'ETL.PA', #aktualne tickre
                  'ALV.DE', 'AIY.DE', 'BAS.DE', 'BRK-B', 'CHFUSD=X', 'EURUSD=X', 'ROG.SW', 'VAR1.DE', 'WIZZ.L', 'ZAL.DE']
    for i in range(len(ticks)):
        if ticks[i] in bad_ticks:
            ticks[i] = good_ticks[bad_ticks.index(ticks[i])]
        else:
            if ticks[i].endswith("d"):
                ticks[i] = ticks[i][:-1] + ".DE"
            else:
                pass
                
    df.loc[:, 'Symbol'] = ticks
    return df


def Assign_Sectors(df: pd.DataFrame, sec_df: pd.DataFrame, out_link: str) -> pd.DataFrame:
    df[['Sectors', 'Currency', 'Description']] = None
    symbol_to_sector_currency = dict(zip(sec_df['Symbol'], zip(sec_df['Sectors'], sec_df['Currency'], sec_df['Description'])))

    new_symbol_sector_currency = []
    for index, row in df.iterrows():
        ticker = row['Symbol']
        if ticker in symbol_to_sector_currency:
            df.loc[index, ['Sectors', 'Currency', 'Description']] = symbol_to_sector_currency[ticker]
        else:
            try:
                ticker_info = yf.Ticker(ticker).info
                sector = ticker_info.get('sector', 'Unknown')
                currency = ticker_info.get('currency', 'Unknown')
                desc = ticker_info.get('longName', 'Unknown')
                df.loc[index, ['Sectors', 'Currency', 'Description']] = [sector, currency, desc]
                new_symbol_sector_currency.append((ticker, sector, currency, desc))
            except Exception as e:
                print(f"Vyskytol sa error pri obsadzovani sektora a meny pre {ticker}: {e}")
                df.loc[index, ['Sectors', 'Currency', 'Description']] = [None, None, None]

    if new_symbol_sector_currency:
        new_entries = pd.DataFrame(new_symbol_sector_currency, columns=['Symbol', 'Sectors', 'Currency', 'Description'])
        sec_df = pd.concat([sec_df, new_entries], ignore_index=True).drop_duplicates(subset=['Symbol'])
        sec_df = sec_df.sort_values(by='Symbol').reset_index(drop=True)
        sec_df.to_csv(out_link, index=False)
    return df

def get_treemap_data(link_pos: str, link_sec: str ) -> pd.DataFrame:
    #cols = ['Symbol', 'Description', 'ReportDate', 'MarkPrice', 'PositionValue']
    cols = ['Symbol', 'MarkPrice', 'PositionValue']
    df = Read_pd_csv_Pos(link_pos, do_date_parse=False)[cols].copy()
    df = df[df["PositionValue"] >= 0]
    df = Repair_EU_Tickers(df)

    sec_df = Read_pd_csv_Pos(link_sec, do_date_parse=False)
    df = Assign_Sectors(df=df, sec_df=sec_df, out_link=link_sec)
    percents = [num for num in list(df['PositionValue'].values/np.sum(list(df['PositionValue'].values))*100)]
    
    return pd.DataFrame({
                            'labels': list(df['Symbol'].values),
                            'parents': list(df['Sectors'].values),
                            'values': percents,
                            'names': list(df['Description'].values),
                            'color': percents,
                            'currency': list(df['Currency'].values)
                        })

def My_Treemap(df: pd.DataFrame, color_continuous_scale: str):
    fig = px.treemap(df,
            path=[px.Constant('Portfolio'), 'parents', 'labels'], 
            values='values',
            custom_data=['names'], 
            color='color',
            color_continuous_scale=color_continuous_scale,
        )

    ids = fig.data[0].ids
    depths = [id_.count('/') for id_ in ids]

    hover_templates = []
    for depth, id_ in zip(depths, ids):
        if depth == 0:  # 'All' level
            hover_templates.append('<b>%{label}</b><br>Portfolio Total %: %{value:.0f}')
        elif depth == 1:  # Sector level
            hover_templates.append('<b>%{label}</b><br>Sector Total %: %{value:.2f}')
        else:  # Ticker level
            hover_templates.append('<b>%{label}</b><br>Name: %{customdata[0]}<br>Portfolio %: %{value:.2f}<extra></extra>')

    fig.update_traces(hovertemplate=hover_templates,
                      marker=dict(cornerradius=5,
                              ),
        )
    fig.update_layout(
        margin=dict(t=50, l=20, r=25, b=25),
        width=500,
        height=400,
        coloraxis_showscale=False
        )
    return fig

'''
def My_Treemap(df: pd.DataFrame, color_continuous_scale: str):
    def generate_id(row):
        return f"Portfolio/{row['parents']}/{row['labels']}" if row['parents'] != 'Portfolio' else f"Portfolio/{row['labels']}"

    ids = df.apply(generate_id, axis=1)
    parents_ids = df['parents'].apply(lambda p: f"Portfolio/{p}" if p != 'Portfolio' else 'Portfolio')

    fig = go.Figure(go.Treemap(
        labels=df['labels'],
        parents=df['parents'],
        values=df['values'],
        customdata=df['names'],
        marker=dict(
            colors=df['color'],
            colorscale=color_continuous_scale,
            showscale=False,
            cornerradius=5  # only supported in Plotly 5.16+
        ),
        hovertemplate='',  # we’ll set it dynamically below
        texttemplate='%{label}',
        textfont=dict(size=14),
        #insidetextorientation='auto',
        textposition='middle center'
    ))

    # Create hovertemplate per depth level
    #ids = fig.data[0].ids
    depths = [id_.count('/') for id_ in ids]

    hover_templates = []
    for depth, id_ in zip(depths, ids):
        if depth == 0:  # Portfolio root
            hover_templates.append('<b>%{label}</b><br>Portfolio Total %: %{value:.0f}')
        elif depth == 1:  # Sector level
            hover_templates.append('<b>%{label}</b><br>Sector Total %: %{value:.2f}')
        else:  # Ticker level
            hover_templates.append('<b>%{label}</b><br>Name: %{customdata[0]}<br>Portfolio %: %{value:.2f}<extra></extra>')

    fig.data[0].hovertemplate = hover_templates

    # Layout tweaks
    fig.update_layout(
        margin=dict(t=50, l=20, r=25, b=25),
        width=500,
        height=400
    )

    return fig
'''

def Update_Trades(link_trades: str, download: bool=False) -> pd.DataFrame:
    trades = pd.read_csv(link_trades, parse_dates=['TradeDate'], date_format='%Y-%m-%d')
    Repair_EU_Tickers(trades)

    trades["QuantityVisual"] = trades.groupby("Symbol", group_keys=False).apply(
    lambda group: 100*group["DefaultPositions"] / (
        group["DefaultPositions"].max() if group["DefaultPositions"].max() > 0 else np.abs(group["DefaultPositions"]).max()
        )).reset_index(drop=True)
    '''
    Toto zarucuje ze mam normalizovane na 1 pre pozitivne maximum kumulativnej pozice, no ak 
    mame len Shorty  -> maximumm je nula, no nanormovane je to na globalne minimum = negativne maximum
    '''
    if download:
        trades.to_csv(link_trades, index=False)
    return trades


