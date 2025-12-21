#src/sentiment/victim_sentiment.py
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
nltk.download("punkt")
from nltk.tokenize import sent_tokenize

nltk.download("vader_lexicon")

sia = SentimentIntensityAnalyzer()

VICTIM_TERMS = {
    "civilian", "civilians",
    "child", "children",
    "kill", "killed", "dead",
    "death", "die",
    "wound", "wounded",
    "casualty", "victim", "victims"
}


import re

def extract_victim_sentiment(docs: dict, window=25):
    rows = []

    for doc_id, text in docs.items():
        tokens = text.lower().split()

        for i in range(0, len(tokens), window):
            chunk = tokens[i:i+window]
            if not chunk:
                continue

            if any(t in chunk for t in VICTIM_TERMS):
                sentence = " ".join(chunk)
                score = sia.polarity_scores(sentence)

                rows.append({
                    "doc_id": doc_id,
                    "segment": sentence,
                    "neg": score["neg"],
                    "neu": score["neu"],
                    "pos": score["pos"],
                    "compound": score["compound"]
                })

    return rows

