# Import required libraries
import os
import datetime as dt
import time

import numpy as np
import pandas as pd

import dash
from dash.dependencies import Input, Output, State, Event
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dcce


# Setup app
app = dash.Dash()

external_css = ["https://fonts.googleapis.com/css?family=Roboto:400,300,600",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/1564e52057ea20b6c23a4047d3d9261fc793f3af/dash-analytics-report.css",
                "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]

for css in external_css:
    app.css.append_css({"external_url": css})


# Load data
df = pd.read_json('http://localhost:8000/api/price_data/?format=json')
tokens = set(df['buy_token'])


DF_GAPMINDER = pd.read_csv(
    'https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv'
)
DF_GAPMINDER = DF_GAPMINDER[DF_GAPMINDER['year'] == 2007]
DF_GAPMINDER.loc[0:20]


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
                    rows=DF_GAPMINDER.to_dict('records'),

                    # optional - sets the order of columns
                    columns=sorted(DF_GAPMINDER.columns),
                    row_selectable=True,
                    filterable=True,
                    sortable=True,
                    id='datatable'
                ),
            ],
                className='nine columns',
            ),
            html.Div([
                html.H4('Exchange'),
                html.Div([
                    dcc.Dropdown(
                        id='first_currency',
                        options=[{'label': i, 'value': i} for i in tokens],
                        multi=True,
                        value='WETH',
                    ),
                    dcc.Input(
                        id='first_currency_amount',
                        value='0.1 WETH',
                        type="text",
                        style={'width': '260'}
                    ),
                ],
                    style={'max-width': '260'}
                ),
                html.H4('Into'),
                html.Div([
                    dcc.Dropdown(
                        id='second_currency',
                        options=[{'label': i, 'value': i} for i in tokens],
                        multi=True,
                        value='ZRX',
                    ),
                    dcc.Input(
                        id='second_currency_amount',
                        value='',
                        type="text",
                        style={'width': '260'}
                    ),
                ],
                    style={'max-width': '260'}
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
            style={'margin-bottom': '10'}
        ),
        html.Div([
            dcc.Graph(id='chart', style={'max-height': '600', 'height': '40vh'}),
        ],
            className='row',
            style={'margin-bottom': '20'}
        ),
    ],
    style={
        'width': '85%',
        'max-width': '1200',
        'margin-left': 'auto',
        'margin-right': 'auto',
        'font-family': 'futura',
        'background-color': '#F3F3F3',
        'padding': '40',
        'padding-top': '20',
        'padding-bottom': '20',
    },
)


@app.callback(
    Output('chart', 'figure'),
    [Input('datatable', 'rows'),
     Input('datatable', 'selected_row_indices')])
def update_figure(rows, selected_row_indices):
    dff = pd.DataFrame(rows)
    fig = plotly.tools.make_subplots(
        rows=3, cols=1,
        subplot_titles=('Life Expectancy', 'GDP Per Capita', 'Population',),
        shared_xaxes=True)
    marker = {'color': ['#0074D9']*len(dff)}
    for i in (selected_row_indices or []):
        marker['color'][i] = '#FF851B'
    fig.append_trace({
        'x': dff['country'],
        'y': dff['lifeExp'],
        'type': 'bar',
        'marker': marker
    }, 1, 1)
    fig.append_trace({
        'x': dff['country'],
        'y': dff['gdpPercap'],
        'type': 'bar',
        'marker': marker
    }, 2, 1)
    fig.append_trace({
        'x': dff['country'],
        'y': dff['pop'],
        'type': 'bar',
        'marker': marker
    }, 3, 1)
    fig['layout']['showlegend'] = False
    fig['layout']['height'] = 800
    fig['layout']['margin'] = {
        'l': 40,
        'r': 10,
        't': 60,
        'b': 200
    }
    fig['layout']['yaxis3']['type'] = 'log'
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
