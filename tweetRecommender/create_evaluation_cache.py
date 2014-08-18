from tweetRecommender.query import evaluation_run as create_cache_for

import sys

if len(sys.argv) < 2:
  print "Usage: %s <url_file>" % (sys.argv[0])
  sys.exit(1)

url_file = open(sys.argv[1])
urls = url_file.readlines()

for url in urls:
  print url
  create_cache_for(url.strip())

