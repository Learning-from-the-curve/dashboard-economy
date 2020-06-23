import datetime
import json
import dash
import pickle
import os
from pathlib import Path
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table as dt
from dash.dependencies import Input, Output, State

import dash_bootstrap_components as dbc
# Custom functions
from layout_functions import draw_singleCountry_Scatter, list_item
from pickle_functions import unpicklify

#####################################################################################################################################
# Boostrap CSS and font awesome . Option 1) Run from codepen directly Option 2) Copy css file to assets folder and run locally
#####################################################################################################################################
external_stylesheets = [dbc.themes.FLATLY]

#Insert your javascript here. In this example, addthis.com has been added to the web app for people to share their webpage

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

app.title = 'COVID-19 - Economic dashboard'

flask_app = app.server

config = {'displayModeBar': True}

#for heroku to run correctly
server = app.server

default = ['Belgium','Italy','France']
#############################################################################
# UNPICKLIFICATION TIME - load the datasets in the variables
#############################################################################

pickles_list = [
    'GDP_card',
    'HICP_card',
    'HU_card',
    'BC_card',
    'GDP_plot',
    'countries',
    'HI00_plot',
    'HU_plot',
    'job_plot',
    'SI_Construction_plot',
    'RS_plot',
    'SV_plot',
    'CN_plot',
    'IRST_LTGBY_plot',
    'IND_plot',
    'PEL_plot',
    'SI_Economic_plot',
    'SI_Industrial_plot',
    'SI_Retail_plot',
    'SI_Consumer_plot',
    'SI_Services_plot',
    'IRST_DDI_plot',
    'IRST_3M_plot',
    'grossVA_plot',
    'employment_plot',
    'CEL_plot',
    'IEL_plot',
    'PNG_plot',
    'CNG_plot',
    'ING_plot',
    'HIIG_plot',
    'HIS_plot',
    'HI00XEF_plot',

]

GDP_card = unpicklify(pickles_list[0])
HICP_card = unpicklify(pickles_list[1])
HU_card = unpicklify(pickles_list[2])
BC_card = unpicklify(pickles_list[3])
GDP_plot = unpicklify(pickles_list[4])
countries = unpicklify(pickles_list[5])
HI00_plot = unpicklify(pickles_list[6])
HU_plot = unpicklify(pickles_list[7])
job_plot = unpicklify(pickles_list[8])
SI_Construction_plot = unpicklify(pickles_list[9])
RS_plot = unpicklify(pickles_list[10])
SV_plot = unpicklify(pickles_list[11])
CN_plot = unpicklify(pickles_list[12])
IRST_LTGBY_plot = unpicklify(pickles_list[13])
IND_plot = unpicklify(pickles_list[14])
PEL_plot = unpicklify(pickles_list[15])
SI_Economic_plot = unpicklify(pickles_list[16])
SI_Industrial_plot = unpicklify(pickles_list[17])
SI_Retail_plot = unpicklify(pickles_list[18])
SI_Consumer_plot = unpicklify(pickles_list[19])
SI_Services_plot = unpicklify(pickles_list[20])
IRST_DDI_plot = unpicklify(pickles_list[21])
IRST_3M_plot = unpicklify(pickles_list[22])
grossVA_plot = unpicklify(pickles_list[23])
employment_plot = unpicklify(pickles_list[24])
CEL_plot = unpicklify(pickles_list[25])
IEL_plot = unpicklify(pickles_list[26])
PNG_plot = unpicklify(pickles_list[27])
CNG_plot = unpicklify(pickles_list[28])
ING_plot = unpicklify(pickles_list[29]) 
HIIG_plot = unpicklify(pickles_list[30]) 
HIS_plot = unpicklify(pickles_list[31]) 
HI00XEF_plot = unpicklify(pickles_list[32]) 

