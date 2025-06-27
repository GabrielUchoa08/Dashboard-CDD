import streamlit as st
import pandas as pd

def inicializar_estado():
    """
    Inicializa todas as chaves necessárias no st.session_state se elas não existirem.
    Esta função deve ser chamada no início de cada página do aplicativo.
    """
    if 'dados_carregados' not in st.session_state:
        st.session_state.dados_carregados = False
    if 'top_n' not in st.session_state:
        st.session_state.top_n = 10
    if 'selected_cities' not in st.session_state:
        st.session_state.selected_cities = []

def criar_sidebar():
    """Cria a sidebar com os filtros interativos."""
    st.sidebar.header("Filtros Interativos")
    
    st.sidebar.slider(
        'Selecione o número de resultados para os gráficos de "Top":',
        min_value=5, max_value=20, key='top_n'
    )
    
    # Usa o DataFrame do session_state para criar a lista de cidades
    cities_list = sorted(st.session_state['all_jobs_df']['city'].dropna().unique())
    st.sidebar.multiselect(
        'Filtre por Cidade:',
        options=cities_list,
        key='selected_cities'
    )

def filtrar_dados():
    """Aplica os filtros selecionados na sidebar aos dataframes e os armazena no session_state."""
    if st.session_state.selected_cities:
        # Filtra os dados se uma ou mais cidades forem selecionadas
        st.session_state['all_jobs_df_filtrado'] = st.session_state['all_jobs_df'][st.session_state['all_jobs_df']['city'].isin(st.session_state.selected_cities)]
        st.session_state['df_salario_filtrado'] = st.session_state['df_salario'][st.session_state['df_salario']['city'].isin(st.session_state.selected_cities)]
    else:
        # Se nenhuma cidade for selecionada, usa os dataframes completos
        st.session_state['all_jobs_df_filtrado'] = st.session_state['all_jobs_df']
        st.session_state['df_salario_filtrado'] = st.session_state['df_salario']

def categorizar_cargo(titulo):
    titulo = str(titulo).lower()
    if 'data scientist' in titulo or 'cientista de dados' in titulo:
        return 'Data Scientist'
    if 'data engineer' in titulo or 'engenheiro de dados' in titulo:
        return 'Data Engineer'
    if 'data analyst' in titulo or 'analista de dados' in titulo:
        return 'Data Analyst'
    if 'software engineer' in titulo or 'developer' in titulo or 'desenvolvedor' in titulo:
        return 'Software Engineer'
    if 'manager' in titulo or 'gerente' in titulo:
        return 'Manager'
    if 'machine learning' in titulo or 'ml engineer' in titulo:
        return 'Machine Learning'
    if 'product' in titulo and 'manager' not in titulo:
        return 'Product (Outros)'
    return 'Outros'        

def categorizar_cargo(titulo):
    """Agrupa títulos de cargos em categorias mais amplas."""
    titulo = str(titulo).lower()
    if 'data scientist' in titulo or 'cientista de dados' in titulo:
        return 'Data Scientist'
    if 'data engineer' in titulo or 'engenheiro de dados' in titulo:
        return 'Data Engineer'
    if 'data analyst' in titulo or 'analista de dados' in titulo:
        return 'Data Analyst'
    if 'software engineer' in titulo or 'developer' in titulo or 'desenvolvedor' in titulo:
        return 'Software Engineer'
    if 'manager' in titulo or 'gerente' in titulo:
        return 'Manager'
    if 'machine learning' in titulo or 'ml engineer' in titulo:
        return 'Machine Learning'
    if 'product' in titulo and 'manager' not in titulo:
        return 'Product (Outros)'
    return 'Outros'

@st.cache_data
def carregar_e_limpar_dados(): # A função não precisa mais de argumentos
    
    # >>> MUDE APENAS O LINK ABAIXO PARA O SEU LINK DO GOOGLE DRIVE <<<
    URL_DO_ARQUIVO = "https://drive.google.com/uc?export=download&id=1WKW1J6Xo0HQWN8mxmBN1GY2WNjFhvwKL"
    
    try:
        # Mostra uma mensagem enquanto carrega, pois pode demorar um pouco
        with st.spinner("Carregando o dataset completo... Por favor, aguarde."):
            all_jobs = pd.read_csv(URL_DO_ARQUIVO)
    except Exception as e:
        st.error(f"Erro ao carregar os dados do Google Drive. Verifique se o link está público e correto. Erro: {e}")
        return None, None

    # O resto da sua função de limpeza continua exatamente igual
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