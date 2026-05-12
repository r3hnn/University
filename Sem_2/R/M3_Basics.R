# Numeric and Non Numeric values 

supermarket_data <- data.frame(
  Customer_ID = c("C001", "C002", "C003", "C004","c005"),
  Age = c(28, 28, 45, 32, 56),
  Total_Spending = c(120.50, 120.50, 250.75, 75.00, 300.00),
  Items_Purchased = c(15, 8, 15, 5, 20),
  Payment_Method = c("Credit Card", "Credit Card", "Digital Wallet", "Cash", "Credit Card"),
  Membership_Status = c("Member", "Member", "Non-Member", "Member", "Member"),
  Product_Category = c("Electronics", "Groceries", "Electronics", "Clothing", "Groceries")
)

print(supermarket_data)
summary(supermarket_data)
summary(supermarket_data[, c("Age", "Total_Spending", "Items_Purchased")])

mean_spending <- mean(supermarket_data$Total_Spending)
median_spending <- median(supermarket_data$Total_Spending)
sd_spending <- sd(supermarket_data$Total_Spending)

cat("Mean Spending: ", mean_spending, "\n")
cat("Median Spending: ", median_spending, "\n")
cat("Standard Deviation of Spending: ", sd_spending, "\n")

table(supermarket_data$Payment_Method)
table(supermarket_data$Membership_Status)
table(supermarket_data$Product_Category)

library(ggplot2)

ggplot(supermarket_data, aes(x = Payment_Method, fill = Payment_Method)) +
  geom_bar() +
  ggtitle("Distribution of Payment Methods")

ggplot(supermarket_data, aes(x = Membership_Status, y = Total_Spending, fill = Membership_Status)) +
  geom_boxplot() +
  ggtitle("Total Spending Based on Membership Status")

---------------------------------------------------------------------------------------------------
# Univariate and Multivariate Data

height <- c(71, 85, 45, 63, 55)
summary(height)

hist(height, col = "yellow", main = "Height Distribution", xlab = "Height (cm)")

students_data <- data.frame(
  Height = c(150, 160, 165, 170, 175, 180, 185),
  Weight = c(50, 60, 65, 70, 75, 80, 85),
  Age = c(14, 15, 16, 17, 18, 19, 20)
)

summary(students_data)
pairs(students_data, col = "cyan", main = "Multivariate Data Analysis")

cor(students_data)

---------------------------------------------------------------------------------------------------
# Counts, Percentages, and Proportions

smartphone_sales <- c("Apple", "Samsung", "Xiaomi", "Apple", "Samsung", "OnePlus", 
                        "Xiaomi", "Apple", "Samsung", "OnePlus", "Apple", "Xiaomi", 
                        "Samsung", "Apple", "Xiaomi", "Samsung", "OnePlus", "Apple", 
                        "Xiaomi", "Samsung")
print(smartphone_sales) 

brand_counts <- table(smartphone_sales)
print("Counts:")
print(brand_counts)

brand_percentages <- prop.table(brand_counts) * 100
print("Market Share (%):")
print(brand_percentages)

brand_proportions <- prop.table(brand_counts)
print("Proportions:")
print(brand_proportions)

market_share_table <- data.frame(
  Brand = names(brand_counts),
  Sales_Count = as.vector(brand_counts),
  Market_Share_Percentage = round(as.vector(brand_percentages), 2),
  Proportion = round(as.vector(brand_proportions), 2)
)
print(market_share_table)


---------------------------------------------------------------------------------------------------
# Covariance and Correlation
study_data <- data.frame(
  Hours_Studied = c(5, 7, 9, 10, 11, 12, 13, 14),
  Exam_Score = c(18, 20, 24, 27, 29, 31, 33, 36)
)

print("Study Data:")
print(study_data)

cov_value <- cov(study_data$Hours_Studied, study_data$Exam_Score)
cat("Covariance between Hours Studied and Exam Score:", cov_value, "\n")

cor_value <- cor(study_data$Hours_Studied, study_data$Exam_Score)
cat("Correlation between Hours Studied and Exam Score:", cor_value, "\n")


plot(
  study_data$Hours_Studied, study_data$Exam_Score,
  main = "Scatter Plot: Hours Studied vs Exam Score",
  xlab = "Hours Studied", ylab = "Exam Score",
  pch = 19, col = "blue"
)
abline(lm(Exam_Score ~ Hours_Studied, data = study_data), col = "red")


study_data <- data.frame(
  Hours_Studied = c(5, 7, 9, 10, 11, 12, 13, 14),
  Exam_Score = c(18, 20, 24, 27, 29, 31, 33, 36)
)

