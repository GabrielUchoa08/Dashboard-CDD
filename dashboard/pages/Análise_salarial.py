import streamlit as st
import plotly.express as px
import pandas as pd
from data_update import inicializar_estado, criar_sidebar, filtrar_dados, categorizar_cargo

inicializar_estado()
criar_sidebar()
filtrar_dados()

st.set_page_config(page_title="Análise Salarial", layout="wide")

st.title("Análise Salarial")

# Verifica se os dados foram carregados na página principal
if 'dados_carregados' not in st.session_state or not st.session_state['dados_carregados']:
    st.error("Por favor, execute a página 'Home' primeiro para carregar os dados.")
    st.stop()

# Recupera os dados e filtros do st.session_state
df_salario_filtrado = st.session_state['df_salario_filtrado']
top_n = st.session_state['top_n']


# --- Gráficos de Salário (agora um embaixo do outro) ---

# Gráfico 1: Distribuição de Vagas por Faixa Salarial
st.markdown("#### Distribuição de Vagas por Faixa Salarial")
nbins_hist = st.slider('Ajustar faixas do histograma:', 10, 100, 50, key="slider_bins")
fig4 = px.histogram(df_salario_filtrado, x="mean_salary", nbins=nbins_hist, labels={'mean_salary': 'Salário Anual (USD)'}, template='plotly_white')
st.plotly_chart(fig4, use_container_width=True)


# Adiciona uma linha divisória para separar os gráficos
st.markdown("---")

# Gráfico 2: Top Cargos com Maior Salário Médio
st.markdown(f"#### Top {top_n} Cargos com Maior Salário Médio")
titles_to_exclude = [
    "professional security contract consultant", "psychiatrist", "orthopedic trauma faculty physician",
    "group product manage growth", "Professional Security Contract Consultant", "Psychiatrist",
    "Orthopedic Trauma Faculty Physician", "Group Product Manager, Growth",
    "Physician Gastroenterology - Competitive Salary", "Physician Gastroenterology - Make up to $530,040/annually",
    "Vice President of Global Accounts", "Manufacture Sales Representive - Industrial Lubricants",
    "Post Production Supervisor, FIN Studios", "Director, Corporate Relations",
    "Sr. Director, Product Management, Personalization", "Product Manager, Member Experiences"
]
filtered_df_salario = df_salario_filtrado[~df_salario_filtrado['title'].isin(titles_to_exclude)]

if not filtered_df_salario.empty:
    salario_por_titulo = filtered_df_salario.groupby("title")["mean_salary"].mean().nlargest(top_n).sort_values(ascending=True)
    fig5 = px.bar(
        x=salario_por_titulo.values, y=salario_por_titulo.index, orientation='h',
        labels={'x': 'Salário Médio Anual (USD)', 'y': 'Cargo'}, text=salario_por_titulo.values,
        template='plotly_white', color=salario_por_titulo.values, color_continuous_scale=px.colors.sequential.Plasma
    )
    fig5.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
    fig5.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig5, use_container_width=True)
else:
    st.warning("Não há dados de salário para os filtros selecionados.")

st.markdown("---")
st.title("Distribuição dos salários anuais para diferentes vagas.")

df_salario_filtrado = st.session_state['df_salario_filtrado'].copy()
df_salario_filtrado['categoria_cargo'] = df_salario_filtrado['title'].apply(categorizar_cargo)

# Remove a categoria "Outros" para um gráfico mais limpo
df_plot = df_salario_filtrado[df_salario_filtrado['categoria_cargo'] != 'Outros']

# Cria o Box Plot
fig = px.box(
    df_plot.sort_values(by='categoria_cargo'),
    x='categoria_cargo',
    y='mean_salary',
    color='categoria_cargo',
    labels={
        "mean_salary": "Salário Anual (USD)",
        "categoria_cargo": "Categoria do Cargo"
    },
    template="plotly_white",
    points="all" # Mostra todos os pontos de dados
)

fig.update_layout(showlegend=False)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

st.header("Salário Médio X Volume de Vagas")

# Embora essa análise específica não estivesse no notebook original, ela é uma ótima adição.
# Primeiro, precisamos agrupar os dados por cargo para calcular a contagem e a média salarial.
if not df_salario_filtrado.empty:
    df_agregado = df_salario_filtrado.groupby('title').agg(
        contagem_vagas=('title', 'count'),
        salario_medio=('mean_salary', 'mean')
    ).reset_index()

    # Filtra para cargos com mais de uma vaga para um gráfico mais limpo
    df_agregado = df_agregado[df_agregado['contagem_vagas'] > 2]

    if not df_agregado.empty:
        fig_scatter = px.scatter(
            df_agregado,
            x="contagem_vagas",
            y="salario_medio",
            size="contagem_vagas",  # Tamanho da bolha reflete o número de vagas
            color="salario_medio",  # Cor reflete o salário
            hover_name="title",     # Mostra o nome do cargo ao passar o mouse
            log_x=True,             # Escala logarítmica para melhor visualização da demanda
            size_max=60,
            labels={
                "contagem_vagas": "Número de Vagas (Escala Log)",
                "salario_medio": "Salário Médio Anual (USD)"
            },
            template="plotly_white"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.warning("Não há cargos com vagas suficientes para gerar o gráfico de dispersão com os filtros atuais.")
else:
    st.warning("Não há dados suficientes para gerar o gráfico de dispersão com os filtros atuais.")
