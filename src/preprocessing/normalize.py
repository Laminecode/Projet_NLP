import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def get_custom_stopwords(language='english'):
    """
    Get standard stopwords plus domain-specific stopwords for news/current events.
    
    Args:
        language: Language for stopwords
        
    Returns:
        Set of stopwords to filter
    """
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
    """
    Normalize text: lowercase, remove punctuation, tokenize, remove stopwords.
    
    Args:
        text: Cleaned text input
        language: Language for stopwords
        
    Returns:
        List of normalized tokens
    """
    # Lowercase
    text = text.lower()

    # Replace punctuation with spaces (keep hyphens for compound words)
    text = re.sub(r"[^\w\s\-]", " ", text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # Tokenize
    try:
        tokens = word_tokenize(text)
    except Exception as e:
        print(f"[WARNING] Tokenization failed: {e}")
        tokens = text.split()

    # Remove stopwords
    stop_words = get_custom_stopwords(language)
    tokens = [t for t in tokens if t not in stop_words]

    return tokens