dropdown_UJ = ['Unemployment', 'Job Vacancy - All NACE activities','Employment - All NACE activities']
dropdown_CRS = ['Consumer', 'Retail Sale', 'Services']
dropdown_SI = ['Construction','Economic', 'Industrial','Retail','Consumer','Services',]
dropdown_IRST = ['Long term government bond yields', 'Day-to-day money market', '3-month']
dropdown_GDP = ['Gross domestic product at market prices', 'Gross Value Added']
dropdown_EN = ['Production of natural gas','Total consumption of natural gas','Imports of natural gas','Production of electricity','Consumption of electricity','Imports of electricity']
dropdown_HICP = ['All items','Industrial goods','Total services','All items excluding energy, food, alcohol and tobacco']

markdown_relevant_info = html.Div([
    html.P([
        "We focus on this dashboard on the Economic impact of the COVID-19 pandemic. This dashboard is part of a larger set of dashboards available ",
        dcc.Link('on our website', href='https://www.learningfromthecurve.net/dashboards/', target="_top"),
    ]),
    html.P([
        "Articles by members of the Learning from the Curve team reporting daily information on COVID-19 are available ",
        dcc.Link('here', href='https://www.learningfromthecurve.net/commentaries/', target="_top"),
    ]),
    html.P([
        "Please, report any bug at the following contact address: ",
        dcc.Link('learningfromthecurve.info@gmail.com', href='mailto:learningfromthecurve.info@gmail.com'),
    ]),
])

markdown_data_info = html.Div([
    html.P([
        "The dashboard is updated when Eurostat updates the data monthly or quarterly.",
    ]),
    html.P([
        "On request we can provide the name and the Eurostat ID code of the series displayed in this dashboard.",
    ]),
    html.P([
        "Data source",
        html.Ul([
            html.Li(dcc.Link('Eurostat', href='https://ec.europa.eu/eurostat', target="_blank"),),])
    ]),
])


############################
# Bootstrap Grid Layout
############################

