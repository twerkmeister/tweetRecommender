
from tweetRecommender.mongo import mongo
from tweetRecommender.config import config
from tweetRecommender.tokenize import get_terms

from gensim import corpora, models
import string
import logging
import os.path
import functools32

LOG = logging.basicConfig(
        level = logging.INFO,
        format = "[%(levelname)s] %(message)s",
    )

MALLET_PATH = "/home/christian/mallet-2.0.7/bin/mallet"

CORPUS_PATH = os.path.join(os.path.dirname(__file__), config["lda"]["corpus_path"])
DICT_PATH = os.path.join(os.path.dirname(__file__), config["lda"]["dict_path"])
MODEL_PATH = os.path.join(os.path.dirname(__file__), config["lda"]["model_path"])

class MongoCorpus(object):
    def __init__(self, dictionary):
        self.dictionary = dictionary

    def __iter__(self):
        for doc in subset():
            yield dictionary.doc2bow(tokenize(doc))


@functools32.lru_cache() 
def get_lda():
    return models.LdaModel.load(MODEL_PATH)
    
@functools32.lru_cache() 
def get_dictionary(): #redundancy for scoring    
    return create_dictionary(DICT_PATH)

def subset():
    return mongo.db.sample_webpages_training.find()

def tokenize(doc):
    return get_terms(doc['content'].encode('utf-8'))

def create_model_mallet(dictionary, corpus, path, overwrite=False):
    if os.path.isfile(path) and not overwrite:
        return models.LdaMallet.load(path)

    model = models.LdaMallet(MALLET_PATH, corpus=corpus, id2word=dictionary, num_topics=100)
    model.save(path)
    return model

def create_model_lda(dictionary, corpus,  path, overwrite=False):
    if os.path.isfile(path) and not overwrite:
        return models.LdaModel.load(path)

    model = models.LdaModel(corpus = corpus, num_topics = 100, id2word = dictionary, passes=2, iterations=200)
    model.save(path)
    return model

def create_dictionary(path, overwrite=False):
    if os.path.isfile(path) and not overwrite:
        return corpora.Dictionary.load(path)

    dictionary = corpora.Dictionary(tokenize(doc) for doc in subset())
    #remove terms occur only in single document
    once_ids = [tokenid for tokenid, docfreq 
                        in dictionary.dfs.iteritems() 
                        if docfreq == 1]
    #remove terms length less than minimal length   
    less_ids = [dictionary.token2id[tokenid] for tokenid 
                                            in dictionary.token2id 
                                            if len(tokenid) <= 3]

    dictionary.filter_tokens(once_ids + less_ids)
    dictionary.compactify()
    dictionary.save(path)
    return dictionary

def create_corpus(path, overwrite=False):
    if os.path.isfile(path) and not overwrite:
        return corpora.MmCorpus(path)

    corpus = MongoCorpus(dictionary)
    corpora.MmCorpus.serialize(path, corpus)
    return corpus

if __name__ == '__main__':
    dictionary = create_dictionary(DICT_PATH)
    corpus = create_corpus(CORPUS_PATH)
    model = create_model_lda(dictionary, corpus, MODEL_PATH)
