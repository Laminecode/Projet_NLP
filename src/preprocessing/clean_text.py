import re
import html

BOILERPLATE_PATTERNS = [
    r'click here.*',
    r'subscribe.*',
    r'privacy policy.*',
    r'terms of use.*',
    r'material published.*',
    r'newsletter.*',
]

def clean_text(text: str) -> str:
    """
    Remove HTML entities, URLs, tags, boilerplate, and encoding artifacts.
    
    Args:
        text: Raw text input
        
    Returns:
        Cleaned text with whitespace normalized
    """
    if not text:
        return ""

    # Decode HTML entities
    text = html.unescape(text)

    # Remove URLs
    text = re.sub(r'http\S+|www\.\S+', ' ', text)

    # Remove HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)

    # Replace _ - . with space (corrected regex)
    text = re.sub(r'[_\-.]+', ' ', text)

    # Remove boilerplate patterns
    for pat in BOILERPLATE_PATTERNS:
        text = re.sub(pat, ' ', text, flags=re.IGNORECASE)

    # Remove media markers like [Photo], [Video]
    text = re.sub(r'\[[^\]]+\]', ' ', text)

    # Fix encoding issues
    text = (
        text.replace('\ufffd', ' ')
            .replace('ï¿½', ' ')
            .replace('\xa0', ' ')
    )

    # Remove non-printable characters
    text = ''.join(c if c.isprintable() else ' ' for c in text)

    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    return text
