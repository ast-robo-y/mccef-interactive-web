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
    df_1 = Read_pd_csv_BM(link_1BM, skiprows=0,)
    df_2 = Read_pd_csv_BM(link_3BM, skiprows=0,)
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
