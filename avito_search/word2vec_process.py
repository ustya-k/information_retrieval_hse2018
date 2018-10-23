from gensim.models import Word2Vec
from preprocessing import preprocessing
import numpy as np
from gensim import matutils
import json


def get_w2v_vector(sentence):
    '''
    Translates sentence into vector using word2vec.

    Args:
        sentence: list of strings

    Returns:
        numpy.ndarray
    '''
    all_words, mean = set(), []

    for word in sentence:
        if word in w2v_model.wv.vocab:
            mean.append(w2v_model.wv.word_vec(word))
            all_words.add(w2v_model.wv.vocab[word].index)

    if mean == []:
        return np.zeros(w2v_model.layer1_size,)

    mean = matutils.unitvec(
        np.array(mean).mean(axis=0)).astype(np.float32)
    return mean


def get_w2v_vectors(text, merge_vectors=False):
    '''
    Translates text into vector using word2vec.

    Args:
        text: str
        merge_vectors: bool, return sentence by sentence vectors or their mean

    Returns:
        numpy.ndarray (if merge_vectors)
        OR dict, where key (str) is a sentence, value (numpy.ndarray) is a vector
    '''
    sentences = preprocessing(text, stopwords=stopwords.words('russian'))
    vectors = [get_w2v_vector(sentences)]
    if vectors == []:
        return None
    if merge_vectors:
        return matutils.unitvec(np.array(vectors).mean(axis=0)).astype(np.float32)
    return {sentence: vector for sentence, vector in zip(text, vectors)}


def save_w2v_base(texts, file_name='vector_base.json'):
    '''
    Computes word2vec vectors of each text and stores them into file.

    Args:
        texts: dict, where key (str) is an id of a text, value (str) is the text itself
        file_name: str
    '''
    output_array = []
    for name in texts:
        new_item = {}
        new_item['id'] = name
        vector = get_w2v_vectors(texts[name], merge_vectors=True)
        if vector is None:
            continue
        new_item['vector'] = vector.tolist()
        output_array.append(new_item)
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(output_array, f, ensure_ascii=False, indent=4)


w2v_model_path = "models/araneum_none_fasttextskipgram_300_5_2018.model"
w2v_model = Word2Vec.load(w2v_model_path)


w2v_vectors_path = 'data/avito_w2v.json'
with open(w2v_vectors_path, 'r', encoding='utf-8') as f:
    w2v_vectors = json.load(f)
    w2v_vectors = {w['id']: np.array(w['vector']) for w in w2v_vectors}
