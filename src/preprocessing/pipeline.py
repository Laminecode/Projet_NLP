from src.preprocessing.clean_text import clean_text
from src.preprocessing.normalize import normalize_text
from src.preprocessing.lemmatization import lemmatize_tokens

def preprocess_pipeline(text, language='english'):
    cleaned_text = clean_text(text)
    tokens = normalize_text(cleaned_text, language)
    lemmatized_tokens = lemmatize_tokens(tokens)
    return lemmatized_tokens

# In preprocessing/pipeline.py
def preprocess_to_string(text, language='english', min_token_length=2, max_tokens=950):
    """
    Enhanced preprocessing with configurable parameters
    """
    if not text or not text.strip():
        return ""
    
    tokens = preprocess_pipeline(text, language)
    filtered_tokens = [
        t for t in tokens 
        if len(t) >= min_token_length 
        and not t.isdigit() 
        and not t.replace('.', '').isdigit()  # Remove decimals like "3.14"
        and t.isalpha()  # Only alphabetic tokens
    ]
    
    return " ".join(filtered_tokens[:max_tokens])