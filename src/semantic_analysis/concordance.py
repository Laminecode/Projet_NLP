# src/semantic_analysis/concordance.py
from typing import Dict, List
from pathlib import Path
import csv

def extract_concordances(
    docs: Dict[str, str],
    keyword: str,
    window: int = 5,
    max_lines: int = 200
):

    rows = []
    for doc_id, text in docs.items():
        tokens = text.split()
        for i, tok in enumerate(tokens):
            if tok == keyword:
                left = " ".join(tokens[max(0, i-window):i])
                right = " ".join(tokens[i+1:i+1+window])
                rows.append({
                    "doc_id": doc_id,
                    "left": left,
                    "keyword": keyword,
                    "right": right
                })
                if len(rows) >= max_lines:
                    return rows
    return rows

def save_concordances(rows: List[dict], out_csv: str):
    Path(out_csv).parent.mkdir(parents=True, exist_ok=True)
    with open(out_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["doc_id", "left", "keyword", "right"]
        )
        writer.writeheader()
        writer.writerows(rows)
