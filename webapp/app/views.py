from tweetRecommender.query import run as recommend
from tweetRecommender.mongo import mongo

from app import app
from flask import render_template, request, url_for, redirect

from random import randint

@app.route("/", methods=['GET'])
def home():
    return redirect(url_for('query'))

@app.route("/query", methods=['GET', 'POST'])
def query():
	if request.method == 'GET':
		return render_template('query.html')

	if request.method == 'POST':	
		limit = int(request.form.get('limit'))
		gather = request.form.get('gather')
		ranking = request.form.get('ranking')
		action = request.form.get('action')

		try:
			if action == "search":
				url = request.form.get('url')

				tweets = recommend(url, gather, [ranking], ['expected_time'],
                                        ['user.screen_name', 'created_at', 'text'],
					'sample_tweets', 'sample_webpages', limit)
				return render_template('result.html', url=url, tweets=tweets)

			elif action == "random":
				random_max = mongo.db["sample_webpages"].count() - 1
				random_webpage = mongo.db["sample_webpages"].find().skip(
					randint(0,random_max)).limit(1)[0]
				url = random_webpage.get('url')

				tweets = recommend(url, gather, [ranking], 
					'sample_tweets', 'sample_webpages', limit)
				return render_template('result.html', url=url, tweets=tweets)

		except Exception, e:
			return render_template('result.html', url=e)
		