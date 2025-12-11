from typing import Counter


def compute_stats(docs):
    tf_global = Counter()
    df = Counter()
    tf_docs = []

    for lemmas in docs:
        tf = Counter(lemmas)
        tf_docs.append(tf)
        tf_global.update(lemmas)
        for word in set(lemmas):
            df[word] += 1

    return {
        "tf_global": tf_global,
        "df": df,
        "tf_docs": tf_docs,
        "doc_count": len(docs)
    }