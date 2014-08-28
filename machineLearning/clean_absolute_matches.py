from tweetRecommender.mongo import mongo

def get_url_matches(webpage_url):
	return mongo.coll("sample_tweets").find(
		{"full_urls": webpage_url})

def compare_content(tweet_text):
	print tweet_text
	decision = False
	user = raw_input(">>> Matching? (N|y):")
	if user == "y":
		decision = True
	return decision

def adjust_evaluation(webpage_url, tweet_objectId):
	print ">>> adjusting tweet rating ..."
	effect = mongo.coll("evaluation").update(
		{"webpage": webpage_url, "tweet": tweet_objectId}, 
		{"$set": {"rating": -1}}, multi=True)
	print ">>> ... updated %d entries" % (effect["n"])

def check_webpage(url):
	webpage = mongo.coll("sample_webpages").find_one({"url": url})

	print "-------------------------------------"
	print webpage["url"]
	print webpage["content"][:500] + "..."
	print "-------------------------------------\n"

	matching_tweets = get_url_matches(webpage["url"])
	for tweet in matching_tweets:
		if (mongo.coll("evaluation").find({"webpage": webpage["url"], 
			"tweet": str(tweet["_id"]), "rating": 1}).count() == 0):
			continue
		decision = compare_content(tweet["text"])
		if decision:
			adjust_evaluation(webpage["url"], str(tweet["_id"]))

def main():
	with file("urls.txt") as _input:
		urls = _input.read().split("\n")
		for url in urls:
			check_webpage(url)

if __name__ == '__main__':
    import sys
    sys.exit(main())