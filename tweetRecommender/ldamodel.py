
from tweetRecommender.mongo import mongo
from tweetRecommender.config import config
from tweetRecommender.tokenize import get_terms

from gensim import corpora, models
import string
import logging
import os.path
import functools32
import numpy

logging.basicConfig(
    filename='ldamodel.log',
    level = logging.INFO,
    format = "[%(levelname)s] %(message)s",
)
LOG = logging.getLogger('tweetRecommender.ldamodel')

MALLET_PATH = "/home/christian/mallet-2.0.7/bin/mallet"

CORPUS_PATH = os.path.join(os.path.dirname(__file__), config["lda"]["corpus_path"])
DICT_PATH = os.path.join(os.path.dirname(__file__), config["lda"]["dict_path"])
MODEL_PATH = os.path.join(os.path.dirname(__file__), config["lda"]["model_path"])

class MongoCorpus(object):
    def __init__(self, dictionary):
        self.dictionary = dictionary

    def __iter__(self):
        for doc in get_test_set():
            yield dictionary.doc2bow(tokenize(doc))


@functools32.lru_cache() 
def get_lda():
    return models.LdaModel.load(MODEL_PATH)
    
@functools32.lru_cache() 
def get_dictionary(): #redundancy for scoring    
    return create_dictionary(DICT_PATH)

def get_training_set():
    return mongo.db.sample_webpages_training.find()

def get_test_set():
    return mongo.db.sample_webpages_test.find()

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

    NUM_TOPICS = 10
    LOG.info("\n~~~~~~~~~~\nStarting new LDA model training run with # topics: %d\n~~~~~~~~~~\n" % (NUM_TOPICS))

    model = models.LdaModel(corpus = corpus, id2word = dictionary, num_topics = NUM_TOPICS)#passes=2, iterations=200, eval_every=1
    #model.save(path)
    test_corpus = create_test_corpus()
    perplexity = numpy.exp2(-model.bound(corpus = test_corpus) / sum(cnt for document in test_corpus for _, cnt in document))
    LOG.info("Perplexity calculated using LdaModel.bound(): %f" % (perplexity))
    return model

def create_dictionary(path, overwrite=False):
    if os.path.isfile(path) and not overwrite:
        return corpora.Dictionary.load(path)

    dictionary = corpora.Dictionary(tokenize(doc) for doc in get_training_set())
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

def create_test_corpus():
    path = "/home/christian/tweetRecommender/tmp/news_corpus_test.mm"

    if os.path.isfile(path):
        return corpora.MmCorpus(path)

    dictionary = create_dictionary(DICT_PATH)
    corpus = MongoCorpus(dictionary)
    corpora.MmCorpus.serialize(path, corpus)
    return corpus

if __name__ == '__main__':
    dictionary = create_dictionary(DICT_PATH)
    corpus = create_corpus(CORPUS_PATH)
    model = create_model_lda(dictionary, corpus, MODEL_PATH)
