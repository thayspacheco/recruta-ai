import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Recrut.AI - Visualização com CSV Pronto", layout="wide")

st.markdown("""
# 🔍 Recruta.AI – Triagem ágil e estratégica com IA

Use este App para tomar decisões mais rápidas e baseadas em dados nos seus processos seletivos!

Aqui você pode:
- Ver o **score dos candidatos por vaga**, com base em Hard Skills, Soft Skills, Idiomas, Formação e Experiência.
- Entender quais **categorias pesam mais** na pontuação de cada vaga.
- **Gerar relatórios prontos** para análises detalhadas.
""")


uploaded_file = st.file_uploader("📤 Envie o arquivo `composicao_mock_simulada.csv`", type="csv")

if uploaded_file:
    df_cat_total = pd.read_csv(uploaded_file)

    st.subheader("📊 Composição do Score por Vaga")
    col1, col2 = st.columns([2, 5])
    with col1:
        vaga_sel = st.selectbox("Selecione uma vaga", df_cat_total["titulo_vaga"].unique())

    categorias = ['Hard Skills', 'Soft Skills', 'Idiomas', 'Formação', 'Experiência']
    categorias_presentes = [c for c in categorias if c in df_cat_total.columns]
    df_vaga = df_cat_total[df_cat_total["titulo_vaga"] == vaga_sel].copy()
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

    st.success("✅ Visualização concluída com dados reais!")
