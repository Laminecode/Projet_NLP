# =========================
# Asymétrie Gaza – Ukraine
# =========================

from typing import Counter


def asymmetry(freq_A, freq_B, topk=40):
    vocab = set(freq_A.keys()) | set(freq_B.keys())
    scores = []

    for w in vocab:
        a = freq_A[w]
        b = freq_B[w]
        if a + b == 0:
            continue

        score = (a - b) / (a + b)  # normalisation
        scores.append((w, score, a, b))

    scores = sorted(scores, key=lambda x: -abs(x[1]))
    return scores[:topk]


# =========================
# Asymétrie Palestiniens – Israéliens
# =========================

PALESTINE_WORDS = ["palestinian", "palestine", "gazans", "hamas"]
ISRAEL_WORDS = ["israeli", "israel", "idf", "netanyahu"]

def contextual_asymmetry(docs, window=3):
    """
    Cherche les mots qui apparaissent dans le voisinage
    de Palestinian* vs Israeli*.
    """
    assoc_P = Counter()
    assoc_I = Counter()

    for lemmas in docs:
        n = len(lemmas)
        for i, w in enumerate(lemmas):

            if w in PALESTINE_WORDS:
                for j in range(max(0, i-window), min(n, i+window+1)):
                    if j != i:
                        assoc_P[lemmas[j]] += 1

            if w in ISRAEL_WORDS:
                for j in range(max(0, i-window), min(n, i+window+1)):
                    if j != i:
                        assoc_I[lemmas[j]] += 1

    return assoc_P.most_common(30), assoc_I.most_common(30)