from preprocessing import preprocessing
from collections import defaultdict
from math import log
import json


def score_BM25(qf, dl, avgdl, N, n, k1=2.0, b=0.75):
    '''
    Computes similarity score between search query and a document from collection.

    Args:
        qf: float, part of documents with query in the collection
        dl: int, length of the document
        avgdl: float, average length of a document in the collection
        N: int, size (in documents) of the collection
        n: int, number of documents containing query
        k1, b: float, free parametres

    Returns:
        float
    '''
    idf = log((N - n + 0.5) / (n + 0.5))
    score = idf * (k1 + 1) * qf / (qf + k1 * (1 - b + b * dl / avgdl))
    return score


def get_avgdl(texts):
    '''
    Computes average length of a document in a collection.

    Args:
        texts: dict, where key (str) is an id of a text, value (str) is the text itself

    Returns:
        float
    '''
    N = len(texts)
    sum_len = 0
    for doc in texts:
        sum_len += len(texts[doc])
    return sum_len / N


def compute_sim(lemma, relevance_dict, avgdl, N, corpus_meta):
    '''
    Compute similarity score between search query and documents from collection

    Args:
        lemma: str, word from the query
        relevance_dict: dict, where key (str) id of a document, value (float) its similarity
        avgdl:  float, average length of a document in the collection
        N: int, size (in documents) of the collection
        corpus_meta: dict of dicts of parametrs of texts
    '''
    try:
        doc_list = td_matrix[lemma]
    except:
        return relevance_dict
    n = len(doc_list)
    for doc in doc_list:
        n = doc_list[doc]
        dl = len(corpus_meta[doc]['text'])
        qf = n / dl
        relevance_dict[doc] += score_BM25(qf, dl, avgdl, N, n)
    return relevance_dict


def get_term_doc_matrix(text, name, matrix=defaultdict(lambda: defaultdict(int))):
    '''
    Updates term-doc matrix with a new document.

    Args:
        text: str
        name: str
        matrix: dict of dicts of ints, implementation of term-doc matrix

    Returns:
        dict of dicts of ints
    '''
    for word in text:
        matrix[word][name] += 1
    return matrix


def get_td_matrix_from_texts(texts):
    '''
    Builds term-doc matrix out of the collection of texts.

    Args:
        texts: dict, where key (str) is an id of a text, value (str) is the text itself

    Returns:
        dict of dicts of ints
    '''
    td_matrix = defaultdict(lambda: defaultdict(int))
    for name in texts:
        tokens = preprocessing(texts[name])
        td_matrix = get_term_doc_matrix(tokens, name, td_matrix)
    return td_matrix


def search_td_matrix(query, corpus, corpus_meta):
    '''
    Compute sim score between search query and all documents in collection
    Collect as pair (doc_id, score)

    Args:
        query: str
        corpus: dict (doc_id, text)

    Returns:
        dict (doc_id, score)
    '''
    relevance_dict = defaultdict(float)
    avgdl = get_avgdl(corpus)
    query = preprocessing(query)
    D = len(corpus)
    for word in query:
        relevance_dict = compute_sim(
            word, relevance_dict, avgdl, D, corpus_meta)
    return relevance_dict


with open('data/td_matrix.json', 'r', encoding='utf-8') as f:
    td_matrix = json.load(f)
