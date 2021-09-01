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

def prevnant_layout():
    return dbc.Col(
        [
            dbc.Row([
                dbc.Col([
                    html.Img(
                        src='data:image/png;base64,{}'.format(
                            base64.b64encode(
                                open(
                                    './assets/pregnant.png', 'rb'
                                ).read()
                            ).decode()
                        ),
                        height='100%',
                        width='100%', 
                        style={'margin-left': '5%'}
                    )
                ], width={'size': 3, 'offset': 0}), 
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Img(
                                    src='data:image/png;base64,{}'.format(
                                        base64.b64encode(
                                            open(
                                                './assets/stats.jpg', 'rb'
                                            ).read()
                                        ).decode()
                                    ),
                                    height='10%',
                                    width='50%'
                                )
                            ], className='text-center'), 
                            html.P('Context', style={'textAlign': 'center', 'fontWeight': 'bold', 'fontSize': '0.9vw', 'font-family':'glacial indifference , sans-serif'}), 
                            html.P('Context tab shows general plots for describing data, which includes age, socioeconomic status and academic level of mothers and pregnant women', style={'textAlign': 'center', 'fontSize': '0.7vw', 'font-family':'glacial indifference , sans-serif'}), 
                        ], width={'size': 4, 'offset': 0}), 
                        dbc.Col([
                            html.Div([
                                html.Img(
                                    src='data:image/png;base64,{}'.format(
                                        base64.b64encode(
                                            open(
                                                './assets/births.png', 'rb'
                                            ).read()
                                        ).decode()
                                    ),
                                    width='40%'
                                )
                            ], className='text-center'), 
                            html.P('Births', style={'textAlign': 'center', 'fontWeight': 'bold', 'fontSize': '0.9vw', 'font-family':'glacial indifference , sans-serif'}), 
                            html.P('Births tab is composed by two sections. The general section shows plots for all registered births in Bucaramanga while the low weight section includes only low-weight registers. Additionally, you can see a geographical distribution for every one.', style={'textAlign': 'center', 'fontSize': '0.7vw', 'font-family':'glacial indifference , sans-serif'}), 
                        ], width={'size': 4, 'offset': 0}), 
                        dbc.Col([
                            html.Div([
                                html.Img(
                                    src='data:image/png;base64,{}'.format(
                                        base64.b64encode(
                                            open(
                                                './assets/morbidity.png', 'rb'
                                            ).read()
                                        ).decode()
                                    ),
                                    width='33%'
                                )
                            ], className='text-center'), 
                            html.P('Morbidity', style={'textAlign': 'center', 'fontWeight': 'bold', 'fontSize': '0.9vw', 'font-family':'glacial indifference , sans-serif'}), 
                            html.P('Morbidity tab shows general failures as well as pregnancy related issues. Additionally, grouped causes for registered morbidity events are also included. Geographical information about municipalities and Bucaramanga registers are available.', style={'textAlign': 'center', 'fontSize': '0.7vw', 'font-family':'glacial indifference , sans-serif'}), 
                        ], width={'size': 4, 'offset': 0})
                    ], style={'margin-top': '13%'}, no_gutters=False, justify='around'), 
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Img(
                                    src='data:image/png;base64,{}'.format(
                                        base64.b64encode(
                                            open(
                                                './assets/mortality.png', 'rb'
                                            ).read()
                                        ).decode()
                                    ),
                                    width='33%'
                                )
                            ], className='text-center'), 
                            html.P('Mortality', style={'textAlign': 'center', 'fontWeight': 'bold', 'fontSize': '0.9vw', 'font-family':'glacial indifference , sans-serif'}), 
                            html.P('Mortality tab shows maternal death information which includes age, gestation weeks as well as corresponding causes. Geographical information about municipalities and Bucaramanga registers are available.', style={'textAlign': 'center', 'fontSize': '0.7vw', 'font-family':'glacial indifference , sans-serif'}), 
                        ]), 
                        dbc.Col([
                            html.Div([
                                html.Img(
                                    src='data:image/png;base64,{}'.format(
                                        base64.b64encode(
                                            open(
                                                './assets/covid.png', 'rb'
                                            ).read()
                                        ).decode()
                                    ),
                                    width='33%'
                                )
                            ], className='text-center'), 
                            html.P('COVID-19', style={'textAlign': 'center', 'fontWeight': 'bold', 'fontSize': '0.9vw', 'font-family':'glacial indifference , sans-serif'}), 
                            html.P('COVID-19 tab shows age of maternals with COVID-19 diagnosis. Geographical information about COVID-19 registers for maternals in Bucaramanga is also shown.', style={'textAlign': 'center', 'fontSize': '0.7vw', 'font-family':'glacial indifference , sans-serif'}), 
                        ]), 
                        dbc.Col([
                            html.Div([
                                html.Img(
                                    src='data:image/png;base64,{}'.format(
                                        base64.b64encode(
                                            open(
                                                './assets/model.png', 'rb'
                                            ).read()
                                        ).decode()
                                    ),
                                    width='37%'
                                )
                            ], className='text-center'), 
                            html.P('Model', style={'textAlign': 'center', 'fontWeight': 'bold', 'fontSize': '0.9vw', 'font-family':'glacial indifference , sans-serif'}), 
                            html.P('Model tab includes two sections. Morbidity section allows to set some interest variables of maternal and then predicts a corresponding probability of issue. Similar for low-weight section.', style={'textAlign': 'center', 'fontSize': '0.7vw', 'font-family':'glacial indifference , sans-serif'}), 
                        ])
                    ], style={'margin-top': '3%'}, no_gutters=False, justify='around')
                ], width={'size': 8, 'offset': 0})
            ], className='fndtb')
        ])


