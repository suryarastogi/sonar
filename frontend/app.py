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

# Dummy data
DF_WALMART = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/1962_2006_walmart_store_openings.csv')

DF_GAPMINDER = pd.read_csv(
    'https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv'
)
DF_GAPMINDER = DF_GAPMINDER[DF_GAPMINDER['year'] == 2007]
DF_GAPMINDER.loc[0:20]

DF_SIMPLE = pd.DataFrame({
    'x': ['A', 'B', 'C', 'D', 'E', 'F'],
    'y': [4, 3, 1, 2, 3, 6],
    'z': ['a', 'b', 'c', 'a', 'b', 'c']
})

ROWS = [
    {'a': 'AA', 'b': 1},
    {'a': 'AB', 'b': 2},
    {'a': 'BB', 'b': 3},
    {'a': 'BC', 'b': 4},
    {'a': 'CC', 'b': 5},
    {'a': 'CD', 'b': 6}
]


# Make app layout
app.layout = html.Div(
    [
        html.Div([
            html.Img(
                src="https://datashop.cboe.com/Themes/Livevol/Content/images/logo.png",
                className='twelve columns',
                style={
                    'height': '60',
                    'width': '160',
                    'float': 'left',
                    'position': 'relative',
                },
            ),
        ],
            className='row'
        ),
        html.Hr(style={'margin': '0', 'margin-bottom': '5'}),
        html.Div([
            html.Div([
                dcce.DataTable(
                    rows=DF_GAPMINDER.to_dict('records'),

                    # optional - sets the order of columns
                    columns=sorted(DF_GAPMINDER.columns),

                    row_selectable=True,
                    filterable=True,
                    sortable=True,
                    id='datatable-gapminder'
                ),
            ],
                className='eight columns',
            ),
            html.Div([
                html.Label('Exchange '),
                dcc.Dropdown(
                    id='first_currency',
                    options=[{'label': i, 'value': i} for i in ['Canada', 'USA', 'Mexico']],
                    value='SPY',
                ),
                html.Label('Into'),
                dcc.Dropdown(
                    id='second_currency',
                    options=[{'label': i, 'value': i} for i in ['Canada', 'USA', 'Mexico']],
                    value='SPY',
                ),
            ],
                className='four columns',
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
        'font-family': 'overpass',
        'background-color': '#F3F3F3',
        'padding': '40',
        'padding-top': '20',
        'padding-bottom': '20',
    },
)


@app.callback(
    Output('chart', 'figure'),
    [Input('datatable-gapminder', 'rows'),
     Input('datatable-gapminder', 'selected_row_indices')])
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
