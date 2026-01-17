# Item 9 — Data App (Streamlit)

## Objetivo
Construir e publicar um **Data App em Streamlit** para explorar o dataset final do projeto, permitindo:
- Visão geral (EDA) do dataset final
- Exploração de **similaridade entre produtos** com base em features de texto
- Visualização em **mapa 2D** (estilo “tensorboard”)
- Opção de **download** do dataset

---

## Dataset utilizado
**Dataset final:** `stg_product_text_features_free.csv`  
**Local no repositório:** `app_streamlit/data/stg_product_text_features_free.csv`  
**Quantidade:** **500 produtos** (linhas)  
**Colunas:** **13**

Campos de texto usados para similaridade:
- `summary`
- `main_topics`
- `pain_points`
- `suggested_improvements`

---

## App publicado (Streamlit Community Cloud)
✅ **URL do App (entrega principal):**  
https://victortintelddftech012026-etq6rseufiwq7kvxqxpyf2.streamlit.app/

---

## Evidências (prints)
Os prints exigidos foram capturados e adicionados ao repositório:

- **Home / EDA:** `01_home_eda.png`
- **Similaridade:** `02_similarity.png`
- **Mapa 2D:** `03_map_2d.png`
- **Download:** `04_download.png`

📌 Caminho sugerido no repositório (onde os prints foram organizados):
`assets/prints/item_09_streamlit/`

---

## O que foi entregue
- Data App em Streamlit com interface completa
- Carregamento do dataset final (500 produtos)
- Abas de análise:
  - **Visão Geral (EDA)**
  - **Similaridade entre Produtos**
  - **Mapa 2D (tipo tensorboard)**
  - **Download do dataset**
- Publicação no Streamlit Community Cloud
- Prints salvos como evidência da entrega

---

## Como reproduzir localmente (opcional)
1. Instalar dependências (exemplo):
   ```bash
   pip install -r app_streamlit/requirements.txt
