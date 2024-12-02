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

st.set_page_config(page_title='Visão Restaurantes', page_icon='🥪', layout='wide')

# Função 5)
# O tempo médio e o desvio padrão de entrega por cidade e tipo de pedido.
def avg_std_city_order (df1):
    # 4. O tempo médio e o desvio padrão de entrega por cidade e tipo de pedido.
    colunas = ['Time_taken(min)','City', 'Type_of_order']
    df_aux = df1.loc[:,colunas].groupby(['City','Type_of_order']).agg({'Time_taken(min)': ['mean','std']})
    df_aux.columns = ['avg_time','std_time']
    df_aux = df_aux.reset_index()
    return df_aux
#--------------------------------------------------------------
#--------------------------------------------------------------
# Função 4)
# O tempo médio e o desvio padrão de entrega por cidade e tipo de tráfego.
def avg_std_city_traffic(df1):
                # 5. O tempo médio e o desvio padrão de entrega por cidade e tipo de tráfego.
                colunas = ['Time_taken(min)','City', 'Road_traffic_density']

                df_aux = df1.loc[:,colunas].groupby(['City','Road_traffic_density']).agg({'Time_taken(min)': ['mean','std']})

                df_aux.columns = ['avg_time','std_time']

                df_aux = df_aux.reset_index()

                # Criação do gráfico de Sunburst
                fig = px.sunburst(
                    df_aux,
                    path=['City', 'Road_traffic_density'],
                    values='avg_time',
                    color='std_time',  # Coluna usada para coloração
                    color_continuous_scale='RdBu',  # Corrigido o nome do parâmetro
                    color_continuous_midpoint=np.average(df_aux['std_time'])  # Corrigido o nome do parâmetro
                )

                fig.update_layout(title="Tempo Médio e Desvio Padrão de Entrega por Cidade e Condição de Tráfego")

                return fig

#--------------------------------------------------------------
#--------------------------------------------------------------
# Função 4)
# Distribuição por tempo
def avg_distance_graph(df1):
            # Calculando a distância média
            cols = ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']
            df1['distance'] = df1.loc[:, cols].apply(lambda x: 
                                                    haversine(
                                                        (x['Restaurant_latitude'], x['Restaurant_longitude']),
                                                        (x['Delivery_location_latitude'], x['Delivery_location_longitude'])
                                                    ), axis=1)

            avg_distance = df1.loc[:, ['City', 'distance']].groupby('City').mean().reset_index()

            # Definindo cores personalizadas para cada cidade
            colors = ['#EB1D1D', '#4472C4', '#00B050']  # Exemplo de paleta com cores distintas para cada cidade

            # Criando o gráfico com título
            fig = go.Figure(data=[go.Pie(labels=avg_distance['City'], values=avg_distance['distance'], pull=[0, 0.1, 0], 
                                marker=dict(colors=colors))])
            
            # Atualizando layout para centralizar título e colocar legenda à direita
            fig.update_layout(
                title={
                'text': "Distância Média de Entrega por Cidade",
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
                },
                legend={
                'orientation': 'v',      # Define a orientação como vertical
                'yanchor': 'middle',     # Centraliza verticalmente
                'y': 0.5,                # Posição vertical (meio)
                'xanchor': 'right',      # Alinha à direita
                'x': 1.1                 # Coloca a legenda à direita do gráfico
                }
            )
            return fig
#--------------------------------------------------------------
#--------------------------------------------------------------
# Função 3)
# Distribuição por tempo
def avg_std_time_graph(df1):
    # 3. O tempo médio e o desvio padrão de entrega por cidade.
    colunas = ['Time_taken(min)','City']

    df_aux = df1.loc[:,colunas].groupby('City').agg({'Time_taken(min)': ['mean','std']})

    df_aux.columns = ['avg_time','std_time']

    df_aux = df_aux.reset_index()

    fig = go.Figure()
    fig.add_trace(go.Bar(name='Control',
                        x=df_aux['City'], 
                        y=df_aux['avg_time'], 
                        marker=dict(color='#20B2AA'), 
                        error_y=dict(type='data',
                                    array=df_aux['std_time']
                                    ) 
                        )
                    )
    fig.update_layout(
        barmode='group',
        title='Tempo Médio de Entrega por Cidade com Desvio Padrão',
        xaxis_title='Cidade',
        yaxis_title='Tempo Médio de Entrega (min)'
        )
    return fig