def context_layout(data):
    info_ = generate_figures_info.context(data)
    return dbc.Col(
        [
            dbc.Alert(
                'Context tab shows general plots for describing data, which includes age, socioeconomic status and academic level of mothers and pregnant women',
                dismissable=True,
                is_open=True,
                color='primary', 
                style={'margin-top': '50px'}
            ), 
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(
                                id='plt_context_ages_status', 
                                style={'height': '500px'}, 
                                figure=info_['plt_context_ages_status']
                            )
                        ])
                    ], no_gutters=False, justify='around', style={"margin-top": "20px"}), 
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(
                                id='plt_context_marital_age_academic', 
                                style={'height': '500px'}, 
                                figure=info_['plt_context_marital_age_academic']
                            ), 
                            dbc.Alert(
                                "Here you can explore some demographic variables such as mother marital status, their age range and academic level. You can click any field in the plot in order to go deeper in the data. Couple > 2: Parents have lived together for more than two years. Couple < 2: Parents have lived together for less than two years", 
                                dismissable=True,
                                is_open=True,
                                color='warning', 
                                style={'margin-top': '10px'}
                            )
                        ])
                    ], style={'margin-top': '65px'}, no_gutters=False, justify='around')
                ], width={'size': 7, 'offset': 0}), 
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                html.Div(info_['mortality_cnt'], id='mortality_cnt', style={'fontWeight': 'bold', 'fontSize': 25}, className='text-center'),
                                html.Div('Deaths', style={'fontSize': 15}, className='text-center')
                            ])
                        ], width={'size': 3, 'offset': 1}),
                        dbc.Col([
                            dbc.Card([
                                html.Div(info_['morbidity_cnt'], id='morbibity_cnt', style={'fontWeight': 'bold', 'fontSize': 25}, className='text-center'),
                                html.Div('Morbidities', style={'fontSize': 15}, className='text-center')
                            ])
                        ], width={'size': 3, 'offset': 1}),
                        dbc.Col([
                            dbc.Card([
                                html.Div(info_['covid_cnt'], id='covid_cnt', style={'fontWeight': 'bold', 'fontSize': 25}, className='text-center'),
                                html.Div('COVID-19', style={'fontSize': 15}, className='text-center'),
                            ])
                        ], width={'size': 3, 'offset': 1})
                    ], style={'margin-top': '20px'}, no_gutters=False, justify='around'), 
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(
                                id='plt_context_consults', 
                                style={'height': '300px'}, 
                                figure=info_['plt_context_consults']
                            )
                        ])
                    ], style={'margin-top': '50px'}, no_gutters=False, justify='around'), 
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(
                                id='plt_context_regime', 
                                style={'height': '400px'}, 
                                figure=info_['plt_context_regime']
                            )
                        ])
                    ], style={'margin-top': '50px'}, no_gutters=False, justify='around'), 
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(
                                id='plt_context_diff_ages', 
                                style={'height': '400px'}, 
                                figure=info_['plt_context_diff_ages']
                            )
                        ])
                    ], style={'margin-top': '50px'}, no_gutters=False, justify='around')
                ], width={'size': 5, 'offset': 0})
            ])
        ], className='fndtb')


def births_layout(data):
    info_ = generate_figures_info.births(data)
    return dbc.Col(
        [
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row(html.H5('General', className="card-title")), 
                            dbc.Alert(
                                "The following plots show all registered births. It includes relationships between weight and marital status as well as birth type and pregnant multiplicity. It also includes a parent's age representation. You can move the cursor over plots to get more information. Additionally, you can use legends to filter data.",
                                dismissable=True,
                                is_open=True,
                                color='primary', 
                                style={'margin-top': '10px'}
                            ), 
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
                                        figure=info_['plt_births_marital']
                                    )
                                ], width={'size': 6, 'offset': 0})
                            ]), 
                            dbc.Row([
                                dbc.Col([
                                    dcc.Graph(
                                        id='plt_births_parents_age', 
                                        style={'height': '400px'}, 
                                        figure=info_['plt_births_parents_age']
                                    )
                                ], width={'size': 3, 'offset': 0}), 
                                dbc.Col([
                                    dcc.Graph(
                                        id='plt_births_birth_type', 
                                        style={'height': '400px'}, 
                                        figure=info_['plt_births_birth_type']
                                    )
                                ], width={'size': 6, 'offset': 0}), 
                                dbc.Col([
                                    dcc.Graph(
                                        id='plt_births_marital', 
                                        style={'height': '400px'}, 
                                        figure=info_['plt_births_multiplicity']
                                    )
                                ], width={'size': 3, 'offset': 0})
                            ], style={'margin-top': '20px'}, no_gutters=False, justify='around')
                        ])
                    ])
                ])
            ], style={'margin-top': '50px'}, no_gutters=False, justify='around'), 
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row(html.H5('Low Weight', className="card-title")), 
                            dbc.Alert(
                                "The following plots show low-weight registered births. It includes weight distribution and you can filter by some demographic variables such as age, socioeconomic status, sex and so on.", 
                                dismissable=True,
                                is_open=True,
                                color='primary', 
                                style={'margin-top': '10px'}
                            ), 
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
                                            {'label': 'Previous pregnancy', 'value': 8}
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
                            ])
                        ])
                    ])
                ])
            ], style={'margin-top': '20px', 'margin-bottom': '20px'}, no_gutters=False, justify='around'), 
            dbc.Row([
                dbc.Col([
                    dbc.Alert(
                        "This map shows births in Bucaramanga. It is allowed to filter by all births as well as low-weight births.", 
                        dismissable=True,
                        is_open=True,
                        color='warning', 
                        style={'margin-top': '10px'}
                    ), 
                    dcc.Dropdown(
                        id='births_map_var_selector', 
                        options=[
                            {'label': 'General Births', 'value': 1},
                            {'label': 'Low Weight Births', 'value': 2}
                        ],
                        value=1
                    )
                ], width={'size': 10, 'offset': 0})
            ], style={'margin-top': '30px'}, no_gutters=False, justify='around'), 
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        id='plt_births_map', 
                        style={'height': '700px'}, 
                        figure={}
                    )
                ], width={'size': 10, 'offset': 0})
            ], style={'margin-top': '5px', 'margin-bottom': '20px'}, no_gutters=False, justify='around'), 
        ], className='fndtb')



