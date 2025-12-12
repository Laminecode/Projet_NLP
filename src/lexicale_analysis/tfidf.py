import math

def compute_tfidf_per_doc(stats, topk=50):
    N = stats["doc_count"]
    df = stats["df"]
    tfidf_docs = []

    for tf in stats["tf_docs"]:
        tfidf = {}
        for word, freq in tf.items():
            idf = math.log((N + 1) / (df[word] + 1)) + 1
            tfidf[word] = freq * idf

        # top TF-IDF
        top = dict(sorted(tfidf.items(), key=lambda x: -x[1])[:topk])
        tfidf_docs.append(top)

    return tfidf_docs