app.layout = html.Div([ #Main Container   
        #Header TITLE
        html.Div([
            #Info Modal Button LEFT
            dbc.ButtonGroup(
                [
                    dbc.Button("Home", href="https://www.learningfromthecurve.net/", target="_top", external_link=True, className="py-2"),
                    dbc.Button("Dashboards", href="https://www.learningfromthecurve.net/Dashboards/", target="_top", external_link=True, className="py-2"),
                ],
                vertical=True,
                size="sm",
            ),
            #H2 Title
            html.H2(
                children='Economic Dash board',
                className="text-center",
            ),
            #Info Modal Button RIGHT
            dbc.ButtonGroup(
                [
                    dbc.Button("Info", id="open-centered-left", className="py-2"),
                    dbc.Button("Datasets", id="open-centered-right", className="py-2"),
                ],
                vertical=True,
                size="sm",
            ),
            dbc.Modal(
                [
                    dbc.ModalHeader("Information on datasets used"),
                    dbc.ModalBody(children = markdown_data_info),
                    dbc.ModalFooter(
                        dbc.Button(
                            "Close", id="close-centered-right", className="ml-auto"
                        )
                    ),
                ],
                id="modal-centered-right",
                centered=True,
            ),
            dbc.Modal(
                [
                    dbc.ModalHeader("Relevant information"),
                    dbc.ModalBody(children = markdown_relevant_info),
                    dbc.ModalFooter(
                        dbc.Button("Close", id="close-centered-left", className="ml-auto")
                    ),
                ],
                id="modal-centered-left",
                centered=True,
            ),
        ],
        className="topRow d-flex justify-content-between align-items-center mb-2"
        ),

      #First Row CARDS 3333
        dbc.Row([
            dbc.Col([
                #Card 1
                dbc.Card([
                    # Card 1 body
                    html.H4(children='GDP Rate (EU28)'),
                    html.H2(f"{GDP_card.iloc[0,-1]:,.1f}", id = 'card1'),
                    dbc.Tooltip([
                        html.P('National Account Indicator: Gross domestic product at market prices'),
                        html.P('Unit: Chain linked volumes, index 2005=100'),
                    ],
                    target="card1",
                    style= {'opacity': '0.9'}
                    ),
                ],
                className='cards'
                ),
            ],
            lg = 3, xs = 12,
            className='colCards'
            ),     
            dbc.Col([
                #Card 2
                dbc.Card([
                    # Card 2 body
                    html.H4(children='HICP aggregate (EU28)'),
                    html.H2(f"{HICP_card.iloc[0,-1]:,.1f}", id = 'card2'),
                    dbc.Tooltip([
                        html.P('indicator: Harmonized index of consumer price - All items'),
                        html.P('Adjustment: Seasonally Unadjusted'),
                        html.P('Unit: Harmonized consumer price index, 2015=100'),
                    ],
                    target="card2",
                    style= {'opacity': '0.9'}
                    ),
                ],
                className='cards'
                ),
            ],
            lg = 3, xs = 12,
            className='colCards'
            ),   
            dbc.Col([
                #Card 3
                dbc.Card([
                    # Card 3 body
                    html.H4(children='Unemployment Rate (EU28)'),
                    html.H2(f"{HU_card.iloc[0,-1]:,.1f}%", id = 'card3'),
                    dbc.Tooltip([
                        html.P('Adjustment: Seasonally Adjusted'),
                        html.P('unit: Percentage of active population'),            
                    ],
                    target="card3",
                    style= {'opacity': '0.9'}
                    ),
                ],
                className='cards'
                ),
            ],
            lg = 3, xs = 12,
            className='colCards'
            ),        
            dbc.Col([
                #Card 4
                dbc.Card([
                    # Card 4 body
                    html.H4(children='Businness Climate (EU19)'),
                    html.H2(f"{BC_card.iloc[0,-1]:,.1f}", id = 'card4'),
                    dbc.Tooltip([
                        html.P('Indicator: Business Climate Indicator'),
                        html.P('Adjustment: Seasonally Adjusted'),
                    ],
                    target="card4",
                    style= {'opacity': '0.9'}
                    ),
                ],
                className='cards'
                ),
            ],
            lg = 3, xs = 12,
            className='colCards'
            ),     
            ],
            className = "midRow d-flex"
            ),
        #Country select Dropdown
        html.Div([
            dbc.Card([
                html.Div([
                    html.H4(
                        children='Add or Remove Countries to Compare',
                        style={},
                        className='text-center my-2'
                    ),
                    dcc.Dropdown(
                        id='demo-dropdown',
                        options=[{'label': i, 'value': i} for i in countries],
                        multi=True,
                        value = default,
                        placeholder = 'Select countries to plot - Default to Belgium and EU27'
                    ),
                ],
                className='p-1'
                ),
            ], 
            className = "my-2", 
            style = {"overflow": "visible"}
            )
        ], className="sticky-top"
        ),

        dbc.Row([
            #GDP
            dbc.Col([
                dbc.Card([
                    html.H4(
                        children='Income',
                        className='text-center my-2',
                    ),
                    html.Div([
                        dcc.Dropdown(
                            id='dropdown_GDP',
                            options=[{'label': i, 'value': i} for i in dropdown_GDP],
                            multi=False,
                            value = dropdown_GDP[0],
                        ),
                    ],
                    className="p-1"
                    ),
                ],
                className='my-2',
                id = 'income'
                ),
                dbc.Tooltip([
                    html.P('Unit: Chain linked volumes, index 2005=100'),
                ],
                target="income",
                style= {'opacity': '0.9'}
                ),
                html.Div([
                    html.Div([
                        dcc.Graph(id='line-graph-GDP',config=config)
                    ],
                    className='p-1'
                    ),
                ],
                className='card my-2 '
                ),
            ],
            lg = 6, md = 12
            ),
            dbc.Col([
                dbc.Card([
                    html.H4(
                        children='Employment',
                        className='text-center my-2',
                    ),
                    html.Div([
                        dcc.Dropdown(
                            id='dropdown_UJ',
                            options=[{'label': i, 'value': i} for i in dropdown_UJ],
                            multi=False,
                            value = dropdown_UJ[0],
                        ),
                    ],
                    className="p-1"
                    )
                ],
                className='my-2 ',
                id = 'UJ'
                ),
                dbc.Tooltip([
                    html.P(['Adjustment:', html.Br(), 'Unemployment - Seasonally Adjusted', html.Br(), 'Job Vacancy - Seasonally Unadjusted', html.Br(), 'Employment - Seasonally and Calendar Adjusted']),
                    html.P(['Unit:', html.Br(), 'Unemployment - Percentage of active population', html.Br(), 'Employment - Percentage change on previous period (based on persons)']),
                ],
                target="UJ",
                style= {'opacity': '0.9'}
                ),
                html.Div([
                    html.Div([
                        dcc.Graph(id='line-graph-UJ',config=config)
                    ],
                    className='p-1'
                    ),
                ],
                className='card my-2 '
                ),
            ],
            lg = 6, md = 12
            ),
        ]),
        dbc.Row([
            #HCP
            dbc.Col([
                dbc.Card([
                    html.H4(
                        children='HICP',
                        className='text-center my-2',
                    ),
                    html.Div([
                        dcc.Dropdown(
                            id='dropdown_HICP',
                            options=[{'label': i, 'value': i} for i in dropdown_HICP],
                            multi=False,
                            value = dropdown_HICP[0],
                        ),
                    ],
                    className="p-1"
                    )
                ],
                className='my-2',
                id = 'HICP'
                ),
                dbc.Tooltip([
                    html.P('Adjustment: Seasonally Unadjusted'),
                    html.P('Unit: Harmonized consumer price index, 2015=100'),
                ],
                target="HICP",
                style= {'opacity': '0.9'}
                ),
                html.Div([
                    html.Div([
                        dcc.Graph(id='line-graph-HICP',config=config)
                    ],
                    className='p-1'
                    ),
                ],
                style={},
                className='card my-2 '
                ),
            ],
            lg = 6, md = 12
            ),
            #interest
            dbc.Col([
                dbc.Card([
                    html.H4(
                        children='Interest Rates',
                        className='text-center my-2',
                    ),
                    html.Div([
                        dcc.Dropdown(
                            id='dropdown_IRST',
                            options=[{'label': i, 'value': i} for i in dropdown_IRST],
                            multi=False,
                            value = dropdown_IRST[0],
                        ),
                    ],
                    className="p-1"
                    )
                ],
                className='my-2',
                id = 'IR'
                ),
                dbc.Tooltip([
                    html.P('Adjustment: Seasonally Unadjusted'),
                ],
                target="IR",
                style= {'opacity': '0.9'}
                ),
                html.Div([
                    html.Div([
                        dcc.Graph(id='line-graph-IRST',config=config)
                    ],
                    className='p-1'
                    ),
                ],
                className='card my-2 '
                ),
            ],
            lg = 6, md = 12
            )
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    html.H4(
                        children='Sentiment Indicators',
                        className='text-center my-2',
                    ),
                    html.Div([
                        dcc.Dropdown(
                            id='dropdown_SI',
                            options=[{'label': i, 'value': i} for i in dropdown_SI],
                            multi=False,
                            value = dropdown_SI[1],
                        ),
                    ],
                    className="p-1"
                    )
                ],
                className='my-2',
                id = 'SI'
                ),
                dbc.Tooltip([
                    html.P('Adjustment: Seasonally Adjusted'),
                ],
                target="SI",
                style= {'opacity': '0.9'}
                ),
                html.Div([
                    html.Div([
                        dcc.Graph(id='line-graph-SI',config=config)
                    ],
                    className='p-1'
                    ),
                ],
                style={},
                className='card my-2 '
                ),
            ],
            lg = 6, md = 12
            ),
            #energy
            dbc.Col([
                dbc.Card([
                    html.H4(
                        children='Energy Production, Consumption and Import',
                        className='text-center my-2',
                    ),
                    html.Div([
                        dcc.Dropdown(
                            id='dropdown_EN',
                            options=[{'label': i, 'value': i} for i in dropdown_EN],
                            multi=False,
                            value = dropdown_EN[0],
                        ),
                    ],
                    className="p-1"
                    )
                ],
                className='my-2',
                id = 'EN'
                ),
                dbc.Tooltip([
                    html.P('Adjustment: Seasonally Unadjusted'),
                ],
                target="EN",
                style= {'opacity': '0.9'}
                ),
                html.Div([
                    html.Div([
                        dcc.Graph(id='line-graph-EN',config=config)
                    ],
                    className='p-1'
                    ),
                ],
                className='card my-2 '
                ),
            ],
            lg = 6, md = 12
            ),
        ]),
],
className="container-fluid cf py-2"
)

