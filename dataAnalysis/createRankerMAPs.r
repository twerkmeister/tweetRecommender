
source("loadData.r")

means = lapply(meanAveragePrecisions[2:4], mean)
m = matrix(unlist(meanAveragePrecisions[2:4]), 25)
colors = c("red", "darkblue", "yellow")
legends = c("lda", "text overlap", "language model")
par(mfrow=c(2,2))
barplot(t(m), ylab="MAP", beside=TRUE, col=colors, legend=legends, space=c(0,2), names.arg=c(1:25), main="combined")
for(i in 1:3){
  barplot(m[,i], ylab="MAP", col=colors[i], main=legends[i], names.arg=c(1:25))
  lines(c(0,30), c(means[i],means[i]), lty="dotted", lwd=3)
}