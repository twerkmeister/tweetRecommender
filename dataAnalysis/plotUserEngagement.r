source("loadData.r")

dataset <- ee2

t <- table(dataset$uid)
barplot(t, ylab="#tweets evaluated", xlab="each bar represents a single user", axisnames = FALSE, main="user engagement")