# draw the two graphs under the map for confirmed cases and deaths
@app.callback(
    Output('line-graph-GDP', 'figure'),
    [Input('demo-dropdown', 'value'),Input('dropdown_GDP', 'value')])
def line_selection(dropdown,plotChoice):
    if len(dropdown) == 0:
        dropdown = default
    if plotChoice == dropdown_GDP[0]:
        fig1 = draw_singleCountry_Scatter(df = GDP_plot, dropdown = dropdown, plotName = plotChoice)
    elif plotChoice == dropdown_GDP[1]:
        fig1 = draw_singleCountry_Scatter(df = grossVA_plot, dropdown = dropdown, plotName = plotChoice)
    return fig1

@app.callback(
    Output('line-graph-HICP', 'figure'),
    [Input('demo-dropdown', 'value'),Input('dropdown_HICP', 'value')])
def line_selection2(dropdown,plotChoice):
    if len(dropdown) == 0:
        dropdown = default
    if plotChoice == dropdown_HICP[0]:
        fig1 = draw_singleCountry_Scatter(df = HI00_plot, dropdown = dropdown, plotName = plotChoice)
    elif plotChoice == dropdown_HICP[1]:
        fig1 = draw_singleCountry_Scatter(df = HIIG_plot, dropdown = dropdown, plotName = plotChoice)
    elif plotChoice == dropdown_HICP[2]:
        fig1 = draw_singleCountry_Scatter(df = HIS_plot, dropdown = dropdown, plotName = plotChoice)
    elif plotChoice == dropdown_HICP[3]:
        fig1 = draw_singleCountry_Scatter(df = HI00XEF_plot, dropdown = dropdown, plotName = plotChoice)
    return fig1

