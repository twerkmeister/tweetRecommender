

mongo -u mpss14n -p twitter 172.16.22.219/twitter_subset `dirname $0`/../mongoscripts/rename_rankers.js
mongoexport --host 172.16.22.219 -u mpss14n -p twitter -d twitter_subset -c evaluation_cache_advanced --csv --fields query_url,eval.map.lda_cossim,eval.map.text_overlap_and_normalized_follower_count,eval.map.language_model > `dirname $0`/../dump/twitter_subset/meanAveragePrecision.csv