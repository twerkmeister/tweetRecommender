var retweet_ids = {};
var original_ids = {}
var tweets = db.sample_tweets;

var retweets = tweets.find({retweeted_status: {$exists: 1}});
print("Collecting RTs..");
while (retweets.hasNext()) {
    var tweet = retweets.next();
    retweet_ids[tweet['tweet_id']] = 1;
    original_ids[tweet['retweeted_status']['id']] = 1;
}
print("Searching..");
for (id in original_ids) {
    if (!original_ids.hasOwnProperty(id)) { continue; }  // not an entry
    if (retweet_ids[id] == 1) {
        print("RT RT! " + id);
    }
}
