from app import app
from flask import render_template, request, url_for, redirect

@app.route("/", methods=['GET'])
def home():
    return redirect(url_for('query'))

@app.route("/query", methods=['GET', 'POST'])
def query():
	if request.method == 'GET':
		return render_template('query.html')
	if request.method == 'POST':	
		url = request.form.get('url')
		return render_template('result.html', url=url)