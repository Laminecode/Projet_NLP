# src/sentiment_analysis/run_sentiment.py
from pathlib import Path
import csv

from load_data import load_corpus_texts
from victim_sentiment import extract_victim_sentiment
from actor_sentiment import extract_actor_sentiment

OUT = "results/sentiment"

def save_csv(rows, out_file):
    Path(out_file).parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

def run_sentiment(data_base):
    corpora = load_corpus_texts(data_base)

    for cat, docs in corpora.items():
        if not docs:
            continue

        victim_rows = extract_victim_sentiment(docs)
        save_csv(victim_rows, f"{OUT}/{cat}_victims_sentiment.csv")

        actor_rows = extract_actor_sentiment(docs)
        save_csv(actor_rows, f"{OUT}/{cat}_actor_sentiment.csv")

        print(f"[OK] Sentiment done for {cat}")

if __name__ == "__main__":
    run_sentiment("data/processed_clean")
    from figures import (
        plot_actor_boxplot,
        plot_victim_histogram,
        plot_victim_mean,
        plot_sentiment_heatmap,
        plot_gaza_vs_ukraine_mean,
    )
    plot_actor_boxplot("results/sentiment/gaza_actor_sentiment.csv")
    plot_victim_histogram("results/sentiment/gaza_victims_sentiment.csv")
    plot_victim_mean("results/sentiment/gaza_victims_sentiment.csv")

    plot_sentiment_heatmap(
    "results/sentiment/gaza_actor_sentiment.csv",
    "Mean sentiment per actor (Gaza)",
    "results/figures_sentiment/gaza_actor_sentiment_heatmap.png"
    )

    plot_sentiment_heatmap(
    "results/sentiment/ukraine_actor_sentiment.csv",
    "Mean sentiment per actor (Ukraine)",
    "results/figures_sentiment/ukraine_actor_sentiment_heatmap.png"
    )

    plot_gaza_vs_ukraine_mean("results/sentiment/gaza_victims_sentiment.csv",
                              "results/sentiment/ukraine_victims_sentiment.csv")


    print("[OK] Sentiment figures generated.")
