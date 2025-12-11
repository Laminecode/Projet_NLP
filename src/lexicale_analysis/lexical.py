import os
import json
import math
from collections import Counter, defaultdict
from glob import glob
from lexicale_analysis.assymetry import asymmetry, contextual_asymmetry
from lexicale_analysis.cooccurrence import compute_corpus_cooccurrence
from lexicale_analysis.frequency import compute_stats, compute_tfidf_per_doc
from lexicale_analysis.ngramms import extract_ngrams

# =========================
# Chargement corpus
# =========================

def load_processed_corpus(folder):
    
    texts = []
    files = glob(os.path.join(folder, "*.txt"))

    for f in files:
        with open(f, "r", encoding="utf-8") as ff:
            lemmas = ff.read().strip().split()
            if lemmas:
                texts.append(lemmas)
    return texts


def main():

    GAZA_DIR = "data/processed/gaza"
    UKRAINE_DIR = "data/processed/ukraine"
    OUT_FILE = "data/analysis/lexical_report.json"

    os.makedirs("data/analysis", exist_ok=True)

    # Chargement corpus
    gaza_docs = load_processed_corpus(GAZA_DIR)
    ukr_docs = load_processed_corpus(UKRAINE_DIR)

    # Stats
    stats_gaza = compute_stats(gaza_docs)
    stats_ukr = compute_stats(ukr_docs)

    # TF-IDF
    tfidf_gaza = compute_tfidf_per_doc(stats_gaza)
    tfidf_ukraine = compute_tfidf_per_doc(stats_ukr)

    # N-grams
    bigrams_gaza = extract_ngrams(sum(gaza_docs, []), 2)
    trigrams_gaza = extract_ngrams(sum(gaza_docs, []), 3)

    bigrams_ukr = extract_ngrams(sum(ukr_docs, []), 2)
    trigrams_ukr = extract_ngrams(sum(ukr_docs, []), 3)

    # Cooccurrences
    cooc_gaza = compute_corpus_cooccurrence(gaza_docs).most_common(40)
    cooc_ukr = compute_corpus_cooccurrence(ukr_docs).most_common(40)

    # Asymétrie Gaza–Ukraine
    asym_gaza_ukr = asymmetry(stats_gaza["tf_global"], stats_ukr["tf_global"])

    # Asymétrie Palestiniens–Israéliens
    asym_P, asym_I = contextual_asymmetry(gaza_docs + ukr_docs)

    # Export
    result = {
        "Gaza": {
            "doc_count": stats_gaza["doc_count"],
            "top_words": stats_gaza["tf_global"].most_common(50),
            "bigrams": bigrams_gaza,
            "trigrams": trigrams_gaza,
            "tfidf_sample": tfidf_gaza[:5],
            "cooccurrences": cooc_gaza
        },
        "Ukraine": {
            "doc_count": stats_ukr["doc_count"],
            "top_words": stats_ukr["tf_global"].most_common(50),
            "bigrams": bigrams_ukr,
            "trigrams": trigrams_ukr,
            "tfidf_sample": tfidf_ukraine[:5],
            "cooccurrences": cooc_ukr
        },
        "Asymmetry_Gaza_vs_Ukraine": asym_gaza_ukr,
        "Asymmetry_Palestinian_vs_Israeli": {
            "palestinian_context": asym_P,
            "israeli_context": asym_I
        }
    }

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print("[OK] Lexical analysis saved to", OUT_FILE)


if __name__ == "__main__":
    main()