# src/semantic_analysis/run_semantic.py

import os
from pathlib import Path
import argparse

<<<<<<< HEAD
from load_data import load_corpus_texts
from concordance import extract_concordances, save_concordances
from word2vec import train_word2vec, save_actor_neighbors
from clustering import cluster_embeddings, save_clusters
from figures import (
    plot_concordance_context,
    plot_word2vec_neighbors,
    plot_clusters_text
)
=======
from src.semantic_analysis.load_data import load_corpus_texts
from src.semantic_analysis.concordance import extract_concordances, save_concordances
from src.semantic_analysis.word2vec import train_word2vec, save_actor_neighbors
from src.semantic_analysis.clustering import cluster_embeddings, save_clusters

>>>>>>> 283e0ecaa66c0c3ca393ef130dc4269f200638d7
RESULTS_DIR = "results/semantic"

def ensure_dirs():
    Path(RESULTS_DIR).mkdir(parents=True, exist_ok=True)

def run_semantic(data_base: str):
    ensure_dirs()

    corpora = load_corpus_texts(data_base)

    # -------- Keywords for concordance ----------
    keywords = ["attack", "strike", "civilian", "resistance", "occupation"]

    for kw in keywords:
        for cat, docs in corpora.items():
            rows = extract_concordances(
                docs,
                keyword=kw,
                window=6,
                max_lines=200
            )
            save_concordances(
                rows,
                f"{RESULTS_DIR}/{cat}_concordance_{kw}.csv"
            )
# -------- Word2Vec & Clustering ----------
    print("[Semantic] Word2Vec & Clustering...")

    actors_terms = ["israel","palestine","hamas","russia","ukraine","putin","idf"]
    print(corpora.keys())
    for cat, docs in corpora.items():
        if not docs:
            continue

        model = train_word2vec(docs)

        save_actor_neighbors(
            model,
            actors_terms,
            f"{RESULTS_DIR}/{cat}_word2vec_neighbors.csv"
        )

        clusters = cluster_embeddings(model, n_clusters=8)
        save_clusters(
            clusters,
            f"{RESULTS_DIR}/{cat}_semantic_clusters.csv"
        )

    # -------- Generate figures --------
    RESULTS_DIR2 = "results/figures_semantic"
    print("[Semantic] Generating figures...")

    for kw in ["attack", "civilian"]:
        for cat in corpora:
            rows = extract_concordances(corpora[cat], kw)
            plot_concordance_context(
                rows,
                kw,
                f"{RESULTS_DIR2}/{cat}_concordance_{kw}.png"
            )

    for cat in corpora:
        plot_word2vec_neighbors(
            f"{RESULTS_DIR}/{cat}_word2vec_neighbors.csv",
            "israel",
            f"{RESULTS_DIR2}/{cat}_word2vec_israel.png"
        )

        plot_clusters_text(
            f"{RESULTS_DIR}/{cat}_semantic_clusters.csv",
            f"{RESULTS_DIR2}/{cat}_clusters.png"
        )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run semantic analysis")
    parser.add_argument(
        "--data",
        default="data/processed_clean",
        help="Base directory of cleaned corpora"
    )
    args = parser.parse_args()
    run_semantic(args.data)
