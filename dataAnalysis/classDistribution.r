source("loadData.r")
par(mfrow=c(1,2))
#par(mfrow=c(1,2))
names = c("lda", "language model")

dataset <- ee2

normalized = data.frame(dataset[[2]], (dataset[[5]]-mean(dataset[[5]], na.rm=T)) / sd(dataset[[5]], na.rm=T), (dataset[[6]]-mean(dataset[[6]], na.rm=T)) / sd(dataset[[6]], na.rm=T))
#normalized = data.frame(dataset[[2]], (dataset[[5]]-mean(dataset[[5]], na.rm=T)) / sd(dataset[[5]], na.rm=T), (dataset[[6]]-mean(dataset[[6]], na.rm=T)) / sd(dataset[[6]], na.rm=T), (dataset[[7]]-mean(dataset[[7]], na.rm=T)) / sd(dataset[[7]], na.rm=T))
colnames(normalized) <- c("rating", "lda", "lm")
#colnames(normalized) <- c("rating", "lda", "lm", "to")

pos = normalized[normalized$rating==1,]
neg = normalized[normalized$rating==-1,]
pos_density_lda <- aggregate(pos[1], by=pos[2], FUN=sum)
neg_density_lda <- aggregate(-neg[1], by=neg[2], FUN=sum)
pos_density_lm <- aggregate(pos[1], by=pos[3], FUN=sum)
neg_density_lm <- aggregate(-neg[1], by=neg[3], FUN=sum)
#pos_density_to <- aggregate(pos[1], by=pos[4], FUN=sum)
#neg_density_to <- aggregate(-neg[1], by=neg[4], FUN=sum)

#means = c(aggregate(normalized[1], by=normalized[2], FUN=mean), aggregate(normalized[1], by=normalized[3], FUN=mean))
#plot(normalized[[2]], normalized[[1]], main=names[1], ylab="label", xlab=paste("normalized", names[1],"score"))
#lines(means[[1]], means[[2]])
#plot(normalized[[3]], normalized[[1]], main=names[2], ylab="label", xlab=paste("normalized", names[2],"score"))
#lines(means[[3]], means[[4]])

lo_pos_lda <- loess(pos_density_lda[[2]]~pos_density_lda[[1]])
lo_neg_lda <- loess(neg_density_lda[[2]]~neg_density_lda[[1]])
lo_pos_lm <- loess(pos_density_lm[[2]]~pos_density_lm[[1]])
lo_neg_lm <- loess(neg_density_lm[[2]]~neg_density_lm[[1]])
#lo_pos_to <- loess(pos_density_to[[2]]~pos_density_to[[1]])
#lo_neg_to <- loess(neg_density_to[[2]]~neg_density_to[[1]])

plot(pos_density_lda[[1]], lo_pos_lda$fitted,ylim=c(0,5), type="l", lwd=2, col="blue", ylab="label density", xlab="standardized lda score")
lines(neg_density_lda[[1]], lo_neg_lda$fitted, lwd=2, col="red")
legend(0,5, legend=c("pos", "neg"), fill=c("blue", "red"))

plot(pos_density_lm[[1]], lo_pos_lm$fitted, ylim=c(0,5),type="l", lwd=2, col="blue", ylab="label density", xlab="standardized lm score")
lines(neg_density_lm[[1]], lo_neg_lm$fitted, lwd=2, col="red")
legend(0,5, legend=c("pos", "neg"), fill=c("blue", "red"))

#plot(pos_density_to[[1]], lo_pos_to$fitted, ylim=c(0,5), type="l", lwd=2, col="blue", ylab="label density", xlab="standardized to score")
#lines(neg_density_to[[1]], lo_neg_to$fitted, lwd=2, col="red")
#legend(1,5, legend=c("pos", "neg"), fill=c("blue", "red"))



