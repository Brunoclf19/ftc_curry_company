# Libraries
from haversine import haversine
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import folium
import streamlit as st
import datetime as datetime
from PIL import Image
from streamlit_folium import st_folium

st.set_page_config(page_title='Visão Entregadores', page_icon= '🚚', layout='wide')

#--------------------------------------------------------------
#--------------------------------------------------------------
# Função 1)
# Mais lentos
def top_delivers(df1, top_asc):
    df_slow = (df1.groupby(['City', 'Delivery_person_ID'])['Time_taken(min)']
                    .mean()
                    .reset_index()
                    .sort_values(['City', 'Time_taken(min)'], ascending = top_asc))
    df_top_slow = df_slow.groupby('City').head(10)
    return df_top_slow
#--------------------------------------------------------------
#--------------------------------------------------------------
# Função 0)
# Limpeza de código
def clean_code (df1):
    """ Esta função tem a responsabilidade de limpar o dataframe

        Tipos de limpeza:
        1. Remoção dos dados NaN
        2. Mudança do tipo da coluna de dados
        3. Remoção dos espaços das variáveis de texto
        4. Formatação da coluna de datas
        5. Limpeza da coluna de tempo (remoção do texto da variável numérica)

        Input: Dataframe
        OutPut: Dataframe

    """
    # 1 - Removendo os espaços e NaN das colunas
    linhas_selecionadas = (df1['Delivery_person_Age'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = (df1['Road_traffic_density'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = (df1['City'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = (df1['Festival'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()

    # 2. Convertendo para o tipo inteiro
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)

    # 3. Convertendo para o tipo float
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)

    # 4. Convertendo para o tipo data
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format = '%d-%m-%Y')

    # 5. Convertendo texto para inteiro
    linhas_selecionadas = (df1['multiple_deliveries'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)

    # 6. Limpando espaços desnecessários nas strings
    df1.loc[:, 'ID'] = df1['ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1['Road_traffic_density'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1['Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1['Type_of_vehicle'].str.strip()
    df1.loc[:, 'City'] = df1['City'].str.strip()
    df1.loc[:, 'Festival'] = df1['Festival'].str.strip()

    # 7. Limpando coluna de time taken
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.split('(min)')[1])
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)

    return df1

# ------------------------------ Inicio da estrutura lógica do código --------------------------------
# ------------------------------
# Importando dataset
# ------------------------------ 
df = pd.read_csv('dataset/train.csv')
# df1 = df.copy()

# ------------------------------ 
# Limpando os dados
# ------------------------------ 
df1 = clean_code(df)

# Visão - Entregadores
st.header('Marketplace - Visão Entregadores')

image = Image.open('logo-ia.png')
st.sidebar.image(image, width=120)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")

st.sidebar.markdown('## Selecione uma data limite')
date_slider = st.sidebar.slider(
    'Até qual data?',
    value=datetime.datetime(2022, 4, 13),
    min_value=datetime.datetime(2022, 2, 11),
    max_value=datetime.datetime(2022, 4, 6),
    format='DD-MM-YYYY'
)

st.sidebar.markdown("""---""")
traffic_options = st.sidebar.multiselect(
    'Quais são as condições do trânsito',
    ['Low', 'Medium', 'High', 'Jam'],
    default=['Low', 'Medium', 'High', 'Jam']
)
st.sidebar.markdown("""---""")
st.sidebar.markdown('### Powered by Comunidade DS')

linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]

# ===============================================
# Layout no Streamlit
# ===============================================

tab1, tab2, tab3 = st.tabs(['Métricas Gerais', 'Avaliações', 'Desempenho de Entrega'])

with tab1:
    st.title('Métricas Gerais dos Entregadores')
    col1, col2, col3, col4 = st.columns(4, gap='large')

    with col1:
        maior_idade = df1['Delivery_person_Age'].max()
        col1.metric('Maior Idade', maior_idade)

    with col2:
        menor_idade = df1['Delivery_person_Age'].min()
        col2.metric('Menor Idade', menor_idade)

    with col3:
        melhor_condicao = df1['Vehicle_condition'].max()
        col3.metric('Melhor Condição', melhor_condicao)

    with col4:
        pior_condicao = df1['Vehicle_condition'].min()
        col4.metric('Pior Condição', pior_condicao)

    st.markdown("### Distribuição de Idade dos Entregadores")
    age_bins = pd.cut(df1['Delivery_person_Age'], bins=[20, 25, 30, 35, 40], labels=['20-25', '25-30', '30-35', '35-40'])
    age_distribution = age_bins.value_counts().sort_index()
    st.bar_chart(age_distribution.rename_axis('Faixa Etária').rename('Contagem'))

with tab2:
    st.title('Avaliação Média por Condição Climática')
    weather_ratings = df1.groupby('Weatherconditions')['Delivery_person_Ratings'].mean().reset_index()
    for index, row in weather_ratings.iterrows():
        st.metric(f"Avaliação Média - {row['Weatherconditions']}", f"{row['Delivery_person_Ratings']:.2f}")

with tab3:
    st.title('Desempenho de Entrega')

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Top 10 Entregadores Mais Rápidos")
        # Função 1) Mais rápidos
        df_top_slow = top_delivers(df1, top_asc=[True, True])
        st.dataframe(df_top_slow, width=500)

    with col2:
        st.subheader("Top 10 Entregadores Mais Lentos")
        # Função 1) Mais lentos
        df_top_slow = top_delivers(df1, top_asc=[True, False])
        st.dataframe(df_top_slow, width=500)
