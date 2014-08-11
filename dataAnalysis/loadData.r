
evaluation = read.csv("../dump/twitter_subset/evaluation.csv")
ee = read.csv("../dump/twitter_subset/evaluationEnriched.csv", header=TRUE, colClasses=c("character", "integer", "character", "character", "double", "double", "double", "double"), na.strings=c("."))
meanAveragePrecisions = read.csv("../dump/twitter_subset/meanAveragePrecisions.csv")
