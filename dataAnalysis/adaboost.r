
source("loadData.r")

library(adabag)

normalized = data.frame(ee[[2]], (ee[[5]]-mean(ee[[5]], na.rm=T)) / sd(ee[[5]], na.rm=T), (ee[[6]]-mean(ee[[6]], na.rm=T)) / sd(ee[[6]], na.rm=T), (ee[[7]]-mean(ee[[7]], na.rm=T)) / sd(ee[[7]], na.rm=T))

real <- data.frame(ee$webpage,ee$scores.lda_cossim, ee$scores.language_model, ee$scores.text_overlap, ee$rating)

colnames(real) <- c("webpage", "lda", "lm", "text_overlap", "rating")
real$rating <- apply(real, 1, function(row){if(row["rating"] == -1) 0 else 1})

real$rating <- factor(real$rating)
real <- real[complete.cases(real),]

uniqueWebpages <- unique(ee$webpage)
sortedWebpages <- uniqueWebpages[order(uniqueWebpages)]

split <- 20
trainingWebpages <- sortedWebpages[1:split]
testWebpages <- sortedWebpages[split+1:length(sortedWebpages)]

trainingSet <- subset(real, webpage %in% trainingWebpages)
testSet <- subset(real, webpage %in% testWebpages)

trainingSet.logistic <- glm(rating ~ lda + lm + text_overlap, data=trainingSet[,-1], family=binomial("logit"))
testSet.logistic.pred <- predict(trainingSet.logistic, newdata=testSet[,-1], type="response")
trainingSet.logistic.pred <- predict(trainingSet.logistic, newdata=trainingSet[,-1], type="response")
summary(trainingSet.logistic)

trainingSet.logistic_lda <- glm(rating ~ lda, data=trainingSet[,-1], family=binomial("logit"))
testSet.logistic_lda.pred <- predict(trainingSet.logistic_lda, newdata=testSet[,-1], type="response")
trainingSet.logistic_lda.pred <- predict(trainingSet.logistic_lda, newdata=trainingSet[,-1], type="response")

trainingSet.logistic_lm <- glm(rating ~ lm, data=trainingSet[,-1], family=binomial("logit"))
testSet.logistic_lm.pred <- predict(trainingSet.logistic_lm, newdata=testSet[,-1], type="response")
trainingSet.logistic_lm.pred <- predict(trainingSet.logistic_lm, newdata=trainingSet[,-1], type="response")

trainingSet.logistic_to <- glm(rating ~ text_overlap, data=trainingSet[,-1], family=binomial("logit"))
testSet.logistic_to.pred <- predict(trainingSet.logistic_to, newdata=testSet[,-1], type="response")
trainingSet.logistic_to.pred <- predict(trainingSet.logistic_to, newdata=trainingSet[,-1], type="response")

trainingSet.adaboost <- boosting(rating ~., data=trainingSet[,-1], mfinal=20, boos=FALSE, control=rpart.control(maxdepth=3))
testSet.adaboost.pred <- predict.boosting(trainingSet.adaboost, newdata=testSet[,-1])
trainingSet.adaboost.pred <- predict.boosting(trainingSet.adaboost, newdata=trainingSet[,-1])
threshold <- 0.5

table(trainingSet.logistic.pred > threshold, trainingSet$rating)
table(trainingSet.logistic_lda.pred >threshold, trainingSet$rating)
table(trainingSet.logistic_lm.pred > threshold, trainingSet$rating)
table(trainingSet.logistic_to.pred > threshold, trainingSet$rating)
trainingSet.adaboost.pred$confusion

table(testSet.logistic.pred > threshold, testSet$rating)
table(testSet.logistic_lda.pred >threshold, testSet$rating)
table(testSet.logistic_lm.pred > threshold, testSet$rating)
table(testSet.logistic_to.pred > threshold, testSet$rating)
testSet.adaboost.pred$confusion
