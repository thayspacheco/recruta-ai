## 🔀 Versões da Aplicação

Este projeto contém duas versões do arquivo principal `app.py`, com finalidades distintas:

| Arquivo                 | Finalidade                                                                 |
|-------------------------|----------------------------------------------------------------------------|
| `app.py`                | Versão mockada para rodar no **Streamlit Cloud**. Utiliza dados simulados para fins de apresentação visual. |
| `app_local_completo.py` | Versão completa com o **modelo real** treinado localmente. Recomendado para rodar com `streamlit run` localmente. |

### 🧠 Observação

> Devido a limitações de compatibilidade com o ambiente do Streamlit Cloud (atualmente rodando Python 3.13), a versão publicada online utiliza um modelo simulado e dados adaptados apenas para visualização.
> A versão local (`app_local_completo.py`) representa fielmente o funcionamento real da aplicação, com modelo de machine learning treinado com dados reais e geração de score por categoria.

### 📦 Rodando localmente

Para executar a versão completa no seu computador:

```bash
streamlit run app_local_completo.py
```

Certifique-se de ter o modelo salvo como `modelo.pkl` e os arquivos `.pkl` auxiliares na mesma pasta.