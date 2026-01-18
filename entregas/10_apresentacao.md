# Item 10 — Apresentação do Case  
## Dadosfera: o caminho mais rápido entre dados e valor (PoC Olist)

### Objetivo
Entregar uma **prova de conceito** de que a Dadosfera é uma alternativa viável (e mais rápida para gerar valor) frente à arquitetura atual baseada em AWS (Generator → Kinesis Stream → Firehose → S3 + Redis), suportando:
- Criação e governança de ativos de dados (catálogo, qualidade, rastreabilidade)
- Base pronta para **analytics** e **modelos de IA** para melhorar a experiência de compra
- Entrega de um **Data App** para exploração dos dados e geração de insights

---

## Entregáveis do Item 10
1) **Apresentação (10 slides)** cobrindo os itens anteriores e defendendo a viabilidade da Dadosfera.  
2) Roteiro + evidências (prints e links) para comprovar execução e ativos.  
3) **Vídeo da apresentação (YouTube - Unlisted)** com link referenciado neste markdown.

---

## Vídeo da apresentação (YouTube)
Link do vídeo (garantir como **Unlisted** e acessível para qualquer pessoa com o link):

https://www.youtube.com/watch?v=8AAQx7k5NEU

---

## Link do Data App (Streamlit)
Aplicação publicada no Streamlit Community Cloud:

https://victortintelddftech012026-etq6rseufiwq7kvxqxpyf2.streamlit.app/

Dataset final usado no App:
- `stg_product_text_features_free.csv` (500 produtos / 13 colunas)

Prints principais do App (conforme solicitado no Item 9):
- `assets/prints/01_home_eda.png`
- `assets/prints/02_similarity.png`
- `assets/prints/03_map_2d.png`
- `assets/prints/04_download.png`

---

## Evidências da plataforma (Dadosfera)
Ativos gerados e catalogados na Dadosfera após execução do pipeline:
- Ativo (tabela) no Catálogo: `PUBLIC.VICTOR_TINTEL_DDF_TECH_012026_OLIST_ORDER_ITEMS_PIPELINE`
- Execução do pipeline com **Status: Sucesso**
- Prévia do ativo (linhas/colunas) acessível pelo catálogo

(prints do Item 8 já adicionados na pasta `assets/prints/` conforme checklist do case)

---

## Como esta PoC substitui (parcial ou totalmente) a arquitetura atual (AWS)
### Arquitetura atual (referência)
Generator → Kinesis Stream → Firehose → S3 Bucket + Redis Cluster

### Proposta com Dadosfera (PoC)
- **Entrada de dados via S3** (fonte) e ingestão via pipeline (CSV)  
- **Catálogo de dados** como camada central de descoberta, rastreio e acesso
- **Modelagem (Kimball)** para consumo analítico consistente (fatos/dimensões)
- **Qualidade / validações** e evidências via execução e ativos catalogados
- **Camada de consumo** via Data App (Streamlit) + análises (EDA / Similaridade / Mapa 2D)

**Substituição parcial:** Dadosfera pode assumir ingestão + catálogo + camada analítica, mantendo componentes de streaming onde fizer sentido.  
**Substituição total (dependendo do cenário):** quando o objetivo é analytics/IA e velocidade de entrega, centralizando ingestão, governança e consumo.

---

## Por que Dadosfera é tecnicamente mais viável e/ou mais barata na prática (PoC)
- Menos componentes para operar (redução de complexidade)
- Menos pontos de falha e menor esforço de manutenção
- Centralização de ativos e governança no Catálogo
- Time-to-value menor: ingestão → ativo → análise → app

---

## Oportunidades e ganhos futuros
- Evoluir para ingestões adicionais (orders, payments, reviews etc.)
- Consolidar camada dimensional (Kimball) como base corporativa
- Implementar modelos de IA (similaridade, recomendação, qualidade de texto, clusters)
- Criar produtos de dados (dashboards, apps, APIs internas)
- Ampliar trilhas de qualidade, testes e linhagem conforme maturidade

---

## Apresentação (slides)
A apresentação do Item 10 está em:
- `entregas/Item10_Apresentacao_Dadosfera_PoC_Olist.pptx`

Estrutura:
1. Capa  
2. Contexto e objetivo  
3. Problema principal  
4. Ativos criados (itens anteriores)  
5. Pipeline + Catálogo (Dadosfera)  
6. Modelagem Kimball  
7. Principais análises  
8. Data App (Streamlit) + prints + link  
9. Substituição da arquitetura AWS (diagrama)  
10. Roadmap e próximos passos  
