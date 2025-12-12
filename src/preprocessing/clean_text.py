import re
import html

def clean_text(text):
    if not text:
        return ""
    text = html.unescape(text)
    text = re.sub(r'http\S+|www\.\S+', '', text)
    text = re.sub(r'<.*?>', '', text)
    text = text.replace('\ufffd', ' ')
    text = text.replace('�', ' ')
    text = ''.join(c for c in text if c.isprintable())
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

# text = "Check out this link: https://example.com <br> &amp; enjoy!"
# cleaned_text = clean_text(text)
# print(cleaned_text)