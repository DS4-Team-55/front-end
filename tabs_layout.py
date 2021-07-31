import datetime
from datetime import date
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import dash_daq as daq
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import plotly.express as px
import re
import os
import base64
import pandas as pd
from PIL import Image
from io import BytesIO
import plotly.graph_objects as go
from scipy import signal
import numpy as np
import generate_figures_info


def context_layout(data):
    info_ = generate_figures_info.context(data)
    return dbc.Row(
        [
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            html.Div('Select year:', style={'fontSize': 13}),
                            dcc.Checklist(
                                id='context_year_sel',
                                options=[
                                    {'label': '2015', 'value': 2015},
                                    {'label': '2016', 'value': 2016},
                                    {'label': '2017', 'value': 2017},
                                    {'label': '2018', 'value': 2018},
                                    {'label': '2019', 'value': 2019},
                                    {'label': '2020', 'value': 2020},
                                    {'label': '2021', 'value': 2021}
                                ],
                                value=[2015, 2016, 2017, 2018, 2019, 2020, 2021], 
                                style={'display': "inline-block"}
                            )
                        ], style={'margin-left': '15px', 'margin-top': '70px'})
                    ], width={'size': 2, 'offset': 0}), 
                    dbc.Col([
                        dcc.Graph(
                            id='plt_context_ages', 
                            style={'height': '300px'}, 
                            figure=info_['plt_context_ages']
                        )
                    ], width={'size': 10, 'offset': 0}),
                ], style={"margin-top": "15px"}), 
                dbc.Row([
                    dcc.Graph(
                        id='plt_context_estrato', 
                        style={'height': '300px'}, 
                        figure=info_['plt_context_estrato']
                    )
                ], no_gutters=False, justify='around'), 
                dbc.Row([
                    dcc.Graph(
                        id='plt_context_marital', 
                        style={'height': '400px'}, 
                        figure=info_['plt_context_marital']
                    )
                ], no_gutters=False, justify='around')
            ], width={'size': 6, 'offset': 0}), 
            dbc.Col([
                dbc.Row([
                    dbc.Card([
                        html.Div('MORTALITY:', style={'margin-left': '30px', 'fontWeight': 'bold', 'fontSize': 25}),
                        html.Div(info_['mortality_cnt'], id='mortality_cnt', style={'margin-left': '170px', 'margin-right': '170px', 'margin-top': '50px', 'fontWeight': 'bold', 'fontSize': 45})
                    ], style={'margin-left': '70px', 'margin-top': '50px'})
                ]), 
                dbc.Row([
                    dbc.Card([
                        html.Div('MORBIDITY:', style={'margin-left': '30px', 'fontWeight': 'bold', 'fontSize': 25}),
                        html.Div(info_['morbidity_cnt'], id='morbility_cnt', style={'margin-left': '170px', 'margin-right': '170px', 'margin-top': '50px', 'fontWeight': 'bold', 'fontSize': 45})
                    ], style={'margin-left': '70px', 'margin-top': '50px'})
                ]), 
                dbc.Row([
                    dbc.Card([
                        html.Div('COVID:', style={'margin-left': '30px', 'fontWeight': 'bold', 'fontSize': 25}),
                        html.Div(info_['covid_cnt'], id='covid_cnt', style={'margin-left': '170px', 'margin-right': '170px', 'margin-top': '50px', 'fontWeight': 'bold', 'fontSize': 45})
                    ], style={'margin-left': '70px', 'margin-top': '50px'})
                ]), 
                dbc.Row([
                    dcc.Graph(
                        id='plt_context_education', 
                        style={'height': '400px'}, 
                        figure=info_['plt_context_education']
                    )
                ], style={'margin-top': '50px'}, no_gutters=False, justify='around') 
            ], width={'size': 5, 'offset': 0})
        ]
    )


def data_viz():
    dg = DataGenerator(1)
    figures = dg.generate_figures()
    return dbc.Col(
        [
            dbc.Row([
                dbc.Col(
                    [
                        dcc.Graph(
                            id='output_1_1', figure=figures[0]
                        )
                    ], 
                    width={'size': 4, 'offset': 0}
                ),
                dbc.Col(
                    [
                        dcc.Graph(
                            id='output_1_2', figure=figures[1]
                        )
                    ], 
                    width={'size': 4, 'offset': 0}
                ), 
                dbc.Col(
                    [
                        dcc.Graph(
                            id='output_1_3', figure=figures[2]
                        )
                    ], 
                    width={'size': 4, 'offset': 0}
                )
            ], no_gutters=False, justify='around'),
            dbc.Row([
                dbc.Col(
                    [
                        dcc.Graph(
                            id='output_2_1', figure=figures[3]
                        )
                    ], 
                    width={'size': 4, 'offset': 0}
                ),
                dbc.Col(
                    [
                        dcc.Graph(
                            id='output_2_2', figure=figures[4]
                        )
                    ], 
                    width={'size': 4, 'offset': 0}
                ), 
                dbc.Col(
                    [
                        dcc.Graph(
                            id='output_2_3', figure=figures[5]
                        )
                    ], 
                    width={'size': 4, 'offset': 0}
                )
            ], no_gutters=False, justify='around')
        ]
    )