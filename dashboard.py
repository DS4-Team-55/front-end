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


tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '2px solid #d6d6d6',
    'backgroundColor': '#5d90cc',
    'padding': '6px',
    'fontWeight': 'bold',
    'color': 'white'
}

tab_selected_style = {
    'borderTop': '2px solid #d6d6d6',
    'borderBottom': '2px solid #d6d6d6',
    'backgroundColor': '#1663b0',
    'color': 'white',
    'fontWeight': 'bold',
    'padding': '6px'
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
                                                        './assets/logo_alcaldia.jpg', 'rb'
                                                    ).read()
                                                ).decode()
                                            ),
                                            height='90',
                                            width='300'
                                        )
                                    ], className='text-left', width=3),
                                    dbc.Col([
                                        html.H1('Prevnat: Maternal Morbidity Alert Generation', style={'fontSize': 35, 'fontWeight': 'bold'})
                                    ], className='text-center', align="center", width=6),
                                    dbc.Col([
                                        html.Img(
                                            src='data:image/png;base64,{}'.format(
                                                base64.b64encode(
                                                    open(
                                                        './assets/logo_mintic.png', 'rb'
                                                    ).read()
                                                ).decode()
                                            ),
                                            height='90',
                                            width='300'
                                        )
                                    ], className='text-right', width=3)
                                ])
                            ],
                            style={
                                'background': 'white',
                                'color':  '#1c1c5e',
                            }
                        )
                    ]
                )
            ), 
            dbc.Row([
                dbc.Col([
                    dcc.Tabs(
                        id="dashboard-tabs", value='tab1', 
                        children=[
                            dcc.Tab(label='Context', value='tab1', style=tab_style, selected_style=tab_selected_style),
                            dcc.Tab(label='Live Births', value='tab2', style=tab_style, selected_style=tab_selected_style),
                            dcc.Tab(label='Morbidity', value='tab3', style=tab_style, selected_style=tab_selected_style),
                            dcc.Tab(label='Mortality', value='tab4', style=tab_style, selected_style=tab_selected_style),
                            dcc.Tab(label='COVID-19', value='tab5', style=tab_style, selected_style=tab_selected_style),
                            dcc.Tab(label='Model', value='tab6', style=tab_style, selected_style=tab_selected_style),
                            dcc.Tab(label='Prevnant', value='tab7', style=tab_style, selected_style=tab_selected_style),
                            dcc.Tab(label='Team', value='tab8', style=tab_style, selected_style=tab_selected_style)
                        ], style=tabs_styles
                    )
                ])
            ], no_gutters=False, justify='around'), 
            dbc.Row(id='tab_content')
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
    Input('dashboard-tabs', 'value')
)
def tab_selector(tab):
    if tab == 'tab1':
        return tabs_layout.context_layout(data)
    elif tab == 'tab2':
        return tabs_layout.context_layout(data)
    elif tab == 'tab3':
        return tabs_layout.context_layout(data)
    elif tab == 'tab4':
        return tabs_layout.context_layout(data)
    elif tab == 'tab5':
        return tabs_layout.context_layout(data)
    elif tab == 'tab6':
        return tabs_layout.context_layout(data)
    elif tab == 'tab7':
        return tabs_layout.context_layout(data)
    elif tab == 'tab8':
        return tabs_layout.context_layout(data)


if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port='8050', debug=True)
