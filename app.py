import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import datetime
import time
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="Recrut.AI - Triagem Inteligente", layout="wide")

# --- Modelo mock embutido ---
def carregar_modelo_mock():
    colunas = [f"feature_{i}" for i in range(50)]
    X = pd.DataFrame([[0]*50], columns=colunas)
    y = [0]
    modelo = RandomForestClassifier()
    modelo.fit(X, y)
    return modelo, colunas, {}

modelo, colunas_X, tfidf_dict = carregar_modelo_mock()

# --- Sidebar e introdução ---
st.sidebar.title("⚙️ Navegação")
st.sidebar.markdown("""
1. Upload do CSV
2. Composição estratégica por vaga
3. Panorama geral por categoria
""")

st.markdown("""
# 🔍 Recrut.AI – Triagem ágil e estratégica com IA

Use este App para tomar decisões mais rápidas e baseadas em dados nos seus processos seletivos!

Aqui você pode:
- Ver o **score dos candidatos por vaga**, com base em Hard Skills, Soft Skills, Idiomas, Formação e Experiência.
- Entender quais **categorias pesam mais** na pontuação de cada vaga.
- **Gerar relatórios prontos** para análises detalhadas.
""")

colunas_categoricas = [
    'area_atuacao', 'nivel_academico_x', 'nivel_ingles_x', 'nivel_espanhol_x',
    'titulo_profissional', 'titulo_vaga', 'cliente_y', 'tipo_contratacao', 'areas_atuacao'
]

# --- Filtros agrupados ---
with st.expander("🏋️ Filtros", expanded=True):
    col1, col2 = st.columns([1, 3])
    with col1:
        modo_simulacao = st.checkbox("⚡ Modo Simulado (carregamento rápido)")
    with col2:
        uploaded_file = st.file_uploader("Envie o CSV com os candidatos", type="csv", key="upload_csv")

