
source("loadData.r")
par(mfrow=c(1,1))
dataset <- ee2

meanTweetScore = aggregate(dataset[2], by=dataset[3], FUN=mean)
ordering = order(meanTweetScore[2])

t <- table(meanTweetScore[2])
totalNegative <- t[names(t)==-1]
totalPositive <- t[names(t)==1]
undecided <- t[names(t) == 0]
other <- length(meanTweetScore[[2]]) - totalNegative - totalPositive - undecided

label <- paste("#:", length(meanTweetScore[[2]]), "#-1:", totalNegative, "#1:", totalPositive, "#0:", undecided, "rest:", other)

barplot(meanTweetScore[2][ordering,], ylab="Average Tweet Rating", las = 1, xlab=label, main="user agreement per tweet")
# savePlot("aggreementGraph.png")