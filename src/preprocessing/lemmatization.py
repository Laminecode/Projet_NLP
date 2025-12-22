import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

def download_nltk_data():
    resources = [
        ('corpora/wordnet', 'wordnet'),
        ('corpora/omw-1.4', 'omw-1.4'),
        ('taggers/averaged_perceptron_tagger', 'averaged_perceptron_tagger'),
    ]

    for path, name in resources:
        try:
            nltk.data.find(path)
        except LookupError:
            nltk.download(name)

download_nltk_data()

def lemmatize_tokens(tokens):

    if not tokens:
        return []

    lemmatizer = WordNetLemmatizer()
    
    try:
        pos_tags = nltk.pos_tag(tokens)
    except Exception as e:
        print(f"[WARNING] POS tagging failed: {e}. Using default lemmatization.")
        return [lemmatizer.lemmatize(token, wordnet.NOUN) for token in tokens]

    lemmas = []
    for word, tag in pos_tags:
        wn_tag = {
            'J': wordnet.ADJ,
            'N': wordnet.NOUN,
            'V': wordnet.VERB,
            'R': wordnet.ADV
        }.get(tag[0], wordnet.NOUN)

        try:
            lemma = lemmatizer.lemmatize(word, wn_tag)
            lemmas.append(lemma)
        except Exception as e:
            print(f"[WARNING] Lemmatization failed for '{word}': {e}")
            lemmas.append(word)

    return lemmas