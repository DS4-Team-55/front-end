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
        self.df_lb = pd.read_sql(queries.livebirths_query, con=self.credentials)
        self.df_lw = pd.read_sql(queries.lowweight_query, con=self.credentials)
        self.df_morbidity = pd.read_sql(queries.morbidity_query, con=self.credentials)
        self.df_mortality = pd.read_sql(queries.mortality_query, con=self.credentials)
        # self.df_covid = pd.read_sql(queries.covid_query, con=self.credentials)

        self.df_loc = pd.read_csv(self.divipola, encoding='ISO-8859-1')
        self.df_loc = self.df_loc[self.df_loc['NOM_DPTO']=='SANTANDER']
        self.df_loc['NOM_CPOB'] = self.df_loc['NOM_CPOB'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
        self.df_loc['NOM_MPIO'] = self.df_loc['NOM_MPIO'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

        # preprocess data
        self.df_lb['edad_madre'] = self.df_lb['edad_madre'].apply(lambda x: x.split('(')[0]).astype(int)
        self.df_lb['edad_padre'] = self.df_lb['edad_padre'].astype(str).apply(lambda x: x.split('(')[0]).astype(int)
        self.df_lw['peso_nacer'] = self.df_lw['peso_nacer'].astype(int)


    '''

    def get_lat(self, idx):
        lat = None
        df_tmp = self.df_loc[self.df_loc['NOM_CPOB']==idx]
        if len(df_tmp) > 0:
            lat = df_tmp.iloc[0]['Latitud']
        else:
            df_tmp = self.df_loc[self.df_loc['NOM_MPIO']==idx]
            if len(df_tmp) > 0:
                lat = df_tmp.iloc[0]['Latitud']
        return lat

    def get_lon(self, idx):
        lon = None
        df_tmp = self.df_loc[self.df_loc['NOM_CPOB']==idx]
        if len(df_tmp) > 0:
            lon = df_tmp.iloc[0]['Longitud']
        else:
            df_tmp = self.df_loc[self.df_loc['NOM_MPIO']==idx]
            if len(df_tmp) > 0:
                lon = df_tmp.iloc[0]['Longitud']
        return lon

    def generate_figures_info(self):
        figures = []
        if self.option == 1:
            # Tab 1            
            df_morbidity = pd.read_sql(queries.morbidity_query, con=self.credentials)
            df_covid = pd.read_sql(queries.covid_query, con=self.credentials)
            df_master = pd.read_sql(queries.master_query, con=self.credentials)

            # Fig 1
            summary = df_covid['municipio'].value_counts().to_frame(name='Count')
            summary['Lat'] = summary.index.map(self.get_lat)
            summary['Lon'] = summary.index.map(self.get_lon)
            summary.dropna(inplace=True)
            summary['size'] = np.log(summary['Count']) * 10
            px.set_mapbox_access_token(self.px_token)

            fig = px.scatter_mapbox(summary, lat='Lat', lon='Lon', color='Count', size='size',
                            color_continuous_scale=px.colors.sequential.Bluered, size_max=15, zoom=10, title='Coronavirus')
            figures.append(fig)

            # Fig 2
            figures.append({})

            # Fig 3 - 4 - 5
            for key in ['sem_ges_morb', 'tip_ss_', 'caus_princ']:
                tmp = df_master.groupby(key).size().to_frame(name='Count')
                ordered_frame = tmp['Count'].sort_values(ascending=False)[:10].to_frame().reset_index()

                figures.append(px.bar(ordered_frame, x=key, y='Count',
                    hover_data=['Count'], color='Count'))

            # Fig 6
            figures.append({})

        return figures
    '''
