from src.preprocessing.clean_text import clean_text
from src.preprocessing.normalize import normalize_text
from src.preprocessing.lemmatization import lemmatize_tokens

def preprocess_pipeline(text, language='english'):
    cleaned_text = clean_text(text)
    tokens = normalize_text(cleaned_text, language)
    lemmatized_tokens = lemmatize_tokens(tokens)
    return lemmatized_tokens

def preprocess_to_string(text, language='english'):
    tokens = preprocess_pipeline(text, language)
    return " ".join(tokens)