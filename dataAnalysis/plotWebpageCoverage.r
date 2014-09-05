
source("loadData.r")

dataset <- ee2

t <- table(dataset$webpage)
barplot(t, names.arg = c(1:17), main="webpage coverage", xlab="each bar represents a webpage", ylab="#tweets evaluated for that webpage")