def morbidity_layout(data):
    years = list(data.years_dict['morbidity'].keys())
    min_year = years[0]
    max_year = years[-1]
    return dbc.Col(
        [
            dbc.Row([
                dbc.Col([
                    dcc.RangeSlider(
                        id='morbidity_year_selector', 
                        min=min_year,
                        max=max_year,
                        step=None,
                        marks=data.years_dict['morbidity'],
                        value=[min_year, max_year]
                    )
                ], width={'size': 7, 'offset': 2}), 
                dbc.Col([
                    dcc.Dropdown(
                        id='morbidity_geo_selector', 
                        options=[
                            {'label': 'Municipalities', 'value': 1},
                            {'label': 'Bucaramanga', 'value': 2}
                        ],
                        value=1
                    )
                ], width={'size': 2, 'offset': 0})
            ], style={'margin-top': '50px'}, no_gutters=False, justify='around'), 
            dbc.Row([
                dbc.Col([
                    dbc.Alert(
                        "Plots below show general failures and pregnancy related issues. Additionally, grouped causes for registered morbidity events are also included. You can filter them by mother age, gestation week and socioeconomic status or with the plots legend.",
                        dismissable=True,
                        is_open=True,
                        color='primary', 
                        style={'margin-top': '10px'}
                    ), 
                    dcc.Dropdown(
                        id='morbidity_var_selector', 
                        options=[
                            {'label': 'Mother Age', 'value': 'quinquenio'},
                            {'label': 'Gestation Week', 'value': 'sem_ges_'}, 
                            {'label': 'Socioeconomic Status', 'value': 'estrato_'}
                        ],
                        value='quinquenio'
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
                    ), 
                    dbc.Alert(
                        "Grouped causes are: 1. Trastornos hipertensivos, 2. Complicaciones hemorrágicas, 3. Complicaciones del aborto, 4. Sepsis de origen obstétrico, 5. Sepsis de origen no obstétrico, 6. Sepsis de origen pulmonar, 7. Enfermedad preexistente que se complica, 8. Otra causa.",
                        dismissable=True,
                        is_open=True,
                        color='warning', 
                        style={'margin-top': '10px'}
                    )
                ], width={'size': 5, 'offset': 0})
            ], style={'margin-top': '20px'}, no_gutters=False, justify='around'), 
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        id='plt_morbidity_grouped_cause_year', 
                        style={'height': '400px'}, 
                        figure={}
                    ), 
                    dbc.Alert(
                        "Grouped causes are: 1. Trastornos hipertensivos, 2. Complicaciones hemorrágicas, 3. Complicaciones del aborto, 4. Sepsis de origen obstétrico, 5. Sepsis de origen no obstétrico, 6. Sepsis de origen pulmonar, 7. Enfermedad preexistente que se complica, 8. Otra causa.",
                        dismissable=True,
                        is_open=True,
                        color='warning', 
                        style={'margin-top': '10px'}
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
                    dbc.Alert(
                        "The map below shows morbidities in department or in Bucaramanga. You can select which one with the corresponding selector above.",
                        dismissable=True,
                        is_open=True,
                        color='warning', 
                        style={'margin-top': '10px'}
                    ), 
                ], width={'size': 10, 'offset': 0})
            ], style={'margin-top': '50px'}, no_gutters=False, justify='around'), 
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        id='plt_morbidity_map', 
                        style={'height': '700px'}, 
                        figure={}
                    )
                ], width={'size': 10, 'offset': 0})
            ], style={'margin-top': '5px'}, no_gutters=False, justify='around')
        ], className='fndtb')


