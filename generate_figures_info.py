import pandas as pd
import plotly.express as px
import queries
import numpy as np
import plotly.graph_objects as go
import plotly.figure_factory as ff
import pandas as pd
from copy import deepcopy

px.set_mapbox_access_token('pk.eyJ1IjoiamNnYXJjaWFjYSIsImEiOiJja3JpcWxqbHMweGx1MzFvNDAycm5kamg0In0.6_WucxN67gPjnTDY908xfQ')

# load divipola municipality
df_mun = pd.read_csv('/home/project/geodata/DIVIPOLA_CentrosPoblados.csv', encoding='ISO-8859-1')
df_mun = df_mun[df_mun['NOM_DPTO']=='SANTANDER']
df_mun['NOM_CPOB'] = df_mun['NOM_CPOB'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
df_mun['NOM_MPIO'] = df_mun['NOM_MPIO'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

# load comunas
df_com = pd.read_csv('/home/project/geodata/coordenadas_bucaramanga.csv', encoding='ISO-8859-1')

def get_lat_mun(idx):
  lat = None  
  df_tmp = df_mun[df_mun['NOM_CPOB']==idx]
  if len(df_tmp) > 0:
    lat = df_tmp.iloc[0]['Latitud']
  else:
    df_tmp = df_mun[df_mun['NOM_MPIO']==idx]
    if len(df_tmp) > 0:
      lat = df_tmp.iloc[0]['Latitud']
  return lat

def get_lon_mun(idx):
  lon = None
  df_tmp = df_mun[df_mun['NOM_CPOB']==idx]
  if len(df_tmp) > 0:
    lon = df_tmp.iloc[0]['Longitud']
  else:
    df_tmp = df_mun[df_mun['NOM_MPIO']==idx]
    if len(df_tmp) > 0:
      lon = df_tmp.iloc[0]['Longitud']
  return lon

def get_lat_comuna(idx):
  lat = None  
  df_tmp = df_com[df_com['COMUNA'].str.replace(' ', '')==str(idx).replace(' ', '')]
  if len(df_tmp) > 0:
    lat = df_tmp.iloc[0]['LATITUD']
  return lat

def get_lon_comuna(idx):
  lon = None
  df_tmp = df_com[df_com['COMUNA'].str.replace(' ', '')==str(idx).replace(' ', '')]
  if len(df_tmp) > 0:
    lon = df_tmp.iloc[0]['LONGITUD']
  return lon

def get_lat_barrio(idx):
  lat = None  
  df_tmp = df_com[df_com['BARRIO'].str.replace(' ', '')==str(idx).replace(' ', '')]
  if len(df_tmp) > 0:
    lat = df_tmp.iloc[0]['LATITUD']
  return lat

def get_lon_barrio(idx):
  lon = None
  df_tmp = df_com[df_com['BARRIO'].str.replace(' ', '')==str(idx).replace(' ', '')]
  if len(df_tmp) > 0:
    lon = df_tmp.iloc[0]['LONGITUD']
  return lon


def set_age_range(x):
  if x <= -15:
    text = 'Diff 15 years'
  elif x <= -10:
    text = 'Diff 10 years'
  elif x <= -5:
    text = 'Diff 5 years'
  elif x < 0:
    text = 'Diff <5 years'
  elif x == 0:
    text = 'W/o Diff'
  elif x > 15:
    text = 'Diff 15 years'
  elif x > 10:
    text = 'Diff 10 years'
  elif x > 5:
    text = 'Diff 5 years'
  elif x > 0:
    text = 'Diff <5 years'
  return text


def context(data):
    resp = {}

    '''
    # plt_context_ages
    ages_ = data.df_lb.groupby('edad_madre').size().to_frame(name='Count')
    fig = go.Figure(go.Bar(
        x=ages_.index,
        y=ages_['Count']
    ))
    fig.update_layout(
        font_family="sans-serif", 
        xaxis=dict(
            tickmode='linear',
            dtick=1
        ),
        title="Maternal's age", 
        xaxis_title="Age",
        yaxis_title="Number of Maternals",
        margin=dict(t=50, b=5, l=5, r=5), 
        plot_bgcolor = "white"
    )
    resp['plt_context_ages'] = deepcopy(fig)
    '''

    # plt_context_ages_status
    morb_tmp = data.df_morbidity.groupby(['estrato_', 'quinquenio']).size().reset_index(name='Count').sort_values(by=['quinquenio', 'estrato_'], ascending=False).set_index('estrato_')
    fig = px.bar(morb_tmp, x=morb_tmp.index, y='Count', color='quinquenio', labels={'estrato_': 'Socio Economic Status', 'Count': 'Cases', 'quinquenio': 'Quinquenium'}, 
            barmode='group', title='Morbidity Cases by Quinquenium and Socio Economic Status')
    fig.update_layout(
        margin=dict(t=50, l=5, r=5, b=5), 
        font_family='sans-serif', 
        legend=dict(orientation='v', yanchor='top', y=1.0, xanchor='right', x=1), 
        showlegend=True,
        plot_bgcolor='white'
    )

    resp['plt_context_ages_status'] = deepcopy(fig)

    '''
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
        margin=dict(t=50, b=5, l=5, r=5), 
        plot_bgcolor = "white"
    )
    resp['plt_context_estrato'] = deepcopy(fig)
    '''

    # plt_context_consults
    ndf = data.df_lb.groupby(['numero_consultas_prenatales', 'Peso']).size().reset_index(name ='Count').sort_values(by=['Peso', 'numero_consultas_prenatales'], ascending=False).set_index('numero_consultas_prenatales')
    fig = px.bar(ndf, x=ndf.index, y='Count', color='Peso', labels={'numero_consultas_prenatales': '# Appointment', 'Count': 'Cases', 'Peso': 'Weight'}, title='Low Weight Cases by Appointment Pregnant')
    fig.update_layout(
        margin=dict(t=50, l=5, r=5, b=5), 
        font_family='sans-serif', 
        legend=dict(orientation='v', yanchor='top', y=1.0, xanchor='right', x=1), 
        showlegend=True,
        plot_bgcolor='white'
    )
    resp['plt_context_consults'] = deepcopy(fig)
    


    # plt_context_marital_age_academic
    fig = px.sunburst(data.df_lb, path=['conyugal_madre_dict', 'edad_madre_rango', 'madre_academic'])
    fig.update_layout(
        font_family="sans-serif",
        title='Marital - Age Range - Academic Level of pregnant women',
        margin=dict(t=50, b=5, l=5, r=5), 
        plot_bgcolor = "white"
    )
    resp['plt_context_marital_age_academic'] = deepcopy(fig)

    '''
    # plt_context_parents_age
    fig = px.sunburst(data.df_lb[data.df_lb['edad_madre'] < 18], path=['edad_madre', 'edad_padre'])
    fig.update_layout(
        font_family="sans-serif",
        title='Mother Age (Teenager) and Father Age',
        margin=dict(t=50, b=5, l=5, r=5), 
        plot_bgcolor = "white"
    )
    resp['plt_context_parents_age'] = deepcopy(fig)
    '''

    # plt_context_regime
    bpdf = data.df_lb.groupby(['regimen_seguridad', 'Peso']).size().reset_index(name ='Count').sort_values(by=['Peso', 'Count'], ascending=False).set_index('regimen_seguridad')
    aws = pd.DataFrame(data.df_lb['regimen_seguridad'].value_counts()).reset_index().rename(columns={'index': 'regimen_seguridad', 'regimen_seguridad': 'Count'}).set_index('regimen_seguridad')
    bpdf['total'] = list(bpdf.reset_index()['regimen_seguridad'].apply(lambda x: aws.loc[x, 'Count']))
    bpdf['perc'] = bpdf['Count'] / bpdf['total']

    fig = px.sunburst(bpdf, path=[bpdf.index, 'Peso'], values='Count', title="Low Weight Cases by Regime", 
            labels={
                'regimen_seguridad': 'Diff. Ages.',
                'Count': 'Cases',
                'Peso': 'Weight'
                }
            )
    fig.update_layout(
        margin = dict(t=50, l=5, r=5, b=5), 
        font_family='sans-serif', 
        legend=dict(orientation='h', yanchor='top', y=1.1, xanchor='right', x=1), 
        showlegend=True,
        plot_bgcolor='white'
    )
    fig.update_traces(textinfo="label+percent entry")
    resp['plt_context_regime'] = deepcopy(fig)

    # plt_context_diff_ages
    ndf = data.df_lb[data.df_lb['edad_padre'].notna()].copy()
    ndf['dif_eda'] = ndf['edad_padre'] - ndf['edad_madre']
    ndf['rang_edad'] = ndf['dif_eda'].map(set_age_range)

    bpdf = ndf.groupby(['rang_edad', 'Peso']).size().reset_index(name ='Count').sort_values(by=['Peso', 'rang_edad'], ascending=False).set_index('rang_edad')
    aws = pd.DataFrame(ndf['rang_edad'].value_counts()).reset_index().rename(columns={'index': 'rang_edad', 'rang_edad': 'Count'}).set_index('rang_edad')

    bpdf['total'] = list(bpdf.reset_index()['rang_edad'].apply(lambda x: aws.loc[x, 'Count']))
    bpdf['perc'] = round((bpdf['Count'] / bpdf['total']) * 100, 2)

    fig = px.bar(bpdf, x=bpdf.index, y='perc', color='Peso', title='Low Weight Cases by Difference between parent ages', text='perc',
            labels={
                'rang_edad': 'Diff. Ages.',
                'perc': '%',
                'Peso': 'Weight'
            }
        )
    fig.update_layout(
        margin=dict(t=40, l=5, r=5, b=5), 
        font_family='sans-serif', 
        #legend=dict(orientation='v', yanchor='top', y=1.1, xanchor='right', x=1), 
        showlegend=True,
        plot_bgcolor='white'
    )
    fig.update_xaxes(categoryorder='array', categoryarray= ['Diff 15 years', 'Diff 10 years', 'Diff 5 years', 'Diff <5 years', 'W/o Diff'])
    resp['plt_context_diff_ages'] = deepcopy(fig)

    # mortality_cnt
    resp['mortality_cnt'] = len(data.df_mortality[data.df_mortality['nmun_resi']=='BUCARAMANGA']['num_ide_'].unique())

    # morbidity_cnt
    resp['morbidity_cnt'] = len(data.df_morbidity)

    # covid_cnt
    resp['covid_cnt'] = data.df_masterv2['fecha_covid'].count()
    
    return resp


def births_low_weight(data, input_value):
    resp = {}
    map_dict = {
        1: ['edad_', 'Mother Age'], 2: ['sem_gest', 'Gestation Weeks'], 3: ['estrato_', 'Socioeconomic Status'], 4: ['sexo', 'Sex'], 
        5: ['niv_edu_ma', 'Academic Level'], 6: ['numero_consultas_prenatales', 'Prenatal consultations'], 7: ['mult_embar', 'Multiplicity of pregnancy'], 
        8: ['num_em_pre', 'Previous pregnancy']
    }

    # plt_births_low_weight_description
    if input_value == 6:
        key = 'numero_consultas_prenatales'
        tmp = data.df_lb[data.df_lb['numero_documento_madre'].astype(str).isin(data.df_lw['num_ide_'].astype(str))].groupby(key).size().to_frame(name='Count').reset_index()
        fig = px.bar(tmp, x=key, y='Count')
    else:
        key = map_dict[input_value][0]
        fig = px.bar(data.df_lw.groupby(key).size().to_frame(name='Count').reset_index(), x=key, y='Count')
    fig.update_layout(
        font_family="sans-serif",
        xaxis=dict(
            tickmode='linear',
            dtick=1
        ),
        title='Low weight representation',
        xaxis_title=map_dict[input_value][1],
        margin=dict(t=50, b=5, l=5, r=5), 
        plot_bgcolor = "white"
    )
    resp['plt_births_low_weight_description'] = deepcopy(fig)

    # plt_births_low_weight_distribution
    fig = go.Figure()
    fig = px.histogram(data.df_lw, x='peso_nacer', nbins=20)
    fig.update_layout(
        font_family="sans-serif",
        title='Low weight distribution',
        yaxis_title='Count',
        xaxis_title='Weight',
        margin=dict(t=50, b=5, l=5, r=5), 
        plot_bgcolor = "white"
    )
    resp['plt_births_low_weight_distribution'] = deepcopy(fig)

    return resp


def births(data):
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
        xaxis_title='Weight',
        yaxis_title='Count',
        margin=dict(t=50, b=5, l=5, r=5), 
        barmode='overlay', 
        plot_bgcolor = "white"
    )
    fig.update_traces(opacity=0.75)
    resp['plt_births_num_children'] = deepcopy(fig)

    # plt_births_multiplicity
    fig = go.Figure()
    for item in ['SIMPLE', 'DOBLE']:
        fig.add_trace(go.Box(y=data.df_lb[data.df_lb['multiplicidad_embarazo'] == item]['peso_gramos'], name=item))
    fig.update_layout(
        font_family="sans-serif",
        title='Weight vs Pregnant multiplicity',
        yaxis_title='Weight',
        margin=dict(t=50, b=5, l=5, r=5), 
        showlegend=False, 
        plot_bgcolor = "white"
    )
    resp['plt_births_multiplicity'] = deepcopy(fig)

    # plt_births_parents_age
    fig = go.Figure()
    for item in ['edad_madre', 'edad_padre']:
        fig.add_trace(go.Box(y=data.df_lb[item], name=item))
    fig.update_layout(
        font_family="sans-serif",
        title='Parents age',
        yaxis_title='Age',
        margin=dict(t=50, b=5, l=5, r=5), 
        showlegend=False, 
        plot_bgcolor = "white"
    )
    resp['plt_births_parents_age'] = deepcopy(fig)

    # plt_births_birth_type
    keep = ['CES??REA', 'ESPONT??NEO']
    colors = ['red', 'blue']
    hist_data = []
    for item in keep:
        hist_data.append(list(data.df_lb[data.df_lb['tipo_parto'] == item]['peso_gramos']))

    fig = ff.create_distplot(hist_data, keep, colors=colors, bin_size=50, show_rug=False)
    fig.update_layout(
        font_family="sans-serif",
        title='Weight vs Birth type',
        xaxis_title='Weight',
        yaxis_title='Distribution',
        margin=dict(t=50, b=5, l=5, r=5), 
        plot_bgcolor = "white"
    )
    fig.update_traces(opacity=0.5)
    resp['plt_births_birth_type'] = deepcopy(fig)

    # plt_births_marital
    fig = go.Figure()
    for item in data.df_lb['estado_conyugal_madre'].unique():
        fig.add_trace(go.Box(y=data.df_lb[data.df_lb['estado_conyugal_madre'] == item]['peso_gramos'], boxpoints='all', name=item))
        fig.update_layout(xaxis=dict(showticklabels=False))
    fig.update_layout(
        font_family="sans-serif",
        title='Weight vs Marital status',
        xaxis_title='Marital status',
        yaxis_title='Weight',
        margin=dict(t=50, b=5, l=5, r=5), 
        showlegend=False, 
        plot_bgcolor = "white"
    )
    resp['plt_births_marital'] = deepcopy(fig)

    return resp


def births_map(data, var_selector):
    if var_selector == 1:
        # general births - Bucaramanga
        fig = generate_map_loc(data.df_lb, 'localidad', 'General Births in Bucaramanga', get_lat_comuna, get_lon_comuna)
    elif var_selector == 2:
        # low weight - Bucaramanga
        df_ = data.df_lb[data.df_lb['numero_documento_madre'].astype(str).isin(data.df_lw['num_ide_'].astype(str))].copy()
        fig = generate_map_loc(df_, 'localidad', 'Low weight Births in Bucaramanga', get_lat_comuna, get_lon_comuna)
    return fig


def morbidity_plots(data, key, years, geo_selector):
    resp = {
        'plt_morbidity_failures': {}, 
        'plt_morbidity_grouped_cause': {}, 
        'plt_morbidity_grouped_cause_year': {}, 
        'plt_morbidity_pregnancy': {}
    }

    map_dict = {
        'quinquenio': 'Quinquennium', 
        'sem_ges_': 'Gestation Weeks', 
        'estrato_': 'Socioeconomic Status'
    }
    
    tmp = data.df_morbidity[(data.df_morbidity['anio'] >= years[0]) & (data.df_morbidity['anio'] <= years[1])]
    if geo_selector == 2:
        # Bucaramanga
        tmp = tmp[tmp['nmun_resi']=='BUCARAMANGA']
    
    if len(tmp) == 0:
        return resp

    set1 = ['num_parvag', 'num_cesare', 'num_aborto', 'num_molas']
    set2 = ['falla_cere', 'falla_resp', 'falla_rena', 'falla_coag', 'falla_hepa', 'falla_card']
    set3 = ['choq_septi', 'eclampsia', 'hemorragia_obstetrica_severa', 'preclampsi']
    set4 = ['edad_', 'ocupacion_', 'estrato_', 'sem_ges_', 'caus_agrup', 'anio', 'quinquenio', 'group_week']

    # plt_morbidity_failures
    morb = tmp[set1 + set2 + set3 + set4].copy()
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
        xaxis_title=map_dict[key], 
        yaxis_title='Count', 
        margin=dict(t=50, b=5, l=5, r=5), 
        plot_bgcolor = "white"
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
        xaxis_title=map_dict[key], 
        margin=dict(t=50, b=5, l=5, r=5), 
        plot_bgcolor = "white"
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
        xaxis_title='Year', 
        margin=dict(t=50, b=5, l=5, r=5), 
        plot_bgcolor = "white"
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
        xaxis_title=map_dict[key], 
        yaxis_title='Count', 
        margin=dict(t=50, b=5, l=5, r=5), 
        plot_bgcolor = "white"
    )
    resp['plt_morbidity_pregnancy'] = deepcopy(fig)

    return resp


