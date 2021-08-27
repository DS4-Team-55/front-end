import pandas as pd
import queries
import numpy as np


class DataLoader:
    def __init__(self):
        self.credentials = 'postgresql://masterbmga:gW2ZmJhjCYhXkRHnHXpM@dbmaternabmga.cx1teneuqyk1.us-east-2.rds.amazonaws.com/maternabmga'
        self.url = 'https://drive.google.com/file/d/1EdmqtgdglX5k3l3TeV0Pv5oxp0TlhjZx/view?usp=sharing'
        self.divipola = 'https://drive.google.com/uc?id=' + self.url.split('/')[-2]
        self.px_token = 'pk.eyJ1IjoiamNnYXJjaWFjYSIsImEiOiJja3JpcWxqbHMweGx1MzFvNDAycm5kamg0In0.6_WucxN67gPjnTDY908xfQ'

        # data
        self.df_master = pd.read_sql(queries.master_query, con=self.credentials)
        self.df_masterv2 = pd.read_sql(queries.master2_query, con=self.credentials)
        self.df_lb = pd.read_sql(queries.livebirths_query, con=self.credentials)
        self.df_lw = pd.read_sql(queries.lowweight_query, con=self.credentials)
        self.df_morbidity = pd.read_sql(queries.morbidity_query, con=self.credentials)
        self.df_mortality = pd.read_sql(queries.mortality_query, con=self.credentials)
        # self.df_covid = pd.read_sql(queries.covid_query, con=self.credentials)

        self.df_loc = pd.read_csv(self.divipola, encoding='ISO-8859-1')
        self.df_loc = self.df_loc[self.df_loc['NOM_DPTO']=='SANTANDER']
        self.df_loc['NOM_CPOB'] = self.df_loc['NOM_CPOB'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
        self.df_loc['NOM_MPIO'] = self.df_loc['NOM_MPIO'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

        # dicts
        marital_dict = {
            'NO ESTÁ CASADA Y LLEVA DOS AÑOS O MÁS VIVIENDO CON SU PAREJA': 'Pareja >2', 
            'NO ESTÁ CASADA Y LLEVA MENOS DE DOS AÑOS VIVIENDO CON SU PAREJA': 'Pareja <2', 
            'ESTÁ CASADA': 'Casada', 
            'ESTÁ SOLTERA': 'Soltera', 
            'ESTÁ SEPARADA, DIVORCIADA': 'Separada', 
            'SIN INFORMACIÓN': 'Sin informacion', 
            'ESTÁ VIUDA': 'Viuda'
        }

        academic_dict = {
            'MEDIA ACADÉMICA O CLÁSICA ': 'Media', 
            'BÁSICA SECUNDARIA ': 'Secundaria', 
            'TECNOLÓGICA': 'Tecnologica', 
            'ESPECIALIZACIÓN': 'Especializacion', 
            'MAESTRÍA': 'Maestria', 
            'PROFESIONAL': 'Profesional', 
            'BÁSICA PRIMARIA': 'Primaria', 
            'TÉCNICA PROFESIONAL': 'Tecnica', 
            'MEDIA TÉCNICA ': 'Media Tec.', 
            'PREESCOLAR': 'Preescolar', 
            'SIN INFORMACIÓN': 'Sin informacion', 
            'NORMALISTA': 'Normalista', 
            'DOCTORADO': 'Doctorado', 
            'NINGUNO': 'Ninguno'
        }

        # preprocess data
        self.df_lb['edad_madre'] = self.df_lb['edad_madre'].apply(lambda x: x.split('(')[0]).astype(int)
        self.df_lb['edad_padre'] = self.df_lb['edad_padre'].astype(str).apply(lambda x: x.split('(')[0]).astype(int)
        self.df_lb['edad_madre_rango'] = self.df_lb['edad_madre'].map(self.get_age_range)
        self.df_lb['conyugal_madre_dict'] = self.df_lb['estado_conyugal_madre'].apply(lambda x: marital_dict[x])
        self.df_lb['madre_academic'] = self.df_lb['nivel_educativo_madre'].apply(lambda x: academic_dict[x])
        self.df_lb['Peso'] = self.df_lb['peso_gramos'].apply(lambda x: 'Bajo Peso' if x<2500 else 'Peso Normal')
        self.df_lw['peso_nacer'] = self.df_lw['peso_nacer'].astype(int)
        self.df_morbidity['quinquenio'] = self.df_morbidity['edad_'].map(self.get_quinquenio)
        self.df_morbidity['trimestre'] = self.df_morbidity['sem_ges_'].map(self.get_trimestre)
        self.df_mortality['quinquenio'] = self.df_mortality['edad_'].map(self.get_quinquenio)        
        self.df_mortality['trimestre'] = self.df_mortality['sem_ges_'].map(self.get_trimestre)


    def get_age_range(self, x):
        if x <= 15:
            return 'Under 15'
        elif x >= 35:
            return 'Over 35'
        else:
            return 'Between 15 and 35'

    
    def get_quinquenio(self, x):
        q_ = (x - 1) // 5
        inf = (q_ * 5) + 1
        sup = (q_ + 1) * 5
        return f'{inf} - {sup}'


    def get_trimestre(self, x):
        if x <= 12:
            trimestre = 1
        elif x <= 26:
            trimestre = 2
        else:
            trimestre = 3
        return trimestre
