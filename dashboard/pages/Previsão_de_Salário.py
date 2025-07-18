import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Previsão de Salário", page_icon="🔮", layout="wide")

# Carrega o modelo treinado (usamos st.cache_resource para carregar apenas uma vez)
@st.cache_resource
def carregar_modelo():
    try:
        pipeline = joblib.load('previsao_salarial.joblib')
        return pipeline
    except FileNotFoundError:
        return None

modelo = carregar_modelo()

st.title("🔮 Ferramenta de Previsão de Salário")
st.markdown("Insira os detalhes de uma vaga para obter uma estimativa do salário anual. O modelo foi treinado com base nos dados do dashboard.")
st.markdown("---")

if modelo is None:
    st.error("Arquivo do modelo não encontrado. Por favor, treine e salve o modelo primeiro ('salary_prediction_model.joblib').")
else:
    # Widgets para entrada do usuário
    col1, col2, col3 = st.columns(3)
    
    with col1:
        titulo_vaga = st.text_input("Título do Cargo", placeholder="Ex: Data Scientist")
    
    with col2:
        empresa = st.text_input("Nome da Empresa", placeholder="Ex: Google")
        
    with col3:
        # Pega a lista de localizações dos dados já carregados para o seletor
        if 'all_jobs_df' in st.session_state:
            localizacoes = sorted(st.session_state['all_jobs_df']['location'].dropna().unique())
            localizacao = st.selectbox("Localização", options=localizacoes)
        else:
            localizacao = st.text_input("Localização", placeholder="Ex: New York, NY, US")

    # Botão para fazer a previsão
    if st.button("Estimar Salário", type="primary", use_container_width=True):
        if titulo_vaga and empresa and localizacao:
            # Cria um DataFrame com os dados de entrada do usuário
            dados_entrada = pd.DataFrame({
                'title': [titulo_vaga],
                'company': [empresa],
                'location': [localizacao]
            })
            
            # Faz a previsão
            previsao = modelo.predict(dados_entrada)[0]
            
            # Exibe o resultado
            st.success(f"**Salário Anual Estimado: ${previsao:,.2f}**")
            st.info("Nota: Esta é uma estimativa baseada em um modelo de machine learning e pode variar em relação aos salários reais.")
        else:
            st.warning("Por favor, preencha todos os campos para fazer uma estimativa.")