def mortality_layout(data):
    years = list(data.years_dict['mortality'].keys())
    min_year = years[0]
    max_year = years[-1]
    return dbc.Col(
        [
            dbc.Row([
                dbc.Col([
                    dcc.RangeSlider(
                        id='mortality_year_selector', 
                        min=min_year,
                        max=max_year,
                        step=None,
                        marks=data.years_dict['mortality'],
                        value=[min_year, max_year]
                    )
                ], width={'size': 7, 'offset': 2}), 
                dbc.Col([
                    dcc.Dropdown(
                        id='mortality_geo_selector', 
                        options=[
                            {'label': 'Municipalities', 'value': 1},
                            {'label': 'Bucaramanga', 'value': 2}
                        ],
                        value=1
                    )
                ], width={'size': 2, 'offset': 0})
            ], style={'margin-top': '50px'}, no_gutters=False, justify='around'), 
            dbc.Row([
                dbc.Col([
                    dbc.Alert(
                        "Here maternal deaths are shown. You can filter them by mother age, gestation week and socioeconomic status.",
                        dismissable=True,
                        is_open=True,
                        color='primary', 
                        style={'margin-top': '10px'}
                    ), 
                    dcc.Dropdown(
                        id='mortality_var_selector', 
                        options=[
                            {'label': 'Mother Age', 'value': 'quinquenio'},
                            {'label': 'Gestation Week', 'value': 'sem_ges_'}, 
                            {'label': 'Socioeconomic Status', 'value': 'estrato_'}
                        ],
                        value='quinquenio'
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
                    ), 
                    dbc.Alert(
                        "UPGD stands for Unidad Primaria Generadora de Datos. It is a public or private entity that captures the occurrence of events of interest in public health and generates useful and necessary information for the purposes of the Public Health Surveillance System, Sivigila",
                        dismissable=True,
                        is_open=True,
                        color='warning', 
                        style={'margin-top': '10px'}
                    )
                ], width={'size': 6, 'offset': 0}),
                dbc.Col([
                    dcc.Graph(
                        id='plt_mortality_cbmte', 
                        style={'height': '500px'}, 
                        figure={}
                    ), 
                    dbc.Alert(
                        "Inner data shows basic cause of death and external number show coresponding mother age. You can click them to extend visualization. U071: COVID-19 (virus identificado). R579: Choque, No Especificado. J159: Neumonía bacteriana, no especificada U072: COVID-19 (virus no identificado). I472: Taquicardia Ventricular. I619: I619	Hemorragia Intracefálica, No Especificada. R571: Choque Hipovolémico",
                        dismissable=True,
                        is_open=True,
                        color='warning', 
                        style={'margin-top': '10px'}
                    )
                ], width={'size': 6, 'offset': 0})
            ], style={'margin-top': '20px'}, no_gutters=False, justify='around'), 
            dbc.Row([
                dbc.Col([
                    dbc.Alert(
                        "The map below shows mortality registers in department or in Bucaramanga. You can select which one with the corresponding selector above.",
                        dismissable=True,
                        is_open=True,
                        color='warning', 
                        style={'margin-top': '10px'}
                    ) 
                ], width={'size': 10, 'offset': 0})
            ], style={'margin-top': '50px'}, no_gutters=False, justify='around'), 
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        id='plt_mortality_map', 
                        style={'height': '700px'}, 
                        figure={}
                    )
                ], width={'size': 10, 'offset': 0})
            ], style={'margin-top': '5px'}, no_gutters=False, justify='around')
        ], className='fndtb')


def covid_layout(data):
    info_ = generate_figures_info.covid(data)
    return dbc.Col(
        [
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        id='plt_covid_age', 
                        style={'height': '400px'}, 
                        figure=info_['plt_covid_age']
                    )
                ], width={'size': 7, 'offset': 0}), 
                dbc.Col([
                    dcc.Graph(
                        id='plt_covid_year', 
                        style={'height': '400px'}, 
                        figure=info_['plt_covid_year']
                    ), 
                    dbc.Alert(
                        "It shows Covid notifications in maternals through time.",
                        dismissable=True,
                        is_open=True,
                        color='warning', 
                        style={'margin-top': '10px'}
                    )
                ], width={'size': 5, 'offset': 0})
            ], style={'margin-top': '20px'}, no_gutters=False, justify='around'), 
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        id='plt_covid_map', 
                        style={'height': '700px'}, 
                        figure=info_['plt_covid_map']
                    )
                ], width={'size': 10, 'offset': 0})
            ], style={'margin-top': '5px'}, no_gutters=False, justify='around')
        ], className='fndtb')


