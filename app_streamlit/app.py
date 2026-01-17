import re
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD

st.set_page_config(page_title="Olist Product Text Explorer", layout="wide")

DATA_PATH = "app_streamlit/data/stg_product_text_features_free.csv"


@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # normaliza nomes das colunas (evita erros por diferença de caixa/espaço)
    df.columns = [c.strip() for c in df.columns]
    return df


def pick_id_column(df: pd.DataFrame) -> str | None:
    candidates = ["product_id", "PRODUCT_ID", "id", "productId"]
    for c in candidates:
        if c in df.columns:
            return c
    # fallback: tenta achar algo que pareça id
    for c in df.columns:
        if re.search(r"id$", c, flags=re.IGNORECASE):
            return c
    return None


def build_text_column(df: pd.DataFrame) -> tuple[pd.DataFrame, str]:
    """
    Cria uma coluna __text__ juntando as melhores colunas textuais disponíveis.
    Não depende de nomes exatos: tenta achar colunas comuns e faz fallback.
    """
    preferred = [
        "title", "product_name", "name",
        "description", "product_description",
        "summary",
        "main_topics",
        "pain_points",
        "suggested_improvements",
        "category", "product_category_name"
    ]
    usable = [c for c in preferred if c in df.columns]

    if not usable:
        # fallback: usa todas as colunas string/object exceto ids
        id_col = pick_id_column(df)
        obj_cols = [c for c in df.columns if df[c].dtype == "object"]
        if id_col and id_col in obj_cols:
            obj_cols.remove(id_col)
        usable = obj_cols[:8]  # limita pra não ficar enorme

    df2 = df.copy()
    df2["__text__"] = ""
    for c in usable:
        df2["__text__"] += df2[c].fillna("").astype(str) + " "
    df2["__text__"] = df2["__text__"].str.replace(r"\s+", " ", regex=True).str.strip()

    return df2, ", ".join(usable) if usable else "(fallback automático)"


@st.cache_resource
def fit_vectorizer(texts: pd.Series):
    vec = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),
        stop_words=None
    )
    X = vec.fit_transform(texts)
    return vec, X


def main():
    st.title("📦 Olist — Data App (Text Features + Similaridade)")

    df = load_data(DATA_PATH)
    id_col = pick_id_column(df)

    df_txt, used_cols = build_text_column(df)
    st.caption(f"Fonte: `{DATA_PATH}` | Linhas: **{len(df_txt)}** | Colunas: **{df_txt.shape[1]}**")
    st.caption(f"Colunas usadas para texto (similaridade): **{used_cols}**")

    tabs = st.tabs(["Visão Geral (EDA)", "Similaridade entre Produtos", "Mapa 2D (tipo tensorboard)", "Download"])

    # ------------------ TAB 1: EDA ------------------
    with tabs[0]:
        c1, c2, c3 = st.columns(3)
        c1.metric("Produtos (linhas)", f"{len(df_txt)}")
        c2.metric("Colunas", f"{df_txt.shape[1]}")
        c3.metric("Texto vazio", f"{int((df_txt['__text__'].str.len() == 0).sum())}")

        st.subheader("Amostra do dataset")
        st.dataframe(df_txt.head(20), use_container_width=True)

        st.subheader("Nulos por coluna (Top 15)")
        nulls = df_txt.isna().sum().sort_values(ascending=False).head(15)
        null_df = pd.DataFrame({"coluna": nulls.index, "nulos": nulls.values})
        fig = px.bar(null_df, x="coluna", y="nulos")
        st.plotly_chart(fig, use_container_width=True)

        # Se tiver coluna de categoria, mostra distribuição
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
            selected = st.selectbox("Escolha um product_id:", options)
            idx = df_txt.index[df_txt[id_col].astype(str) == str(selected)][0]
        else:
            st.warning("Não encontrei uma coluna clara de ID. Vou usar índice da linha.")
            idx = st.number_input("Escolha o índice da linha:", min_value=0, max_value=len(df_txt)-1, value=0)

        top_k = st.slider("Quantos similares mostrar?", 3, 20, 10)

        sims = cosine_similarity(X[idx], X).flatten()
        best_idx = np.argsort(-sims)[0: top_k + 1]  # inclui o próprio
        best_idx = [i for i in best_idx if i != idx][:top_k]

        st.markdown("### Produto selecionado")
        st.dataframe(df_txt.loc[[idx]].drop(columns=["__text__"]), use_container_width=True)

        st.markdown("### Produtos mais similares")
        out = df_txt.loc[best_idx].copy()
        out["similarity"] = sims[best_idx]
        # organiza colunas para visualizar melhor
        cols_show = ["similarity"] + ([id_col] if id_col else []) + [c for c in out.columns if c not in ["__text__", "similarity", id_col]]
        st.dataframe(out[cols_show].sort_values("similarity", ascending=False), use_container_width=True)

    # ------------------ TAB 3: Mapa 2D (tipo tensorboard) ------------------
    with tabs[2]:
        st.subheader("🧭 Mapa 2D de produtos (projeção do texto)")
        st.write("Isto é um 'similar ao tensorboard projector': reduzimos o texto para 2 dimensões e plotamos.")

        vec, X = fit_vectorizer(df_txt["__text__"])
        svd = TruncatedSVD(n_components=2, random_state=42)
        coords = svd.fit_transform(X)

        plot_df = pd.DataFrame({"x": coords[:, 0], "y": coords[:, 1]})
        if id_col:
            plot_df["product_id"] = df_txt[id_col].astype(str)
        # tenta adicionar categoria se existir
        for c in ["category", "product_category_name", "product_category"]:
            if c in df_txt.columns:
                plot_df["category"] = df_txt[c].fillna("UNKNOWN").astype(str)
                break

        fig = px.scatter(
            plot_df,
            x="x", y="y",
            color="category" if "category" in plot_df.columns else None,
            hover_data=["product_id"] if "product_id" in plot_df.columns else None
        )
        st.plotly_chart(fig, use_container_width=True)

    # ------------------ TAB 4: Download ------------------
    with tabs[3]:
        st.subheader("⬇️ Baixar dataset do app")
        st.write("Útil para facilitar o avaliador a baixar a versão final.")
        csv_bytes = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download stg_product_text_features_free.csv",
            data=csv_bytes,
            file_name="stg_product_text_features_free.csv",
            mime="text/csv"
        )


if __name__ == "__main__":
    main()
