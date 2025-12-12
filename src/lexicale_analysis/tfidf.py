# src/lexicale_analysis/tfidf.py
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import csv
from pathlib import Path
from typing import Dict, List, Tuple
import numpy as np

def compute_tfidf_for_corpus(docs: Dict[str, str],
                             max_features: int = 20000,
                             ngram_range=(1,2),
                             min_df=2, max_df=0.95) -> Tuple[TfidfVectorizer, "sparse_matrix", List[str]]:
    doc_ids = list(docs.keys())
    texts = [docs[_id] for _id in doc_ids]
    vectorizer = TfidfVectorizer(max_features=max_features, ngram_range=ngram_range, min_df=min_df, max_df=max_df)
    X = vectorizer.fit_transform(texts)
    return vectorizer, X, doc_ids

def top_terms_per_corpus(vectorizer: TfidfVectorizer, X, top_k: int = 30) -> List[Tuple[str, float]]:
    import numpy as np
    mean_tfidf = np.asarray(X.mean(axis=0)).ravel()
    terms = vectorizer.get_feature_names_out()
    idx_sorted = np.argsort(-mean_tfidf)[:top_k]
    return [(terms[i], float(mean_tfidf[i])) for i in idx_sorted]

def save_tfidf_terms(terms_scores: List[Tuple[str, float]], out_csv: str):
    Path(out_csv).parent.mkdir(parents=True, exist_ok=True)
    with open(out_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["term", "score"])
        writer.writerows(terms_scores)
