
source("loadData.r")

dataset <- e2

t <- table(dataset$webpage)
barplot(t, names.arg = c(1:17))