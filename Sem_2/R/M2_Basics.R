# Non-Numeric Values

# 1. Logical values

result <- (15 > 23)
print(result)

# 2. Character values

name <- "John"
greeting <- "Hiii, Hello!"
print(name)
print(greeting)

# 3. Factors

colors1 <- factor(c("Red", "Blue", "Red", "Green", "Blue", "Green"))
print(colors1)
print(levels(colors1))

--------------------------------------------------------------------------------  
# Lists
  
# 1. Creating a list
  
mylist <- list("R","programming","for","Analytics")
mylist

# 2. Accessing elements in the list

mylist[2]
mylist[4]
mylist[-1]

# 3. Changing a particular element of the list

mylist[2] <- "is used"
mylist

# 4. Finding length of the list

length(mylist)

# 5. Check if an element is present in the list

"Analytics" %in% mylist

# 6. Appending elements to the list

mylist1 <- append(mylist, "and Inference")
mylist1

# 7. Removing elements from a list

mylist2 <- mylist1[-2]
mylist2

# 8. Range of Indexes

num_list <- list("ab","ac","ad","ae","af")
num_list
(num_list)[2:4]

# 9. Loop Through a List

for (x in num_list) {
  print(x)
}

# 10. Join lists

list1 <- list("a", "b", "c")
list2 <- list(1,2,3)
list3 <- append(list1,list2)
print(list3)

--------------------------------------------------------------------------------  
# Data Frame

# 1. Create a data frame
Data_Frame <- data.frame (
  Training = c("Strength", "Stamina", "Other"),
  Pulse = c(100, 150, 120),
  Duration = c(60, 30, 45)
)
Data_Frame

# 2. Summarizing the data

summary(Data_Frame)

# 3. Accessing elements in the data frame

Data_Frame[1]
Data_Frame[["Training"]]
Data_Frame$Duration

# 4. Adding rows to the existing data frame

new_df <- rbind(Data_Frame, c("Power", 110, 117))
new_df

# 5. Adding columns to the existing data frame

new_df1 <- cbind(new_df, Steps = c(1000, 5300, 4700, 2200))
new_df1

# 6. Removing rows and columns from the data frame

refined_df <- new_df1[-c(1),-c(2)]
refined_df

# 7. Number of rows and columns in a data frame

dim(new_df)
dim(new_df1)
dim(refined_df)

ncol(new_df)
nrow(new_df)

# 8. Combining data frames

df_1 <- data.frame (
  Training = c("Strength", "Stamina", "Other"),
  Pulse = c(100, 150, 120),
  Duration = c(60, 30, 45)
)
df_1

df_2 <- data.frame (
  Training = c("Strength", "Stamina", "Other"),
  Pulse = c(100, 150, 120),
  Duration = c(60, 30, 45)
)
df_2

summary(df_2)

n_df <- rbind(df_1,df_2)
n_df

--------------------------------------------------------------------------------  
# Special values

# 1. Inf and -Inf (Infinity) 
  
x <- 10 / 0
y <- -10 / 0

print(x)
print(y) 
is.finite(x)

# 2. NaN (Not a Number)

z <- 0 / 0  
print(z)

# 3. NA (Not Available / Missing Values)

data <- c(10, 20, NA, 40)
mean(data)
mean(data, na.rm = TRUE)

# 4. NULL (Empty or Undefined Object)

x <- NULL
print(x)
length(x)

# 5. Data handling functions

df <- data.frame(Name = c("Abc", "Bcd", "Cde","Def",
                          "Efg","Fgh","Ghi","Hij","Ijk"),
                   Age = c(25, 30, 35, 40, 45, 50, 55, 60, 65),
                   Score = c(90, 85, 88, 75, 87, 92, 77, 81, 98))
print(df)
print(dim(df))
print(str(df))
print(summary(df))
print(head(df))
print(tail(df))
head(df, 3)
tail(df, 4)
--------------------------------------------------------------------------------  
# Functions

add_numbers <- function(a, b) {
  return(a + b)
}

result <- add_numbers(5, 10)
print(result)
--------------------------------------------------------------------------------  
# Decision making statement

# 1. Simple if statement

n <- 3

if (n > 5) {
  print("n is greater than 5")
}

# 2. if else statement

n <- 3

if (n > 5) {
  print("n is greater than 5")
} else {
  print("n is less than or equal to 5")
}

# 3. if else if statement

n <- 15

if (n < 10) {
  print("n is less than 10")
} else if (n == 15) {
  print("n is exactly 15")
} else {
  print("n is greater than 10 but not 15")
}

# 4. Nested if statement

marks <- 49

if (marks >= 50) {
  print("You have passed the exam.")
  
  if (marks >= 90) {
    print("Grade: A")
  } else if (marks >= 30) { 
    print("Grade: B")
  } else {
    print("Grade: C")
  }
  
} else {
  print("You have failed the exam.")
}

# 5. switch statement

y <- "F"
review <- switch(y,
                 "A" = "Excellent",
                 "B" = "Good",
                 "C" = "Average",
                 "D" = "Poor",
                 "Invalid Grade"
)
print(review)

# 6. ifelse statement

z <- c(10, 20, 30, 40)

result <- ifelse(z > 25, "High", "Low")
print(result)

--------------------------------------------------------------------------------  
# Looping Statements

# for loop

for (i in 1:9) {
  print(paste("Iteration:", i))
}

# while loop

x <- 1
while (x <= 5) {
  print(paste("Iteration:", x))
  x <- x + 1  
}

# repeat loop

y <- 12
repeat {
  print(paste("Iteration:", y))
  y <- y + 1
  if (y > 11) break  
}

# 1.

N <- 5
sum <- 0

for (i in 1:N) {
  sum <- sum + i
}

print(paste("Sum of first", N, "natural numbers is:", sum))

# 2.

N <- 10
x <- 2  


while (x <= N) {
  print(x)
  x <- x + 2
}

# 3.

N <- 5
factorial <- 1
i <- 6

repeat {
  factorial <- factorial * i
  i <- i + 1
  if (i > N) break
}

print(paste("Factorial of", N, "is:", factorial))

--------------------------------------------------------------------------------  
# Scoping

x <- 10
my_function <- function() {
  x <- 5
  return(x)
}
print(my_function())
print(x)

x <- 10
my_function <- function() {
  y <- 5
  return(y)
}
print(my_function())
print(y)
print(x)

--------------------------------------------------------------------------------  
# Argument Matching

my_function <- function(a, b, c) {
  return(a + b + c)
}

print(my_function(2, 3, 4))
print(my_function(b = 3, c = 4, 4))
print(my_function(a = 2, b = 3, c = 4))

--------------------------------------------------------------------------------  
# Built-in Functions
  
# 1. Mathematical Functions
  
n <- -10
print(abs(n))
print(sqrt(25))
print(ceiling(4.2))
print(floor(4.8))
print(round(3.567, 2))

# 2. Statistical Functions

num <- c(10, 20, 30, 40, 50)
mean(num)
median(num)
var(num)
sd(num)
sum(num)
min(num)
max(num) 

# 3. Character/String Functions

dsa <- "R Programming!"
print(nchar(dsa))
print(toupper(dsa))
print(tolower(dsa))
print(substr(dsa, 1, 5))
print(paste("Welcome", "to", "R"))

