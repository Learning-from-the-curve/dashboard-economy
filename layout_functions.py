import numpy as np 
import pandas as pd
from pickle_functions import unpicklify
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table as dt
from dash.dependencies import Input, Output, State
#from app_functions import *
from pickle_functions import unpicklify
from process_functions import write_log

def list_item(opening, data, ending):
    '''
    input: 
    info data about a statistic for a country
    a string describing it
    a string of eventual text after data
    output: 
    if the data is valid returns an item, otherwise nothing
    '''
    if pd.isna(data) or data == 'None' or data == 0:
        return
    else:
        return dbc.ListGroupItemText(f'{opening}{data}{ending}')


def draw_singleCountry_Scatter(df, dropdown, plotName):
    '''
    Function to generate and plot a scatterplot for the selected countries
    '''
    #print(df.index)
    fig = go.Figure()
    #countries = df.columns
    #dates = df.loc[df['Region'] == selected_region,'date']
    for country in dropdown:
        #x = [x for x in range(len(df[country]))]
        fig.add_trace(go.Scatter(x =  list(df.index), y = list(df[country]),
                                mode='lines+markers',
                                name=country,
                                line=dict(width=3), marker = dict(size = 3, line = dict(width = 1,color = 'DarkSlateGrey')), hoverinfo = "text",
                                hovertext = [f"{country}: {df.iloc[indice][country]} <br>Year: {df.index[indice]}" for indice in range(len(df))]))
    fig.update_layout(title = plotName)

    fig.update_layout(
        hovermode='closest',
        legend=dict(
            x = 0, 
            y=-0.3, 
            orientation = 'h',
            traceorder="normal",
            font=dict(
                family="sans-serif",
                size=12,
            ),
            borderwidth=0,
            #x=0,
            #y=-0.4,
            #orientation="h"
        ),
        plot_bgcolor = 'white',
        paper_bgcolor = 'white',
                xaxis = dict(
            tickangle = -45
        ),
        margin=dict(l=0, r=0, t=65, b=0),
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey')
    fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor='black')
    return fig
