import re
import html

def clean_text(text):

    if not text:
        return ""
    text = html.unescape(text)
    text = re.sub(r'http\S+|www\.\S+', '', text)
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    #remove non-printable characters
    text = ''.join(c for c in text if c.isprintable())

    return text