source("loadData.r")
par(mfrow=c(1,3))
names = c("lda", "language model", "text overlap")

normalized = data.frame(ee[[2]], (ee[[5]]-mean(ee[[5]], na.rm=T)) / sd(ee[[5]], na.rm=T), (ee[[6]]-mean(ee[[6]], na.rm=T)) / sd(ee[[6]], na.rm=T), (ee[[7]]-mean(ee[[7]], na.rm=T)) / sd(ee[[7]], na.rm=T))


means = c(aggregate(normalized[1], by=normalized[2], FUN=mean), aggregate(normalized[1], by=normalized[3], FUN=mean), aggregate(normalized[1], by=normalized[4], FUN=mean))
plot(normalized[[2]], normalized[[1]], main=names[1], ylab="label", xlab=paste("normalized", names[1],"score"))
lines(means[[1]], means[[2]])
plot(normalized[[3]], normalized[[1]], main=names[2], ylab="label", xlab=paste("normalized", names[2],"score"))
lines(means[[3]], means[[4]])
plot(normalized[[4]], normalized[[1]], main=names[3], ylab="label", xlab=paste("normalized", names[3],"score"))
lines(means[[5]], means[[6]])