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
from io import BytesIO
import plotly.graph_objects as go
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
    'width': '12.5%'
}

label_style = {
    'color': 'white',
    'width': '100%',
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
                                            width='60%',
					    style={'margin-top': '5%', 'margin-bottom': '5%', 'margin-left': '5%'},
                                        )
                                    ], width={'size': 3}, className='text-left'),
                                    dbc.Col([
                                        html.H1('Prevention before complication', style={'textAlign': 'center', 'fontWeight': 'bold', 'fontSize': '2vw', 'font-family':'glacial indifference , sans-serif'})
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
					    style={'margin-top': '10%', 'margin-right': '5%'},
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
            dbc.Row(id='tab_content',style={'padding':'0px 15px 15px '})
        ], fluid=True
    )
        
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
            meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}])
app.config.suppress_callback_exceptions = True
app.title = 'Prevnant'
app.layout = serve_layout

data = DataLoader()

# Tabs callback
@app.callback(
    Output('tab_content', 'children'),
    Input('dashboard-tabs', 'active_tab')
)
def tab_selector(tab):
    if tab == 'tab1':
        return tabs_layout.context_layout(data)
    elif tab == 'tab2':
        return tabs_layout.context_layout(data)
    elif tab == 'tab3':
        return tabs_layout.births_layout(data)
    elif tab == 'tab4':
        return tabs_layout.morbidity_layout(data)
    elif tab == 'tab5':
        return tabs_layout.mortality_layout(data)
    elif tab == 'tab6':
        return tabs_layout.births_layout_2(data)
    elif tab == 'tab7':
        return tabs_layout.context_layout(data)
    elif tab == 'tab8':
        return tabs_layout.context_layout(data)


# Births callbacks
@app.callback(
    Output('plt_births_low_weight_description', 'figure'), 
    Output('plt_births_low_weight_distribution', 'figure'), 
    Input('low_weight_description_selector', 'value')
)
def morbidity_plots(input_value):
    if input_value is None:
        return {}, {}

    info_ = generate_figures_info.births_low_weight(data, input_value)
    return info_['plt_births_low_weight_description'], info_['plt_births_low_weight_distribution']


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


if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port='8050', debug=True)
