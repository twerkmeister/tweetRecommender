
evaluation = read.csv("../dump/twitter_subset/evaluation.csv")
e2 = read.csv("../dump/twitter_subset/evaluation2.csv", header=TRUE, colClasses=c("character", "integer", "character", "character"))
ee = read.csv("../dump/twitter_subset/evaluationEnriched.csv", header=TRUE, colClasses=c("character", "integer", "character", "character", "double", "double", "double"), na.strings=c("."))
ee2 = read.csv("../dump/twitter_subset/evaluationEnriched2.csv", header=TRUE, colClasses=c("character", "integer", "character", "character", "double", "double", "double", "double", "logical", "double", "double", "double", "double", "double", "double", "double", "double", "logical", "double", "double"), na.strings=c("."))

meanAveragePrecisions = read.csv("../dump/twitter_subset/meanAveragePrecisions.csv")
