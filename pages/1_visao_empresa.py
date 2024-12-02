# Bibliotecas
from haversine import haversine
import pandas as pd
import numpy as np
import plotly.express as px
import folium
import streamlit as st
from streamlit_folium import st_folium
from PIL import Image
import datetime as datetime

st.set_page_config(page_title='Visão Empresa', page_icon='🎲', layout='wide')

# ----------------
# Funções
# ----------------
# Função 6)
# Retorno do mapa
def mapa_pais (df1):
    # Filtrando apenas colunas numéricas para o cálculo de medianas
    colunas_numericas = ['Delivery_location_latitude', 'Delivery_location_longitude']
    df_map = df1.groupby(['City', 'Road_traffic_density'])[colunas_numericas].median().reset_index()

    map_ = folium.Map(location=[df_map['Delivery_location_latitude'].mean(), df_map['Delivery_location_longitude'].mean()], zoom_start=11)
    
    for _, location_info in df_map.iterrows():
        folium.Marker(
            [location_info['Delivery_location_latitude'], location_info['Delivery_location_longitude']],
            popup=f"{location_info['City']} - {location_info['Road_traffic_density']}"
        ).add_to(map_)
    
    st_folium(map_, width=1024, height=600)
#--------------------------------------------------------------
#--------------------------------------------------------------
# Função 5)
# Pedidos por entregador por semana
def pedidos_entregador_semana (df1):
    # Pedidos por Entregador por Semana
    df_aux1 = df1.groupby('week_of_year').count().reset_index()[['week_of_year', 'ID']]
    df_aux2 = df1.groupby('week_of_year').nunique().reset_index()[['week_of_year', 'Delivery_person_ID']]
    df_aux = pd.merge(df_aux1, df_aux2, on='week_of_year')
    df_aux['Pedidos_por_Entrega'] = df_aux['ID'] / df_aux['Delivery_person_ID']
    fig = px.line(df_aux, x='week_of_year', y='Pedidos_por_Entrega', title='Pedidos por Entrega ao Longo das Semanas')
    fig.update_layout(title_x=0.4)
    return fig 
#--------------------------------------------------------------
#--------------------------------------------------------------
# Função 4)
# Pedidos por semana
def pedidos_semana (df1):
    # Quantidade de pedidos por semana
    df1['week_of_year'] = df1['Order_Date'].dt.isocalendar().week
    df_aux = df1.groupby('week_of_year').count().reset_index()[['week_of_year', 'ID']]
    df_aux.columns = ['week_of_year', 'Qtd_Pedidos']
    fig = px.bar(df_aux, x='week_of_year', y='Qtd_Pedidos', title='Quantidade de pedidos por semana')
    fig.update_layout(title_x=0.4, hovermode="x unified")
    return fig
#--------------------------------------------------------------
#--------------------------------------------------------------
# Função 3)
# Gráficos de Tráfego e Cidade
def traffic_order_city(df1):
    coluna = ['ID', 'Road_traffic_density', 'City']
    df_aux = df1.loc[:, coluna].groupby(['City', 'Road_traffic_density']).count().reset_index()

    fig5 = px.bar(
        df_aux, x='City', y='ID', color='Road_traffic_density', barmode='group',
        labels={'Road_traffic_density': 'Tipo de Tráfego', 'ID': 'Quantidade de pedidos', 'City': 'Cidade'},
        title='Quantidade de pedidos: cidade e tráfego'
    )
    fig5.update_layout(title_x=0)
    return fig5
#--------------------------------------------------------------
#--------------------------------------------------------------
# Função 2)
# Gráficos de Tráfego
def traffic_order_share(df1):
    df_aux = df1.groupby('Road_traffic_density').count().reset_index()[['Road_traffic_density', 'ID']]
    df_aux.columns = ['Road_traffic_density', 'Pedidos']
    fig = px.pie(df_aux, values='Pedidos', names='Road_traffic_density', title='Representatividade por Tráfego')
    fig.update_layout(title_x=0)
    return fig
#--------------------------------------------------------------
#--------------------------------------------------------------
# Função 1)
# Recebe o dataframe, gera um figura (gráfico) e retorna o gráfico
def order_metric(df1):
    # Gráfico de Quantidade de Entregas por Dia
    df_aux = df1.groupby('Order_Date').count().reset_index()[['Order_Date', 'ID']]
    df_aux.columns = ['Order_Date', 'Qtd_Entregas']
    fig = px.bar(df_aux, x='Order_Date', y='Qtd_Entregas', title='Quantidade de entregas por dia')
    fig.update_layout(title_x = 0.4, hovermode="x unified")
    return fig
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
df = pd.read_csv(r'dataset\train.csv')
# df1 = df.copy()

# ------------------------------ 
# Limpando os dados
# ------------------------------ 
df1 = clean_code(df)

#--------------------------------------------------------------
# Barra lateral - Filtros
#--------------------------------------------------------------
# Visão - Empresa

st.header('Marketplace - Visão Empresa')
image = Image.open('logo-ia.png')
st.sidebar.image(image, width=120)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")

# Filtros de Data e Condição de Trânsito
st.sidebar.subheader("Filtros")
date_slider = st.sidebar.slider(
    "Até qual data?",
    min_value=datetime.datetime(2022, 2, 11),
    max_value=datetime.datetime(2022, 4, 6),
    value=datetime.datetime(2022, 4, 13),
    format="DD-MM-YYYY"
)

traffic_options = st.sidebar.multiselect(
    "Condições do Trânsito",
    ['Low', 'Medium', 'High', 'Jam'],
    default=['Low', 'Medium', 'High', 'Jam']
)
st.sidebar.markdown("### Powered by Comunidade DS")

# Aplicando filtros no DataFrame
df1 = df1[df1['Order_Date'] < date_slider]
df1 = df1[df1['Road_traffic_density'].isin(traffic_options)]

#--------------------------------------------------------------
# Dashboard
#--------------------------------------------------------------

# Definindo as abas no Streamlit
tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

#--------------------------------------------------------------
# Aba Visão Gerencial
#--------------------------------------------------------------
with tab1:
    st.subheader("Resumo das Entregas")
    st.markdown("Esta aba apresenta um resumo geral das entregas diárias e a distribuição por condição de trânsito e cidade.")

    # Função 1)
    fig = order_metric(df1)
    st.plotly_chart(fig, use_container_width=True)
    

    # Gráficos de Tráfego e Cidade
    col1, col2 = st.columns(2)
    with col1:
        # Função 2)
        fig = traffic_order_share(df1)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Função 3)
        fig5 = traffic_order_city(df1)
        st.plotly_chart(fig5, use_container_width=True)


#--------------------------------------------------------------            
# Aba Visão Tática
#--------------------------------------------------------------
with tab2:
    st.subheader("Pedidos Semanais")
    st.markdown("Exibe a quantidade de pedidos e média de pedidos por entregador ao longo das semanas.")
    
    # Função 4)
    fig = pedidos_semana(df1)
    st.plotly_chart(fig, use_container_width=True)
    
    # Função 5)
    fig = pedidos_entregador_semana(df1)
    st.plotly_chart(fig, use_container_width=True)

        
#--------------------------------------------------------------
# Aba Visão Geográfica
#--------------------------------------------------------------
with tab3:
    st.subheader("Mapa de Entregas")
    st.markdown("Veja a localização central das entregas em cada cidade, dividida por condição de trânsito.")
    # Função 6)
    mapa_pais(df1)
