source("loadData.r")
par(mfrow=c(1,2))
names = c("lda", "language model")

dataset <- ee2

normalized = data.frame(dataset[[2]], (dataset[[5]]-mean(dataset[[5]], na.rm=T)) / sd(dataset[[5]], na.rm=T), (dataset[[6]]-mean(dataset[[6]], na.rm=T)) / sd(dataset[[6]], na.rm=T))


means = c(aggregate(normalized[1], by=normalized[2], FUN=mean), aggregate(normalized[1], by=normalized[3], FUN=mean))
plot(normalized[[2]], normalized[[1]], main=names[1], ylab="label", xlab=paste("normalized", names[1],"score"))
lines(means[[1]], means[[2]])
plot(normalized[[3]], normalized[[1]], main=names[2], ylab="label", xlab=paste("normalized", names[2],"score"))
lines(means[[3]], means[[4]])