
from gensim.models import Word2Vec
from pathlib import Path
import csv

def train_word2vec(docs: dict,
                   vector_size=200,
                   window=5,
                   min_count=5,
                   workers=4):
    sentences = []
    for txt in docs.values():
        tokens = txt.split()
        if len(tokens) > 5:
            sentences.append(tokens)

    model = Word2Vec(
        sentences=sentences,
        vector_size=vector_size,
        window=window,
        min_count=min_count,
        workers=workers,
        sg=1  
    )
    return model

def save_actor_neighbors(model, actor_terms, out_csv, topk=20):
    rows = []
    for actor in actor_terms:
        if actor in model.wv:
            for word, score in model.wv.most_similar(actor, topn=topk):
                rows.append({
                    "actor": actor,
                    "neighbor": word,
                    "similarity": float(score)
                })

    Path(out_csv).parent.mkdir(parents=True, exist_ok=True)
    with open(out_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["actor","neighbor","similarity"])
        writer.writeheader()
        writer.writerows(rows)
