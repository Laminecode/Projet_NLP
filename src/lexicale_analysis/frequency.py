# src/lexicale_analysis/frequency.py
from collections import Counter
from typing import Dict, List, Tuple
from pathlib import Path
import csv, os
import math

def get_word_counts(docs: Dict[str, str]) -> Counter:
    c = Counter()
    for text in docs.values():
        tokens = [t for t in text.split() if t]
        c.update(tokens)
    return c

def get_ngrams_counts(docs: Dict[str, str], n:int=2, min_count:int=1) -> Counter:
    c = Counter()
    for text in docs.values():
        tokens = [t for t in text.split() if t]
        for i in range(len(tokens)-n+1):
            ng = " ".join(tokens[i:i+n])
            c[ng] += 1
    # optionally filter
    if min_count>1:
        for k in list(c.keys()):
            if c[k] < min_count:
                del c[k]
    return c

def save_wordfreq(counter, out_csv: str, top_n: int = None):
    Path(out_csv).parent.mkdir(parents=True, exist_ok=True)
    items = counter.most_common(top_n)
    with open(out_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["term", "count"])
        writer.writerows(items)

def actor_term_contexts(docs: Dict[str, str], actor_lemmas:List[str], window:int=10, topk:int=100):
    c = Counter()
    for text in docs.values():
        tokens = text.split()
        L = len(tokens)
        for i, t in enumerate(tokens):
            if t in actor_lemmas:
                left = tokens[max(0,i-window):i]
                right = tokens[i+1: i+1+window]
                context = left + right
                c.update(context)
    return c.most_common(topk)

def compute_and_save_all(corpora: Dict[str, Dict[str, str]], out_dir: str):

    Path(out_dir).mkdir(parents=True, exist_ok=True)
    counters = {}
    for cat, docs in corpora.items():
        cnt = get_word_counts(docs)
        counters[cat] = cnt
        save_wordfreq(cnt, os.path.join(out_dir, f"{cat}_wordfreq.csv"))
        # ngrams
        bi = get_ngrams_counts(docs, n=2, min_count=1)
        tri = get_ngrams_counts(docs, n=3, min_count=1)
        save_wordfreq(bi, os.path.join(out_dir, f"{cat}_bigrams.csv"))
        save_wordfreq(tri, os.path.join(out_dir, f"{cat}_trigrams.csv"))
    return counters
