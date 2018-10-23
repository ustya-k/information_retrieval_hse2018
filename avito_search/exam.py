
# coding: utf-8

import numpy as np
import json
from nltk.corpus import stopwords
import os
from gensim import matutils
from preprocessing import preprocessing
from word2vec_process import get_w2v_vector, w2v_vectors
from doc2vec_process import get_d2v_vector, d2v_vectors
from inverted_index_process import search_td_matrix


def get_corpus(path, meta=True):
    '''
    Collects corpus and its meta from file.

    Args:
        path: str
        meta: bool, if meta is needed

    Returns:
        dict (doc_id, text)
        AND dict (doc_id, dict of meta) (if meta)
    '''
    counter = 0
    texts = {}
    meta = {}
    for file in os.listdir(path):
        with open(path + file, 'r', encoding='utf-8') as f:
            d = json.load(f)
        if d['text'] is not None:
            counter += 1
            texts[d['id']] = d['text']
            meta[d['id']] = d
            meta[d['id']]['text'] = preprocessing(meta[d['id']]['text'])
    if meta:
        return texts, meta
    return texts


def similarity(v1, v2):
    '''
    Computes similarity between two vectors.

    Args:
        v1, v2: numpy.ndarray

    Returns:
        float
    '''
    v1_norm = matutils.unitvec(np.array(v1))
    v2_norm = matutils.unitvec(np.array(v2))
    return np.dot(v1_norm, v2_norm)


def search_w2v(query, vectors):
    '''
    Search for query in collection using word2vec model.

    Args:
        query: str
        vectors: dict, where key (str) is an id of a document, value (numpy.ndarray) is its vector

    Returns:
        dict, where key (str) is an id of a document, value (float) is a similarity score between the doc and the query
    '''
    query = preprocessing(query)
    query_vector = get_w2v_vector(query)
    return {v: similarity(query_vector, vectors[v]) for v in vectors}


def search_d2v(query, vectors):
    '''
    Search for query in collection using doc2vec model.

    Args:
        query: str
        vectors: dict, where key (str) is an id of a document, value (numpy.ndarray) is its vector

    Returns:
        dict, where key (str) is an id of a document, value (float) is a similarity score between the doc and the query
    '''
    query_vector = get_d2v_vector(query)
    return {v: similarity(query_vector, vectors[v]) for v in vectors}


def get_search_output(result, top):
    '''
    Gets a sorted list of dicts (text + meta) of top results.

    Args:
        result: dict, where key (str) is an id of a document, value (float) is a similarity score between the doc and the query
        top: int, desired amount of best matches

    Returns:
        list of dicts
    '''
    dicts = []
    for key in sorted(result, key=lambda x: result[x], reverse=True)[:top]:
        dicts.append(corpus_meta[key])
        dicts[-1]['text'] = corpus[key]
    return dicts


def search(query, method, top=10):
    '''
    Search for query using specified method.

    Args:
        query: str
        method: str
        top: int, desired amount of best matches

    Returns:
        list of dicts
    '''
    if method == 'inverted_index':
        result = search_td_matrix(query, corpus, corpus_meta)
    elif method == 'word2vec':
        result = search_w2v(query, w2v_vectors)
    elif method == 'doc2vec':
        result = search_d2v(query, d2v_vectors)
    else:
        raise TypeError('unsupported search method')
    output = get_search_output(result, top)
    if output == []:
        return "None"
    return output


corpus_path = 'data/ads_json/'
corpus, corpus_meta = get_corpus(corpus_path, meta=True)
