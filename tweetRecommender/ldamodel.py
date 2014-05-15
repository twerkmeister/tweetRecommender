from tweetRecommender.mongo import mongo
from tweetRecommender.config import config
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from gensim import corpora, models, similarities
import string
import logging
import os.path

MALLET_PATH = "/home/christian/mallet-2.0.7/bin/mallet"

class MongoCorpus(object):
    def __init__(self, dictionary):
        self.dictionary = dictionary

    def __iter__(self):
        for doc in subset():
            yield dictionary.doc2bow(tokenize(doc))

ps = PorterStemmer()

def subset():
    return mongo.db.sample_webpages_training.find()

def tokenize(doc):
    return [ps.stem(w) 
            for s in sent_tokenize(doc["content"].encode("ascii", "ignore").lower()) 
            for w in word_tokenize(s)]

def create_model_mallet(dictionary, corpus, path, overwrite=False):
    if os.path.isfile(path) and not overwrite:
        return models.LdaMallet.load(path)

    model = models.LdaMallet(MALLET_PATH, corpus=corpus, id2word=dictionary, num_topics=100, iterations=10)
    model.save("tmp/news_mallet_model.model")
    return model

def create_model_lda(dictionary, corpus):
    model = models.LdaModel(corpus = corpus, num_topics = 100, id2word = dictionary)
    model.save("tmp/news_lda_model.model")
    return model

def create_dictionary(path, overwrite=False):
    if os.path.isfile(path) and not overwrite:
        return corpora.Dictionary.load(path)

    stops = stopwords.words('english')
    stops.extend(["'re", "n't", "'s"])
    stops.extend(string.punctuation)

    minlength = 3

    dictionary = corpora.Dictionary(tokenize(doc) for doc in subset())
    #remove terms occur only in single document
    once_ids = [tokenid for tokenid, docfreq 
                        in dictionary.dfs.iteritems() 
                        if docfreq == 1]
    #remove terms length less than minimal length   
    less_ids = [dictionary.token2id[tokenid] for tokenid 
                                            in dictionary.token2id 
                                            if len(tokenid) <= minlength]
    #remove stop words
    stop_ids = [dictionary.token2id[stopword] for stopword 
                                            in stops 
                                            if stopword in dictionary.token2id]
    dictionary.filter_tokens(once_ids + less_ids + stop_ids)
    dictionary.compactify()
    dictionary.save(path)
    return dictionary

def create_corpus(path, overwrite=False):
    if os.path.isfile(path) and not overwrite:
        return corpora.MmCorpus(corpus_path)

    corpus = MongoCorpus(dictionary)
    corpora.MmCorpus.serialize(path, corpus)
    return corpus

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', 
                        level=logging.INFO)

    dict_path = config["lda"]["dict_path"]
    corpus_path = config["lda"]["corpus_path"]
    model_path = config["lda"]["model_path"]

    dictionary = create_dictionary(dict_path)
    corpus = create_corpus(corpus_path)

    model = create_model_mallet(dictionary, corpus, model_path)
