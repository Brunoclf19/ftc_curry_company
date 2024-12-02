import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Home",
    page_icon='🏠',
    layout='centered'
)


image = Image.open('logo-ia.png')
st.sidebar.image(image, width=120)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")

st.write("# Curry Company Growth Dashboard")

st.markdown(
    """
    Growth Dashboard foi construído para acompanhar as métricas de crescimento dos Entregadores e Restaurantes.
    ### Como utilizar esse Growth Dashboard?
    - Visão Empresa:
        - Visão Gerencial: Métricas gerais de comportamento.
        - Visão Tática: Indicadores semanais de crescimento.
        - Visão Geográfica: Insights de geolocalização.
    - Visão Entregador:
        - Métricas Gerais: KPIs gerais dos entregadores.
        - Avaliações: Média das avalições dos entregadores.
        - Desempenho de Entrega: Comportamento dos entregadores dadas as condições climáticas.
    - Visão Restaurante:
        - Métricas Gerais: KPIs de desempenho geral dos restaturantes.
    ### Ask for Help
    - LinkedIn
        - www.linkedin.com/in/bruno-freitas-mat-est
"""
)