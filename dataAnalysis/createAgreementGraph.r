
source("loadData.r")

meanTweetScore = aggregate(evaluation[2], by=evaluation[3], FUN=mean)
ordering = order(meanTweetScore[2])
barplot(meanTweetScore[2][ordering,], ylab="Average Tweet Score", las = 1)
# savePlot("aggreementGraph.png")