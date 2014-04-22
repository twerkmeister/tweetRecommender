from tweetRecommender.mongo import mongo
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from gensim import corpora, models, similarities
import string

class MongoCorpus(object):
	def __init__(self, dictionary):
		self.dictionary = dictionary

	def __iter__(self):
		for doc in subset():
			yield dictionary.doc2bow(tokenize(doc))

ps = PorterStemmer()
stopwords = stopwords.words('english')
stopwords.extend(["'re", "n't", "'s"])

def subset():
	return mongo.db.webpages.find().skip(172).limit(1000)

def tokenize(doc):
	return [ps.stem(w) for s in sent_tokenize(doc["content"].lower()) for w in word_tokenize(s)]

if __name__ == '__main__':
	# Building Dictionary
	dictionary = corpora.Dictionary(tokenize(doc) for doc in subset())
	print dictionary
	dictionary.filter_tokens([dictionary.token2id[stopword] for stopword in stopwords if stopword in dictionary.token2id] + [dictionary.token2id[token] for token in string.punctuation if token in dictionary.token2id])
	dictionary.compactify()
	print dictionary

	dictionary.save("tmp/mongocorpus.dict")

	# Working with corpus
	corpus = MongoCorpus(dictionary)
	
	corpora.MmCorpus.serialize("tmp/corpus.mm", corpus)

	model = models.ldamodel.LdaModel(corpus, id2word=dictionary, num_topics=10)
	model.print_topics(2)
