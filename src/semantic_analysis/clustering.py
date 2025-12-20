# src/semantic_analysis/clustering.py

import numpy as np
from sklearn.cluster import KMeans
from pathlib import Path
import csv

def cluster_embeddings(model, vocab_size=2000, n_clusters=8):
    words = list(model.wv.index_to_key[:vocab_size])
    vectors = np.array([model.wv[w] for w in words])

    kmeans = KMeans(
        n_clusters=n_clusters,
        random_state=42,
        n_init=10
    )

    labels = kmeans.fit_predict(vectors)

    clusters = {}
    for w, lab in zip(words, labels):
        clusters.setdefault(lab, []).append(w)

    return clusters

def save_clusters(clusters: dict, out_csv: str, max_words=30):
    rows = []
    for cid, words in clusters.items():
        rows.append({
            "cluster_id": cid,
            "keywords": ", ".join(words[:max_words])
        })

    Path(out_csv).parent.mkdir(parents=True, exist_ok=True)
    with open(out_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["cluster_id", "keywords"])
        writer.writeheader()
        writer.writerows(rows)
