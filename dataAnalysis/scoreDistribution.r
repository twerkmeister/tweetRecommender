
source("loadData.r")
par(mfrow=c(1,2))

dataset <- ee2

names = c("lda", "language model")
unique_pairs = dataset[!duplicated(data.frame(dataset$webpage, dataset$tweet)),]

for(i in 5:6){
  hist((unique_pairs[[i]]-mean(unique_pairs[[i]], na.rm=T)) / sd(unique_pairs[[i]], na.rm=T), breaks=100, main=names[i-4], ylab="count", xlab=paste("normalized",names[i-4], "score"))
}
