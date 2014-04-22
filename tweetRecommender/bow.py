from tweetRecommender.mongo import mongo
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from gensim import corpora, models, similarities
import string

class MongoCorpus(object):
	def __init__(self):
		self.ps = PorterStemmer()
		self.stopwords = stopwords.words('english')
		self.stopwords.extend(["'re", "n't", "'s"])
	
	def __iter__(self):
		for doc in mongo.db.webpages.find().skip(172).limit(1):
			yield [w.lower() for s in sent_tokenize(doc["content"]) for w in word_tokenize(s) if not (w in string.punctuation) and not (w.lower() in self.stopwords)]

if __name__ == '__main__':
	corpus = MongoCorpus()
	texts = []
	for doc in corpus:
		print len(doc)
		texts.append(doc)
		#print doc
		#pass

	dictionary = corpora.Dictionary(texts)
	print dictionary