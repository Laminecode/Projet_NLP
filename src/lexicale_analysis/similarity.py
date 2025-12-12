# src/lexicale_analysis/similarity.py
from typing import Dict, List, Tuple
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import csv
from pathlib import Path
from collections import defaultdict
import math

def compute_cosine_similarity(X) -> np.ndarray:
    """
    X : doc-term matrix (sparse or dense)
    returns similarity matrix (dense)
    """
    sim = cosine_similarity(X)
    return sim

def save_similarity_matrix(sim: np.ndarray, doc_ids: List[str], out_csv: str):
    Path(out_csv).parent.mkdir(parents=True, exist_ok=True)
    header = ["doc_id"] + doc_ids
    with open(out_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for i, row in enumerate(sim):
            writer.writerow([doc_ids[i]] + [float(x) for x in row])

# ----------------------------
# Cooccurrence & PMI
# ----------------------------
from collections import defaultdict, Counter
def build_cooccurrence(docs: Dict[str, str], vocab_set:set=None, window:int=5):
    """
    Build cooccurrence counts (token-token) across docs.
    Returns (co_counts: dict[(w1,w2)]->count, unigram_counts)
    """
    co = defaultdict(int)
    unigram = Counter()
    for txt in docs.values():
        tokens = [t for t in txt.split() if t]
        L = len(tokens)
        for i,t in enumerate(tokens):
            unigram[t] += 1
            start = max(0, i-window); end = min(L, i+window+1)
            for j in range(start, end):
                if i == j: continue
                pair = (t, tokens[j])
                if vocab_set and (t not in vocab_set or tokens[j] not in vocab_set):
                    continue
                co[pair] += 1
    return co, unigram

def compute_pmi(co_counts: dict, unigram: dict, total_windows:int):
    """
    Compute PMI for each pair in co_counts.
    total_windows: total count to normalize (approx. sum of unigram)
    """
    pmi = {}
    for (w1,w2), c in co_counts.items():
        p_w1 = unigram[w1] / total_windows if total_windows>0 else 0.0
        p_w2 = unigram[w2] / total_windows if total_windows>0 else 0.0
        p_w1w2 = c / total_windows if total_windows>0 else 0.0
        # small-smoothing
        score = math.log2((p_w1w2 / (p_w1 * p_w2 + 1e-12)) + 1e-12)
        pmi[(w1,w2)] = score
    return pmi

def top_pmi_bigrams(pmi_dict:dict, topk:int=100):
    items = sorted(pmi_dict.items(), key=lambda x: -x[1])
    return [(f"{a} {b}",score) for (a,b),score in items[:topk]]
