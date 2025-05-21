import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier
import numpy as np

st.set_page_config(page_title="Recrut.AI - Triagem Inteligente", layout="wide")

# --- Modelo fictício com pesos simulados por categoria ---
def carregar_modelo_mock():
    colunas = [f"feature_{i}" for i in range(50)]
    X = pd.DataFrame([[0]*50, [1]*50], columns=colunas)
    y = [0, 1]
    modelo = RandomForestClassifier()
    modelo.fit(X, y)
    # Simular importâncias coerentes
    importancias = [0]*50
    importancias[0:10] = [0.02]*10  # Hard Skills
    importancias[10:20] = [0.015]*10  # Soft Skills
    importancias[20:30] = [0.01]*10  # Idiomas
    importancias[30:40] = [0.007]*10  # Formação
    importancias[40:50] = [0.005]*10  # Experiência
    modelo.feature_importances_ = np.array(importancias)
    return modelo, colunas

modelo, colunas_X = carregar_modelo_mock()

st.sidebar.title("⚙️ Navegação")
st.sidebar.markdown("""
1. Upload do CSV
2. Score por Vaga
3. Análise por Categoria
""")

st.markdown("""
# 🔍 Recrut.AI – Triagem ágil com IA (versão mock para apresentação)

Este app simula o funcionamento do modelo com categorias reais para fins de apresentação:

- Upload de CSV com colunas `nome`, `titulo_vaga`, `feature_0` a `feature_49`
- Score e gráficos gerados com categorização visual realista
""")

uploaded_file = st.file_uploader("📤 Envie o arquivo CSV com os candidatos", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    expected = ["nome", "titulo_vaga"] + [f"feature_{i}" for i in range(50)]
    if not all(col in df.columns for col in expected):
        st.error("❌ O arquivo não contém as colunas esperadas.")
        st.stop()

    # Previsão
    X = df[[f"feature_{i}" for i in range(50)]]
    proba = modelo.predict_proba(X)[:, 1]
    df["score"] = proba.round(4)

    # Categorias simuladas
    pesos = modelo.feature_importances_
    categorias_map = []
    for i in range(len(df)):
        linha = X.iloc[i]
        contrib = {'nome': df.loc[i, 'nome'], 'titulo_vaga': df.loc[i, 'titulo_vaga']}
        for j, val in enumerate(linha):
            if val > 0:
                if 0 <= j < 10:
                    cat = 'Hard Skills'
                elif 10 <= j < 20:
                    cat = 'Soft Skills'
                elif 20 <= j < 30:
                    cat = 'Idiomas'
                elif 30 <= j < 40:
                    cat = 'Formação'
                else:
                    cat = 'Experiência'
                contrib[cat] = contrib.get(cat, 0) + val * pesos[j]
        categorias_map.append(contrib)

    df_cat_total = pd.DataFrame(categorias_map).fillna(0)

    # Score por vaga
    st.subheader("📊 Composição do Score por Vaga")
    col1, col2 = st.columns([2, 5])
    with col1:
        vaga_sel = st.selectbox("Selecione uma vaga", df_cat_total["titulo_vaga"].unique())

    df_vaga = df_cat_total[df_cat_total["titulo_vaga"] == vaga_sel]
    categorias = ['Hard Skills', 'Soft Skills', 'Idiomas', 'Formação', 'Experiência']
    categorias_presentes = [c for c in categorias if c in df_vaga.columns]
    df_vaga = df_vaga.sort_values(by=categorias_presentes, ascending=False)

    fig = px.bar(df_vaga, x="nome", y=categorias_presentes, title=f"Gráfico", height=500)
    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig)

    st.subheader("📈 Panorama Geral - Impacto das Categorias")
    df_panorama = df_cat_total[categorias_presentes].sum().reset_index()
    df_panorama.columns = ['Categoria', 'Impacto Total']
    fig_pan = px.bar(df_panorama.sort_values('Impacto Total'), x='Impacto Total', y='Categoria', orientation='h', color='Categoria', title='Gráfico')
    fig_pan.update_layout(title_x=0.5)
    st.plotly_chart(fig_pan)

    st.subheader("📊 Proporção por Categoria em Cada Vaga")
    df_summary = df_cat_total.groupby('titulo_vaga')[categorias_presentes].mean()
    df_summary['Total'] = df_summary.sum(axis=1)
    for col in categorias_presentes:
        df_summary[col] = (df_summary[col] / df_summary['Total'] * 100).round(1)
    df_summary = df_summary.drop(columns='Total').reset_index()
    df_melt = df_summary.melt(id_vars='titulo_vaga', var_name='Categoria', value_name='Proporção (%)')

    fig_final = px.bar(df_melt, x='titulo_vaga', y='Proporção (%)', color='Categoria', text='Proporção (%)', title='Gráfico')
    fig_final.update_layout(title_x=0.5)
    st.plotly_chart(fig_final)