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
import numpy as np
import generate_figures_info


def context_layout(data):
    info_ = generate_figures_info.context(data)
    return dbc.Col(
        [
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(
                                id='plt_context_ages', 
                                style={'height': '300px'}, 
                                figure=info_['plt_context_ages']
                            )
                        ])
                    ], no_gutters=False, justify='around', style={"margin-top": "50px"}), 
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(
                                id='plt_context_marital_age_academic', 
                                style={'height': '600px'}, 
                                figure=info_['plt_context_marital_age_academic']
                            )
                        ])
                    ], style={'margin-top': '20px'}, no_gutters=False, justify='around')
                ], width={'size': 7, 'offset': 0}), 
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                html.Div(info_['mortality_cnt'], id='mortality_cnt', style={'fontWeight': 'bold', 'fontSize': 25}, className='text-center'),
                                html.Div('Deaths', style={'fontWeight': 'bold', 'fontSize': 15}, className='text-center')
                            ])
                        ], width={'size': 3, 'offset': 1}),
                        dbc.Col([
                            dbc.Card([
                                html.Div(info_['morbidity_cnt'], id='morbility_cnt', style={'fontWeight': 'bold', 'fontSize': 25}, className='text-center'),
                                html.Div('Morbidities', style={'fontWeight': 'bold', 'fontSize': 15}, className='text-center')
                            ])
                        ], width={'size': 3, 'offset': 1}),
                        dbc.Col([
                            dbc.Card([
                                html.Div(info_['covid_cnt'], id='covid_cnt', style={'fontWeight': 'bold', 'fontSize': 25}, className='text-center'),
                                html.Div('COVID-19', style={'fontWeight': 'bold', 'fontSize': 15}, className='text-center'),
                            ])
                        ], width={'size': 3, 'offset': 1})
                    ], style={'margin-top': '50px'}, no_gutters=False, justify='around'), 
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(
                                id='plt_context_estrato', 
                                style={'height': '300px'}, 
                                figure=info_['plt_context_estrato']
                            )
                        ])
                    ], style={'margin-top': '50px'}, no_gutters=False, justify='around'), 
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(
                                id='plt_context_parents_age', 
                                style={'height': '400px'}, 
                                figure=info_['plt_context_parents_age']
                            )
                        ])
                    ], style={'margin-top': '50px'}, no_gutters=False, justify='around')
                ], width={'size': 5, 'offset': 0})
            ],className='fndtb')
        ])


def births_layout(data):
    info_ = generate_figures_info.births(data)
    return dbc.Col(
        [
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        id='plt_births_low_weight', 
                        style={'height': '400px'}, 
                        figure=info_['plt_births_low_weight']
                    )
                ])
            ], style={'margin-top': '50px'}, no_gutters=False, justify='around'), 
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        id='plt_births_num_children', 
                        style={'height': '400px'}, 
                        figure=info_['plt_births_num_children']
                    )
                ], width={'size': 6, 'offset': 0}), 
                dbc.Col([
                    dcc.Graph(
                        id='plt_births_multiplicity', 
                        style={'height': '400px'}, 
                        figure=info_['plt_births_multiplicity']
                    )
                ], width={'size': 6, 'offset': 0})
            ], style={'margin-top': '20px'}, no_gutters=False, justify='around'), 
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        id='plt_births_parents_age', 
                        style={'height': '400px'}, 
                        figure=info_['plt_births_parents_age']
                    )
                ], width={'size': 4, 'offset': 0}), 
                dbc.Col([
                    dcc.Graph(
                        id='plt_births_birth_type', 
                        style={'height': '400px'}, 
                        figure=info_['plt_births_birth_type']
                    )
                ], width={'size': 4, 'offset': 0}), 
                dbc.Col([
                    dcc.Graph(
                        id='plt_births_marital', 
                        style={'height': '400px'}, 
                        figure=info_['plt_births_marital']
                    )
                ], width={'size': 4, 'offset': 0})
            ], style={'margin-top': '20px'}, no_gutters=False, justify='around')
        ],className='fndtb')


