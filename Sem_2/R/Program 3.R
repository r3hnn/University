data <- read.csv(("C:\\Users\\rehan\\AppData\\Local\\Packages\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm\\LocalState\\sessions\\81212264D0BB4AECC69930381B2B99B11621FFE3\\transfers\\2026-12\\Missing_values.csv"))
print("Original Data:")
print(data)

print("Number of na values in each column: ")
print(colSums(is.na(data)))

numeric_cols <- sapply(data, is.numeric)
print("numeric Columns:")
print(numeric_cols)

print("Mean Values (Ignoring NA): ")
mean_values <- colMeans(data[, numeric_cols], na.rm = TRUE)
print(mean_values)

par(mar = c(5,4,4,2))
hist(data$Salary,
	main = "Salary Distribution",
	xlab = "Salary",
	col = "lightgreen")

for (i in colnames(data)) {
	if (is.numeric(data[[i]])) {
		mean_values <- mean(data[[i]], na.rm = TRUE)
		data[[i]][is.na(data[[i]])] <- mean_values
	}
}

print("Data After Imputation:")
print(data)

print("Mean after imputation: ")
new_mean <- colMeans(data[, numeric_cols])
print(new_mean)

hist(data$Salary,
	main = "Salary Distribution After Imputation",
	xlab = "Salary",
	col = "pink",)

boxplot(data$Salary,
	main = "Salary Distribution",
	col = "yellow")

plot(data$Age, data$Salary,
	main = "Age vs Salary",
	xlab = "Age",
	ylab = "Salary",
	pch = 12,
	col = "red")

print("Summary of the dataset:")
summary(data)
