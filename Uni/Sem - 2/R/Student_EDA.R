# 1. Import the dataset
# Put your CSV file in the same folder as this script
df <- read.csv("C:\\Users\\rehan\\Downloads\\archive\\StudentsPerformance.csv")

# 2. Understand structure
str(df)
summary(df)

# 3. Identify missing values
is.na(df)
colSums(is.na(df))

# 4. Visualizations (BEFORE)
# This splits the screen into 5 parts
par(mfrow=c(2,3))
hist(df$math.score)
barplot(table(df$parental.level.of.education))
boxplot(df$reading.score)
plot(df$math.score, df$writing.score)
pie(table(df$gender))

# 5. Data Cleaning
# Handle missing values (Mean imputation)
# This replaces NAs with the average math score
df$math.score[is.na(df$math.score)] <- mean(df$math.score, na.rm = TRUE)

# Check data types and convert
df$gender <- as.factor(df$gender)

# Detect duplicates
sum(duplicated(df))

# Identify outliers
boxplot.stats(df$math.score)$out

# Basic statistics
mean(df$math.score)
median(df$math.score)
sd(df$math.score)

# 6. Visualizations (AFTER)
# We just run them again to show the cleaned data
par(mfrow=c(2,3))
hist(df$math.score, col="blue")
barplot(table(df$parental.level.of.education), col="red")
boxplot(df$reading.score, col="green")
plot(df$math.score, df$writing.score, col="purple")
pie(table(df$gender))
