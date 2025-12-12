import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def download_nltk_data():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
    
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')

download_nltk_data()

def to_lowercase(text):
    return text.lower()

def remove_punctuation(text):
    extended_punctuation = string.punctuation + "”’“‘–—«»…"
    return text.translate(str.maketrans('', '', extended_punctuation))

def tokenize_text(text):
    return word_tokenize(text)

def remove_stopwords(tokens, language='english'):
    stop_words = set(stopwords.words(language))
    extra_sw = {"say","says","said","also","include","report","reports","reported","news","media","one","two","new","first","last","year","years","people","percent","many","most","some","may","like","even","u","us","would","could","should","might","must"}
    stop_words |= extra_sw
    return [word for word in tokens if word.lower() not in stop_words]

def normalize_text(text, language='english'):
    text = to_lowercase(text)
    text = remove_punctuation(text)
    tokens = tokenize_text(text)
    tokens = remove_stopwords(tokens, language)
    return tokens