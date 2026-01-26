import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def get_custom_stopwords(language='english'):
    stop_words = set(stopwords.words(language))

    domain_stopwords = {
        "say", "says", "said",
        "according", "source", "sources",
        "news", "media",
        "report", "reports", "reported",
        "one", "two", "three",
        "year", "years",
        "people", "percent", "many", "some",
        "u", "us", "im", "ive",
        "dont", "doesnt", "didnt", "wont", "cant",
        "october"
    }

    return stop_words | domain_stopwords


def normalize_text(text, language='english'):

    text = text.lower()

    text = re.sub(r"[^\w\s\-]", " ", text)

    text = re.sub(r"\s+", " ", text).strip()

    try:
        tokens = word_tokenize(text)
    except Exception as e:
        print(f"[WARNING] Tokenization failed: {e}")
        tokens = text.split()

    stop_words = get_custom_stopwords(language)
    tokens = [t for t in tokens if t not in stop_words]

    return tokens