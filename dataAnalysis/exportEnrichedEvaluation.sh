#!/bin/sh

mongoexport --host 72.16.22.219 -u mpss14n -p twitter -d twitter_subset -c evaluation_enriched --csv --fields webpage,rating,tweet,uid,scores.lda_cossim,scores.language_model,scores.text_overlap > `dirname $0`/../dump/twitter_subset/evaluationEnriched.csv