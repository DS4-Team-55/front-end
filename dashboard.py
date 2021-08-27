import datetime
from datetime import date
import dash
from dash.dependencies import Input, Output, State
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
import cv2
from io import BytesIO
import plotly.graph_objects as go
from scipy import signal
import numpy as np
import requests
import json
import tabs_layout
from data_loader import DataLoader
import generate_figures_info


tab_style = {
    'borderTop': '1px solid #d6d6d6',
    'backgroundColor': '#5d90cc',
    'fontWeight': 'bold',
    'color': 'white',
    'textAlign': 'center', 
    'width': '12.5%'
}

label_style = {
    'color': 'white',
    'width': '100%'
}

active_label_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#1663b0',
    'color': 'white',
    'fontWeight': 'bold',
    'width': '100%'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#1663b0',
    'color': 'white',
    'fontWeight': 'bold',
    'width': '12.5%'
}

def serve_layout():
    return dbc.Container(
        [
            dbc.Row(
                dbc.Col([
                        dcc.Location(id='url', refresh=False),
                        html.Div(
                            id='app-page-header',
                            children=[
                                dbc.Row([
                                    dbc.Col([
                                        html.Img(
                                            src='data:image/png;base64,{}'.format(
                                                base64.b64encode(
                                                    open(
                                                        './assets/Prevant_noBgr.png', 'rb'
                                                    ).read()
                                                ).decode()
                                            ),
                                            height='auto',
                                            width='50%', 
                                            style={'margin-left': '5%'}
                                        )
                                    ], width={'size': 3}, className='text-left'),
                                    dbc.Col([
                                        html.H1('Prevention before complication', style={'textAlign': 'center', 'fontWeight': 'bold', 'fontSize': '2.5vw', 'font-family':'glacial indifference , sans-serif'})
                                    ], width={'size': 6}, className='text-center', align="center"),
                                    dbc.Col([
                                        html.Img(
                                            src='data:image/png;base64,{}'.format(
                                                base64.b64encode(
                                                    open(
                                                        './assets/logo_mintic.png', 'rb'
                                                    ).read()
                                                ).decode()
                                            ),
                                            height='auto',
                                            width='60%', 
                                            style={'margin-top': '5%'}
                                        )   
                                    ], width={'size': 3}, className='text-right')
                                ])
                            ],
                            style={
                                'background': 'linear-gradient(90deg, rgba(223,223,223,1) 0%, rgba(254,254,254,1) 25%, rgba(254,254,254,1) 75%, rgba(223,223,223,1) 100%)'
                            }
                        )
                    ]
                )
            ), 
            dbc.Row([
                dbc.Col([
                    dbc.Tabs(
                        id="dashboard-tabs", active_tab='tab1', 
                        children=[
                            dbc.Tab(label='Prevnant', tab_id='tab1', tab_style=tab_style, label_style=label_style, active_label_style=active_label_style, active_tab_style=tab_selected_style),
                            dbc.Tab(label='Context', tab_id='tab2', tab_style=tab_style, label_style=label_style, active_label_style=active_label_style, active_tab_style=tab_selected_style),
                            dbc.Tab(label='Births', tab_id='tab3', tab_style=tab_style, label_style=label_style, active_label_style=active_label_style, active_tab_style=tab_selected_style),
                            dbc.Tab(label='Morbidity', tab_id='tab4', tab_style=tab_style, label_style=label_style, active_label_style=active_label_style, active_tab_style=tab_selected_style),
                            dbc.Tab(label='Mortality', tab_id='tab5', tab_style=tab_style, label_style=label_style, active_label_style=active_label_style, active_tab_style=tab_selected_style),
                            dbc.Tab(label='COVID-19', tab_id='tab6', tab_style=tab_style, label_style=label_style, active_label_style=active_label_style, active_tab_style=tab_selected_style),
                            dbc.Tab(label='Model', tab_id='tab7', tab_style=tab_style, label_style=label_style, active_label_style=active_label_style, active_tab_style=tab_selected_style),
                            dbc.Tab(label='Team', tab_id='tab8', tab_style=tab_style, label_style=label_style, active_label_style=active_label_style, active_tab_style=tab_selected_style)
                        ]
                    )
                ])
            ], no_gutters=False, justify='around'), 
            dbc.Row(id='tab_content', style={'padding': '0px 15px 15px'})
        ], fluid=True
    )
        
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
            meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}])
app.config.suppress_callback_exceptions = True
app.title = 'Prevnant'
app.layout = serve_layout

data = DataLoader()
morbidity_url = 'http://35.188.136.150:5000/morbidity'
low_weight_url = 'http://35.188.136.150:5000/low_weight'

# Tabs callback
@app.callback(
    Output('tab_content', 'children'),
    Input('dashboard-tabs', 'active_tab')
)
def tab_selector(tab):
    if tab == 'tab1':
        return tabs_layout.prevnant_layout()
    elif tab == 'tab2':
        return tabs_layout.context_layout(data)
    elif tab == 'tab3':
        return tabs_layout.births_layout(data)
    elif tab == 'tab4':
        return tabs_layout.morbidity_layout(data)
    elif tab == 'tab5':
        return tabs_layout.mortality_layout(data)
    elif tab == 'tab6':
        return tabs_layout.covid_layout(data)
    elif tab == 'tab7':
        return tabs_layout.model_layout()
    elif tab == 'tab8':
        return tabs_layout.team_layout()


# Births callbacks
@app.callback(
    Output('plt_births_low_weight_description', 'figure'), 
    Output('plt_births_low_weight_distribution', 'figure'), 
    Input('low_weight_description_selector', 'value')
)
def births_plots(input_value):
    if input_value is None:
        return {}, {}

    info_ = generate_figures_info.births_low_weight(data, input_value)
    return info_['plt_births_low_weight_description'], info_['plt_births_low_weight_distribution']

