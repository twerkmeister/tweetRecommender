#!/bin/bash

rsync -avz --filter=':- .gitignore' . twerkmeister@fb13-fint:/usr/lib/tweetrecommender

