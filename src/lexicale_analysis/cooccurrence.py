from typing import Counter

def compute_cooccurrence(tokens, window=4):
    pairs = Counter()
    n = len(tokens)

    for i in range(n):
        for j in range(i+1, min(i + window + 1, n)):
            a, b = tokens[i], tokens[j]
            if a != b:
                k = tuple(sorted((a, b)))
                pairs[k] += 1
    return pairs


def compute_corpus_cooccurrence(docs):
    agg = Counter()
    for lemmas in docs:
        agg.update(compute_cooccurrence(lemmas))
    return agg