@app.callback(
    Output('plt_births_map', 'figure'), 
    Input('births_map_var_selector', 'value')
)
def births_map(var_selector):
    if var_selector is None:
        return {}

    return generate_figures_info.births_map(data, var_selector)


# Morbidity callbacks
@app.callback(
    Output('plt_morbidity_failures', 'figure'), 
    Output('plt_morbidity_grouped_cause', 'figure'), 
    Output('plt_morbidity_grouped_cause_year', 'figure'), 
    Output('plt_morbidity_pregnancy', 'figure'), 
    Input('morbidity_var_selector', 'value')
)
def morbidity_plots(input_value):
    if input_value is None:
        return {}, {}, {}, {}

    info_ = generate_figures_info.morbidity_plots(data, input_value)
    return info_['plt_morbidity_failures'], info_['plt_morbidity_grouped_cause'], info_['plt_morbidity_grouped_cause_year'], info_['plt_morbidity_pregnancy']

@app.callback(
    Output('plt_morbidity_map', 'figure'), 
    Input('morbidity_geo_selector', 'value')
)
def morbidity_map(geo_selector):
    if geo_selector is None:
        return {}

    return generate_figures_info.morbidity_map(data, geo_selector)


# Mortality callbacks
@app.callback(
    Output('plt_mortality_demographic', 'figure'), 
    Output('plt_mortality_year', 'figure'), 
    Output('plt_mortality_upgd', 'figure'), 
    Output('plt_mortality_cbmte', 'figure'),
    Input('mortality_var_selector', 'value')
)
def mortality_plots(input_value):
    if input_value is None:
        return {}, {}, {}, {}

    info_ = generate_figures_info.mortality_plots(data, input_value)
    return info_['plt_mortality_demographic'], info_['plt_mortality_year'], info_['plt_mortality_upgd'], info_['plt_mortality_cbmte']

@app.callback(
    Output('plt_mortality_map', 'figure'), 
    Input('mortality_geo_selector', 'value')
)
def mortality_map(geo_selector):
    if geo_selector is None:
        return {}

    return generate_figures_info.mortality_map(data, geo_selector)


# Model callbacks
@app.callback(
    Output('morbidity_pred', 'children'), 
    Output('morbidity_pred', 'value'),
    Output('morbidity_pred', 'color'),
    Output('morb_predict_btn', 'n_clicks'), 
    Input('morb_predict_btn', 'n_clicks'), 
    Input('morbidity_mother_age', 'value'), 
    Input('morbidity_gest_weeks', 'value'), 
    Input('morbidity_sec_reg', 'value'), 
    Input('morbidity_pren_con', 'value'), 
    Input('morbidity_num_pregnancies', 'value'), 
    Input('morbidity_num_hosp', 'value'), 
    Input('morbidity_marital', 'value'), 
    Input('morbidity_mother_academic', 'value'), 
    Input('morbidity_covid', 'value')
)
def morbidity_prediction(n_clicks, m_age, gest_week, sec_reg, pren_con, num_preg, num_hosp, marital, m_academ, covid):
    if n_clicks == 0 or None in (m_age, gest_week, sec_reg, pren_con, num_preg, num_hosp, marital, m_academ, covid):
        return None, None, None, 0
    
    data = {
        'covid': covid,
        'numero_embarazos': int(num_preg),
        'numero_consultas': int(pren_con),
        'no_hospitalizaciones': int(num_hosp),
        'edad_madre': int(m_age),
        'conyugal': marital,
        'educacion': m_academ,
        'regimen': sec_reg,
        'tiempo_de_gestacion': int(gest_week)
    }
    r = requests.post(morbidity_url, data=json.dumps(data))
    pred = r.json()['prediction']
    color = 'success' if pred < 50 else 'danger'

    return f'{pred}%', pred, color, 0


@app.callback(
    Output('low_weight_pred', 'children'), 
    Output('low_weight_pred', 'value'),
    Output('low_weight_pred', 'color'),
    Output('low_weight_predict_btn', 'n_clicks'),
    Input('low_weight_predict_btn', 'n_clicks'), 
    Input('low_weight_sex', 'value'), 
    Input('low_weight_mother_age', 'value'), 
    Input('low_weight_father_age', 'value'), 
    Input('low_weight_mother_academic', 'value'), 
    Input('low_weight_sec_reg', 'value'), 
    Input('low_weight_pren_con', 'value'), 
    Input('low_weight_prev_children', 'value'), 
    Input('low_weight_num_pregnancies', 'value'), 
    Input('low_weight_preg_mult', 'value')
)
def low_weight_prediction(n_clicks, sex, m_age, f_age, m_academ, sec_reg, pren_con, prev_child, num_preg, mult):
    if n_clicks == 0 or None in (sex, m_age, f_age, m_academ, sec_reg, pren_con, prev_child, num_preg, mult):
        return None, None, None, 0

    data = {
        'sex': sex, 
        'mother_age': int(m_age), 
        'father_age': int(f_age), 
        'mother_academic': m_academ, 
        'sec_reg': sec_reg, 
        'prenatal_consultations': int(pren_con), 
        'previous_children': int(prev_child), 
        'num_pregnancies': int(num_preg), 
        'multiplicity': mult
    }
    r = requests.post(low_weight_url, data=json.dumps(data))
    pred = r.json()['prediction']
    color = 'success' if pred < 50 else 'danger'

    return f'{pred}%', pred, color, 0


if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port='8050', debug=True)
