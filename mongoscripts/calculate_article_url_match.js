db.sample_tweets.aggregate(
    { 
	$group : {_id : "$full_urls", total : { $sum : 1 }}
    },
    {
	$sort : { total : -1 }
    }
  );