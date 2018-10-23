from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from preprocessing import preprocessing
import numpy as np
import json


def save_d2v_base(texts, file_name):
    '''
    Computes doc2vec vectors of each text and stores them into file.

    Args:
        texts: dict, where key (str) is an id of a text, value (str) is the text itself
        file_name: str
    '''
    output_array = []
    for name in texts:
        new_item = {}
        new_item['id'] = name
        new_item['vector'] = get_d2v_vectors(texts[name]).tolist()
        output_array.append(new_item)
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(output_array, f, ensure_ascii=False, indent=4)


def train_doc2vec(texts, filename='doc2vec'):
    '''
    Trains and saves a doc2vec mode on a given data.

    Args:
        texts: dict, where key (str) is an id of a text, value (str) is the text itself
        filename: str
    '''
    preprocessed_texts = []
    for id_ in texts:
        preprocessed_texts.append(TaggedDocument(
            words=preprocessing(texts[id_], stopwords_), tags=[id_]))
    print('preprocessing is done')
    model = Doc2Vec(vector_size=300, min_count=3, alpha=0.25,
                    min_alpha=0.025, epochs=100, workers=4, dm=1)
    model.build_vocab(preprocessed_texts)
    print(len(model.wv.vocab))

    model.train(preprocessed_texts, total_examples=model.corpus_count,
                epochs=model.epochs, report_delay=60)
    model.save(filename + '.model')


def get_d2v_vector(text, stopwords=None):
    '''
    Translates text into vector using doc2vec model.

    Args:
        text: str

    Returns:
        numpy.ndarray
    '''
    preprocessed = preprocessing(text, stopwords=stopwords)
    return d2v_model.infer_vector(preprocessed)


d2v_model_path = "models/d2v.model"
d2v_model = Doc2Vec.load(d2v_model_path)

d2v_vectors_path = 'data/avito_d2v.json'
with open(d2v_vectors_path, 'r', encoding='utf-8') as f:
    d2v_vectors = json.load(f)
    d2v_vectors = {w['id']: np.array(w['vector']) for w in d2v_vectors}
