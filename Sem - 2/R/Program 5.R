# Create the data frame
data <- data.frame(
  ID = 1:20,
  Age = c(25, 30, 28, 22, 40, 35, NA, 29, 33, 45, 50, 23, 27, 31, 60, 21, 26, 38, 41, 19),
  Salary = c(50000, 60000, 58000, NA, 58000, 72000, 54000, 52000, 61000, 65000, 62000, 1000000, 61000, 59000, 57000, 55000, 63000, 64000, 56000, 1000),
  Experience = c(2, 5, 4, 3, 15, 8, 6, 5, 7, 12, 20, 2, 3, 5, 30, 71, 3, 9, 14, 0)
)

print(" The original Data is : ")
print(data)

# Identify numeric columns
numeric_cols <- sapply(data, is.numeric)
numeric_cols

numeric_cols["ID"] <- FALSE # Exclude ID from processing

# Loop through numeric columns for Imputation and Outlier handling
for (i in names(data)[numeric_cols]) {
  # 1. Mean Imputation for NAs
  data[[i]][is.na(data[[i]])] <- mean(data[[i]], na.rm = TRUE)

  # 2. Calculate IQR and Bounds
  Q1 <- quantile(data[[i]], 0.25)
  Q3 <- quantile(data[[i]], 0.75)
  IQR <- Q3 - Q1

  lower <- Q1 - (1.5 * IQR)
  upper <- Q3 + (1.5 * IQR)

  print(paste(" Processing columns: ", i))
  print(paste(" Lower Bound: ", lower, " Upper Bound: ", upper))

  # 3. Outlier Imputation (Capping)
  data[[i]] <- ifelse(data[[i]] < lower, lower,
    ifelse(data[[i]] > upper, upper, data[[i]])
  )
}

print(" The data after outlier Imputation: ")
print(data)
