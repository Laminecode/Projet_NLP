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
    """
    POS-aware lemmatization using WordNet.
    POS tagging is performed once on the full token list.
    """
    if not tokens:
        return []

    lemmatizer = WordNetLemmatizer()
    pos_tags = nltk.pos_tag(tokens)

    lemmas = []
    for word, tag in pos_tags:
        wn_tag = {
            'J': wordnet.ADJ,
            'N': wordnet.NOUN,
            'V': wordnet.VERB,
            'R': wordnet.ADV
        }.get(tag[0], wordnet.NOUN)

        lemmas.append(lemmatizer.lemmatize(word, wn_tag))

    return lemmas
