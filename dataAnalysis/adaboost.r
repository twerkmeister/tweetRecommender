
source("loadData.r")

library(adabag)

normalized = data.frame(ee[[2]], (ee[[5]]-mean(ee[[5]], na.rm=T)) / sd(ee[[5]], na.rm=T), (ee[[6]]-mean(ee[[6]], na.rm=T)) / sd(ee[[6]], na.rm=T), (ee[[7]]-mean(ee[[7]], na.rm=T)) / sd(ee[[7]], na.rm=T))

real <- data.frame(ee$webpage,ee$scores.lda_cossim, ee$scores.language_model, ee$scores.text_overlap, ee$tweet_length, ee$rating)
colnames(real) <- c("webpage", "lda", "lm", "text_overlap", "tweet_length", "rating")
real$rating <- factor(real$rating)
real <- real[complete.cases(real),]

for(i in 2:4){
  real[[i]] <- (real[[i]] - mean(real[[i]])) / sd(real[[i]]) 
}

uniqueWebpages <- unique(ee$webpage)
sortedWebpages <- uniqueWebpages[order(uniqueWebpages)]

split <- 20
trainingWebpages <- sortedWebpages[1:split]
testWebpages <- sortedWebpages[split+1:length(sortedWebpages)]

trainingSet <- subset(real, webpage %in% trainingWebpages)
testSet <- subset(real, webpage %in% testWebpages)

trainingSet.adaboost <- boosting(rating ~., data=trainingSet[,-1], mfinal=20, boos=FALSE, control=rpart.control(maxdepth=3))
testSet.adaboost.pred <- predict.boosting(trainingSet.adaboost, newdata=testSet[,-1])

testSet.adaboost.pred$confusion