#--------------------------------------------------------------
#--------------------------------------------------------------
# Função 2)
# Cálculo de média e desvio padrão de tempo de entrega
def avg_std_time_delivery(df1, festival, op):
    """
    Calcula o tempo médio ou o desvio padrão do tempo de entrega para um festival específico.
    
    Args:
    df1 (DataFrame): O DataFrame com os dados.
    festival (str): O festival ("Yes" ou "No").
    op (str): Operação desejada ("avg_time" ou "std_time").
    
    Returns:
    float: Valor calculado (média ou desvio padrão), arredondado para 2 casas decimais.
    """
    # Agrupamento para calcular média e desvio padrão
    df_aux = (df1.loc[:, ['Time_taken(min)', 'Festival']]
                .groupby('Festival')
                .agg({'Time_taken(min)': ['mean', 'std']}))
    
    # Renomeando colunas
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()
    
    # Filtrando pelo festival e operação solicitada
    result = df_aux.loc[df_aux['Festival'] == festival, op].round(2).values[0]
    return result

#--------------------------------------------------------------
#--------------------------------------------------------------
# Função 1)
# Cálculo de distância
def distance(df1):

    # 2. A distância média dos resturantes e dos locais de entrega.
    colunas = ['Restaurant_latitude','Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']

    df1['Distancia'] = df1.loc[:, colunas].apply(lambda x: 
                                        haversine
                                        ((x['Restaurant_latitude'], x['Restaurant_longitude']),
                                            (x['Delivery_location_latitude'], x['Delivery_location_longitude'])),
                                            axis=1)

    distancia = df1.Distancia.mean().round(2)
    return distancia
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
df = pd.read_csv(r'/workspaces/ftc_curry_company/dataset/train.csv')
# df1 = df.copy()

# ------------------------------ 
# Limpando os dados
# ------------------------------ 
df1 = clean_code(df)



# Visão - Restaturantes
st.header('Marketplace - Visão Restaurantes')

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

tab1 = st.tabs(['Métricas Gerais'])

with tab1[0]:
    with st.container():
        st.title('Overal Metrics')

        col1,col2,col3,col4,col5,col6 = st.columns(6)
        with col1:
            qtd_entregadores = df1.loc[:, 'Delivery_person_ID'].nunique()
            col1.markdown("Entregadores Únicos")
            col1.write(f"{qtd_entregadores}")

        with col2:
            distancia = distance(df1)
            col2.markdown("Distância Média")
            col2.write(f"{distancia} km")

        with col3:
            df_aux = avg_std_time_delivery(df1, 'Yes', 'avg_time')
            col3.markdown("Tempo Médio com Festival")
            col3.write(f"{df_aux} min")

        with col4:
            df_aux = avg_std_time_delivery(df1, 'Yes', 'std_time')
            col4.markdown("Desvio padrão com Festival")
            col4.write(f"{df_aux} min")

        with col5:
            # Tempo médio de entrega com festival
            df_aux = avg_std_time_delivery(df1, 'No', 'avg_time')
            col5.markdown("Tempo Médio sem Festival")
            col5.write(f"{df_aux} min")
        
        with col6:
            # Desvio padrão médio de entrega com festival
            df_aux = avg_std_time_delivery(df1, 'No', 'std_time')
            col6.markdown("Desvio Padrão sem Festival")
            col6.write(f"{df_aux} min")          

    
    with st.container():
        st.markdown("""---""")
        st.title('Distribuição por tempo')
        fig = avg_std_time_graph(df1)
        st.plotly_chart(fig)

    with st.container():
        st.markdown("""---""")
        st.title('Tempo médio de entrega por cidade')
        # Exibindo gráfico
        fig = avg_distance_graph(df1)
        st.plotly_chart(fig)

    with st.container():
            fig = avg_std_city_traffic(df1)
            st.plotly_chart(fig)
            
    with st.container():
        st.markdown("""---""")
        st.title('Distribuição da distância')
        df_aux = avg_std_city_order(df1)
        st.dataframe(df_aux)
