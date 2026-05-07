#R program to accept user input and calculate mean and standard deviation for different values.
calculate_mean_sd <- function(data, freq = NULL) {
  #CALCULATE MEAN
  if (is.null(freq)) {
    mean_value <- sum(data) / length(data)
  } else {
    mean_value <- sum(data * freq) / sum(freq)
  }
  
  #CALCULATE STANDARD DEVIATION
  if (is.null(freq)) {
    varience <- sum((data - mean_value)^2) / length(data)
  } else {
    varience <- sum(((data - mean_value)^2) * freq) / sum(freq)
  }
  
  sd_value <- sqrt(varience)
  
  cat("Mean:", round(mean_value, 2), "\n")
  cat("standard Deviation:", round(sd_value, 2), "\n")
}

cat("Choose the data type:\n")
cat("1. Direct data\n")
cat("2. discreate data\n")
cat("3. continuous data\n")
choice <- as.integer(readline(prompt = "Enter your choice (1/2/3): "))

if (choice == 1) {
    #DIRECT DATA
  n <- as.integer(readline(prompt = "Enter the number of data points: "))
  data <- numeric(n)
  for (i in 1:n) {
    data[i] <- as.numeric(readline(prompt = paste("enter data point", i, ":")))
  }
  cat("\n data entered:\n")
  print(data)
  calculate_mean_sd(data)
} else if (choice == 2) {
    #DISCRETE DATA
  n <- as.integer(readline(prompt = "Enter the number of different values: "))
  data <- numeric(n)
  freq <- numeric(n)
  for (i in 1:n) {
    data[i] <- as.numeric(readline(prompt = paste("enter value", i, ":")))
    freq[i] <- as.integer(readline(prompt = paste("enter frequency of value", i, ":")))
  }
  cat("\ndata entered:\n")
  print(data.frame(value = data, frequency = freq))
  calculate_mean_sd(data, freq)
  
} else if (choice == 3) {
    #CONTINUOUS DATA
  n <- as.integer(readline(prompt = "Enter the number of classes: "))
  lower <- numeric(n)
  upper <- numeric(n)
  freq <- numeric(n)
  mid <- numeric(n)
  
  for (i in 1:n) {
    lower[i] <- as.numeric(readline(prompt = paste("enter lower limit of class", i, ":")))
    upper[i] <- as.numeric(readline(prompt = paste("enter upper limit of class", i, ":")))
    freq[i] <- as.integer(readline(prompt = paste("Enter frequency of class", i, ":")))
    mid[i] <- (lower[i] + upper[i]) / 2
  }
  cat("\nData Entered:\n")
  print(data.frame(Lower = lower, Upper = upper, Midpoint = mid, Frequency = freq))
  calculate_mean_sd(mid, freq)
  
} else {
  cat("Invalid choice! Please enter 1, 2, or 3.\n")
}