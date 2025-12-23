from pathlib import Path
from typing import Dict, Tuple, List
import json
import csv
import os

def load_corpus_texts(base_dir: str, max_docs_per_category=None) -> Dict[str, Dict[str, str]]:

    base = Path(base_dir)
    corpora = {}
    
    for cat in ("gaza", "ukraine"):
        cat_dir = base / cat
        docs = {}
        if cat_dir.exists():
            files = sorted(cat_dir.glob("*.txt"))
            if max_docs_per_category:
                files = files[:max_docs_per_category]
            
            for p in files:
                doc_id = p.stem
                try:
                    text = p.read_text(encoding="utf-8")
                    if len(text.split()) < 50:
                        continue
                    docs[doc_id] = text
                except Exception as e:
                    print(f"[ERROR] Failed to load {p}: {e}")
                    
        print(f"[INFO] Loaded {len(docs)} documents for {cat}")
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
