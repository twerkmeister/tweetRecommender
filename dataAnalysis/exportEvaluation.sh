#!/bin/sh

mongoexport --host localhost -u mpss14n -p twitter -d twitter_subset -c evaluation --csv --fields webpage,rating,tweet,uid > `dirname $0`/../dump/twitter_subset/evaluation2.csv