def model_layout():
    return dbc.Col(
        [
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row(html.H5('Morbidities and Mortality', className="card-title")), 
                            dbc.Alert(
                                "This model predicts morbidity probability in pregnant woman. Enter corresponding data then press Predict.",
                                dismissable=True,
                                is_open=True,
                                color='primary', 
                                style={'margin-top': '10px'}
                            ), 
                            dbc.Row([
                                dbc.Col([
                                    dbc.Row([
                                        dbc.Col([
                                            html.P('Mother Age', style={'textAlign': 'right', 'fontSize': '0.75vw', 'font-family':'glacial indifference , sans-serif'})
                                        ], width={'size': 2, 'offset': 1}), 
                                        dbc.Col([
                                            dbc.Input(id='morbidity_mother_age', placeholder='Enter mother age', type="text")
                                        ], width={'size': 6, 'offset': 0}), 
                                        dbc.Col([], width={'size': 3, 'offset': 0})
                                    ], no_gutters=False, justify='around'), 
                                    dbc.Row([
                                        dbc.Col([
                                            html.P('Gestations weeks', style={'textAlign': 'right', 'fontSize': '0.75vw', 'font-family':'glacial indifference , sans-serif'})
                                        ], width={'size': 2, 'offset': 1}), 
                                        dbc.Col([
                                            dbc.Input(id='morbidity_gest_weeks', placeholder='Enter gestations weeks', type="text")
                                        ], width={'size': 6, 'offset': 0}), 
                                        dbc.Col([], width={'size': 3, 'offset': 0})
                                    ], no_gutters=False, justify='around'),
                                    dbc.Row([
                                        dbc.Col([
                                            html.P('Security Regime', style={'textAlign': 'right', 'fontSize': '0.75vw', 'font-family':'glacial indifference , sans-serif'})
                                        ], width={'size': 2, 'offset': 1}), 
                                        dbc.Col([
                                            dcc.Dropdown(
                                                id='morbidity_sec_reg', 
                                                options=[
                                                    {'label': 'No asegurado', 'value': 0},
                                                    {'label': 'Subsidiado', 'value': 1},
                                                    {'label': 'Contributivo/Excepcion/Especial', 'value': 2}
                                                ],
                                                value=0
                                            )
                                        ], width={'size': 6, 'offset': 0}), 
                                        dbc.Col([], width={'size': 3, 'offset': 0})
                                    ], no_gutters=False, justify='around'), 
                                    dbc.Row([
                                        dbc.Col([
                                            html.P('# Prenatal consultations', style={'textAlign': 'right', 'fontSize': '0.75vw', 'font-family':'glacial indifference , sans-serif'})
                                        ], width={'size': 2, 'offset': 1}), 
                                        dbc.Col([
                                            dbc.Input(id='morbidity_pren_con', placeholder='Enter prenatal consultations', type="text")
                                        ], width={'size': 6, 'offset': 0}), 
                                        dbc.Col([], width={'size': 3, 'offset': 0})
                                    ], no_gutters=False, justify='around'), 
                                    dbc.Row([
                                        dbc.Col([
                                            html.P('# Pregnancies', style={'textAlign': 'right', 'fontSize': '0.75vw', 'font-family':'glacial indifference , sans-serif'})
                                        ], width={'size': 2, 'offset': 1}), 
                                        dbc.Col([
                                            dbc.Input(id='morbidity_num_pregnancies', placeholder='Enter number of pregnancies', type="text")
                                        ], width={'size': 6, 'offset': 0}), 
                                        dbc.Col([], width={'size': 3, 'offset': 0})
                                    ], no_gutters=False, justify='around'), 
                                    dbc.Row([
                                        dbc.Col([
                                            html.P('# Hospitalizations', style={'textAlign': 'right', 'fontSize': '0.75vw', 'font-family':'glacial indifference , sans-serif'})
                                        ], width={'size': 2, 'offset': 1}), 
                                        dbc.Col([
                                            dbc.Input(id='morbidity_num_hosp', placeholder='Enter number of hospitalizations', type="text")
                                        ], width={'size': 6, 'offset': 0}), 
                                        dbc.Col([], width={'size': 3, 'offset': 0})
                                    ], no_gutters=False, justify='around'), 
                                    dbc.Row([
                                        dbc.Col([
                                            html.P('Marital Status', style={'textAlign': 'right', 'fontSize': '0.75vw', 'font-family':'glacial indifference , sans-serif'})
                                        ], width={'size': 2, 'offset': 1}), 
                                        dbc.Col([
                                            dcc.Dropdown(
                                                id='morbidity_marital', 
                                                options=[
                                                    {'label': 'Without partner', 'value': 0},
                                                    {'label': 'With partner', 'value': 1}
                                                ],
                                                value=0
                                            )
                                        ], width={'size': 6, 'offset': 0}), 
                                        dbc.Col([], width={'size': 3, 'offset': 0})
                                    ], no_gutters=False, justify='around'), 
                                    dbc.Row([
                                        dbc.Col([
                                            html.P('Mother Academic Level', style={'textAlign': 'right', 'fontSize': '0.75vw', 'font-family':'glacial indifference , sans-serif'})
                                        ], width={'size': 2, 'offset': 1}), 
                                        dbc.Col([
                                            dcc.Dropdown(
                                                id='morbidity_mother_academic', 
                                                options=[
                                                    {'label': 'Ninguno', 'value': 0},
                                                    {'label': 'Preescolar', 'value': 1}, 
                                                    {'label': 'Basica Primaria', 'value': 2},
                                                    {'label': 'Basica Secundaria', 'value': 3},
                                                    {'label': 'Media Academica/Clasica/Tecnica/Normalista', 'value': 4},
                                                    {'label': 'Tecnica Profesional', 'value': 5},
                                                    {'label': 'Tecnologica', 'value': 6},
                                                    {'label': 'Profesional', 'value': 7},
                                                    {'label': 'Especializacion', 'value': 8},
                                                    {'label': 'Maestria', 'value': 9},
                                                    {'label': 'Doctorado', 'value': 10},
                                                ],
                                                value=0
                                            )
                                        ], width={'size': 6, 'offset': 0}), 
                                        dbc.Col([], width={'size': 3, 'offset': 0})
                                    ], no_gutters=False, justify='around'), 
                                    dbc.Row([
                                        dbc.Col([
                                            html.P('Covid 19', style={'textAlign': 'right', 'fontSize': '0.75vw', 'font-family':'glacial indifference , sans-serif'})
                                        ], width={'size': 2, 'offset': 1}), 
                                        dbc.Col([
                                            dcc.Dropdown(
                                                id='morbidity_covid', 
                                                options=[
                                                    {'label': 'No', 'value': 0},
                                                    {'label': 'Yes', 'value': 1}
                                                ],
                                                value=0
                                            )
                                        ], width={'size': 6, 'offset': 0}), 
                                        dbc.Col([], width={'size': 3, 'offset': 0})
                                    ], no_gutters=False, justify='around')
                                ], width={'size': 6, 'offset': 0}), 
                                dbc.Col([
                                    html.P('Predict probablity of morbidity in maternal', style={'textAlign': 'left', 'fontWeight': 'bold', 'fontSize': '0.9vw', 'font-family':'glacial indifference , sans-serif'}), 
                                    dbc.Alert(
                                        "Press Predict to obtain the corresponding result",
                                        dismissable=True,
                                        is_open=True,
                                        color='info'
                                    ), 
                                    dbc.Button("Predict", id='morb_predict_btn', color="primary", outline=True, className="mr-1", n_clicks=0),
                                    dbc.Progress(id='morbidity_pred', className="mb-3", style={'margin-top': '2%'})
                                ], width={'size': 6, 'offset': 0})
                            ])
                        ])
                    ])
                ])
            ], style={'margin-top': '50px'}, no_gutters=False, justify='around'), 
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row(html.H5('Low Weight', className="card-title")), 
                            dbc.Alert(
                                "This model predicts low-weight probability of baby. Enter corresponding data then press Predict.",
                                dismissable=True,
                                is_open=True,
                                color='primary', 
                                style={'margin-top': '10px'}
                            ), 
                            dbc.Row([
                                dbc.Col([
                                    dbc.Row([
                                        dbc.Col([
                                            html.P('Sex', style={'textAlign': 'right', 'fontSize': '0.75vw', 'font-family':'glacial indifference , sans-serif'})
                                        ], width={'size': 2, 'offset': 1}), 
                                        dbc.Col([
                                            dcc.Dropdown(
                                                id='low_weight_sex', 
                                                options=[
                                                    {'label': 'Male', 'value': 0},
                                                    {'label': 'Female', 'value': 1}
                                                ],
                                                value=0
                                            )
                                        ], width={'size': 6, 'offset': 0}), 
                                        dbc.Col([], width={'size': 3, 'offset': 0})
                                    ], no_gutters=False, justify='around'),
                                    dbc.Row([
                                        dbc.Col([
                                            html.P('Mother Age', style={'textAlign': 'right', 'fontSize': '0.75vw', 'font-family':'glacial indifference , sans-serif'})
                                        ], width={'size': 2, 'offset': 1}), 
                                        dbc.Col([
                                            dbc.Input(id='low_weight_mother_age', placeholder='Enter mother age', type="text")
                                        ], width={'size': 6, 'offset': 0}), 
                                        dbc.Col([], width={'size': 3, 'offset': 0})
                                    ], no_gutters=False, justify='around'), 
                                    dbc.Row([
                                        dbc.Col([
                                            html.P('Father Age', style={'textAlign': 'right', 'fontSize': '0.75vw', 'font-family':'glacial indifference , sans-serif'})
                                        ], width={'size': 2, 'offset': 1}), 
                                        dbc.Col([
                                            dbc.Input(id='low_weight_father_age', placeholder='Enter father age', type="text")
                                        ], width={'size': 6, 'offset': 0}), 
                                        dbc.Col([], width={'size': 3, 'offset': 0})
                                    ], no_gutters=False, justify='around'), 
                                    dbc.Row([
                                        dbc.Col([
                                            html.P('Mother Academic Level', style={'textAlign': 'right', 'fontSize': '0.75vw', 'font-family':'glacial indifference , sans-serif'})
                                        ], width={'size': 2, 'offset': 1}), 
                                        dbc.Col([
                                            dcc.Dropdown(
                                                id='low_weight_mother_academic', 
                                                options=[
                                                    {'label': 'Kinder', 'value': 0},
                                                    {'label': 'Elemetary/Middle', 'value': 1}, # Middle
                                                    {'label': 'High School', 'value': 2},
                                                    {'label': 'Technical or Professional', 'value': 3},
                                                    {'label': 'Postgraduate/MSc/PhD', 'value': 4},
                                                    {'label': 'Unknown/None', 'value': 5}
                                                ],
                                                value=0
                                            )
                                        ], width={'size': 6, 'offset': 0}), 
                                        dbc.Col([], width={'size': 3, 'offset': 0})
                                    ], no_gutters=False, justify='around'), 
                                    dbc.Row([
                                        dbc.Col([
                                            html.P('Security Regime', style={'textAlign': 'right', 'fontSize': '0.75vw', 'font-family':'glacial indifference , sans-serif'})
                                        ], width={'size': 2, 'offset': 1}), 
                                        dbc.Col([
                                            dcc.Dropdown(
                                                id='low_weight_sec_reg', 
                                                options=[
                                                    {'label': 'No asegurado', 'value': 0},
                                                    {'label': 'Subsidiado', 'value': 1},
                                                    {'label': 'Contributivo/Excepcion/Especial', 'value': 2}
                                                ],
                                                value=0
                                            )
                                        ], width={'size': 6, 'offset': 0}), 
                                        dbc.Col([], width={'size': 3, 'offset': 0})
                                    ], no_gutters=False, justify='around'), 
                                    dbc.Row([
                                        dbc.Col([
                                            html.P('# Prenatal consultations', style={'textAlign': 'right', 'fontSize': '0.75vw', 'font-family':'glacial indifference , sans-serif'})
                                        ], width={'size': 2, 'offset': 1}), 
                                        dbc.Col([
                                            dbc.Input(id='low_weight_pren_con', placeholder='Enter prenatal consultations', type="text")
                                        ], width={'size': 6, 'offset': 0}), 
                                        dbc.Col([], width={'size': 3, 'offset': 0})
                                    ], no_gutters=False, justify='around'), 
                                    dbc.Row([
                                        dbc.Col([
                                            html.P('# Previous living children', style={'textAlign': 'right', 'fontSize': '0.75vw', 'font-family':'glacial indifference , sans-serif'})
                                        ], width={'size': 2, 'offset': 1}), 
                                        dbc.Col([
                                            dbc.Input(id='low_weight_prev_children', placeholder='Enter previous living children', type="text")
                                        ], width={'size': 6, 'offset': 0}), 
                                        dbc.Col([], width={'size': 3, 'offset': 0})
                                    ], no_gutters=False, justify='around'), 
                                    dbc.Row([
                                        dbc.Col([
                                            html.P('# Pregnancies', style={'textAlign': 'right', 'fontSize': '0.75vw', 'font-family':'glacial indifference , sans-serif'})
                                        ], width={'size': 2, 'offset': 1}), 
                                        dbc.Col([
                                            dbc.Input(id='low_weight_num_pregnancies', placeholder='Enter number of pregnancies', type="text")
                                        ], width={'size': 6, 'offset': 0}), 
                                        dbc.Col([], width={'size': 3, 'offset': 0})
                                    ], no_gutters=False, justify='around'), 
                                    dbc.Row([
                                        dbc.Col([
                                            html.P('Pregnancy multiplicity', style={'textAlign': 'right', 'fontSize': '0.75vw', 'font-family':'glacial indifference , sans-serif'})
                                        ], width={'size': 2, 'offset': 1}), 
                                        dbc.Col([
                                            dcc.Dropdown(
                                                id='low_weight_preg_mult', 
                                                options=[
                                                    {'label': 'No', 'value': 0},
                                                    {'label': 'Yes', 'value': 1}
                                                ],
                                                value=0
                                            )
                                        ], width={'size': 6, 'offset': 0}), 
                                        dbc.Col([], width={'size': 3, 'offset': 0})
                                    ], no_gutters=False, justify='around')
                                ], width={'size': 6, 'offset': 0}), 
                                dbc.Col([
                                    html.P('Predict low-weight probability', style={'textAlign': 'left', 'fontWeight': 'bold', 'fontSize': '0.9vw', 'font-family':'glacial indifference , sans-serif'}), 
                                    dbc.Alert(
                                        "Press Predict to obtain the corresponding result",
                                        dismissable=True,
                                        is_open=True,
                                        color='info'
                                    ), 
                                    dbc.Button("Predict", id='low_weight_predict_btn', color="primary", outline=True, className="mr-1", n_clicks=0),
                                    dbc.Progress(id='low_weight_pred', className="mb-3", style={'margin-top': '2%'})
                                ], width={'size': 6, 'offset': 0})
                            ])
                        ])
                    ])
                ])
            ], style={'margin-top': '20px', 'margin-bottom': '20px'}, no_gutters=False, justify='around')
        ], className='fndtb')


