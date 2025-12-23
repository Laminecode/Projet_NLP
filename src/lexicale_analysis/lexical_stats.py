# src/lexicale_analysis/lexical_stats.py
from email.mime import text
from typing import Dict, Tuple, List
from collections import Counter
from pathlib import Path
import csv
import os
import numpy as np

USE_SPACY = False
try:
    import spacy
    nlp = spacy.load("en_core_web_sm", disable=["ner"])  # enable ner optionally
    doc = nlp(text)
except Exception:
    USE_SPACY = False
    import nltk
    try:
        nltk.data.find('tokenizers/punkt')
    except Exception:
        nltk.download('punkt')
    try:
        nltk.data.find('taggers/averaged_perceptron_tagger')
    except Exception:
        nltk.download('averaged_perceptron_tagger')
    from nltk import word_tokenize, pos_tag

def article_stats(docs: Dict[str, str]) -> Dict[str, Dict]:
    stats = {}
    for doc_id, text in docs.items():
        tokens = [t for t in text.split() if t]
        tokens_count = len(tokens)
        vocab = set(tokens)
        vocab_size = len(vocab)
        diversity = (vocab_size / tokens_count) if tokens_count > 0 else 0.0
        avg_len = float(np.mean([len(t) for t in tokens])) if tokens_count > 0 else 0.0
        longest = max(tokens, key=len) if tokens else ""
        stats[doc_id] = {
            "tokens": tokens_count,
            "vocab": vocab_size,
            "diversity": float(diversity),
            "avg_word_len": float(avg_len),
            "longest_word": longest
        }
    return stats

def save_article_stats(all_stats: Dict[str, Dict[str, Dict]], out_csv: str):
    Path(out_csv).parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["category", "doc_id", "tokens", "vocab", "diversity", "avg_word_len", "longest_word"]
    rows = []
    for cat, stats in all_stats.items():
        for doc_id, st in stats.items():
            rows.append({
                "category": cat,
                "doc_id": doc_id,
                "tokens": st["tokens"],
                "vocab": st["vocab"],
                "diversity": st["diversity"],
                "avg_word_len": st["avg_word_len"],
                "longest_word": st["longest_word"]
            })
    with open(out_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

# -----------------------
# POS-based context analysis
# -----------------------
from collections import Counter
def actor_pos_contexts(docs: Dict[str, str], actor_lemmas:List[str], window:int=5, topk:int=50):

    results = {"ADJ": Counter(), "VERB": Counter(), "NOUN": Counter()}
    if USE_SPACY:
        for text in docs.values():
            doc = nlp(text)
            for token in doc:
                if token.lemma_.lower() in actor_lemmas:

                    i = token.i
                    start = max(0, i-window); end = min(len(doc), i+window+1)
                    for t in doc[start:end]:
                        if t.pos_ == "ADJ":
                            results["ADJ"][t.lemma_.lower()] += 1
                        elif t.pos_ == "VERB":
                            results["VERB"][t.lemma_.lower()] += 1
                        elif t.pos_ == "NOUN":
                            results["NOUN"][t.lemma_.lower()] += 1
    else:
        from nltk import word_tokenize, pos_tag
        for text in docs.values():
            tokens = word_tokenize(text)
            tags = pos_tag(tokens)
            for i,(tok,tag) in enumerate(tags):
                if tok.lower() in actor_lemmas:
                    start = max(0, i-window); end = min(len(tags), i+window+1)
                    for j in range(start, end):
                        w, t = tags[j]
                        if t.startswith("JJ"): results["ADJ"][w.lower()] += 1
                        elif t.startswith("VB"): results["VERB"][w.lower()] += 1
                        elif t.startswith("NN"): results["NOUN"][w.lower()] += 1
    return {k: v.most_common(topk) for k,v in results.items()}


