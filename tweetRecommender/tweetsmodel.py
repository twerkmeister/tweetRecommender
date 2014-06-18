from tweetRecommender.mongo import mongo
from tweetRecommender.tokenize import tokenize
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from gensim import corpora, models
import os.path
import string
import logging
import tweetfilter

count = 0

hashtag_stopwords = ["Jobs", "job", "jobs", "hiring", "ebook", "Job" 
                     "Anonymous", "jobs4u", "TweetMyJobs", "hiring","GetAllJobs"
                     ,"rt"]

class MongoCorpus(object):
    def __init__(self, dictionary):
        self.dictionary = dictionary

    def __iter__(self):
        for doc in subset():
            if not doc["_id"].encode("utf-8") in hashtag_stopwords:        
                yield dictionary.doc2bow(tokenize(get_doc(doc["_id"].encode("utf-8"))))

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
minlength = 3
ps = PorterStemmer()
stops = stopwords.words('english')
stops.extend(["'re", "n't", "'s"])
stops.extend(string.punctuation)


def subset():
    return mongo.db.tweets_per_hashtag.find().sort("count", -1)    

def get_doc(hashtag):    
        doc = ""                        
        for tweet in mongo.db.tweets.find({"hashtags" : { "$in" : [hashtag] }}):
            doc = doc + " " + tweetfilter.clean_tweet(tweet["text"].encode("utf-8"))        
        return doc                

def create_model_lda(dictionary, corpus,  path, overwrite=False):
    if os.path.isfile(path) and not overwrite:
        return models.LdaModel.load(path)

    model = models.LdaModel(corpus = corpus, num_topics = 100, id2word = dictionary)
    model.save(path)
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
