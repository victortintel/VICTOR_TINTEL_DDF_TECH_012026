import re
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer
from sklearn.pipeline import make_pipeline
from sklearn.manifold import TSNE

st.set_page_config(page_title="Olist Product Text Explorer", layout="wide")

DATA_PATH = "app_streamlit/data/stg_product_text_features_free.csv"


# ---------------------------
# Helpers (carregamento/colunas)
# ---------------------------
@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]  # normaliza nomes
    return df


def pick_id_column(df: pd.DataFrame) -> str | None:
    candidates = ["product_id", "PRODUCT_ID", "id", "productId"]
    for c in candidates:
        if c in df.columns:
            return c
    for c in df.columns:
        if re.search(r"id$", c, flags=re.IGNORECASE):
            return c
    return None


def build_text_column(df: pd.DataFrame) -> tuple[pd.DataFrame, str]:
    """
    Cria __text__ juntando colunas textuais relevantes para busca/similaridade.
    """
    preferred = [
        "title", "product_name", "name",
        "description", "product_description",
        "summary",
        "main_topics",
        "pain_points",
        "suggested_improvements",
        "top_keywords",
        "reviews_blob",
        "category", "product_category_name"
    ]
    usable = [c for c in preferred if c in df.columns]

    if not usable:
        id_col = pick_id_column(df)
        obj_cols = [c for c in df.columns if df[c].dtype == "object"]
        if id_col and id_col in obj_cols:
            obj_cols.remove(id_col)
        usable = obj_cols[:8]  # limita fallback

    df2 = df.copy()
    df2["__text__"] = ""
    for c in usable:
        df2["__text__"] += df2[c].fillna("").astype(str) + " "
    df2["__text__"] = df2["__text__"].str.replace(r"\s+", " ", regex=True).str.strip()
    return df2, ", ".join(usable) if usable else "(fallback automático)"


@st.cache_resource
def fit_vectorizer(texts: pd.Series):
    vec = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
    X = vec.fit_transform(texts)
    return vec, X


# ---------------------------
# Mapa 2D (cacheado)
# ---------------------------
@st.cache_data(show_spinner=False)
def compute_2d_projection(texts: list[str], method: str, random_state: int, perplexity: int):
    """
    Retorna coords Nx2.
    method: "tsne" ou "svd"
    """
    tfidf = TfidfVectorizer(min_df=2, max_features=8000, ngram_range=(1, 2))
    X = tfidf.fit_transform(texts)

    # SVD base (sempre) para estabilizar
    n_svd = 50
    if X.shape[1] <= 2:
        n_svd = 2
    else:
        n_svd = min(n_svd, X.shape[1] - 1)

    svd = TruncatedSVD(n_components=n_svd, random_state=random_state)
    normalizer = Normalizer(copy=False)
    X_reduced = make_pipeline(svd, normalizer).fit_transform(X)

    if method == "svd":
        # 2D rápido: SVD direto pra 2 dimensões
        svd2 = TruncatedSVD(n_components=2, random_state=random_state)
        coords = svd2.fit_transform(X)
        return coords

    # t-SNE (mais “humano”)
    n_points = len(texts)
    # segurança: perplexity precisa ser < n_points
    perplexity = int(min(perplexity, max(5, n_points - 1)))

    tsne = TSNE(
        n_components=2,
        perplexity=perplexity,
        learning_rate="auto",
        init="pca",
        random_state=random_state
    )
    coords = tsne.fit_transform(X_reduced)
    return coords


