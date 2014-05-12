def gather(url, tweets, webpages):
    return tweets.find({"urls": url})
