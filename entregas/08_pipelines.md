# Item 8 — Pipelines (Ingestão via Amazon S3 → Dadosfera)

## Objetivo
Criar uma Pipeline na Dadosfera para ingestão de dados do case (Olist), garantindo que o dataset esteja:
- ingerido com sucesso;
- catalogado automaticamente como Ativo de Dados;
- pronto para uso nos próximos itens (Data App no Item 9 e Modelagem/consumo no Item 6/7/10).

---

## Fonte de dados escolhida
**Sistema fonte:** Amazon S3  
**Fonte cadastrada utilizada:** `Brazilian E-commerce Data Analysis` (case técnico base disponibilizado no ambiente de Treinamentos).

> Observação: a fonte já existia no ambiente como template/exemplo institucional. Para o case, a pipeline criada e o ativo gerado são de minha autoria e estão no meu namespace (`VICTOR_TINTEL_DDF_TECH_012026_*`).

---

## Pipeline criada

**Nome da pipeline:**
`VICTOR_TINTEL_DDF_TECH_012026_olist_order_items_pipeline`

**Descrição (pipeline):**
Pipeline S3 (CSV) para ingestão do dataset `olist_order_items_dataset` (>=100k linhas). Base para análises, modelagem Kimball e Data App.

**Configuração aplicada**
- Tipo de arquivo: CSV  
- Encoding: UTF-8  
- Separador: `,`  
- Cabeçalho: ativo  
- Bucket: `dadosfera-ecommerce-2024`  
- Arquivo: `olist_order_items_dataset.csv`

### Evidências (prints)
- Criação/configuração da pipeline:
  - `assets/prints/item8_pipeline_config.png`
- Pipeline criada e executada com status **Sucesso**:
  - `assets/prints/item8_pipeline_success.png`
- Logs da execução (se aplicável):
  - `assets/prints/item8_pipeline_logs.png`

---

## Ativo de dados gerado no Catálogo

Após a execução, a pipeline gerou automaticamente o ativo:

**Ativo no Catálogo:**
`PUBLIC.VICTOR_TINTEL_DDF_TECH_012026_OLIST_ORDER_ITEMS_PIPELINE`

**Link do ativo no Catálogo (Dadosfera):**
> Cole aqui o link do seu ativo (URL do navegador)  
Ex.: `https://app.dadosfera.ai/pt-BR/catalog/data-assets/<ASSET_ID>`

### Visão geral do ativo (schema + volume)
- Total de colunas: **8**
- Total de linhas: **112650**
- Colunas principais:
  - `ORDER_ID`
  - `ORDER_ITEM_ID`
  - `PRODUCT_ID`
  - `SELLER_ID`
  - `PRICE`
  - `FREIGHT_VALUE`
  - `SHIPPING_LIMIT_DATE`
  - `_PROCESSING_TIMESTAMP`

### Descrição do ativo (catalogação)
O ativo foi documentado com descrição contextualizada para facilitar descoberta e reutilização no case.

### Evidências (prints)
- Página do ativo (informações gerais):
  - `assets/prints/item8_catalog_asset_page.png`
- Estatísticas e colunas (8 colunas / 112650 linhas):
  - `assets/prints/item8_catalog_columns_stats.png`
- Descrição preenchida no catálogo:
  - `assets/prints/item8_catalog_description_filled.png`
- Prévia com amostra de dados:
  - `assets/prints/item8_catalog_preview.png`

---

## Resultado do Item 8
✅ Pipeline criada e executada com sucesso (Amazon S3 → Dadosfera)  
✅ Ativo catalogado automaticamente no Catálogo  
✅ Evidências registradas via prints para rastreabilidade e avaliação  
✅ Dataset pronto para consumo no **Item 9 (Data App em Streamlit)** e análises do case