def morbidity_map(data, geo_selector):
    if geo_selector == 1:
        # municipalities
        fig = generate_map_mun(data.df_morbidity, 'nmun_resi', 'Morbidity by residence municipality')
    elif geo_selector == 2:
        # Bucaramanga
        fig = generate_map_loc(data.df_morbidity, 'bar_ver_', 'Morbidity in Bucaramanga', get_lat_barrio, get_lon_barrio)
    return fig


def mortality_plots(data, key, years, geo_selector):
    resp = {
        'plt_mortality_demographic': {}, 
        'plt_mortality_year': {}, 
        'plt_mortality_upgd': {}, 
        'plt_mortality_cbmte': {}
    }

    map_dict = {
        'quinquenio': 'Quinquennium', 
        'sem_ges_': 'Gestation Weeks', 
        'estrato_': 'Socioeconomic Status'
    }

    tmp = data.df_mortality[(data.df_mortality['anio'] >= years[0]) & (data.df_mortality['anio'] <= years[1])]
    tmp.drop_duplicates(subset='num_ide_', inplace=True)
    if geo_selector == 2:
        # Bucaramanga
        tmp = tmp[tmp['nmun_resi']=='BUCARAMANGA']

    if len(tmp) == 0:
        return resp

    # plt_mortality_demographic
    summary = tmp.groupby(key).size().to_frame(name='Count')
    fig = px.bar(summary, x=summary.index, y='Count')
    fig.update_layout(
        xaxis=dict(
            tickmode='linear',
            dtick=1
        ), 
        font_family="sans-serif",
        title='Maternal Deaths',
        xaxis_title=map_dict[key], 
        margin=dict(t=50, b=5, l=5, r=5), 
        plot_bgcolor = "white"
    )
    resp['plt_mortality_demographic'] = deepcopy(fig)

    # plt_mortality_year
    summary = tmp.groupby('anio').size().to_frame(name='Count')
    fig = px.bar(summary, x=summary.index, y='Count')
    fig.update_layout(
        xaxis=dict(
            tickmode='linear',
            dtick=1
        ), 
        font_family="sans-serif",
        title='Deaths vs Year',
        xaxis_title='Year',
        margin=dict(t=50, b=5, l=5, r=5), 
        plot_bgcolor = "white"
    )
    resp['plt_mortality_year'] = deepcopy(fig)


    # plt_mortality_upgd
    summary = tmp.groupby('nom_upgd').size().to_frame(name='Count')
    fig = px.bar(summary, x=summary.index, y='Count')
    fig.update_layout(
        xaxis=dict(showticklabels=False), 
        font_family="sans-serif",
        title='Deaths vs UPGD',
        xaxis_title='UPGD',
        margin=dict(t=50, b=5, l=5, r=5), 
        plot_bgcolor = "white"
    )
    resp['plt_mortality_upgd'] = deepcopy(fig)


    # plt_mortality_cbmte
    keep = ['U071', 'R579', 'J159', 'U072', 'I472', 'R571', 'I619'] # more than 1
    fig = px.sunburst(tmp[tmp['cbmte_'].isin(keep)], path=['cbmte_', 'edad_'])
    fig.update_layout(
        font_family="sans-serif",
        title='Basic Death Cause and Age',
        margin=dict(t=50, b=5, l=5, r=5), 
        plot_bgcolor = "white"
    )
    resp['plt_mortality_cbmte'] = deepcopy(fig)

    return resp