def births_layout_2(data):
    info_ = generate_figures_info.births2(data)
    return dbc.Col(
        [
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row(html.H5('Low Weight', className="card-title")), 
                            dbc.Row([
                                dbc.Col([
                                    dcc.Dropdown(
                                        id='low_weight_description_selector', 
                                        options=[
                                            {'label': 'Mother Age', 'value': 1},
                                            {'label': 'Gestation Weeks', 'value': 2}, 
                                            {'label': 'Socioeconomic Status', 'value': 3},
                                            {'label': 'Sex', 'value': 4},
                                            {'label': 'Academic Level', 'value': 5},
                                            {'label': 'Prenatal consultations', 'value': 6},
                                            {'label': 'Multiplicity of pregnancy', 'value': 7},
                                            {'label': 'Previous pergnancy', 'value': 8}
                                        ],
                                        value=1
                                    )
                                ], width={'size': 6, 'offset': 0}), 
                                dbc.Col([], width={'size': 6, 'offset': 0})
                            ]), 
                            dbc.Row([
                                dbc.Col([
                                    dcc.Graph(
                                        id='plt_births_low_weight_description', 
                                        style={'height': '400px'}, 
                                        figure={}
                                    )
                                ], width={'size': 6, 'offset': 0}), 
                                dbc.Col([
                                    dcc.Graph(
                                        id='plt_births_low_weight_distribution', 
                                        style={'height': '400px'}, 
                                        figure={}
                                    )
                                ], width={'size': 6, 'offset': 0})
                            ]), 
                            dbc.Row([
                                dbc.Col([
                                    dcc.Graph(
                                        id='plt_lowweight_map', 
                                        style={'height': '700px'}, 
                                        figure={}#"generate_figures_info.generate_map(data.df_morbidity, 'nmun_resi', 'Morbidity') #morbidity_map(data.df_morbidity)
                                    )
                                ], width={'size': 10, 'offset': 0})
                            ])
                        ])
                    ])
                ])
            ], style={'margin-top': '50px'}, no_gutters=False, justify='around'), 
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row(html.H5('General', className="card-title")), 
                            dbc.Row([
                                dbc.Col([
                                    dcc.Graph(
                                        id='plt_births_num_children', 
                                        style={'height': '400px'}, 
                                        figure=info_['plt_births_num_children_2']
                                    )
                                ], width={'size': 6, 'offset': 0}), 
                                dbc.Col([
                                    dcc.Graph(
                                        id='plt_births_multiplicity', 
                                        style={'height': '400px'}, 
                                        figure=info_['plt_births_marital_2']
                                    )
                                ], width={'size': 6, 'offset': 0})
                            ]), 
                            dbc.Row([
                                dbc.Col([
                                    dcc.Graph(
                                        id='plt_births_parents_age', 
                                        style={'height': '400px'}, 
                                        figure=info_['plt_births_parents_age_2']
                                    )
                                ], width={'size': 3, 'offset': 0}), 
                                dbc.Col([
                                    dcc.Graph(
                                        id='plt_births_birth_type', 
                                        style={'height': '400px'}, 
                                        figure=info_['plt_births_birth_type_2']
                                    )
                                ], width={'size': 6, 'offset': 0}), 
                                dbc.Col([
                                    dcc.Graph(
                                        id='plt_births_marital', 
                                        style={'height': '400px'}, 
                                        figure=info_['plt_births_multiplicity_2']
                                    )
                                ], width={'size': 3, 'offset': 0})
                            ], style={'margin-top': '20px'}, no_gutters=False, justify='around')
                        ])
                    ])
                ])
            ], style={'margin-top': '20px', 'margin-bottom': '20px'}, no_gutters=False, justify='around')
        ],className='fndtb')



def morbidity_layout(data):
    return dbc.Col(
        [
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(
                        id='morbidity_var_selector', 
                        options=[
                            {'label': 'Mother Age', 'value': 'edad_'},
                            {'label': 'Gestation Week', 'value': 'sem_ges_'}, 
                            {'label': 'Socioeconomic Status', 'value': 'estrato_'}
                        ],
                        value='edad_'
                    )
                ])
            ], style={'margin-top': '50px'}, no_gutters=False, justify='around'), 
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        id='plt_morbidity_failures', 
                        style={'height': '400px'}, 
                        figure={}
                    )
                ], width={'size': 7, 'offset': 0}), 
                dbc.Col([
                    dcc.Graph(
                        id='plt_morbidity_grouped_cause', 
                        style={'height': '400px'}, 
                        figure={}
                    )
                ], width={'size': 5, 'offset': 0})
            ], style={'margin-top': '20px'}, no_gutters=False, justify='around'), 
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        id='plt_morbidity_grouped_cause_year', 
                        style={'height': '400px'}, 
                        figure={}
                    )
                ], width={'size': 5, 'offset': 0}), 
                dbc.Col([
                    dcc.Graph(
                        id='plt_morbidity_pregnancy', 
                        style={'height': '400px'}, 
                        figure={}
                    )
                ], width={'size': 7, 'offset': 0})
            ], style={'margin-top': '20px'}, no_gutters=False, justify='around'),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        id='plt_morbidity_map', 
                        style={'height': '700px'}, 
                        figure=generate_figures_info.generate_map(data.df_morbidity, 'nmun_resi', 'Morbidity') #morbidity_map(data.df_morbidity)
                    )
                ], width={'size': 10, 'offset': 0})
            ], style={'margin-top': '20px'}, no_gutters=False, justify='around')
        ],className='fndtb')


def mortality_layout(data):
    return dbc.Col(
        [
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(
                        id='mortality_var_selector', 
                        options=[
                            {'label': 'Mother Age', 'value': 'edad_'},
                            {'label': 'Gestation Week', 'value': 'sem_ges_'}, 
                            {'label': 'Socioeconomic Status', 'value': 'estrato_'}
                        ],
                        value='edad_'
                    )
                ], width={'size': 7, 'offset': 0}), 
                dbc.Col([], width={'size': 5, 'offset': 0})
            ], style={'margin-top': '50px'}, no_gutters=False, justify='around'), 
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        id='plt_mortality_demographic', 
                        style={'height': '400px'}, 
                        figure={}
                    )
                ], width={'size': 7, 'offset': 0}), 
                dbc.Col([
                    dcc.Graph(
                        id='plt_mortality_year', 
                        style={'height': '400px'}, 
                        figure={}
                    )
                ], width={'size': 5, 'offset': 0})
            ], style={'margin-top': '20px'}, no_gutters=False, justify='around'), 
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        id='plt_mortality_upgd', 
                        style={'height': '400px'}, 
                        figure={}
                    )
                ], width={'size': 6, 'offset': 0}),
                dbc.Col([
                    dcc.Graph(
                        id='plt_mortality_cbmte', 
                        style={'height': '500px'}, 
                        figure={}
                    )
                ], width={'size': 6, 'offset': 0})
            ], style={'margin-top': '20px'}, no_gutters=False, justify='around'),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        id='plt_mortality_map', 
                        style={'height': '700px'}, 
                        figure=generate_figures_info.generate_map(data.df_mortality, 'nmun_resi', 'Mortality')
                    )
                ], width={'size': 10, 'offset': 0})
            ], style={'margin-top': '20px'}, no_gutters=False, justify='around')
        ],className='fndtb')