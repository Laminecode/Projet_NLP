from src.preprocessing.clean_text import clean_text
from src.preprocessing.normalize import normalize_text
from src.preprocessing.lemmatization import lemmatize_tokens

def preprocess_pipeline(text, language='english'):
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
    if not text or not text.strip():
        return ""
    
    tokens = preprocess_pipeline(text, language)
    
    filtered_tokens = []
    for token in tokens:
        if len(token) < min_token_length:
            continue
        
        if filter_numbers and (token.isdigit() or token.replace('.', '', 1).isdigit()):
            continue
        
        if preserve_hyphenated:
            if not (token.replace('-', '').isalpha()):
                continue
        else:
            if not token.isalpha():
                continue
        
        filtered_tokens.append(token)
    
    if len(filtered_tokens) > max_tokens:
        print(f"[INFO] Truncating {len(filtered_tokens)} tokens to {max_tokens}")
        filtered_tokens = filtered_tokens[:max_tokens]
    
    return " ".join(filtered_tokens)

