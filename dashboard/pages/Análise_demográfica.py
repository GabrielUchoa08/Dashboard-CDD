import streamlit as st
import plotly.express as px
import pandas as pd
from data_update import inicializar_estado, criar_sidebar, filtrar_dados

inicializar_estado()
criar_sidebar()
filtrar_dados()

st.set_page_config(page_title="Análise Demográfica", layout="wide")

st.title("Análise Demográfica")
st.markdown("Explore os cargos, empresas e localizações mais comuns nas vagas de tecnologia.")

# Verifica se os dados foram carregados na página principal
if 'dados_carregados' not in st.session_state or not st.session_state['dados_carregados']:
    st.error("Por favor, execute a página 'Home' primeiro para carregar os dados.")
    st.stop()

# Recupera os dados e filtros do st.session_state
all_jobs_df_filtrado = st.session_state['all_jobs_df_filtrado']
top_n = st.session_state['top_n']

# --- Geração dos Gráficos ---

st.markdown(f"#### Top {top_n} Cargos Mais Comuns")
top_titles = all_jobs_df_filtrado['title'].value_counts().nlargest(top_n).sort_values(ascending=True)
fig1 = px.bar(x=top_titles.values, y=top_titles.index, orientation='h', labels={'x': 'Número de Vagas', 'y': 'Cargo'}, text_auto=True, template='plotly_white')
st.plotly_chart(fig1, use_container_width=True)

st.markdown(f"#### Top {top_n} Empresas com Mais Vagas")
top_companies = all_jobs_df_filtrado['company'].value_counts().nlargest(top_n).sort_values(ascending=True)
fig3 = px.bar(x=top_companies.values, y=top_companies.index, orientation='h', labels={'x': 'Número de Vagas', 'y': 'Empresa'}, text_auto=True, color=top_companies.values, color_continuous_scale=px.colors.sequential.Blues)
fig3.update_layout(coloraxis_showscale=False)
st.plotly_chart(fig3, use_container_width=True)


st.markdown(f"#### Top {top_n} Localizações Físicas")
top_locations = all_jobs_df_filtrado['location'].value_counts().nlargest(top_n).sort_values(ascending=True)
fig2 = px.bar(x=top_locations.values, y=top_locations.index, orientation='h', labels={'x': 'Número de Vagas', 'y': 'Localização'}, text_auto=True, color=top_locations.values, color_continuous_scale=px.colors.sequential.Greens)
fig2.update_layout(coloraxis_showscale=False)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("#### Distribuição: Vagas Remotas vs. Presenciais")
counts = all_jobs_df_filtrado['is_remote'].value_counts()
remoto_df = pd.DataFrame({'Tipo de Vaga': ['Presencial', 'Remoto'], 'Quantidade': [counts.get(0, 0), counts.get(1, 0)]})
fig6 = px.pie(remoto_df, values='Quantidade', names='Tipo de Vaga', hole=.3, color_discrete_map={'Remoto':'#007BFF', 'Presencial':'#FFA500'})
fig6.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig6, use_container_width=True)