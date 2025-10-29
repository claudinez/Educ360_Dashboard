import pandas as pd
import plotly.express as px
import streamlit as st
import os

# Demanda Cliente
# 1 - Numero de Consultas Geral e por Data (Selectbox) - Grafico de Barras
# 2 - Por unidade as consutas - Especialidade
# # layout da pagina

st.set_page_config(page_title="Painel de Consultas Médicas", layout="wide")

# CSV
csv_local = "Dados/consultas.csv"
csv_remoto = "https://raw.githubusercontent.com/claudinez/Educ360_Dashboard_Clinica/main/consultas.csv"

if os.path.exists(csv_local):
    df = pd.read_csv("Dados/consultas.csv", parse_dates=["dataconsulta"])
    datas_unicas = sorted(df["dataconsulta"].dt.strftime("%d-%m-%Y").unique())
else:
    df = pd.read_csv("Dados/consultas.csv", parse_dates=["dataconsulta"])
    datas_unicas = sorted(df["dataconsulta"].dt.strftime("%d-%m-%Y").unique())

#df = pd.read_csv("Dados/consultas.csv", parse_dates=["dataconsulta"])
#datas_unicas = sorted(df["dataconsulta"].dt.strftime("%d-%m-%Y").unique())

# combo das datas
opcao_data = st.sidebar.selectbox("Selecione uma data", options=["Todas"] + datas_unicas)

# combo das unidades
unidade = sorted(df["unidade"].unique())
opcao_unidade = st.sidebar.selectbox("Selecione uma unidade", options=["Todas"] + unidade)

# aplicar filtros
df_filtrado = df.copy()
if opcao_data != "Todas":
    df_filtrado = df_filtrado[df_filtrado["dataconsulta"].dt.strftime("%d-%m-%Y") == opcao_data]
if opcao_unidade != "Todas":
    df_filtrado = df_filtrado[df_filtrado["unidade"] == opcao_unidade]

# Composição dos gráficos
st.title("📊 Painel de Consultas Médicas")
col1, col2 = st.columns(2)

# Gráfico 1 - Número de Consultas por Unidade
consultas_unidade = df_filtrado.groupby("unidade").size().reset_index(name="Total")

fig1 = px.bar(
    consultas_unidade,
    x="unidade",
    y="Total",
    color="unidade",
    title=f"Número de Consultas por Unidade ({opcao_data})",
    text="Total"
)
fig1.update_layout(xaxis_title="Unidade", yaxis_title="Total de Consultas")

# ✅ Correção: uso do novo parâmetro
col1.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})

# Gráfico 2 - Consultas por Especialidade
consultas_tipo = df_filtrado.groupby("tipoconsulta").size().reset_index(name="Total")

# Paleta de cores discretas (tons suaves e equilibrados)
cores_discretas = {
    "Clínico Geral": "#6baed6",
    "Pediatria": "#9ecae1",
    "Ginecologia": "#a1d99b",
    "Ortopedia": "#74c476",
    "Cardiologia": "#fd8d3c",
    "Dermatologia": "#fdae6b",
    "Oftalmologia": "#bcbddc",
    "Outros": "#969696"
}

fig2 = px.pie(
    consultas_tipo,
    values="Total",
    names="tipoconsulta",
    color="tipoconsulta",
    color_discrete_map=cores_discretas,
    title="Consultas por Especialidade",
    hole=0.2
)

fig2.update_traces(
    textinfo="percent+label",
    textposition="inside",
    pull=[0.03] * len(consultas_tipo)
)

fig2.update_layout(
    legend_title="Tipo de Consulta",
    title_x=0.25,
    showlegend=True,
    font=dict(size=14),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)

# ✅ Correção: uso do novo parâmetro
col2.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

# Visão dos atendimentos
st.subheader(f"Registros: {opcao_unidade}")

# Formata a coluna de data
df_exibicao = df_filtrado.copy()
df_exibicao["dataconsulta"] = df_exibicao["dataconsulta"].dt.strftime("%d/%m/%Y")

# Exibe com formatação ajustada
st.dataframe(df_exibicao, use_container_width=True)
