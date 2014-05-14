from app import app
from flask import render_template, request, url_for, redirect

from tweetRecommender.mongo import mongo
from tweetRecommender.query import query as recommend
from tweetRecommender.gather.urlmatching import gather
from tweetRecommender.rank.follower_count import score

@app.route("/", methods=['GET'])
def home():
    return redirect(url_for('query'))

@app.route("/query", methods=['GET', 'POST'])
def query():
	if request.method == 'GET':
		return render_template('query.html')
	if request.method == 'POST':	
		url = request.form.get('url')
		try:
			tweets_coll = mongo.db['sample_tweets']
			webpages_coll = mongo.db['sample_webpages']
			tweets = recommend(url, gather, score, tweets_coll, webpages_coll)
			print len(tweets)
			return render_template('result.html', url=url, tweets=tweets)
		except Exception, e:
			return render_template('result.html', url=e)
		