import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

def download_nltk_data():
    resources = ['wordnet', 'omw-1.4', 'averaged_perceptron_tagger_eng']
    for resource in resources:
        try:
            if resource == 'averaged_perceptron_tagger_eng':
                nltk.data.find('taggers/averaged_perceptron_tagger_eng')
            else:
                nltk.data.find(f'corpora/{resource}')
        except LookupError:
            nltk.download(resource)

download_nltk_data()

def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)

def lemmatize_tokens(tokens):
    """
    Lemmatise une liste de tokens en utilisant les POS tags.
    """
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(token, get_wordnet_pos(token)) for token in tokens]