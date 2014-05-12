db = connect("127.0.0.1:27017/twitter_subset");
db.auth("mpss14n", "twitter")

webpages = db.sample_webpages.find({"created_at": {$exists: 0}})

while(webpages.hasNext()){
  webpage = webpages.next()
  tweets = db.sample_tweets.find({full_urls: webpage.url}, {created_at: 1}).limit(1).sort({created_at: 1})
  if(tweets.hasNext()){
    tweet = tweets.next()
    webpage.created_at = tweet.created_at
    db.sample_webpages.save(webpage)
  }
  else {
    print("did not find matching tweet for: ", webpage.url)
  }

}