def team_layout():
    return dbc.Col(
        [
            dbc.Row([
                dbc.Col([
                    dbc.Col([
                        html.Div([
                            html.Img(
                                src='data:image/png;base64,{}'.format(
                                    base64.b64encode(
                                        open(
                                            './assets/melissa.png', 'rb'
                                        ).read()
                                    ).decode()
                                ),
                                height='10%',
                                width='50%'
                            )
                        ], className='text-center')
                    ]), 
                    dbc.Col([
                        html.P('Melissa Garcia', style={'textAlign': 'center', 'fontWeight': 'bold', 'fontSize': '0.9vw', 'font-family':'glacial indifference , sans-serif'}), 
                        html.P('Economist', style={'textAlign': 'center', 'fontSize': '0.7vw', 'font-family':'glacial indifference , sans-serif'}), 
                    ])
                ], width={'size': 4, 'offset': 0}), 
                dbc.Col([
                    dbc.Col([
                        html.Div([
                            html.Img(
                                src='data:image/png;base64,{}'.format(
                                    base64.b64encode(
                                        open(
                                            './assets/andrea.png', 'rb'
                                        ).read()
                                    ).decode()
                                ),
                                height='10%',
                                width='50%'
                            )
                        ], className='text-center')
                    ]), 
                    dbc.Col([
                        html.P('Andrea Jimenez', style={'textAlign': 'center', 'fontWeight': 'bold', 'fontSize': '0.9vw', 'font-family':'glacial indifference , sans-serif'}), 
                        html.P('Systems Engineer', style={'textAlign': 'center', 'fontSize': '0.7vw', 'font-family':'glacial indifference , sans-serif'}), 
                    ])
                ], width={'size': 4, 'offset': 0}), 
                dbc.Col([
                    dbc.Col([
                        html.Div([
                            html.Img(
                                src='data:image/png;base64,{}'.format(
                                    base64.b64encode(
                                        open(
                                            './assets/diana.png', 'rb'
                                        ).read()
                                    ).decode()
                                ),
                                height='10%',
                                width='50%'
                            )
                        ], className='text-center')
                    ]), 
                    dbc.Col([
                        html.P('Diana Castellanos', style={'textAlign': 'center', 'fontWeight': 'bold', 'fontSize': '0.9vw', 'font-family':'glacial indifference , sans-serif'}), 
                        html.P('Industrial Engineer', style={'textAlign': 'center', 'fontSize': '0.7vw', 'font-family':'glacial indifference , sans-serif'}), 
                    ])
                ], width={'size': 4, 'offset': 0})
            ], style={'margin-top': '20px'}, no_gutters=False, justify='around'), 
            dbc.Row([
                dbc.Col([
                    dbc.Col([
                        html.Div([
                            html.Img(
                                src='data:image/png;base64,{}'.format(
                                    base64.b64encode(
                                        open(
                                            './assets/david_c.png', 'rb'
                                        ).read()
                                    ).decode()
                                ),
                                height='10%',
                                width='50%'
                            )
                        ], className='text-center')
                    ]), 
                    dbc.Col([
                        html.P('David Castrillon', style={'textAlign': 'center', 'fontWeight': 'bold', 'fontSize': '0.9vw', 'font-family':'glacial indifference , sans-serif'}), 
                        html.P('Industrial Engineer', style={'textAlign': 'center', 'fontSize': '0.7vw', 'font-family':'glacial indifference , sans-serif'}), 
                    ])
                ], width={'size': 4, 'offset': 0}), 
                dbc.Col([
                    dbc.Col([
                        html.Div([
                            html.Img(
                                src='data:image/png;base64,{}'.format(
                                    base64.b64encode(
                                        open(
                                            './assets/david_a.png', 'rb'
                                        ).read()
                                    ).decode()
                                ),
                                height='10%',
                                width='50%'
                            )
                        ], className='text-center')
                    ]), 
                    dbc.Col([
                        html.P('David Angarita', style={'textAlign': 'center', 'fontWeight': 'bold', 'fontSize': '0.9vw', 'font-family':'glacial indifference , sans-serif'}), 
                        html.P('Bachelor of Mathematics and Physics', style={'textAlign': 'center', 'fontSize': '0.7vw', 'font-family':'glacial indifference , sans-serif'}), 
                    ])
                ], width={'size': 4, 'offset': 0}), 
                dbc.Col([
                    dbc.Col([
                        html.Div([
                            html.Img(
                                src='data:image/png;base64,{}'.format(
                                    base64.b64encode(
                                        open(
                                            './assets/ever.png', 'rb'
                                        ).read()
                                    ).decode()
                                ),
                                height='10%',
                                width='50%'
                            )
                        ], className='text-center')
                    ]), 
                    dbc.Col([
                        html.P('Ever Torres', style={'textAlign': 'center', 'fontWeight': 'bold', 'fontSize': '0.9vw', 'font-family':'glacial indifference , sans-serif'}), 
                        html.P('Biomedical Engineer', style={'textAlign': 'center', 'fontSize': '0.7vw', 'font-family':'glacial indifference , sans-serif'}), 
                    ])
                ], width={'size': 4, 'offset': 0})
            ], style={'margin-top': '5px'}, no_gutters=False, justify='around'), 
            dbc.Row([
                dbc.Col([
                    dbc.Col([
                        html.Div([
                            html.Img(
                                src='data:image/png;base64,{}'.format(
                                    base64.b64encode(
                                        open(
                                            './assets/julio.png', 'rb'
                                        ).read()
                                    ).decode()
                                ),
                                height='10%',
                                width='50%'
                            )
                        ], className='text-center')
                    ]), 
                    dbc.Col([
                        html.P('Julio Cesar Garcia', style={'textAlign': 'center', 'fontWeight': 'bold', 'fontSize': '0.9vw', 'font-family':'glacial indifference , sans-serif'}), 
                        html.P('Mechatronic Engineer', style={'textAlign': 'center', 'fontSize': '0.7vw', 'font-family':'glacial indifference , sans-serif'}), 
                    ])
                ], width={'size': 4, 'offset': 0}), 
                dbc.Col([
                    dbc.Col([
                        html.Div([
                            html.Img(
                                src='data:image/png;base64,{}'.format(
                                    base64.b64encode(
                                        open(
                                            './assets/karen.png', 'rb'
                                        ).read()
                                    ).decode()
                                ),
                                height='10%',
                                width='50%'
                            )
                        ], className='text-center')
                    ]), 
                    dbc.Col([
                        html.P('Karen Figueroa', style={'textAlign': 'center', 'fontWeight': 'bold', 'fontSize': '0.9vw', 'font-family':'glacial indifference , sans-serif'}), 
                        html.P('Teaching Assistant', style={'textAlign': 'center', 'fontSize': '0.7vw', 'font-family':'glacial indifference , sans-serif'}), 
                    ])
                ], width={'size': 4, 'offset': 0}), 
                dbc.Col([
                    dbc.Col([
                        html.Div([
                            html.Img(
                                src='data:image/png;base64,{}'.format(
                                    base64.b64encode(
                                        open(
                                            './assets/nilson.png', 'rb'
                                        ).read()
                                    ).decode()
                                ),
                                height='10%',
                                width='50%'
                            )
                        ], className='text-center')
                    ]), 
                    dbc.Col([
                        html.P('Nilson Mossos', style={'textAlign': 'center', 'fontWeight': 'bold', 'fontSize': '0.9vw', 'font-family':'glacial indifference , sans-serif'}), 
                        html.P('Teaching Assistant', style={'textAlign': 'center', 'fontSize': '0.7vw', 'font-family':'glacial indifference , sans-serif'}), 
                    ])
                ], width={'size': 4, 'offset': 0})
            ], style={'margin-top': '5px'}, no_gutters=False, justify='around')
        ], className='fndtb')