def mortality_map(data, geo_selector):
    if geo_selector == 1:
        # municipalities
        fig = generate_map_mun(data.df_mortality, 'nmun_resi', 'Mortality by residence municipality')
    elif geo_selector == 2:
        # Bucaramanga
        fig = generate_map_loc(data.df_mortality, 'bar_ver_', 'Mortality in Bucaramanga', get_lat_barrio, get_lon_barrio)
    return fig


def covid(data):
    resp = {}
    covid_m = data.df_masterv2[~data.df_masterv2['fecha_covid'].isna()].copy()

    # plt_covid_age
    summary = covid_m.groupby('edad_madre').size().to_frame('Count')
    fig = px.bar(
        summary, x=summary.index, y='Count', 
        labels={
            'edad_madre': 'Mother Age'
        }
    )
    fig.update_layout(
        xaxis=dict(
            tickmode='linear',
            dtick=1
        ), 
        font_family="sans-serif",
        title='Covid notifications in maternals vs Age',
        margin=dict(t=50, b=5, l=5, r=5), 
        plot_bgcolor = "white"
    )
    resp['plt_covid_age'] = deepcopy(fig)

    # plt_covid_year
    covid_m['year'] = pd.to_datetime(covid_m['fecha_covid'], format='%d/%m/%Y').dt.year
    covid_m['month'] = pd.to_datetime(covid_m['fecha_covid'], format='%d/%m/%Y').dt.month
    summary = covid_m[['year', 'month']].groupby(['year', 'month']).size().to_frame(name='Count').reset_index()
    summary['ym'] = pd.to_datetime(summary[['year', 'month']].assign(DAY=1)).dt.date.apply(lambda x: x.strftime('%Y-%m'))

    fig = px.bar(
        summary, x='ym', y='Count', 
        labels={
            'ym': 'Date'
        }
    )
    fig.update_layout(
        font_family="sans-serif",
        title='Covid notifications in maternals',
        margin=dict(t=50, b=5, l=5, r=5), 
        plot_bgcolor = "white"
    )
    resp['plt_covid_year'] = deepcopy(fig)

    # plt_covid_map
    df_1 = data.df_lb[data.df_lb['numero_documento_madre'].astype(str).isin(covid_m['numero_documento_madre'].astype(str))][['numero_certificado', 'localidad']]
    df_2 = data.df_morbidity[data.df_morbidity['num_ide_'].astype(str).isin(covid_m['numero_documento_madre'].astype(str))][['num_ide_', 'bar_ver_']].rename(columns={'num_ide_': 'numero_certificado', 'bar_ver_': 'localidad'})
    df_3 = data.df_mortality[data.df_mortality['num_ide_'].astype(str).isin(covid_m['numero_documento_madre'].astype(str))][['num_ide_', 'bar_ver_']].rename(columns={'num_ide_': 'numero_certificado', 'bar_ver_': 'localidad'})
    df_ = pd.concat([df_1, df_2, df_3], axis=0)
    fig = generate_map_loc(df_, 'localidad', 'Covid in Maternals Bucaramanga', get_lat_barrio, get_lon_barrio)
    resp['plt_covid_map'] = deepcopy(fig)

    return resp


def generate_map_mun(data, col, title):
    summary = data[col].value_counts().to_frame(name='Count')
    summary['Lat'] = summary.index.map(get_lat_mun)
    summary['Lon'] = summary.index.map(get_lon_mun)
    summary.dropna(inplace=True)
    summary['size'] = np.log(summary['Count']) * 10
    
    fig = px.scatter_mapbox(summary, lat='Lat', lon='Lon', color='Count', size='size', 
                    color_continuous_scale=px.colors.sequential.Bluered, size_max=15, zoom=8, title=title)

    return fig


def generate_map_loc(data, col, title, fn_lat, fn_lon):
    summary = data[col].value_counts().to_frame(name='Count')
    summary['Lat'] = summary.index.map(fn_lat).astype(float)
    summary['Lon'] = summary.index.map(fn_lon).astype(float)
    summary.dropna(inplace=True)
        
    fig = px.scatter_mapbox(summary, lat='Lat', lon='Lon', color='Count', size='Count', 
                    color_continuous_scale=px.colors.sequential.Bluered, size_max=15, zoom=12, title=title)

    return fig