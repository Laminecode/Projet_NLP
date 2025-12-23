# src/sentiment_analysis/figures.py
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

FIG_DIR = "results/figures_sentiment"
Path(FIG_DIR).mkdir(parents=True, exist_ok=True)

def plot_actor_boxplot(csv_file):
    df = pd.read_csv(csv_file)

    actors = df["actor"].unique()
    data = [df[df["actor"] == a]["compound"] for a in actors]

    plt.figure(figsize=(8, 5))
    plt.boxplot(data, labels=actors, showmeans=True)
    plt.axhline(0, linestyle="--")

    plt.title("Sentiment distribution per actor (Gaza)")
    plt.ylabel("Compound sentiment score")
    plt.tight_layout()

    plt.savefig(f"{FIG_DIR}/sentiment_actor_boxplot.png")
    plt.close()

def plot_victim_histogram(csv_file):
    df = pd.read_csv(csv_file)

    plt.figure(figsize=(7, 5))
    plt.hist(df["compound"], bins=20)
    plt.axvline(0, linestyle="--")

    plt.title("Distribution of victim-related sentiment (Gaza)")
    plt.xlabel("Compound sentiment score")
    plt.ylabel("Number of segments")

    plt.tight_layout()
    plt.savefig(f"{FIG_DIR}/sentiment_victims_histogram.png")
    plt.close()


def plot_victim_mean(csv_file):
    df = pd.read_csv(csv_file)
    mean_val = df["compound"].mean()

    plt.figure(figsize=(4, 4))
    plt.bar(["Victims"], [mean_val])
    plt.axhline(0, linestyle="--")

    plt.ylabel("Mean compound score")
    plt.title("Average sentiment for civilian victims (civilian, child, death, wounded, ...)")
    #definier les victims
    # VICTIM_TERMS = {
    # "civilian", "civilians",
    # "child", "children",
    # "kill", "killed", "dead",
    # "death", "die",
    # "wound", "wounded",
    # "casualty", "victim", "victims"
    # }

    plt.tight_layout()
    plt.savefig(f"{FIG_DIR}/sentiment_victims_mean.png")
    plt.close()


def plot_gaza_vs_ukraine_mean(gaza_csv, ukraine_csv):
    import pandas as pd
    import matplotlib.pyplot as plt

    gaza = pd.read_csv(gaza_csv)["compound"].mean()
    ukr = pd.read_csv(ukraine_csv)["compound"].mean()

    plt.figure(figsize=(5,5))
    plt.bar(["Gaza", "Ukraine"], [gaza, ukr])
    plt.axhline(0, linestyle="--")

    plt.ylabel("Mean compound sentiment")
    plt.title("Average sentiment comparison for victims (civilians, children, deaths, wounded, ...)")

    plt.tight_layout()
    plt.savefig("results/figures_sentiment/gaza_vs_ukraine_victims_mean.png")
    plt.close()

def plot_sentiment_heatmap(csv_file, title, out_png):
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np

    df = pd.read_csv(csv_file)
    pivot = df.pivot_table(
        index="actor",
        values="compound",
        aggfunc="mean"
    )

    plt.figure(figsize=(5,3))
    plt.imshow(pivot, aspect="auto")
    plt.colorbar(label="Mean compound score")

    plt.yticks(range(len(pivot.index)), pivot.index)
    plt.xticks([0], ["Sentiment"])

    plt.title(title)
    plt.tight_layout()
    plt.savefig(out_png)
    plt.close()


