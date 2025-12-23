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

# Graphique TF-IDF comparatif Gaza vs Ukraine
def plot_tfidf_comparative():
    print("[INFO] Plotting comparative TF-IDF...")

    path_gaza = os.path.join(STATS_DIR, "tfidf_gaza.csv")
    path_ukraine = os.path.join(STATS_DIR, "tfidf_ukraine.csv")
    if not os.path.exists(path_gaza) or not os.path.exists(path_ukraine):
        return
    
    df_gaza = pd.read_csv(path_gaza).head(20)  # Top 20 termes
    df_ukraine = pd.read_csv(path_ukraine).head(20)
    df_gaza['corpus'] = 'Gaza'
    df_ukraine['corpus'] = 'Ukraine'
   
    df_gaza = df_gaza.rename(columns={'score': 'tfidf_score'})
    df_ukraine = df_ukraine.rename(columns={'score': 'tfidf_score'})

    df_combined = pd.concat([df_gaza, df_ukraine], ignore_index=True)
   
    plt.figure(figsize=(12, 8))
    sns.barplot(data=df_combined, y='term', x='tfidf_score', hue='corpus', 
                palette=['#e74c3c', '#3498db'])
    plt.title("Comparative TF-IDF Terms – Gaza vs Ukraine", fontsize=14, fontweight='bold')
    plt.xlabel("TF-IDF Score", fontsize=12)
    plt.ylabel("Term", fontsize=12)
    plt.legend(title='Corpus', fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGS_DIR, "tfidf_gaza_vs_ukraine.png"), dpi=200)
    plt.close()


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

# figure Réseau de cooccurrences pour acteurs clés and save figure
def plot_actor_cooccurrences(actor):
    print(f"[INFO] Plotting actor co-occurrences: {actor}")

    for corpus in ["gaza", "ukraine"]:
        path = os.path.join(
            STATS_DIR, f"{corpus}_actor_{actor}_cooccurrences.csv"
        )
        if not os.path.exists(path):
            continue

        df = pd.read_csv(path)
        barplot(
            df,
            x="count",
            y="term",
            title=f"Co-occurrences with '{actor}' – {corpus.capitalize()}",
            filename=f"{corpus}_{actor}_cooccurrences.png"
        )

def plot_distinctive_terms(csv_file, title, out_png, top_n=20):
    df = pd.read_csv(csv_file)

    # on prend les termes les plus distinctifs
    df = df.sort_values("z", ascending=False).head(top_n)

    plt.figure(figsize=(7, 5))
    plt.barh(df["term"], df["z"])
    plt.axvline(0, linestyle="--")

    plt.xlabel("Log-odds z-score")
    plt.title(title)

    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(out_png)
    plt.close()


# ------------------ MAIN ------------------
def main():
<<<<<<< HEAD
    # plot_word_frequencies()
    # plot_tfidf()
    # plot_logodds()
    # plot_tfidf_comparative()
    plot_distinctive_terms(
        "results/statistics/gaza_vs_ukraine_logodds_top200.csv",
        "Top Distinctive Terms: Gaza vs Ukraine",
        "results/figures/distinctive_terms_gaza_ukraine.png"
    )
=======
    plot_word_frequencies()
    plot_tfidf()
    plot_logodds()

    # Actors 
    for actor in ["israel", "palestin", "ukraine", "russia"]:
        plot_actor_context(actor)
>>>>>>> 1f3b24556b639fd39149f7148eadb24c7bc7adf1

    # # Actors (adapt to your project)
    # for actor in ["israel", "palestin", "ukraine", "russia"]:
    #     plot_actor_context(actor)
    #     plot_actor_cooccurrences(actor)
    print("[DONE] All figures generated in results/figures/")


if __name__ == "__main__":
    main()
