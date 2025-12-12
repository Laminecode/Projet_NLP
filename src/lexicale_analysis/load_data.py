# src/lexicale_analysis/load_data.py
from pathlib import Path
from typing import Dict, Tuple, List
import json
import csv
import os

def load_corpus_texts(base_dir: str) -> Dict[str, Dict[str, str]]:
    """
    Load cleaned texts from data/processed_clean/{gaza,ukraine}/
    Returns dict: { "gaza": {id: text, ...}, "ukraine": {id: text, ...} }
    ID is filename without extension.
    """
    base = Path(base_dir)
    corpora = {}
    for cat in ("gaza", "ukraine"):
        cat_dir = base / cat
        docs = {}
        if cat_dir.exists():
            for p in sorted(cat_dir.glob("*.txt")):
                doc_id = p.stem
                try:
                    text = p.read_text(encoding="utf-8")
                except Exception:
                    text = p.read_text(encoding="latin-1")
                docs[doc_id] = text
        corpora[cat] = docs
    return corpora

def save_json(obj, path):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")

def save_csv_rows(path, fieldnames, rows):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8", newline="") as f:
        import csv
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
