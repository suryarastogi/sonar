# Import required libraries
import os
import datetime as dt
import time

import numpy as np
import pandas as pd
import cufflinks as cf

import dash
from dash.dependencies import Input, Output, State, Event
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dcce

from history import download_data, extract_data

# Setup app
app = dash.Dash()

external_css = ["https://cdn.rawgit.com/plotly/dash-app-stylesheets/1564e52057ea20b6c23a4047d3d9261fc793f3af/dash-analytics-report.css",
                "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]

for css in external_css:
    app.css.append_css({"external_url": css})


# Load data
df = pd.read_json('http://localhost:8000/api/price_data/?format=json')

# Coinmarketcap tables
translate = {
    'ANT': 'currencies/aragon/',
    'DNT': '/currencies/district0x/',
    'MTL': 'currencies/metal/',
    'OMG': 'currencies/omisego/',
    'WETH': 'currencies/ethereum',
    'ZRX': 'currencies/0x/'}


# Convert to ratio table
df['ratio'] = df['sell_quantity']/df['buy_quantity']
df_matrix = df.pivot('buy_token', 'sell_token')['ratio'].round(decimals=8)
df_matrix['[INTO]'] = df_matrix.index
df_dict = df_matrix.to_dict('records')

# For selector
tokens = set(df['buy_token'])

# Make app layout
app.layout = html.Div(
    [
        html.Div([
            html.Img(
                src="https://rawgit.com/suryanash/sonar/master/assets/1024.png",
                className='twelve columns',
                style={
                    'height': '80',
                    'width': '350',
                    'float': 'left',
                    'position': 'relative',
                },
            ),
        ],
            className='row'
        ),
        html.Hr(style={'margin': '0', 'margin-bottom': '15'}),
        html.Div([
            html.Div([
                dcce.DataTable(
                    rows=df_dict,
                    columns=df_matrix.columns,
                    row_selectable=False,
                    filterable=True,
                    sortable=True,
                    id='datatable'
                ),
            ],
                className='nine columns',
                style={'background-color': '#F5F5F5'}
            ),
            html.Div([
                html.H4('Exchange'),
                html.Div([
                    dcc.Dropdown(
                        id='first_currency',
                        options=[{'label': i, 'value': i} for i in tokens],
                        multi=True,
                        value=['WETH'],
                    ),
                    dcc.Input(
                        id='first_currency_amount',
                        value='0.1 WETH',
                        type="text",
                        style={'width': '260'}
                    ),
                ],
                    style={'max-width': '260', 'background-color': '#FFFFFF'}
                ),
                html.H4('Into'),
                html.Div([
                    dcc.Dropdown(
                        id='second_currency',
                        options=[{'label': i, 'value': i} for i in tokens],
                        multi=True,
                        value=['ZRX'],
                    ),
                    dcc.Input(
                        id='second_currency_amount',
                        value='',
                        type="text",
                        style={'width': '260'}
                    ),
                ],
                    style={'max-width': '260', 'background-color': '#FFFFFF'}
                ),
                html.Hr(style={'margin-top': '30', 'margin-bottom': '30'}),
                html.Button(
                    'TRADE',
                    id='trade_button',
                    style={'background-color': '#e3e5f8', 'width': '130'}
                ),
                html.Button(
                    'ADVANCED',
                    id='trade_button',
                    style={'background-color': '#FFFFFF', 'width': '130'}
                ),
            ],
                className='three columns',
            ),
        ],
            className='row',
            style={'margin-bottom': '20'}
        ),
        html.Div([
            dcc.Graph(id='chart', style={'max-height': '600', 'height': '40vh'}),
        ],
            className='row',
            style={'margin-bottom': '20'}
        ),
    ],
    style={
        'width': '95%',
        'max-width': '1200',
        'margin-left': 'auto',
        'margin-right': 'auto',
        'font-family': 'overpass',
        'background-color': '#F3F3F3',
        'padding': '40',
        'padding-top': '20',
        'padding-bottom': '20',
    },
)


@app.callback(Output('chart', 'figure'),
              [Input('first_currency', 'value'),
               Input('second_currency', 'value')])
def update_figure(first_currency, second_currency):

    # print(first_currency, second_currency)

    scraped1 = extract_data(download_data(translate[first_currency[0]], '2000', '2018'))
    pair1 = pd.DataFrame(scraped1[1], columns=scraped1[0])

    scraped2 = extract_data(download_data(translate[second_currency[0]], '2000', '2018'))
    pair2 = pd.DataFrame(scraped2[1], columns=scraped2[0])

    if len(pair1) <= len(pair2):
        cut = len(pair1)
        index = pair1.index
    else:
        cut = len(pair2)
        index = pair2.index

    pair = pd.DataFrame([], index=index)
    for i in ['Open', 'High', 'Low', 'Close']:
        pair[i] = pair1[i][:cut].values.astype(float) / pair2[i][:cut].values.astype(float)

    trace = dict(
        type='candlestick',
        x=pair.index,
        open=pair.Open,
        high=pair.High,
        low=pair.Low,
        close=pair.Close
    )

    data = [trace]

    layout = dict(
        autosize=True,
        font=dict(family='Overpass'),
        paper_bgcolor='#FAFAFA',
        margin=dict(
            l=40,
            r=20,
            b=40,
            t=60
        ),
        title=first_currency[0] + '_' + second_currency[0],
        showlegend=False,
    )

    return dict(data=data, layout=layout)


if __name__ == '__main__':
    app.run_server(debug=True)
