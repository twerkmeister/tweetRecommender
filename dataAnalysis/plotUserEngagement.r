source("loadData.r")

dataset <- e2

t <- table(dataset$uid)
barplot(t, ylab="#tweets evaluated", xlab="users", axisnames = FALSE)