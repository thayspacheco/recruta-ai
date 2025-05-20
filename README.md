# 🤖 Recrut.AI – Triagem Inteligente com IA para Recrutamento

Este é o projeto desenvolvido para o **Datathon de Data Analytics** com o desafio de aplicar **Inteligência Artificial** aos processos de recrutamento da empresa **Decision**, especializada em serviços de bodyshop no setor de TI.

---

## 🎯 Objetivo

Desenvolver uma solução com IA que otimize o processo de seleção, melhorando o **match entre candidatos e vagas** de forma ágil, escalável e baseada em dados concretos. O projeto foca em responder três perguntas principais:

- Este candidato tem o perfil técnico ideal para a vaga?
- Ele se encaixa na cultura e no tipo de empresa contratante?
- Demonstra engajamento e motivação para a posição?

---

## 🧠 Visão Geral da Solução

A solução foi dividida em duas partes principais:

1. **Notebook analítico** (`/notebooks/DATATHON_DecisionFinal.ipynb`): análise exploratória, tratamento de dados, feature engineering e treinamento do modelo com Random Forest.
2. **Aplicação web** (`app.py`): interface interativa construída em Streamlit que permite:
   - Upload de arquivo CSV com candidatos
   - Geração do score por candidato/vaga com base em 5 categorias
   - Visualizações gráficas da composição dos scores
   - Download dos resultados

---

## 🔍 Principais Categorias Avaliadas

O modelo analisa os candidatos com base em:

- **Hard Skills**: competências técnicas (linguagens, ferramentas, etc.)
- **Soft Skills**: habilidades comportamentais e objetivos profissionais
- **Idiomas**: nível de inglês e espanhol
- **Formação**: nível acadêmico
- **Experiência**: áreas de atuação, cargos anteriores, tipo de contratação

---

## 🚀 Como Rodar Localmente

### Pré-requisitos
- Python 3.8+
- Streamlit

### Passos
1. Clone o repositório:
   ```bash
   git clone https://github.com/thayspacheco/recruta-ai.git
   cd recruta-ai
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute a aplicação:
   ```bash
   streamlit run app.py
   ```

---

## 📁 Bases de Teste

Uma base mock de candidatos está disponível em `/data/candidatos_mock_limpo.csv` para testes com a aplicação.

### 📌 Estrutura esperada do CSV:
A base deve conter as seguintes colunas:

- `nome`, `titulo_vaga`, `objetivo_profissional`, `conhecimentos_tecnicos`,
- `principais_atividades`, `competencia_tecnicas_e_comportamentais`,
- `habilidades_comportamentais_necessarias`, `area_atuacao`, `nivel_academico_x`,
- `nivel_ingles_x`, `nivel_espanhol_x`, `titulo_profissional`, `cliente_y`,
- `tipo_contratacao`, `areas_atuacao`

---

## 📁 Outras bases utilizadas (versões reduzidas)

Foram incluídas versões "light" das bases originais para viabilizar a execução no GitHub:

- `data/applicants_light.json`
- `data/prospects_light.json`
- `data/vagas_light.json`

Esses arquivos são anonimizados, reduzidos e compatíveis com o notebook analítico.

---

## 📊 Tecnologias Utilizadas

- Python
- Streamlit
- Pandas, Plotly, Seaborn
- Scikit-learn
- Joblib
- TF-IDF (Scikit-learn)

---

## 🌐 Links Importantes

- 🔗 [Aplicação online no Streamlit](https://NOME_DA_APLICACAO.streamlit.app) *(atualizar com seu link)*
- 💻 [Notebook completo de análise](notebooks/DATATHON_DecisionFinal.ipynb)
- 📁 [Base de dados de exemplo](data/)

---

## 🙋‍♀️ Autora

**Thays Pacheco**  
Especialista em FP&A, apaixonada por IA aplicada a problemas reais.  
[LinkedIn](https://www.linkedin.com/in/thayspacheco)

---

## 🏁 Resultados Esperados

Com a Recrut.AI, a Decision pode:
- Reduzir o tempo de triagem
- Aumentar a qualidade dos candidatos selecionados
- Ter uma visão clara dos critérios que mais impactam em cada vaga
- Padronizar o processo com base em dados históricos e IA