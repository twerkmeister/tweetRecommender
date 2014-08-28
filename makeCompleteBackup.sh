#!/bin/bash

collections=(evaluation evaluation_cache_fresh evaluation_enriched first_evaluation sample_tweets sample_webpages)

for coll in ${collections[@]}
do
  mongodump --host 172.16.22.219 -u mpss14n -p twitter -d twitter_subset -c $coll -o completeDBDump
done