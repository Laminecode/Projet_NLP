import matplotlib.pyplot as plt
from collections import Counter
from pathlib import Path
import csv


def plot_concordance_context(rows, keyword, out_png, topk=15):
    """
    rows: output of extract_concordances
    """
    words = []
    for r in rows:
        words.extend(r["left"].split())
        words.extend(r["right"].split())

    counter = Counter(words)
    most = counter.most_common(topk)

    if not most:
        return

    labels, counts = zip(*most)

    plt.figure(figsize=(10,5))
    plt.bar(labels, counts)
    plt.xticks(rotation=45, ha="right")
    plt.title(f"Context words around '{keyword}'")
    plt.tight_layout()

    Path(out_png).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_png)
    plt.close()

def plot_word2vec_neighbors(csv_file, actor, out_png, topk=10):
    import csv

    words, scores = [], []

    with open(csv_file, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["actor"] == actor:
                words.append(row["neighbor"])
                scores.append(float(row["similarity"]))

    if not words:
        return

    plt.figure(figsize=(10,5))
    plt.bar(words[:topk], scores[:topk])
    plt.xticks(rotation=45, ha="right")
    plt.title(f"Word2Vec neighbors of '{actor}'")
    plt.tight_layout()

    Path(out_png).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_png)
    plt.close()



def plot_clusters_text(csv_file, out_png, max_words=12):
    clusters = []

    with open(csv_file, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            clusters.append((
                row["cluster_id"],
                row["keywords"].split(", ")[:max_words]
            ))

    if not clusters:
        print(f"[WARN] No clusters found in {csv_file}")
        return

    fig, ax = plt.subplots(figsize=(14, 2 + len(clusters)))

    ax.set_xlim(0, 1)
    ax.set_ylim(0, len(clusters) + 1)
    ax.axis("off")

    for i, (cid, words) in enumerate(clusters):
        text = f"Cluster {cid}: " + ", ".join(words)
        ax.text(
            0.01,
            len(clusters) - i,
            text,
            fontsize=11,
            verticalalignment="top"
        )

    ax.set_title("Semantic Clusters (Word2Vec + KMeans)", fontsize=14)

    Path(out_png).parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(out_png, dpi=150)
    plt.close()

    print(f"[OK] Saved clusters figure → {out_png}")

