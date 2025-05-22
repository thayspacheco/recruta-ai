# 🤖 Recruta.AI – Triagem Inteligente com IA

Este projeto foi desenvolvido para o Datathon de Data Analytics com o objetivo de aplicar técnicas de Inteligência Artificial no processo de recrutamento e seleção da empresa Decision.

---

## 🎯 Objetivo

Desenvolver um MVP com IA capaz de:

- Automatizar a triagem de candidatos
- Avaliar categorias como Hard Skills, Soft Skills, Idiomas, Formação e Experiência
- Gerar scores por candidato e gráficos interativos por vaga

---

## 🧠 Visão Geral da Solução

O projeto inclui:

- **Modelo de Machine Learning (Random Forest)** treinado com dados simulados
- **App Streamlit** interativo com visualização por vaga e categoria
- **Pipeline de pré-processamento com TF-IDF e One-Hot Encoding**
- Arquivo `.csv` de composição pronto para gerar os gráficos mesmo sem rodar o modelo

---

## 🚀 Executando o Projeto

### 🔗 Versão online no Streamlit Cloud

> [Clique aqui para acessar a aplicação](https://recruta-ai-app.streamlit.app/)
> *(Substituir com o link do seu deploy)*

Faça o upload do arquivo [`composicao_mock_simulada.csv`](./composicao_mock_simulada.csv) para visualizar os gráficos gerados com base nos dados reais exportados da versão local.

---

### 🖥️ Versão local (com modelo real)

1. Clone este repositório:
```bash
git clone https://github.com/thayspacheco/recruta-ai.git
cd recruta-ai
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute a versão completa:
```bash
streamlit run app_local_completo.py
```

> Requer os arquivos:
> - `modelo.pkl`
> - `colunas_X.pkl`
> - `tfidf_dict.pkl`

---

## 🔀 Versões da Aplicação

| Arquivo                 | Finalidade                                                                 |
|-------------------------|----------------------------------------------------------------------------|
| `app.py`                | Versão mockada para rodar no **Streamlit Cloud**. Utiliza dados simulados para fins de apresentação visual. |
| `app_local_completo.py` | Versão completa com o **modelo real** treinado localmente. Recomendado para rodar com `streamlit run` localmente. |

---

## 🧠 Observação Importante

> Devido a limitações de compatibilidade com o ambiente do Streamlit Cloud (atualmente rodando Python 3.13), a versão publicada online utiliza um modelo simulado e dados adaptados apenas para visualização.
> A versão local representa fielmente o funcionamento real da aplicação, com modelo de machine learning treinado com dados históricos e geração de score real por categoria.

---

## 📁 Arquivos importantes

- `candidatos_local.csv` → base original dos candidatos para rodar localmente (vscode)
- `candidatos_streamlit.csv` → base convertida para rodar no streamlit
- `app_local_completo.py` → app completo com modelo real
- `app.py` → app mock usado no deploy online
- `README.md` → este arquivo :)

---

##  Autores

Marcelo Rodrigues - RM 357580

Ricardo da Silva - RM 357196

Thays Pacheco - RM 357535

Vitor Henrique da Silva Matos - RM 357474

Wesley Bonpam dos Santos - RM 357542


---
