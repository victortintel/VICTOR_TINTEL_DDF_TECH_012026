# Item 3 — Dadosfera: Explorar (Catálogo + Data Lake Zones)

## 3.1 Objetivo
Catalogar os datasets importados na Dadosfera e organizá-los seguindo boas práticas de Data Lake (camadas raw → staging → curated), com documentação e governança básica (descrição, tags, sensibilidade e uso).

## 3.2 Camadas do Data Lake (proposta)
- **Raw / Landing (já implementado):** `raw_olist_*`  
  Dados importados como recebidos (sem transformações).
- **Staging (a ser gerado nos itens 4/5):** `stg_olist_*`  
  Padronização de tipos, tratamento de nulos, deduplicação e regras de qualidade.
- **Curated (a ser gerado nos itens 6/7):** `cur_olist_*`  
  Dados prontos para consumo (BI/ML), incluindo modelagem dimensional e features extraídas de texto.

## 3.3 Datasets catalogados (Raw)
- raw_olist_orders — LINK_AQUI  
- raw_olist_order_items — LINK_AQUI  
- raw_olist_products — LINK_AQUI  
- raw_olist_customers — LINK_AQUI  
- raw_olist_reviews — LINK_AQUI  
- raw_olist_payments — LINK_AQUI  
- raw_olist_sellers — LINK_AQUI  
- raw_olist_category_translation — LINK_AQUI  

## 3.4 Evidências (prints)
**Lista de assets raw no catálogo**
![Catálogo raw](../assets/prints/ITEM3_catalog_raw_list.png)

**Exemplo de catalogação: order_items (principal)**
![Order items details](../assets/prints/ITEM3_catalog_order_items_details.png)

**Exemplo de catalogação: reviews (desestruturado)**
![Reviews details](../assets/prints/ITEM3_catalog_reviews_details.png)
