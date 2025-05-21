import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="Recrut.AI - Triagem Inteligente", layout="wide")

# --- Modelo fictício direto no app ---
def carregar_modelo_mock():
    colunas = [f"feature_{i}" for i in range(50)]
    X = pd.DataFrame([[0]*50, [1]*50], columns=colunas)
    y = [0, 1]
    modelo = RandomForestClassifier()
    modelo.fit(X, y)
    return modelo, colunas

modelo, colunas_X = carregar_modelo_mock()

# --- Interface ---
st.sidebar.title("⚙️ Navegação")
st.sidebar.markdown("""
1. Upload do CSV
2. Score por Vaga
3. Análise por Categoria
""")

st.markdown("""
# 🔍 Recrut.AI – Triagem ágil com IA (versão mock para Streamlit Cloud)

Este app simula o funcionamento da IA com dados estruturados de candidatos.

- Upload de CSV com colunas `nome`, `titulo_vaga`, `feature_0` a `feature_49`
- Geração de scores por candidato
- Gráficos de distribuição e impacto
""")

uploaded_file = st.file_uploader("📤 Envie o arquivo CSV com os candidatos", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Verifica se as colunas esperadas estão presentes
    expected = ["nome", "titulo_vaga"] + [f"feature_{i}" for i in range(50)]
    if not all(col in df.columns for col in expected):
        st.error("❌ O arquivo não contém as colunas esperadas. Use o arquivo gerado com feature_0 a feature_49.")
        st.stop()

    # Previsão
    X = df[[f"feature_{i}" for i in range(50)]]
    proba = modelo.predict_proba(X)[:, 1]
    df["score"] = proba.round(4)

    # Score por vaga
    st.subheader("📊 Score por Vaga")
    col1, col2 = st.columns([2, 5])
    with col1:
        vaga_sel = st.selectbox("Selecione uma vaga", df["titulo_vaga"].unique())

    df_vaga = df[df["titulo_vaga"] == vaga_sel].sort_values("score", ascending=False)
    fig = px.bar(df_vaga, x="nome", y="score", title=f"Scores - {vaga_sel}")
    st.plotly_chart(fig)

    # Impacto simulado por categoria
    st.subheader("📈 Distribuição dos Scores")
    fig2 = px.histogram(df, x="score", nbins=10, title="Distribuição dos scores dos candidatos")
    st.plotly_chart(fig2)

    st.success("✅ Análise concluída!")
    st.download_button("⬇️ Baixar resultados", data=df.to_csv(index=False), file_name="resultados_mock.csv")