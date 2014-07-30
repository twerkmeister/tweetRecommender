
source("loadData.r")

means = lapply(meanAveragePrecisions[2:4], mean)
barplot(unlist(means), ylab="MMAP", ylim=c(0,1), names.arg=c("lda", "text overlap", "language model"))