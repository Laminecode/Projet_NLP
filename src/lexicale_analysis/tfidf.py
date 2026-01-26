# src/lexicale_analysis/tfidf.py
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import csv
from pathlib import Path
from typing import Dict, List, Tuple
import numpy as np
from scipy.sparse import csr_matrix

def compute_tfidf_for_corpus(docs: Dict[str, str],
                             max_features: int = 20000,
                             ngram_range=(1,2),
                             min_df=2, max_df=0.95) -> Tuple[TfidfVectorizer, csr_matrix, List[str]]:
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


# def compute_tfidf_simple(docs: Dict[str, str]):
   
#     doc_ids = list(docs.keys())
#     texts = [docs[_id] for _id in doc_ids]
#     tokenized = [[w.lower() for w in txt.split() if w] for txt in texts]
#     vocab_set = set()
#     for toks in tokenized:
#         vocab_set.update(toks)
#     vocab = sorted(vocab_set)
#     term_idx = {t: i for i, t in enumerate(vocab)}
#     N = len(doc_ids)
#     V = len(vocab)
#     tf = np.zeros((N, V), dtype=float)
#     for i, toks in enumerate(tokenized):
#         for t in toks:
#             j = term_idx.get(t)
#             if j is not None:
#                 tf[i, j] += 1.0

#     doc_lengths = tf.sum(axis=1, keepdims=True)
#     nonzero = doc_lengths.squeeze() > 0
#     tf[nonzero, :] = tf[nonzero, :] / doc_lengths[nonzero]
#     df = np.count_nonzero(tf > 0, axis=0)
#     idf = np.log((N + 1) / (df + 1)) + 1.0
#     tfidf = tf * idf

#     return tfidf, vocab, doc_ids
