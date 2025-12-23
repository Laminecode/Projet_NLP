from clean_text import clean_text
from normalize import normalize_text
from lemmatization import lemmatize_tokens

def preprocess_pipeline(text, language='english'):
    """
    Execute full preprocessing pipeline: clean → normalize → lemmatize.
    
    Args:
        text: Raw input text
        language: Language for processing
        
    Returns:
        List of processed tokens
    """
    cleaned_text = clean_text(text)
    tokens = normalize_text(cleaned_text, language)
    lemmatized_tokens = lemmatize_tokens(tokens)
    return lemmatized_tokens


def preprocess_to_string(
    text,
    language='english',
    min_token_length=2,
    max_tokens=950,
    preserve_hyphenated=True,
    filter_numbers=True
):
    """
    Preprocess text and return as space-separated string.
    
    This function:
    - Cleans, normalizes, and lemmatizes text
    - Filters tokens by length and type
    - Limits output to max_tokens
    
    Args:
        text: Raw input text
        language: Language for processing
        min_token_length: Minimum token length to keep (default: 2)
        max_tokens: Maximum number of tokens to return (default: 950)
        preserve_hyphenated: Keep hyphenated terms like "far-right" (default: True)
        filter_numbers: Remove numeric tokens (default: True)
        
    Returns:
        Space-separated string of processed tokens, or empty string if no valid tokens
    """
    if not text or not text.strip():
        return ""
    
    tokens = preprocess_pipeline(text, language)
    
    # Filter tokens
    filtered_tokens = []
    for token in tokens:
        # Check minimum length
        if len(token) < min_token_length:
            continue
        
        # Skip pure numeric tokens
        if filter_numbers and (token.isdigit() or token.replace('.', '', 1).isdigit()):
            continue
        
        # Check if token is alphabetic (or hyphenated if preserve_hyphenated)
        if preserve_hyphenated:
            # Allow tokens with hyphens: "far-right", "co-operate"
            if not (token.replace('-', '').isalpha()):
                continue
        else:
            # Only pure alphabetic tokens
            if not token.isalpha():
                continue
        
        filtered_tokens.append(token)
    
    # Truncate to max_tokens
    if len(filtered_tokens) > max_tokens:
        print(f"[INFO] Truncating {len(filtered_tokens)} tokens to {max_tokens}")
        filtered_tokens = filtered_tokens[:max_tokens]
    
    return " ".join(filtered_tokens)

