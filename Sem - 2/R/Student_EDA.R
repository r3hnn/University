# 1. Import the dataset
# Put your CSV file in the same folder as this script
df <- read.csv("C:\\Users\\rehan\\Downloads\\archive\\StudentsPerformance.csv")

# 2. Understand structure
str(df)
summary(df)

# 3. Identify missing values
colSums(is.na(df))

# 4. Visualizations (BEFORE)
# This splits the screen into 5 parts
hist(df$math.score,
    col = "blue",
    main = "Distribution of Math Scores (Before Cleaning)",
    xlab = "Math Score (Marks out of 100)",
    ylab = "Number of Students")
barplot(table(df$parental.level.of.education),
    col="red",
    main = "Distribution of Parental Levels of Education (Before Cleaning)",
    xlab = "Parental Level of Education (Highest Degree)",
    ylab = "Number of Students")
boxplot(df$reading.score,
    col="green",
    main = "Distribution of Reading Scores (Before Cleaning)",
    xlab = "Reading Score (Marks out of 100)",
    ylab = "Number of Students")
plot(df$math.score, df$writing.score,
    col="purple",
    main = "Math vs Writing Scores (Before Cleaning)",
    xlab = "Math Score (Marks out of 100)",
    ylab = "Writing Score")
pie(table(df$gender),
    col=c("pink", "lightblue"),
    main = "Distribution of Gender (Before Cleaning)",
    labels = c("Female", "Male"))

# 5. Data Cleaning
# Handle missing values (Mean imputation)
# This replaces NAs with the average math score
df$math.score[is.na(df$math.score)] <- mean(df$math.score, na.rm = TRUE)

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
hist(df$math.score,
    col = "blue",
    main = "Distribution of Math Scores (After Cleaning)",
    xlab = "Math Score (Marks out of 100)",
    ylab = "Number of Students")
barplot(table(df$parental.level.of.education),
    col="red",
    main = "Distribution of Parental Levels of Education (After Cleaning)",
    xlab = "Parental Level of Education (Highest Degree)",
    ylab = "Number of Students")
boxplot(df$reading.score,
    col="green",
    main = "Distribution of Reading Scores (After Cleaning)",
    xlab = "Reading Score (Marks out of 100)",
    ylab = "Number of Students")
plot(df$math.score, df$writing.score,
    col="purple",
    main = "Math vs Writing Scores (After Cleaning)",
    xlab = "Math Score (Marks out of 100)",
    ylab = "Writing Score")
pie(table(df$gender),
    col=c("pink", "lightblue"),
    main = "Distribution of Gender (After Cleaning)",
    labels = c("Female", "Male"))