def main():
    st.title("📦 Olist — Data App (Text Features + Similaridade)")

    df = load_data(DATA_PATH)
    id_col = pick_id_column(df)
    df_txt, used_cols = build_text_column(df)

    st.caption(f"Fonte: `{DATA_PATH}` | Linhas: **{len(df_txt)}** | Colunas: **{df_txt.shape[1]}**")
    st.caption(f"Colunas usadas para texto (similaridade): **{used_cols}**")

    tabs = st.tabs([
        "Visão Geral (EDA)",
        "Similaridade entre Produtos",
        "Mapa 2D (tipo tensorboard)",
        "Download"
    ])

    # ------------------ TAB 1: EDA ------------------
    with tabs[0]:
        c1, c2, c3 = st.columns(3)
        c1.metric("Produtos (linhas)", f"{len(df_txt)}")
        c2.metric("Colunas", f"{df_txt.shape[1]}")
        c3.metric("Texto vazio", f"{int((df_txt['__text__'].str.len() == 0).sum())}")

        st.subheader("Amostra do dataset")

        # ✅ Aqui está o motivo do “só 19 linhas”:
        # o st.dataframe tem altura padrão limitada; então você vê poucas linhas “na tela”.
        # Abaixo você controla QUANTAS linhas (head) e a ALTURA do quadro.
        max_show = min(300, len(df_txt))
        n_show = st.slider("Quantas linhas mostrar na amostra?", 20, max_show, 120, step=10)
        table_height = st.slider("Altura da tabela (px)", 300, 1200, 650, step=50)

        st.dataframe(df_txt.head(n_show), use_container_width=True, height=table_height)

        st.subheader("Nulos por coluna (Top 15)")
        nulls = df_txt.isna().sum().sort_values(ascending=False).head(15)
        null_df = pd.DataFrame({"coluna": nulls.index, "nulos": nulls.values})
        fig = px.bar(null_df, x="coluna", y="nulos")
        st.plotly_chart(fig, use_container_width=True)

        # categoria (se existir)
        cat_col = None
        for c in ["category", "product_category_name", "product_category"]:
            if c in df_txt.columns:
                cat_col = c
                break

        if cat_col:
            st.subheader(f"Distribuição por categoria (`{cat_col}`)")
            top = df_txt[cat_col].fillna("UNKNOWN").value_counts().head(20)
            cat_df = pd.DataFrame({cat_col: top.index, "count": top.values})
            fig2 = px.bar(cat_df, x=cat_col, y="count")
            st.plotly_chart(fig2, use_container_width=True)

    # ------------------ TAB 2: Similaridade ------------------
    with tabs[1]:
        st.subheader("🔎 Similaridade por texto (TF-IDF + Cosine Similarity)")

        vec, X = fit_vectorizer(df_txt["__text__"])

        if id_col:
            st.write(f"Coluna de ID detectada: **{id_col}**")
            options = df_txt[id_col].astype(str).tolist()
            selected = st.selectbox("Escolha um product_id:", options, index=0)
            idx = df_txt.index[df_txt[id_col].astype(str) == str(selected)][0]
        else:
            st.warning("Não encontrei uma coluna clara de ID. Vou usar índice da linha.")
            idx = st.number_input("Escolha o índice da linha:", min_value=0, max_value=len(df_txt) - 1, value=0)

        top_k = st.slider("Quantos similares mostrar?", 3, 20, 10)

        sims = cosine_similarity(X[idx], X).flatten()
        best_idx = np.argsort(-sims)[0: top_k + 1]  # inclui o próprio
        best_idx = [i for i in best_idx if i != idx][:top_k]

        st.markdown("### Produto selecionado")
        st.dataframe(df_txt.loc[[idx]].drop(columns=["__text__"]), use_container_width=True)

        st.markdown("### Produtos mais similares")
        out = df_txt.loc[best_idx].copy()
        out["similarity"] = sims[best_idx]

        cols_show = ["similarity"]
        if id_col:
            cols_show += [id_col]
        cols_show += [c for c in out.columns if c not in ["__text__", "similarity", id_col]]

        st.dataframe(
            out[cols_show].sort_values("similarity", ascending=False),
            use_container_width=True,
            height=650
        )

    # ------------------ TAB 3: Mapa 2D ------------------
    with tabs[2]:
        st.subheader("🧭 Mapa 2D de produtos (projeção do texto)")
        st.caption(
            "Objetivo: visualizar agrupamentos por similaridade textual. "
            "Use a amostragem e os filtros para deixar o gráfico legível."
        )

        left, mid, right = st.columns([1, 1, 1])

        with left:
            max_n = min(len(df_txt), 800)
            n_points = st.slider("Quantidade de produtos no mapa", 50, max_n, min(300, max_n), step=50)
            sample_mode = st.selectbox("Amostragem", ["Aleatória (recomendado)", "Primeiros registros (head)"], index=0)

        with mid:
            method = st.selectbox("Método de projeção", ["t-SNE (melhor visual)", "SVD (mais rápido)"], index=0)
            random_state = st.number_input("Seed (reprodutibilidade)", min_value=0, max_value=9999, value=42, step=1)

        with right:
            perplexity = st.slider("Perplexity (t-SNE)", 5, 50, 25, step=1)
            marker_size = st.slider("Tamanho do ponto", 4, 16, 9, step=1)
            marker_opacity = st.slider("Opacidade", 0.3, 1.0, 0.75, step=0.05)

        # define amostra
        if sample_mode.startswith("Aleatória"):
            plot_src = df_txt.sample(n=n_points, random_state=int(random_state)).copy()
        else:
            plot_src = df_txt.head(n_points).copy()

        # id para hover / destaque
        if id_col and id_col in plot_src.columns:
            plot_src["product_id"] = plot_src[id_col].astype(str)
        else:
            plot_src["product_id"] = plot_src.index.astype(str)

        highlight_id = None
        if id_col and id_col in df_txt.columns:
            highlight_id = st.selectbox(
                "Destacar um product_id (opcional)",
                ["(nenhum)"] + plot_src["product_id"].astype(str).tolist(),
                index=0
            )
            if highlight_id == "(nenhum)":
                highlight_id = None

        # categoria (se existir)
        cat_source = None
        for c in ["category", "product_category_name", "product_category"]:
            if c in plot_src.columns:
                cat_source = c
                break
        plot_src["category"] = plot_src[cat_source].fillna("UNKNOWN").astype(str) if cat_source else "ALL"

        # calcula coords
        method_key = "tsne" if method.startswith("t-SNE") else "svd"
        texts = plot_src["__text__"].fillna("").astype(str).tolist()

        with st.spinner("Gerando projeção 2D..."):
            coords = compute_2d_projection(texts, method_key, int(random_state), int(perplexity))

        plot_df = plot_src.copy()
        plot_df["x"] = coords[:, 0]
        plot_df["y"] = coords[:, 1]

        # gráfico
        fig = px.scatter(
            plot_df,
            x="x",
            y="y",
            color="category",
            hover_data={
                "product_id": True,
                "category": True,
                "x": False,
                "y": False,
            },
            render_mode="webgl"
        )

        fig.update_traces(marker=dict(size=marker_size, opacity=marker_opacity))
        fig.update_layout(
            height=680,
            legend_title_text="Categoria",
            xaxis_title=f"Dim 1 ({'t-SNE' if method_key=='tsne' else 'SVD'})",
            yaxis_title=f"Dim 2 ({'t-SNE' if method_key=='tsne' else 'SVD'})",
            margin=dict(l=10, r=10, t=40, b=10)
        )

        # destaque
        if highlight_id:
            hi = plot_df[plot_df["product_id"] == str(highlight_id)]
            if len(hi) > 0:
                fig.add_scatter(
                    x=hi["x"],
                    y=hi["y"],
                    mode="markers",
                    marker=dict(size=marker_size + 8, symbol="x", line=dict(width=2)),
                    name="Destaque"
                )

        st.plotly_chart(fig, use_container_width=True)

        st.info(
            "Dica: se o mapa ainda ficar confuso, reduza para 150–300 pontos, use amostragem aleatória, "
            "aumente a opacidade para ~0.85 e ajuste a perplexity (ex: 15–35)."
        )

    # ------------------ TAB 4: Download ------------------
    with tabs[3]:
        st.subheader("⬇️ Baixar dataset do app")
        st.write("Útil para facilitar o avaliador a baixar a versão final usada no app.")
        csv_bytes = df_txt.drop(columns=["__text__"]).to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download stg_product_text_features_free.csv",
            data=csv_bytes,
            file_name="stg_product_text_features_free.csv",
            mime="text/csv"
        )


if __name__ == "__main__":
    main()
