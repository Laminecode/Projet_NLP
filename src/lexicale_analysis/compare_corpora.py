# src/lexicale_analysis/compare_corpora.py
import os
from pathlib import Path
import argparse

from load_data import load_corpus_texts, save_json, save_csv_rows
from frequency import compute_and_save_all, actor_term_contexts, get_word_counts
from lexical_stats import article_stats, save_article_stats, actor_pos_contexts
from tfidf import compute_tfidf_for_corpus, top_terms_per_corpus, save_tfidf_terms
from similarity import compute_cosine_similarity, save_similarity_matrix, build_cooccurrence
import numpy as np
import pandas as pd
from collections import Counter
import math

RESULTS_DIR = "results"
STATS_DIR = os.path.join(RESULTS_DIR, "statistics")
FIGS_DIR = os.path.join(RESULTS_DIR, "figures")

def ensure_dirs():
    Path(STATS_DIR).mkdir(parents=True, exist_ok=True)
    Path(FIGS_DIR).mkdir(parents=True, exist_ok=True)

# -------- Log-odds ratio (with Dirichlet prior) ----------
def compute_log_odds(counts_a:Counter, counts_b:Counter, prior:float=0.01):
    """
    Returns pandas DataFrame with columns:
      term, count_a, count_b, logodds, z
    """
    vocab = sorted(set(list(counts_a.keys()) + list(counts_b.keys())))
    a = np.array([counts_a.get(w,0) for w in vocab], dtype=float)
    b = np.array([counts_b.get(w,0) for w in vocab], dtype=float)
    alpha = prior
    a_p = a + alpha
    b_p = b + alpha
    A = a_p.sum()
    B = b_p.sum()
    p_a = a_p / A
    p_b = b_p / B
    logodds = np.log(p_a) - np.log(p_b)
    var = 1.0/(a_p) + 1.0/(b_p)
    z = logodds / np.sqrt(var)
    df = pd.DataFrame({
        "term": vocab,
        "count_a": a.astype(int),
        "count_b": b.astype(int),
        "logodds": logodds,
        "z": z
    }).sort_values("z", ascending=False)
    return df

