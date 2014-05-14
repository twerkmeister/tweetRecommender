from app import app
from flask import render_template, request, url_for, redirect

from tweetRecommender.query import run as recommend

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
			tweets = recommend(url, 'urlmatching', 'follower_count', 'sample_tweets', 'sample_webpages')
			return render_template('result.html', url=url, tweets=tweets)
		except Exception, e:
			return render_template('result.html', url=e)
		