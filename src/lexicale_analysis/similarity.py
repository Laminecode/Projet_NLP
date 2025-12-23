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
# Cooccurrence
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

#Réseau de cooccurrences pour acteurs clés
def build_actor_cooccurrence(docs: Dict[str, str], actor_lemmas: List[str], window:int=5):
    """
    Build cooccurrence counts for given actor lemmas.
    Returns (co_counts: dict[(actor_lemma, context_word)]->count)
    """
    co = defaultdict(int)
    for txt in docs.values():
        tokens = [t for t in txt.split() if t]
        L = len(tokens)
        for i,t in enumerate(tokens):
            if t in actor_lemmas:
                start = max(0, i-window); end = min(L, i+window+1)
                for j in range(start, end):
                    if i == j: continue
                    pair = (t, tokens[j])
                    co[pair] += 1
    return co