def run_all(data_base: str = "data/processed_clean"):
    ensure_dirs()
    corpora = load_corpus_texts(data_base)
    # 1) Frequency + ngrams
    print("[1/9] Frequency & n-grams...")
    counters = compute_and_save_all(corpora, STATS_DIR)

    # 2) Lexical stats per article
    print("[2/9] Lexical stats...")
    all_art_stats = {}
    for cat, docs in corpora.items():
        art_stats = article_stats(docs)
        all_art_stats[cat] = art_stats
    save_article_stats(all_art_stats, os.path.join(STATS_DIR, "article_stats.csv"))

    # 3) TF-IDF per corpus and top terms
    print("[3/9] TF-IDF Gaza...")
    if corpora["gaza"]:
        vec_gaza, X_gaza, ids_gaza = compute_tfidf_for_corpus(corpora["gaza"])
        top_gaza = top_terms_per_corpus(vec_gaza, X_gaza, top_k=200)
        save_tfidf_terms(top_gaza, os.path.join(STATS_DIR, "tfidf_gaza.csv"))
    else:
        print("No Gaza docs found.")

    print("[4/9] TF-IDF Ukraine...")
    if corpora["ukraine"]:
        vec_ukr, X_ukr, ids_ukr = compute_tfidf_for_corpus(corpora["ukraine"])
        top_ukr = top_terms_per_corpus(vec_ukr, X_ukr, top_k=200)
        save_tfidf_terms(top_ukr, os.path.join(STATS_DIR, "tfidf_ukraine.csv"))
    else:
        print("No Ukraine docs found.")

    # 4) Actor-term contexts
    print("[5/9] Actor term contexts...")
    # default actor list (lemmatized forms that should match processed_clean)
    actors = {
        "palestin": ["palestin","palestinian","palestine","hamas"],
        "israel": ["israel","israeli","idf"],
        "ukraine": ["ukraine","ukrainian","zelensky"],
        "russia": ["russia","russian","putin"]
    }
    for actor_key, lemmas in actors.items():
        # combine both corpora to find actor contexts per-corpus
        for cat, docs in corpora.items():
            if not docs: continue
            ctx = actor_term_contexts(docs, lemmas, window=8, topk=200)
            # write CSV
            rows = [{"term": t, "count": c} for t,c in ctx]
            save_csv_rows(os.path.join(STATS_DIR, f"{cat}_actor_{actor_key}_context.csv"), ["term","count"], rows)

    # 5) POS context analysis per actor
    print("[6/9] POS contexts...")
    for actor_key, lemmas in actors.items():
        for cat, docs in corpora.items():
            if not docs: continue
            pos_counts = actor_pos_contexts(docs, lemmas, window=5, topk=100)
            # save results for ADJ/VERB/NOUN
            for pos_tag, items in pos_counts.items():
                rows = [{"token": t, "count": c} for t,c in items]
                save_csv_rows(os.path.join(STATS_DIR, f"{cat}_actor_{actor_key}_{pos_tag}.csv"), ["token","count"], rows)

    # 6) Log-odds comparison (Gaza vs Ukraine)
    print("[7/9] Log-odds comparison...")
    cnt_gaza = counters.get("gaza", Counter())
    cnt_ukr = counters.get("ukraine", Counter())
    df_logodds = compute_log_odds(cnt_gaza, cnt_ukr, prior=0.01)
    # save top and bottom
    df_logodds.to_csv(os.path.join(STATS_DIR, "gaza_vs_ukraine_logodds_full.csv"), index=False)
    df_logodds.head(200).to_csv(os.path.join(STATS_DIR, "gaza_vs_ukraine_logodds_top200.csv"), index=False)
    df_logodds.tail(200).to_csv(os.path.join(STATS_DIR, "gaza_vs_ukraine_logodds_bottom200.csv"), index=False)

    # 7) Cooccurrence per corpus
    print("[8/9] Cooccurrence...")
    for cat, docs in corpora.items():
        if not docs: continue
        co, unig = build_cooccurrence(docs, vocab_set=None, window=5)
        total_windows = sum(unig.values())

        # optionally save cooccurrence counts (sparse)
        # we'll save top pairs by count
        top_pairs = sorted(co.items(), key=lambda x: -x[1])[:500]
        rows2 = [{"w1": a, "w2": b, "count": c} for (a,b),c in top_pairs]
        save_csv_rows(os.path.join(STATS_DIR, f"{cat}_top_cooccurrence_pairs.csv"), ["w1","w2","count"], rows2)

    # 8) Combined TF-IDF and similarity matrix (cross-corpus)
    print("[9/9] Combined TF-IDF and similarity...")
    combined_docs = {}
    for cat, docs in corpora.items():
        for doc_id, txt in docs.items():
            pref_id = f"{cat}__{doc_id}"
            combined_docs[pref_id] = txt
    if combined_docs:
        vec_comb, X_comb, ids_comb = compute_tfidf_for_corpus(combined_docs, max_features=30000, ngram_range=(1,2), min_df=1)
        sim = compute_cosine_similarity(X_comb)
        save_similarity_matrix(sim, ids_comb, os.path.join(STATS_DIR, "similarity_matrix.csv"))

    # Summary
    summary = {
        "gaza_n_docs": len(corpora.get("gaza", {})),
        "ukraine_n_docs": len(corpora.get("ukraine", {})),
        "files": {
            "gaza_wordfreq": os.path.join(STATS_DIR, "gaza_wordfreq.csv"),
            "ukraine_wordfreq": os.path.join(STATS_DIR, "ukraine_wordfreq.csv"),
            "gaza_tfidf": os.path.join(STATS_DIR, "tfidf_gaza.csv"),
            "ukraine_tfidf": os.path.join(STATS_DIR, "tfidf_ukraine.csv"),
            "logodds": os.path.join(STATS_DIR, "gaza_vs_ukraine_logodds_top200.csv")
        }
    }
    save_json(summary, os.path.join(STATS_DIR, "summary.json"))
    print("All done. Results in:", STATS_DIR)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run lexical analysis pipeline (integrated)")
    parser.add_argument("--data", default="data/processed_clean", help="Base folder for cleaned texts")
    args = parser.parse_args()
    run_all(data_base=args.data)
