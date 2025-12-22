import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------ PATHS ------------------
STATS_DIR = "results/statistics"
FIGS_DIR = "results/figures"

os.makedirs(FIGS_DIR, exist_ok=True)

sns.set(style="whitegrid")

# ------------------ HELPERS ------------------
def barplot(df, x, y, title, filename, top_n=20, rotate=False):
    df = df.head(top_n)

    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x=x, y=y)
    plt.title(title)

    if rotate:
        plt.xticks(rotation=45, ha="right")

    plt.tight_layout()
    plt.savefig(os.path.join(FIGS_DIR, filename), dpi=200)
    plt.close()


# ------------------ FIGURES ------------------
def plot_word_frequencies():
    print("[INFO] Plotting word frequencies...")

    for corpus in ["gaza", "ukraine"]:
        path = os.path.join(STATS_DIR, f"{corpus}_wordfreq.csv")
        if not os.path.exists(path):
            continue

        df = pd.read_csv(path)
        barplot(
            df,
            x="count",
            y="term",
            title=f"Top 20 Most Frequent Words – {corpus.capitalize()}",
            filename=f"{corpus}_top_words.png"
        )


def plot_tfidf():
    print("[INFO] Plotting TF-IDF...")

    for corpus in ["gaza", "ukraine"]:
        path = os.path.join(STATS_DIR, f"tfidf_{corpus}.csv")
        if not os.path.exists(path):
            continue

        df = pd.read_csv(path)
        barplot(
            df,
            x="score",
            y="term",
            title=f"Top TF-IDF Terms – {corpus.capitalize()}",
            filename=f"{corpus}_tfidf.png"
        )


def plot_logodds():
    print("[INFO] Plotting log-odds comparison...")

    path = os.path.join(STATS_DIR, "gaza_vs_ukraine_logodds_top200.csv")
    if not os.path.exists(path):
        return

    df = pd.read_csv(path)

    # Gaza-biased terms
    top_gaza = df.head(15)
    barplot(
        top_gaza,
        x="z",
        y="term",
        title="Terms Overused in Gaza Coverage",
        filename="logodds_gaza.png"
    )

    # Ukraine-biased terms
    top_ukraine = df.tail(15).sort_values("z", ascending=False)
    barplot(
        top_ukraine,
        x="z",
        y="term",
        title="Terms Overused in Ukraine Coverage",
        filename="logodds_ukraine.png"
    )


def plot_actor_context(actor):
    print(f"[INFO] Plotting actor context: {actor}")

    for corpus in ["gaza", "ukraine"]:
        path = os.path.join(
            STATS_DIR, f"{corpus}_actor_{actor}_context.csv"
        )
        if not os.path.exists(path):
            continue

        df = pd.read_csv(path)
        barplot(
            df,
            x="count",
            y="term",
            title=f"Lexical Context around '{actor}' – {corpus.capitalize()}",
            filename=f"{corpus}_{actor}_context.png"
        )


# ------------------ MAIN ------------------
def main():
    plot_word_frequencies()
    plot_tfidf()
    plot_logodds()

    # Actors 
    for actor in ["israel", "palestin", "ukraine", "russia"]:
        plot_actor_context(actor)

    print("[DONE] All figures generated in results/figures/")


if __name__ == "__main__":
    main()