@app.callback(
    Output('line-graph-UJ', 'figure'),
    [Input('demo-dropdown', 'value'),Input('dropdown_UJ', 'value'),])
def line_selection3(dropdown,plotChoice):
    if len(dropdown) == 0:
        dropdown = default
    if plotChoice == dropdown_UJ[0]:
        fig1 = draw_singleCountry_Scatter(df = HU_plot, dropdown = dropdown, plotName = plotChoice)
    elif plotChoice == dropdown_UJ[1]:
        fig1 = draw_singleCountry_Scatter(df = job_plot, dropdown = dropdown, plotName = plotChoice)
    elif plotChoice == dropdown_UJ[2]:
        fig1 = draw_singleCountry_Scatter(df = employment_plot, dropdown = dropdown, plotName = plotChoice)
    return fig1

@app.callback(
    Output('line-graph-SI', 'figure'),
    [Input('demo-dropdown', 'value'),Input('dropdown_SI', 'value')])
def line_selection5(dropdown,plotChoice):
    if len(dropdown) == 0:
        dropdown = default
    if plotChoice == dropdown_SI[0]:
        fig1 = draw_singleCountry_Scatter(df = SI_Construction_plot, dropdown = dropdown, plotName = plotChoice)
    elif plotChoice == dropdown_SI[1]:
        fig1 = draw_singleCountry_Scatter(df = SI_Economic_plot, dropdown = dropdown, plotName = plotChoice)
    elif plotChoice == dropdown_SI[2]:
        fig1 = draw_singleCountry_Scatter(df = SI_Industrial_plot, dropdown = dropdown, plotName = plotChoice)
    elif plotChoice == dropdown_SI[3]:
        fig1 = draw_singleCountry_Scatter(df = SI_Retail_plot, dropdown = dropdown, plotName = plotChoice)
    elif plotChoice == dropdown_SI[4]:
        fig1 = draw_singleCountry_Scatter(df = SI_Services_plot, dropdown = dropdown, plotName = plotChoice)
    elif plotChoice == dropdown_SI[5]:
        fig1 = draw_singleCountry_Scatter(df = SI_Consumer_plot, dropdown = dropdown, plotName = plotChoice)
    return fig1


