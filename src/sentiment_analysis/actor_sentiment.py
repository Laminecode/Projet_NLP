from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

nltk.download("vader_lexicon")

sia = SentimentIntensityAnalyzer()

ACTORS = {
    "israel": ["israel", "idf"],
    "palestine": ["palestine", "palestinian"],
    "hamas": ["hamas"],
    "russia": ["russia", "russian"],
    "ukraine": ["ukraine", "ukrainian"]
}

def extract_actor_sentiment(docs: dict):
    rows = []

    for doc_id, text in docs.items():
        sentences = text.split(".")
        for s in sentences:
            s_low = s.lower()
            for actor, terms in ACTORS.items():
                if any(t in s_low for t in terms):
                    score = sia.polarity_scores(s)
                    rows.append({
                        "doc_id": doc_id,
                        "actor": actor,
                        "compound": score["compound"],
                        "neg": score["neg"],
                        "neu": score["neu"],
                        "pos": score["pos"]
                    })
    return rows
