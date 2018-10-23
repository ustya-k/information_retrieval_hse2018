from nltk.corpus import stopwords
from pymystem3 import Mystem
import re


m = Mystem()


def word_preprocessing(word):
    '''
    Removes non-cyrillic characters.

    Args:
        word: str

    Returns:
        str
    '''
    return re.sub('[^А-Яа-яЁё]', '', word)


def sentence_preprocessing(sentence, stopwords=None):
    '''
    Lemmatization of the sentence, splitting into words

    Args:
        sentence: str
        stopwords: list or None

    Returns:
        list of strings
    '''
    sent = m.lemmatize(sentence)
    sent = [word_preprocessing(word.lower()) for word in sent if not re.search(
        '\s', word) and word != '']
    if stopwords is None:
        return sent
    return [word_preprocessing(word.lower()) for word in sent if word not in stopwords]


def preprocessing(text, stopwords=None):
    '''
    Args:
        text: str
        stopwords: list or None

    Returns:
        list of lists of string (if more than 1 sentence)
        OR list of strings (if 1 sentence)
    '''
    text = text.lower()
    # text = text.translate({el: "" for el in string.punctuation})
    text = re.sub('[A-Za-z0-9]', '', text)
    paragraphs = text.split('\n')
    paragraphs = [sentence_preprocessing(
        sent, stopwords) for sent in paragraphs]
    if len(paragraphs) == 1:
        return paragraphs[0]
