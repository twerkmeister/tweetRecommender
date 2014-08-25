
source("loadData.r")

dataset <- e2

meanTweetScore = aggregate(dataset[2], by=dataset[3], FUN=mean)
ordering = order(meanTweetScore[2])
barplot(meanTweetScore[2][ordering,], ylab="Average Tweet Score", las = 1)
# savePlot("aggreementGraph.png")