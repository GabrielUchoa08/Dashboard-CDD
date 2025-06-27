# Arquivo: Home.py

import streamlit as st
import pandas as pd
from data_update import carregar_e_limpar_dados, inicializar_estado, criar_sidebar, filtrar_dados

inicializar_estado()

st.set_page_config(
    page_title="Home | 100K US Tech Jobs",
    page_icon="🏠",
    layout="wide"
)

# --- Carregamento de Dados ---
if not st.session_state.dados_carregados:
    # >>> ESTA É A LINHA QUE FOI CORRIGIDA <<<
    all_jobs_df, df_salario = carregar_e_limpar_dados('all_jobs_amostra.csv')
    
    if all_jobs_df is not None:
        st.session_state['all_jobs_df'] = all_jobs_df
        st.session_state['df_salario'] = df_salario
        st.session_state['dados_carregados'] = True
    else:
        st.stop()

# --- Chamada das funções globais ---
criar_sidebar()
filtrar_dados() 

# --- Conteúdo da Página Home ---
st.title("📊 Dashboard de Análise de Vagas de Emprego")
st.markdown("Bem-vindo! Este dashboard apresenta uma análise interativa de vagas de emprego na área de tecnologia nos EUA.")
st.markdown("Use a barra lateral à esquerda para navegar entre as diferentes análises e aplicar filtros globais.")

st.subheader("Visão Geral dos Dados Filtrados")
total_vagas = len(st.session_state['all_jobs_df_filtrado'])
total_empresas = st.session_state['all_jobs_df_filtrado']['company'].nunique()
salario_medio = st.session_state['df_salario_filtrado']['mean_salary'].mean() if not st.session_state['df_salario_filtrado'].empty else 0

col1, col2, col3 = st.columns(3)
col1.metric("Total de Vagas Analisadas", f"{total_vagas:,}")
col2.metric("Total de Empresas Únicas", f"{total_empresas:,}")
col3.metric("Média Salarial Anual (USD)", f"${salario_medio:,.2f}")

st.info("Navegue pelas páginas na barra lateral para ver análises detalhadas.")