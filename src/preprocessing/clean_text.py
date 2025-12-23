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
    if not text:
        return ""

    text = html.unescape(text)

    text = re.sub(r'http\S+|www\.\S+', ' ', text)

    text = re.sub(r'<[^>]+>', ' ', text)

    text = re.sub(r'[_\-.]+', ' ', text)

    for pat in BOILERPLATE_PATTERNS:
        text = re.sub(pat, ' ', text, flags=re.IGNORECASE)

    text = re.sub(r'\[[^\]]+\]', ' ', text)

    text = (
        text.replace('\ufffd', ' ')
            .replace('ï¿½', ' ')
            .replace('\xa0', ' ')
    )

    text = ''.join(c if c.isprintable() else ' ' for c in text)

    text = re.sub(r'\s+', ' ', text).strip()

    return text
