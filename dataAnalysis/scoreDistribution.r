
source("loadData.r")
par(mfrow=c(1,3))

names = c("lda", "language model", "text overlap")
unique_pairs = ee[!duplicated(data.frame(ee$webpage, ee$tweet)),]

for(i in 5:7){
  hist((unique_pairs[[i]]-mean(unique_pairs[[i]], na.rm=T)) / sd(unique_pairs[[i]], na.rm=T), breaks=100, main=names[i-4], ylab="count", xlab=paste("normalized",names[i-4], "score"))
}
