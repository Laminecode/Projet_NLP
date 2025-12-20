# src/semantic_analysis/run_semantic.py

import os
from pathlib import Path
import argparse

from src.semantic_analysis.load_data import load_corpus_texts
from src.semantic_analysis.concordance import extract_concordances, save_concordances
from src.semantic_analysis.word2vec import train_word2vec, save_actor_neighbors
from src.semantic_analysis.clustering import cluster_embeddings, save_clusters

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

    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run semantic analysis")
    parser.add_argument(
        "--data",
        default="data/processed_clean",
        help="Base directory of cleaned corpora"
    )
    args = parser.parse_args()
    run_semantic(args.data)