print("Study Data:")
print(study_data)

sample_cov <- cov(study_data$Hours_Studied, study_data$Exam_Score)
sample_cor <- cor(study_data$Hours_Studied, study_data$Exam_Score)

mean_x <- mean(study_data$Hours_Studied)
mean_y <- mean(study_data$Exam_Score)

pop_cov <- sum((study_data$Hours_Studied - mean_x) * 
                 (study_data$Exam_Score - mean_y)) / nrow(study_data)

sd_x_pop <- sqrt(sum((study_data$Hours_Studied - mean_x)^2) / nrow(study_data))
sd_y_pop <- sqrt(sum((study_data$Exam_Score - mean_y)^2) / nrow(study_data))

pop_cor <- pop_cov / (sd_x_pop * sd_y_pop)

# Output Results
cat("Sample Covariance:", sample_cov, "\n")
cat("Sample Correlation:", sample_cor, "\n")
cat("Population Covariance:", pop_cov, "\n")
cat("Population Correlation:", pop_cor, "\n")


plot(
  study_data$Hours_Studied, study_data$Exam_Score,
  main = "Scatter Plot: Hours Studied vs Exam Score",
  xlab = "Hours Studied", ylab = "Exam Score",
  pch = 19, col = "blue"
)
abline(lm(Exam_Score ~ Hours_Studied, data = study_data), col = "red")

---------------------------------------------------------------------------------------------------  
# Outlier Detection and Analysis
library(dplyr)
library(ggplot2)

set.seed(123)
exam_scores <- c(sample(60:80, 18, replace = TRUE), 10, 260)
print(exam_scores)

mean_value <- mean(exam_scores)
median_value <- median(exam_scores)
mode_value <- as.numeric(names(sort(table(exam_scores), decreasing = TRUE)[1]))
cat("Mean:", mean_value, "\n")
cat("Median:", median_value, "\n")
cat("Mode:", mode_value, "\n")

Q1 <- quantile(exam_scores, 0.25)
Q3 <- quantile(exam_scores, 0.75)
IQR_value <- Q3 - Q1
print(IQR_value)

lower_bound <- Q1 - 1.5 * IQR_value
upper_bound <- Q3 + 1.5 * IQR_value
print(lower_bound)
print(upper_bound)

outliers <- exam_scores[exam_scores < lower_bound | exam_scores > upper_bound]
cat("Outliers:", outliers, "\n")

exam_scores_adjusted <- ifelse(exam_scores < lower_bound, lower_bound, 
                               ifelse(exam_scores > upper_bound, upper_bound, exam_scores))
print(exam_scores_adjusted)

mean_adjusted <- mean(exam_scores_adjusted)
median_adjusted <- median(exam_scores_adjusted)
cat("Mean before handling outliers:", mean_value, "\n")
cat("Median before handling outliers:", median_value, "\n")
cat("Mean after handling outliers:", mean_adjusted, "\n")
cat("Median after handling outliers:", median_adjusted, "\n")

df_original <- data.frame(Score = exam_scores)
df_original$IsOutlier <- df_original$Score < lower_bound | df_original$Score > upper_bound
df_original$Label <- ifelse(df_original$IsOutlier, as.character(df_original$Score), NA)

ggplot(df_original, aes(x = "Exam Scores", y = Score)) +
  geom_boxplot(outlier.colour = "red", outlier.shape = 8, fill = "skyblue") +
  geom_text(aes(label = Label), na.rm = TRUE, hjust = -0.2, color = "red", size = 4) +
  labs(title = "Boxplot with Outliers Labeled", x = "", y = "Score") +
  theme_minimal()

df_adjusted <- data.frame(Score = exam_scores_adjusted, Type = "Adjusted")
df_original$Type <- "Original"
df_original$Score <- exam_scores  # Ensure original scores are retained
df_combined <- rbind(df_original[, c("Score", "Type")], df_adjusted)

ggplot(df_combined, aes(x = Type, y = Score, fill = Type)) +
  geom_boxplot(outlier.colour = "red", outlier.shape = 8) +
  labs(title = "Boxplot: Original vs Adjusted Exam Scores") +
  theme_minimal()

ggplot(df_combined, aes(x = Score, fill = Type)) +
  geom_histogram(binwidth = 5, position = "dodge", alpha = 0.7, color = "black") +
  labs(title = "Histogram: Original vs Adjusted Exam Scores", x = "Score", y = "Frequency") +
  theme_minimal()

---------------------------------------------------------------------------------------------------
  