import pandas as pd
import plotly.express as px
import queries
import numpy as np
import plotly.graph_objects as go
import plotly.figure_factory as ff
import pandas as pd
from copy import deepcopy

px.set_mapbox_access_token('pk.eyJ1IjoiamNnYXJjaWFjYSIsImEiOiJja3JpcWxqbHMweGx1MzFvNDAycm5kamg0In0.6_WucxN67gPjnTDY908xfQ')
url = 'https://drive.google.com/file/d/1EdmqtgdglX5k3l3TeV0Pv5oxp0TlhjZx/view?usp=sharing'
url2 = 'https://drive.google.com/uc?id=' + url.split('/')[-2]
df_loc = pd.read_csv(url2, encoding='ISO-8859-1')
df_loc = df_loc[df_loc['NOM_DPTO']=='SANTANDER']
df_loc['NOM_CPOB'] = df_loc['NOM_CPOB'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
df_loc['NOM_MPIO'] = df_loc['NOM_MPIO'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')


def get_age_range(x):
  if x <= 15:
    return 'Under 15'
  elif x >= 35:
    return 'Over 35'
  else:
    return 'Between 15 and 35'

def get_lat(idx):
  lat = None  
  df_tmp = df_loc[df_loc['NOM_CPOB']==idx]
  if len(df_tmp) > 0:
    lat = df_tmp.iloc[0]['Latitud']
  else:
    df_tmp = df_loc[df_loc['NOM_MPIO']==idx]
    if len(df_tmp) > 0:
      lat = df_tmp.iloc[0]['Latitud']
  return lat

def get_lon(idx):
  lon = None
  df_tmp = df_loc[df_loc['NOM_CPOB']==idx]
  if len(df_tmp) > 0:
    lon = df_tmp.iloc[0]['Longitud']
  else:
    df_tmp = df_loc[df_loc['NOM_MPIO']==idx]
    if len(df_tmp) > 0:
      lon = df_tmp.iloc[0]['Longitud']
  return lon


def context(data):
    resp = {}

    # plt_context_ages
    ages_ = data.df_lb.groupby('edad_madre').size().to_frame(name='Count')
    fig = go.Figure(go.Bar(
        x=ages_.index,
        y=ages_['Count']
    ))
    fig.update_layout(
        font_family="sans-serif", 
        title="Maternal's age", 
        xaxis_title="Age",
        yaxis_title="Number of Maternals",
        margin=dict(t=50, b=5, l=5, r=5),
	plot_bgcolor = "white"
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
        font_family="sans-serif",
        yaxis=dict(
            tickmode='linear',
            dtick=1
        ), 
        title='Pregnant women per socioeconomic status', 
        xaxis_title="Number of Pregnant women",
        yaxis_title="Status",
        margin=dict(t=50, b=5, l=5, r=5),plot_bgcolor = "white"
    )
    resp['plt_context_estrato'] = deepcopy(fig)

    # plt_context_marital_age_academic
    data.df_lb['edad_madre_rango'] = data.df_lb['edad_madre'].map(get_age_range)
    fig = px.sunburst(data.df_lb, path=['estado_conyugal_madre', 'edad_madre_rango', 'nivel_educativo_madre'])
    fig.update_layout(
        font_family="sans-serif",
        title='Marital - Age Range - Academic Level of pregnant women',
        margin=dict(t=50, b=5, l=5, r=5),
	plot_bgcolor = "white"
    )
    resp['plt_context_marital_age_academic'] = deepcopy(fig)

    # plt_context_parents_age
    fig = px.sunburst(data.df_lb[data.df_lb['edad_madre'] < 18], path=['edad_madre', 'edad_padre'])
    fig.update_layout(
        font_family="sans-serif",
        title='Mother Age (Teenager) and Father Age',
        margin=dict(t=50, b=5, l=5, r=5),
	plot_bgcolor = "white"
    )
    resp['plt_context_parents_age'] = deepcopy(fig)

    # mortality_cnt
    resp['mortality_cnt'] = len(data.df_mortality)

    # morbidity_cnt
    resp['morbidity_cnt'] = len(data.df_morbidity)

    # covid_cnt
    resp['covid_cnt'] = len(data.df_morbidity) # data.df_master['ini_sin_covid'].notnull().sum()
    
    return resp


def births(data):
    resp = {}

    # plt_births_low_weight
    data.df_lb['bajo_peso'] = data.df_lb['peso_gramos'].apply(lambda x: 1 if x < 2500 else 0)
    fig = px.bar(data.df_lb.groupby('edad_madre')['bajo_peso'].sum().to_frame().reset_index(), x='edad_madre', y='bajo_peso')
    fig.update_layout(
        font_family="sans-serif",
        xaxis=dict(
            tickmode='linear',
            dtick=1
        ),
        title='Low weight vs Mother Age',
        margin=dict(t=50, b=5, l=5, r=5),plot_bgcolor = "white"
    )
    resp['plt_births_low_weight'] = deepcopy(fig)

    # plt_births_num_children
    fig = go.Figure()
    for item in [x for x in range(1, 11)]:
        fig.add_trace(go.Box(y=data.df_lb[data.df_lb['numero_hijos_nacidos_vivos'] == item]['peso_gramos'], name=item))
    fig.update_layout(
        font_family="sans-serif",
        title='Weight vs Number of children',
        margin=dict(t=50, b=5, l=5, r=5),plot_bgcolor = "white", 
        showlegend=False
    )
    resp['plt_births_num_children'] = deepcopy(fig)
    
    # plt_births_multiplicity
    fig = go.Figure()
    for item in ['SIMPLE', 'DOBLE']:
        fig.add_trace(go.Box(y=data.df_lb[data.df_lb['multiplicidad_embarazo'] == item]['peso_gramos'], name=item))
    fig.update_layout(
        font_family="sans-serif",
        title='Weight vs Pregnant multiplicity',
        margin=dict(t=50, b=5, l=5, r=5),plot_bgcolor = "white", 
        showlegend=False
    )
    resp['plt_births_multiplicity'] = deepcopy(fig)

    # plt_births_parents_age
    fig = go.Figure()
    for item in ['edad_madre', 'edad_padre']:
        fig.add_trace(go.Box(y=data.df_lb[item], name=item))
    fig.update_layout(
        font_family="sans-serif",
        title='Parents age',
        margin=dict(t=50, b=5, l=5, r=5),plot_bgcolor = "white", 
        showlegend=False
    )
    resp['plt_births_parents_age'] = deepcopy(fig)

    # plt_births_birth_type
    fig = go.Figure()
    for item in ['CESÁREA', 'ESPONTÁNEO', 'INSTRUMENTADO']:
        fig.add_trace(go.Box(y=data.df_lb[data.df_lb['tipo_parto'] == item]['peso_gramos'], name=item))
    fig.update_layout(
        font_family="sans-serif",
        title='Weight vs Birth type',
        margin=dict(t=50, b=5, l=5, r=5),plot_bgcolor = "white", 
        showlegend=False
    )
    resp['plt_births_birth_type'] = deepcopy(fig)

    # plt_births_marital
    fig = go.Figure()
    for item in data.df_lb['estado_conyugal_madre'].unique():
        fig.add_trace(go.Box(y=data.df_lb[data.df_lb['estado_conyugal_madre'] == item]['peso_gramos'], name=item))
        fig.update_layout(xaxis=dict(showticklabels=False))
    fig.update_layout(
        font_family="sans-serif",
        title='Weight vs Marital status',
        margin=dict(t=50, b=5, l=5, r=5),plot_bgcolor = "white", 
        showlegend=False
    )
    resp['plt_births_marital'] = deepcopy(fig)

    return resp


def births_low_weight(data, input_value):
    resp = {}
    map_dict = {
        1: 'edad_', 2: 'sem_gest', 3: 'estrato_', 4: 'sexo', 
        5: 'niv_edu_ma', 7: 'mult_embar', 8: 'num_em_pre'
    }

    # plt_births_low_weight_description
    if input_value == 6:
        key = 'numero_consultas_prenatales'
        tmp = data.df_lb[data.df_lb['numero_documento_madre'].astype(str).isin(data.df_lw['num_ide_'].astype(str))].groupby(key).size().to_frame(name='Count').reset_index()
        fig = px.bar(tmp, x=key, y='Count')
    else:
        key = map_dict[input_value]
        fig = px.bar(data.df_lw.groupby(key).size().to_frame(name='Count').reset_index(), x=key, y='Count')
    fig.update_layout(
        font_family="sans-serif",
        xaxis=dict(
            tickmode='linear',
            dtick=1
        ),
        title='Low weight representation',
        margin=dict(t=50, b=5, l=5, r=5),plot_bgcolor = "white"
    )
    resp['plt_births_low_weight_description'] = deepcopy(fig)

    # plt_births_low_weight_distribution
    fig = go.Figure()
    fig = px.histogram(data.df_lw, x='peso_nacer', nbins=20)
    fig.update_layout(
        font_family="sans-serif",
        title='Low weight distribution',
        margin=dict(t=50, b=5, l=5, r=5),plot_bgcolor = "white"
    )
    resp['plt_births_low_weight_distribution'] = deepcopy(fig)

    return resp


def births2(data):
    resp = {}

    # plt_births_num_children
    tmp = data.df_lb[['numero_hijos_nacidos_vivos', 'peso_gramos']].copy()
    tmp['nhnv'] = tmp['numero_hijos_nacidos_vivos'].apply(lambda x: str(x) if x <= 3 else 'More than 3')

    keep = ['1', '2', '3', 'More than 3']
    colors = ['red', 'blue', 'green', 'orange']
    fig = go.Figure()
    for idx, item in enumerate(keep):
        fig.add_trace(go.Histogram(x=tmp[tmp['nhnv'] == item]['peso_gramos'], name=item, marker_color=colors[idx]))

    fig.update_layout(
        font_family="sans-serif",
        title='Weight vs Number of children',
        margin=dict(t=50, b=5, l=5, r=5),plot_bgcolor = "white", 
        barmode='overlay'
    )
    fig.update_traces(opacity=0.75)
    resp['plt_births_num_children_2'] = deepcopy(fig)

    # plt_births_multiplicity
    fig = go.Figure()
    for item in ['SIMPLE', 'DOBLE']:
        fig.add_trace(go.Box(y=data.df_lb[data.df_lb['multiplicidad_embarazo'] == item]['peso_gramos'], name=item))
    fig.update_layout(
        font_family="sans-serif",
        title='Weight vs Pregnant multiplicity',
        margin=dict(t=50, b=5, l=5, r=5),plot_bgcolor = "white", 
        showlegend=False
    )
    resp['plt_births_multiplicity_2'] = deepcopy(fig)

    # plt_births_parents_age
    fig = go.Figure()
    for item in ['edad_madre', 'edad_padre']:
        fig.add_trace(go.Box(y=data.df_lb[item], name=item))
    fig.update_layout(
        font_family="sans-serif",
        title='Parents age',
        margin=dict(t=50, b=5, l=5, r=5),plot_bgcolor = "white", 
        showlegend=False
    )
    resp['plt_births_parents_age_2'] = deepcopy(fig)

    # plt_births_birth_type
    keep = ['CESÁREA', 'ESPONTÁNEO']
    colors = ['red', 'blue']
    hist_data = []
    for item in keep:
        hist_data.append(list(data.df_lb[data.df_lb['tipo_parto'] == item]['peso_gramos']))

    fig = ff.create_distplot(hist_data, keep, colors=colors, bin_size=50, show_rug=False)
    fig.update_layout(
        font_family="sans-serif",
        title='Weight vs Birth type',
        margin=dict(t=50, b=5, l=5, r=5),plot_bgcolor = "white", 
    )
    fig.update_traces(opacity=0.5)
    resp['plt_births_birth_type_2'] = deepcopy(fig)

    # plt_births_marital
    fig = go.Figure()
    for item in data.df_lb['estado_conyugal_madre'].unique():
        fig.add_trace(go.Box(y=data.df_lb[data.df_lb['estado_conyugal_madre'] == item]['peso_gramos'], boxpoints='all', name=item))
        fig.update_layout(xaxis=dict(showticklabels=False))
    fig.update_layout(
        font_family="sans-serif",
        title='Weight vs Marital status',
        margin=dict(t=50, b=5, l=5, r=5),plot_bgcolor = "white", 
        showlegend=False
    )
    resp['plt_births_marital_2'] = deepcopy(fig)

    return resp


def morbidity_plots(data, key):
    resp = {}

    set1 = ['num_parvag', 'num_cesare', 'num_aborto', 'num_molas']
    set2 = ['falla_card', 'falla_rena', 'falla_hepa', 'falla_cere', 'falla_resp', 'falla_coag']
    set3 = ['eclampsia', 'preclampsi', 'choq_septi', 'hemorragia_obstetrica_severa']
    set4 = ['edad_', 'ocupacion_', 'estrato_', 'sem_ges_', 'caus_agrup', 'anio']

    # plt_morbidity_failures
    morb = data.df_morbidity[set1 + set2 + set3 + set4].copy()
    for item in set2 + set3:
        morb[item] = morb[item].apply(lambda x: 0 if x == 2 else x)
    morb_tmp = morb[set1 + set2 + set3 + [key]].groupby(key).sum()

    fig = go.Figure()
    for col in set2:
            tmp_ = morb_tmp[col]
            fig.add_trace(go.Bar(x=tmp_.index, y=tmp_, name=col))

    fig.update_layout(
        xaxis=dict(
            tickmode='linear',
            dtick=1
        ), 
        font_family="sans-serif",
        title='Health failures',
        margin=dict(t=50, b=5, l=5, r=5),plot_bgcolor = "white"
    )
    resp['plt_morbidity_failures'] = deepcopy(fig)


    # plt_morbidity_grouped_cause
    summary = morb.groupby([key, 'caus_agrup']).size().to_frame('Count').reset_index().set_index(key)
    summary['caus_agrup'] = summary['caus_agrup'].astype('category')
    fig = px.bar(summary, x=summary.index, y='Count', color='caus_agrup', orientation='v')

    fig.update_layout(
        xaxis=dict(
            tickmode='linear',
            dtick=1
        ), 
        font_family="sans-serif",
        title='Grouped cause',
        margin=dict(t=50, b=5, l=5, r=5),plot_bgcolor = "white"
    )
    resp['plt_morbidity_grouped_cause'] = deepcopy(fig)


    # plt_morbidity_grouped_cause_year
    summary = morb.groupby(['anio', 'caus_agrup']).size().to_frame('Count').reset_index().set_index('anio')
    summary['caus_agrup'] = summary['caus_agrup'].astype('category')
    fig = px.bar(summary, x=summary.index, y='Count', color='caus_agrup', orientation='v')

    fig.update_layout(
        xaxis=dict(
            tickmode='linear',
            dtick=1
        ), 
        font_family="sans-serif",
        title='Grouped cause by year',
        margin=dict(t=50, b=5, l=5, r=5),plot_bgcolor = "white"
    )
    resp['plt_morbidity_grouped_cause_year'] = deepcopy(fig)


    # plt_morbidity_pregnancy
    fig = go.Figure()
    for col in set3:
        tmp_ = morb_tmp[col]
        fig.add_trace(go.Bar(x=tmp_.index, y=tmp_, name=col))

    fig.update_layout(
        xaxis=dict(
            tickmode='linear',
            dtick=1
        ), 
        font_family="sans-serif",
        title='Maternal situation',
        margin=dict(t=50, b=5, l=5, r=5),plot_bgcolor = "white"
    )
    resp['plt_morbidity_pregnancy'] = deepcopy(fig)

    return resp


def mortality_plots(data, key):
    resp = {}

    # plt_mortality_demographic
    summary = data.df_mortality.groupby(key).size().to_frame(name='Count')
    fig = px.bar(summary, x=summary.index, y='Count')
    fig.update_layout(
        xaxis=dict(
            tickmode='linear',
            dtick=1
        ), 
        font_family="sans-serif",
        title='Maternal Deaths',
        margin=dict(t=50, b=5, l=5, r=5),plot_bgcolor = "white"
    )
    resp['plt_mortality_demographic'] = deepcopy(fig)

    # plt_mortality_year
    summary = data.df_mortality.groupby('anio').size().to_frame(name='Count')
    fig = px.bar(summary, x=summary.index, y='Count')
    fig.update_layout(
        xaxis=dict(
            tickmode='linear',
            dtick=1
        ), 
        font_family="sans-serif",
        title='Deaths vs Year',
        margin=dict(t=50, b=5, l=5, r=5),plot_bgcolor = "white"
    )
    resp['plt_mortality_year'] = deepcopy(fig)


    # plt_mortality_upgd
    summary = data.df_mortality.groupby('nom_upgd').size().to_frame(name='Count')
    fig = px.bar(summary, x=summary.index, y='Count')
    fig.update_layout(
        xaxis=dict(showticklabels=False), 
        font_family="sans-serif",
        title='Deaths vs UPGD',
        margin=dict(t=50, b=5, l=5, r=5),plot_bgcolor = "white"
    )
    resp['plt_mortality_upgd'] = deepcopy(fig)


    # plt_mortality_cbmte
    keep = ['U071', 'R579', 'J159', 'U072', 'I472', 'R571', 'I619'] # more than 1
    fig = px.sunburst(data.df_mortality[data.df_mortality['cbmte_'].isin(keep)], path=['cbmte_', 'edad_'])
    fig.update_layout(
        font_family="sans-serif",
        title='Basic Death Cause and Age',
        margin=dict(t=50, b=5, l=5, r=5),plot_bgcolor = "white"
    )
    resp['plt_mortality_cbmte'] = deepcopy(fig)

    return resp



def generate_map(data, col, title):
    summary = data[col].value_counts().to_frame(name='Count')
    summary['Lat'] = summary.index.map(get_lat)
    summary['Lon'] = summary.index.map(get_lon)
    summary.dropna(inplace=True)
    summary['size'] = np.log(summary['Count']) * 10
    
    fig = px.scatter_mapbox(summary, lat='Lat', lon='Lon', color='Count', size='size', 
                    color_continuous_scale=px.colors.sequential.Bluered, size_max=15, zoom=8, title=title)

    return fig