@st.cache_data(show_spinner="⏳ Processando dados...")
def processar_dados(df):
    df = df.drop_duplicates(subset=['nome', 'titulo_vaga']).reset_index(drop=True)
    df[colunas_categoricas] = df[colunas_categoricas].fillna('desconhecido')

    tfidf_frames = []
    for col in tfidf_dict:
        if col in df.columns:
            vetor = tfidf_dict[col]
            df[col] = df[col].fillna('')
            tfidf_vals = vetor.transform(df[col])
            tfidf_df = pd.DataFrame(tfidf_vals.toarray(), columns=[f"{col}_tfidf_{i}" for i in range(tfidf_vals.shape[1])])
            tfidf_frames.append(tfidf_df)

    df_tfidf = pd.concat(tfidf_frames, axis=1) if tfidf_frames else pd.DataFrame(index=df.index)
    df_dummies = pd.get_dummies(df[colunas_categoricas], drop_first=True)
    X = pd.concat([df_tfidf, df_dummies], axis=1).reset_index(drop=True)

    for col in colunas_X:
        if col not in X.columns:
            X[col] = 0
    X = X[colunas_X]

    proba = modelo.predict_proba(X)[:, 1]
    df['score'] = proba.round(4)

    pesos = modelo.feature_importances_
    categorias_map = []
    for i in range(len(df)):
        linha = X.iloc[i]
        contrib = {'nome': df.loc[i, 'nome'], 'titulo_vaga': df.loc[i, 'titulo_vaga']}
        for j, val in enumerate(linha):
            if val > 0:
                feature = X.columns[j]
                if 'ingles' in feature or 'espanhol' in feature:
                    cat = 'Idiomas'
                elif 'competencia' in feature or 'tecnico' in feature:
                    cat = 'Hard Skills'
                elif 'habilidades_comportamentais' in feature or 'objetivo_profissional' in feature:
                    cat = 'Soft Skills'
                elif 'nivel_academico' in feature:
                    cat = 'Formação'
                elif 'area_atuacao' in feature or 'titulo_profissional' in feature:
                    cat = 'Experiência'
                else:
                    continue
                contrib[cat] = contrib.get(cat, 0) + val * pesos[j]
        categorias_map.append(contrib)

    df_cat_total = pd.DataFrame(categorias_map).fillna(0)
    df_cat_total.to_pickle("cat_total.pkl")
    with open("cat_total_info.txt", "w") as f:
        f.write(f"Cache gerado em: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    return df_cat_total

# --- Processamento ---
if uploaded_file is not None:
    if modo_simulacao:
        try:
            df_cat_total = pd.read_pickle("cat_total.pkl")
            with open("cat_total_info.txt", "r") as f:
                cache_info = f.read()
            st.success(f"✅ Dados simulados carregados com sucesso!\n{cache_info}")
        except FileNotFoundError:
            st.error("Arquivo de simulação 'cat_total.pkl' não encontrado.")
            st.stop()
    else:
        df = pd.read_csv(uploaded_file)
        start = time.perf_counter()
        df_cat_total = processar_dados(df)
        end = time.perf_counter()
        tempo_execucao = end - start
        st.success(f"✅ Arquivo processado com sucesso em {tempo_execucao:.2f} segundos.")

    st.divider()
    st.subheader("📊 Composição do Score por Vaga")

    col1, col2 = st.columns([2, 5])
    with col1:
        vaga_sel = st.selectbox("Selecione uma vaga", df_cat_total['titulo_vaga'].unique())

    df_vaga = df_cat_total[df_cat_total['titulo_vaga'] == vaga_sel].copy()
    if not df_vaga.empty:
        categorias = ['Hard Skills', 'Soft Skills', 'Idiomas', 'Formação', 'Experiência']
        categorias_presentes = [c for c in categorias if c in df_vaga.columns]
        df_vaga = df_vaga.sort_values(by=categorias_presentes, ascending=False)
        fig_stacked = px.bar(df_vaga, x='nome', y=categorias_presentes, title=f"Gráfico", height=500)
        fig_stacked.update_layout(title_x=0.5)
        st.plotly_chart(fig_stacked)
    else:
        st.info("Sem dados suficientes para esta vaga.")

    st.divider()
    st.subheader("📈 Panorama Geral - Impacto das Categorias")
    categorias_presentes_panorama = [c for c in ['Hard Skills', 'Soft Skills', 'Idiomas', 'Formação', 'Experiência'] if c in df_cat_total.columns]
    df_panorama = df_cat_total[categorias_presentes_panorama].sum().reset_index()
    df_panorama.columns = ['Categoria', 'Impacto Total']
    fig_pan = px.bar(df_panorama.sort_values('Impacto Total'), x='Impacto Total', y='Categoria', orientation='h', color='Categoria', title='Gráfico')
    fig_pan.update_layout(title_x=0.5)
    st.plotly_chart(fig_pan)

    st.divider()
    st.subheader("🧐 Insights por Categoria")
    df_summary = df_cat_total.groupby('titulo_vaga')[categorias_presentes_panorama].mean()
    df_summary['Total'] = df_summary.sum(axis=1)
    for col in categorias_presentes_panorama:
        df_summary[col] = (df_summary[col] / df_summary['Total'] * 100).round(1)
    df_summary = df_summary.drop(columns='Total').reset_index()

    df_melt = df_summary.melt(id_vars='titulo_vaga', var_name='Categoria', value_name='Proporção (%)')
    for categoria in df_melt['Categoria'].unique():
        top_vaga = df_melt[df_melt['Categoria'] == categoria].sort_values(by='Proporção (%)', ascending=False).iloc[0]
        if top_vaga['Proporção (%)'] > 0:
            st.markdown(f"- A vaga **{top_vaga['titulo_vaga']}** é a mais influenciada por **{categoria}** ({top_vaga['Proporção (%)']}%).")

    st.divider()
    st.subheader("📊 Proporção por Categoria em Cada Vaga")
    fig_stacked_vagas = px.bar(df_melt, x='titulo_vaga', y='Proporção (%)', color='Categoria', text='Proporção (%)', title='Gráfico')
    fig_stacked_vagas.update_layout(title_x=0.5)
    st.plotly_chart(fig_stacked_vagas)

    csv = df_cat_total.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Baixar dados", data=csv, file_name="composicao_candidatos.csv")

    st.divider()
    st.subheader("📘 Como funciona o modelo?")
    st.markdown("""
    Este modelo é fictício e usado apenas para fins demonstrativos.

    Ele avalia candidatos com base em 5 categorias:
    - **Hard Skills**
    - **Soft Skills**
    - **Idiomas**
    - **Formação**
    - **Experiência**
    """)