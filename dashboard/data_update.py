# Arquivo: data_update.py

import streamlit as st
import pandas as pd

# Funções que não mudam
def inicializar_estado():
    if 'dados_carregados' not in st.session_state:
        st.session_state.dados_carregados = False
    if 'top_n' not in st.session_state:
        st.session_state.top_n = 10
    if 'selected_cities' not in st.session_state:
        st.session_state.selected_cities = []

def criar_sidebar():
    st.sidebar.header("Filtros Interativos")
    st.sidebar.slider(
        'Selecione o número de resultados para os gráficos de "Top":',
        min_value=5, max_value=20, key='top_n'
    )
    cities_list = sorted(st.session_state['all_jobs_df']['city'].dropna().unique())
    st.sidebar.multiselect(
        'Filtre por Cidade:',
        options=cities_list,
        key='selected_cities'
    )

def filtrar_dados():
    if st.session_state.selected_cities:
        st.session_state['all_jobs_df_filtrado'] = st.session_state['all_jobs_df'][st.session_state['all_jobs_df']['city'].isin(st.session_state.selected_cities)]
        st.session_state['df_salario_filtrado'] = st.session_state['df_salario'][st.session_state['df_salario']['city'].isin(st.session_state.selected_cities)]
    else:
        st.session_state['all_jobs_df_filtrado'] = st.session_state['all_jobs_df']
        st.session_state['df_salario_filtrado'] = st.session_state['df_salario']

def categorizar_cargo(titulo):
    titulo = str(titulo).lower()
    if 'data scientist' in titulo: return 'Data Scientist'
    if 'data engineer' in titulo: return 'Data Engineer'
    if 'data analyst' in titulo: return 'Data Analyst'
    if 'software engineer' in titulo: return 'Software Engineer'
    if 'manager' in titulo: return 'Manager'
    if 'machine learning' in titulo: return 'Machine Learning'
    return 'Outros'

# >>> VERSÃO FINAL DA FUNÇÃO DE CARREGAMENTO <<<
@st.cache_data
def carregar_e_limpar_dados():
    # Define o nome do arquivo de amostra que ESTÁ no seu GitHub
    nome_do_arquivo = 'all_jobs_amostra.csv'
    
    try:
        # Lê o arquivo localmente
        all_jobs = pd.read_csv(nome_do_arquivo)
    except FileNotFoundError:
        st.error(f"Erro Crítico: O arquivo '{nome_do_arquivo}' não foi encontrado no repositório do GitHub. Verifique se ele foi enviado.")
        return None, None

    # O resto da função de limpeza
    all_jobs = all_jobs.dropna(subset=['location']) # Garante que a coluna exista antes de usar
    all_jobs = all_jobs[~all_jobs['location'].str.contains('Remote', na=False)]
    all_jobs['location'] = all_jobs['location'].replace('Seattle, WA, USA', 'Seattle, WA, US')
    all_jobs = all_jobs[all_jobs['location'] != 'US']
    all_jobs['city'] = all_jobs['location'].astype(str).apply(lambda x: x.split(',')[0].strip())
    all_jobs = all_jobs[~all_jobs['city'].str.isnumeric()]
    
    df_salario = all_jobs.dropna(subset=['mean_salary']).copy()
    df_salario['mean_salary'] = pd.to_numeric(df_salario['mean_salary'], errors='coerce')
    df_salario = df_salario.dropna(subset=['mean_salary'])
    df_salario.loc[df_salario['mean_salary'] > 1_000_000, 'mean_salary'] /= 100
    df_salario = df_salario[df_salario['mean_salary'] < 1_000_000]

    return all_jobs, df_salario