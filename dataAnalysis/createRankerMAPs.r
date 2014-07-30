
source("loadData.r")

m = matrix(unlist(meanAveragePrecisions[2:4]), 25)
par(mfrow=c(2,2))
barplot(t(m), ylab="MAP", beside=TRUE, col=c("red", "darkblue", "yellow"), legend=c("lda", "text overlap", "language model"), space=c(0,2), names.arg=c(1:25), main="combined")
barplot(m[,1], ylab="MAP", col="red", main="lda", names.arg=c(1:25))
barplot(m[,2], ylab="MAP", col="darkblue", main="text overlap", names.arg=c(1:25))
barplot(m[,3], ylab="MAP", col="yellow", main="language model", names.arg=c(1:25))