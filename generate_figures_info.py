import pandas as pd
import plotly.express as px
import queries
import numpy as np
import plotly.graph_objects as go
from copy import deepcopy

def get_age_range(x):
  if x <= 15:
    return 1
  elif x >= 35:
    return 3
  else:
    return 2

def context(data):
    resp = {}

    # plt_context_ages
    ages_range = data.df_lb['edad_madre'].apply(get_age_range).to_frame().groupby('edad_madre').size().to_frame(name='Count')
    fig = go.Figure(go.Bar(
        x=ages_range.index,
        y=ages_range['Count']
    ))
    fig.update_layout(
        font_family="Courier New",
        xaxis = dict(
            tickmode = 'array',
            tickvals = [1, 2, 3],
            ticktext = ['Less than 15', 'Between 15 and 35', 'More than 35']
        ), 
        title='Age Range of pregnant women', 
        xaxis_title="Age range",
        yaxis_title="Number of Pregnant women",
        margin=dict(t=50, b=0, l=0, r=0)
    )
    resp['plt_context_ages'] = deepcopy(fig)

    # plt_context_estrato
    estrato = data.df_master['estrato_'].to_frame().groupby('estrato_').size().to_frame(name='Count')
    fig = go.Figure(go.Bar(
        y=estrato.index,
        x=estrato['Count'],
        orientation='h'
    ))
    fig.update_layout(
        font_family="Courier New",
        yaxis=dict(
            tickmode='linear',
            dtick=1
        ), 
        title='Pregnant women per socioeconomic status', 
        xaxis_title="Number of Pregnant women",
        yaxis_title="Status",
        margin=dict(t=50, b=0, l=0, r=0)
    )
    resp['plt_context_estrato'] = deepcopy(fig)

    # plt_context_marital
    marital = data.df_lb[['estado_conyugal_madre']].groupby('estado_conyugal_madre').size().to_frame(name='Count')
    fig = go.Figure(data=[go.Pie(labels=marital.index, values=marital['Count'], hole=.4)])
    fig.update_layout(
        font_family="Courier New",
        title='Marital state of pregnant women',
        margin=dict(t=50, b=0, l=0, r=0)
    )
    resp['plt_context_marital'] = deepcopy(fig)

    # plt_context_education
    studies = data.df_lb[['nivel_educativo_madre']].groupby('nivel_educativo_madre').size().sort_values(ascending=False).to_frame(name='Count')
    fig = go.Figure(go.Treemap(
        labels=studies.index,
        values=studies['Count'],
        parents=[''] + list(studies.index),
        marker_colors = ["pink", "royalblue", "lightgray", "purple",
                        "cyan", "lightgray", "lightblue", "lightgreen", "yellow", "red"],
        maxdepth=10
    ))
    fig.update_layout(
        font_family="Courier New",
        title='Academic level of pregnant women',
        margin=dict(t=50, l=25, r=25, b=25)
    )
    resp['plt_context_education'] = deepcopy(fig)

    # mortality_cnt
    resp['mortality_cnt'] = len(data.df_mortality)

    # morbidity_cnt
    resp['morbidity_cnt'] = len(data.df_morbidity)

    # covid_cnt
    resp['covid_cnt'] = data.df_master['ini_sin_covid'].notnull().sum()
    
    return resp



'''
nacidos vivos
Index(['numero_certificado', 'departamento', 'municipio', 'area_nacimiento',
       'inspeccion_corregimiento_o_caserio_nacimiento', 'sitio_nacimiento',
       'codigo_institucion', 'nombre_institucion', 'sexo', 'peso_gramos',
       'talla_centimetros', 'fecha_nacimiento', 'hora_nacimiento',
       'parto_atendido_por', 'tiempo_de_gestacion',
       'numero_consultas_prenatales', 'tipo_parto', 'multiplicidad_embarazo',
       'apgar1', 'apgar2', 'grupo_sanguineo', 'factor_rh',
       'pertenencia_etnica', 'grupo_indigena', 'nombres_madre',
       'apellidos_madre', 'tipo_documento_madre', 'numero_documento_madre',
       'edad_madre', 'estado_conyugal_madre', 'nivel_educativo_madre',
       'ultimo_aÑo_aprobado_madre', 'pais_residencia',
       'departamento_residencia', 'municipio_residencia', 'area_residencia',
       'localidad', 'barrio', 'direccion', 'centro_poblado', 'rural_disperso',
       'numero_hijos_nacidos_vivos', 'fecha_anterior_hijo_nacido_vivo',
       'numero_embarazos', 'regimen_seguridad', 'tipo_administradora',
       'nombre_administradora', 'edad_padre', 'nivel_educativo_padre',
       'ultimo_aÑo_aprobado_padre', 'nombres_y_apellidos_certificador',
       'numero_documento_certificador', 'tipo_documento_certificador',
       'profesion_certificador', 'registro_profesional_certificador',
       'departamento_expedicion', 'municipio_expedicion', 'fecha_expedicion',
       'estado_certificado', 'codigo_entidad_registro', 'usuario_registro',
       'ultima_fecha_modificacion', 'fecha_registro'],
      dtype='object')
'''