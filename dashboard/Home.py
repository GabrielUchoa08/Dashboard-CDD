# Arquivo: Home.pyAdd commentMore actions

import streamlit as st
import pandas as pd
# >>> MUDANÇA: Importar a nova função
from data_update import carregar_e_limpar_dados, inicializar_estado, criar_sidebar

inicializar_estado()

st.set_page_config(
    page_title="100K US Tech Jobs",
    layout="wide"
)

# Carregamento de Dados (só executa se os dados ainda não estiverem na sessão)
if not st.session_state.dados_carregados:
    all_jobs_df, df_salario = carregar_e_limpar_dados('all_jobs.csv')
    if all_jobs_df is not None:
        st.session_state['all_jobs_df'] = all_jobs_df
        st.session_state['df_salario'] = df_salario
        st.session_state['dados_carregados'] = True
    else:
        st.stop()


# --- Lógica de filtragem ---
if st.session_state.selected_cities:
    st.session_state['all_jobs_df_filtrado'] = st.session_state['all_jobs_df'][st.session_state['all_jobs_df']['city'].isin(st.session_state.selected_cities)]
    st.session_state['df_salario_filtrado'] = st.session_state['df_salario'][st.session_state['df_salario']['city'].isin(st.session_state.selected_cities)]
else:
    st.session_state['all_jobs_df_filtrado'] = st.session_state['all_jobs_df']
    st.session_state['df_salario_filtrado'] = st.session_state['df_salario']

# --- Conteúdo da Página Home ---
st.title("📊 Dashboard sobre vagas de emprego em tecnologia nos EUA")
st.markdown("Esse dashboard contém dados obtidos do dataset 100K US Tech Jobs, com dados de outubro de 2024 a dezembro de 2024 com vagas de empregos na área de tecnologia, os dados foram colhidos com a ajuda do Jobspy (uma ferramenta de busca e seleção de empregos) em sites como Indeed, ZipRecruiter e Glassdoor")
st.markdown("---")

st.subheader("Visão Geral dos Dados")
total_vagas = len(st.session_state['all_jobs_df_filtrado'])
total_empresas = st.session_state['all_jobs_df_filtrado']['company'].nunique()
salario_medio = st.session_state['df_salario_filtrado']['mean_salary'].mean() if not st.session_state['df_salario_filtrado'].empty else 0

col1, col2, col3 = st.columns(3)
col1.metric("Total de Vagas Analisadas", f"{total_vagas:,}")
col2.metric("Total de Empresas Únicas", f"{total_empresas:,}")
col3.metric("Média Salarial Anual (USD)", f"${salario_medio:,.2f}")
st.markdown("---")
st.subheader("Sobre o projeto:")
st.markdown("Esse projeto é referente a 2º Unidade da matéria de Ciência de dados (DCA3501) do Departamento de Computação e Automação (DCA) da Universidade Federal do Rio Grande do Norte (UFRN) lecionada pelo professor Luiz Affonso H. G. de Oliveira, no qual consiste em criar um Dashboard para visualização de dados de um dataset previamente escolhido.")

st.subheader("Discentes:")
st.markdown("Cassio Costa Alves Domingues <br> Gabriel Uchôa da Escóssia", unsafe_allow_html=True)
