# Item 0 — Agilidade e Planejamento (PMBOK)

## 0.1 Objetivo
Planejar e representar todas as etapas do projeto (da concepção à implementação), com boas práticas de PMBOK, incluindo dependências, riscos, custos e pontos críticos.

---

## 0.2 Escopo (alto nível)
**Entrega do case (end-to-end):**
- Ingestão e integração de dados (>= 100k registros)
- Catalogação e organização em camadas (Data Lake)
- Data Quality (relatório automatizado)
- Processamento de texto com GenAI/LLM (features estruturadas)
- Modelagem dimensional (Kimball) com 2 visões finais
- Dashboards (categorias + série temporal + 5 visualizações)
- Pipeline automatizado (ETL)
- Data App em Streamlit (deploy)
- Apresentação final (vídeo) propondo substituição parcial/total da arquitetura atual

**Fora do escopo (para este case):**
- Operação 24/7, SLAs formais, e monitoramento corporativo completo
- Custos reais com contrato enterprise (aqui são estimativas)

---

## 0.3 Artefato de Planejamento (Fluxo + Dependências)

```mermaid
flowchart TD;
A[Item 1: Definir Base + Volume 100k+] --> B[Item 2.1: Integrar na Dadosfera];
B --> C[Item 3: Explorar / Catalogar / Camadas];
C --> D[Item 4: Data Quality (Relatorio)];
D --> E[Item 5: GenAI/LLM (Texto -> Features)];
E --> F[Item 6: Modelagem (Kimball + 2 visoes)];
F --> G[Item 7: Dashboards + Queries + 5 visuais];
G --> H[Item 8: Pipelines (ETL)];
H --> I[Item 9: Data App Streamlit + Deploy];
I --> J[Item 10: Apresentacao (Video + Arquitetura)];
```

---

## 0.4 Kanban (visão de execução)

| To Do | Doing | Done |
|------|-------|------|
| Integrar dados |  | Estrutura do repositório |
| Catalogar ativos |  |  |
| Data Quality |  |  |
| Features com LLM |  |  |
| Modelagem Kimball |  |  |
| Dashboards |  |  |
| Pipelines |  |  |
| Streamlit App |  |  |
| Vídeo final |  |  |

---

## 0.5 Análise de Riscos (PMBOK)

| Risco | Prob. | Impacto | Mitigação | Evidência |
|------|------|---------|----------|----------|
| Não atingir 100k registros | Média | Alto | Gerar transações sintéticas (order_items 500k) | Print da contagem na Dadosfera |
| Dados inconsistentes (nulos, datas inválidas) | Alta | Alto | Great Expectations com suites por tabela | Relatório + prints |
| LLM gerar JSON inválido | Média | Médio | Validar com schema + fallback (regex/heurística) | Amostra validada |
| Tempo curto para dashboards/app | Média | Alto | Priorizar MVP: 5 visuais + app de similaridade | Dashboard + app publicado |
| Custos / limitações de ambiente | Baixa | Médio | Usar Colab + Streamlit Community Cloud | Links e reprodutibilidade |

---

## 0.6 Estimativa de Custos (alto nível)

| Componente | Opção | Custo estimado |
|----------|-------|----------------|
| Desenvolvimento Python/LLM | Google Colab | 0 |
| Data App | Streamlit Community Cloud | 0 |
| Plataforma de Dados | Dadosfera (ambiente de treino) | fornecido |
| Repositório | GitHub | 0 |

---

## 0.7 Recursos e papéis

- **Você (Data Specialist):** ingestão, modelagem, qualidade, BI, app, apresentação
- **Dadosfera:** plataforma (catálogo, visualização, pipelines, IAM)
