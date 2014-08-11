#!/bin/sh

mongoexport --host localhost -u mpss14n -p twitter -d twitter_subset -c evaluation_enriched --csv --fields webpage,rating,tweet,uid,scores.lda_cossim,scores.language_model,scores.text_overlap,tweet_length > `dirname $0`/../dump/twitter_subset/evaluationEnriched.csv