@app.callback(
    Output('line-graph-IRST', 'figure'),
    [Input('demo-dropdown', 'value'),Input('dropdown_IRST', 'value')])
def line_selection9(dropdown, plotChoice):
    if len(dropdown) == 0:
        dropdown = default
    if plotChoice == dropdown_IRST[0]:
        fig1 = draw_singleCountry_Scatter(df = IRST_LTGBY_plot, dropdown = dropdown, plotName = plotChoice)
    elif plotChoice == dropdown_IRST[1]:
        fig1 = draw_singleCountry_Scatter(df = IRST_3M_plot, dropdown = dropdown, plotName = plotChoice)
    elif plotChoice == dropdown_IRST[2]:
        fig1 = draw_singleCountry_Scatter(df = IRST_DDI_plot, dropdown = dropdown, plotName = plotChoice)
    return fig1

@app.callback(
    Output('line-graph-EN', 'figure'),
    [Input('demo-dropdown', 'value'),Input('dropdown_EN', 'value')])
def line_selection12(dropdown,plotChoice):
    if len(dropdown) == 0:
        dropdown = default
    if plotChoice == dropdown_EN[0]:
        fig1 = draw_singleCountry_Scatter(df = PNG_plot, dropdown = dropdown, plotName = plotChoice)
    elif plotChoice == dropdown_EN[1]:
        fig1 = draw_singleCountry_Scatter(df = CNG_plot, dropdown = dropdown, plotName = plotChoice)
    elif plotChoice == dropdown_EN[2]:
        fig1 = draw_singleCountry_Scatter(df = ING_plot, dropdown = dropdown, plotName = plotChoice)
    elif plotChoice == dropdown_EN[3]:
        fig1 = draw_singleCountry_Scatter(df = PEL_plot, dropdown = dropdown, plotName = plotChoice)
    elif plotChoice == dropdown_EN[4]:
        fig1 = draw_singleCountry_Scatter(df = CEL_plot, dropdown = dropdown, plotName = plotChoice)
    elif plotChoice == dropdown_EN[5]:
        fig1 = draw_singleCountry_Scatter(df = IEL_plot, dropdown = dropdown, plotName = plotChoice)
    return fig1

# open/close the left modal
@app.callback(
    Output("modal-centered-left", "is_open"),
    [Input("open-centered-left", "n_clicks"), Input("close-centered-left", "n_clicks")],
    [State("modal-centered-left", "is_open")],)
def toggle_modal_left(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

# open/close the right modal
@app.callback(
    Output("modal-centered-right", "is_open"),
    [Input("open-centered-right", "n_clicks"), Input("close-centered-right", "n_clicks")],
    [State("modal-centered-right", "is_open")],)
def toggle_modal_right(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

if __name__ == '__main__':
   app.run_server(debug=False)
