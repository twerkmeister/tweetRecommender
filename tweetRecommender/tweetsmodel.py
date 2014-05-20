from tweetRecommender.mongo import mongo
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from gensim import corpora, models, similarities
import string
import logging
import sys
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
    return mongo.db.tweets_per_hashtag.find().sort("count", -1).limit(200)    

def get_doc(hashtag):    
        doc = ""                        
        for tweet in mongo.db.tweets.find({"hashtags" : { "$in" : [hashtag] }}).limit(200):
            doc = doc + " " + tweetfilter.clean_tweet(tweet["text"].encode("utf-8"))        
        return doc                

def tokenize(text):
    return [ps.stem(w) for s in sent_tokenize(text) for w in word_tokenize(s)]

if __name__ == '__main__':    
    # Building Dictionary    
    dictionary = corpora.Dictionary(tokenize(get_doc(doc["_id"].encode("utf-8"))) for doc in subset() if not doc["_id"].encode("utf-8") in hashtag_stopwords)
    print dictionary        
    #remove terms occur only in single document
    once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq == 1]
    #remove terms length less than minimal length     
    less_ids = [dictionary.token2id[tokenid] for tokenid in dictionary.token2id if len(tokenid) <= minlength]
    dictionary.filter_tokens([dictionary.token2id[stopword] for stopword in stops if stopword in dictionary.token2id])
    dictionary.filter_tokens(once_ids + less_ids)
    dictionary.compactify()
    print dictionary    
    dictionary.save("c:\\tmp\\mongocorpus.dict")  
    count = 0  
    # Working with corpus
    corpus = MongoCorpus(dictionary)

    corpora.MmCorpus.serialize("c:\\tmp\\corpus.mm", corpus)
    mm = corpora.MmCorpus("c:\\tmp\\corpus.mm")
    print mm    
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]

    model = models.ldamodel.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=10, iterations=10000)
    model.save("c:\\tmp\\model.lda")
    print model
    print model.show_topics()
