import streamlit as st
import plotly.express as px
import pandas as pd
from data_update import inicializar_estado, criar_sidebar, filtrar_dados

inicializar_estado()
criar_sidebar()
filtrar_dados()

st.set_page_config(page_title="Explorar Dados", layout="wide")

st.title("Explore os Dados Completos com Paginação")

if 'dados_carregados' not in st.session_state or not st.session_state['dados_carregados']:
    st.error("Por favor, execute a página 'Home' primeiro para carregar os dados.")
    st.stop()

all_jobs_df_filtrado = st.session_state['all_jobs_df_filtrado']

if not all_jobs_df_filtrado.empty:
    items_per_page = st.number_input("Itens por página:", min_value=10, max_value=200, value=20)
    total_items = len(all_jobs_df_filtrado)
    total_pages = (total_items // items_per_page) + (1 if total_items % items_per_page > 0 else 0) if total_items > 0 else 1
    
    page_selection_col, total_pages_col = st.columns([1, 4])
    with page_selection_col:
        page_number = st.number_input("Página", min_value=1, max_value=total_pages, value=1, label_visibility="collapsed")
    with total_pages_col:
        st.markdown(f"<p style='margin-top: 2.2em;'>de {total_pages} páginas</p>", unsafe_allow_html=True)

    start_index = (page_number - 1) * items_per_page
    end_index = min(start_index + items_per_page, total_items)
    
    st.dataframe(all_jobs_df_filtrado.iloc[start_index:end_index])
    st.write(f"Mostrando registros de {start_index + 1} a {end_index} de um total de {total_items}.")
else:
    st.warning("Nenhum dado encontrado para os filtros selecionados.")