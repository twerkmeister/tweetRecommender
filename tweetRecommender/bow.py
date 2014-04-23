from tweetRecommender.mongo import mongo
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from gensim import corpora, models, similarities
import string
import logging

class MongoCorpus(object):
	def __init__(self, dictionary):
		self.dictionary = dictionary

	def __iter__(self):
		for doc in subset():
			yield dictionary.doc2bow(tokenize(doc))

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

ps = PorterStemmer()
stops = stopwords.words('english')
stops.extend(["'re", "n't", "'s"])
stops.extend(string.punctuation)

def subset():
	return mongo.db.sample_webpages.find()

def tokenize(doc):
	return [ps.stem(w) for s in sent_tokenize(doc["content"].lower()) for w in word_tokenize(s)]

if __name__ == '__main__':
	# Building Dictionary
	dictionary = corpora.Dictionary(tokenize(doc) for doc in subset())
	print dictionary
	dictionary.filter_tokens([dictionary.token2id[stopword] for stopword in stops if stopword in dictionary.token2id])
	dictionary.compactify()
	print dictionary

	dictionary.save("tmp/mongocorpus.dict")

	# Working with corpus
	corpus = MongoCorpus(dictionary)

	corpora.MmCorpus.serialize("tmp/corpus.mm", corpus)
	mm = corpora.MmCorpus("tmp/corpus.mm")
	print mm

	tfidf = models.TfidfModel(corpus)
	corpus_tfidf = tfidf[corpus]

	model = models.ldamodel.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=10, iterations=10000)
	model.save("tmp/model.lda")
	print model
	print model.show_topics()
