#Basic Printing

"Programming with R"
7 + 7
---------------------------------------------------------------------------------
#Basic Plotting
  
plot(1:10)
summary(1:10)
plot(1:10, main = "Simple Plot")
barplot(c(5, 10, 7, 12))
pie(c(10, 20, 30))

--------------------------------------------------------------------------------
#Using Print Statements
  
print("Programming with R")
--------------------------------------------------------------------------------
#Variable Creation

name = 'Arun'
age = 15
class(name)
class(age)
name
age
print(name)
print(age)

print("The name is: ", name)
print(paste("The name is: ", name))
cat("The name is: ", name)
--------------------------------------------------------------------------------
#Assignment Operator
#var <- value

name1 <- "Kevin"
age1 <- 26
marks <- 86.5

print(name1)
print(age1)
print(marks)
--------------------------------------------------------------------------------
#Concatenating Strings or Elements

review <- "Awesome"
print("I am", review)
paste("I am", review)

a <- 3
b <- 4
a + b
--------------------------------------------------------------------------------
#Multiple Variables
a<- 'Data Science'
a1 <- b1 <- c1 <- 'Data Science'
a1
b1
c1
--------------------------------------------------------------------------------
#A variable name must start with a letter and can be a combination of letters, digits, period(.)
#and underscore(_). If it starts with period(.), it cannot be followed by a digit.
#A variable name cannot start with a number or underscore (_)
#Variable names are case-sensitive (age, Age and AGE are three different variables)
#Reserved words cannot be used as variables (TRUE, FALSE, NULL, if...)

bowlername <- "Bumrah"
bowler_name <- "Bumrah"
bowlerName <- "Bumrah"
BOWLERNAME <- "Bumrah"
bowlername1 <- "Bumrah"
.bowlername <- "Bumrah"
1bowlername <- "Bumrah"


bowlername
bowler_name
bowlerName
BOWLERNAME
bowlername1
.bowlername
1bowlername
--------------------------------------------------------------------------------
#Data type of the Variable

class(name1)
class(age1)
class(marks)
--------------------------------------------------------------------------------
#Built-in Functions

#min() and max()
min(5, 15, 25)
max(27, 49, 53)

#sqrt()
sqrt(49)

#abs()
abs(-16)

#ceiling() and floor()
ceiling(6.8)
floor(22.4)
--------------------------------------------------------------------------------
#string Length
  
var1 <- 'R is used for Statistical Programming and inference'
nchar(var1)
--------------------------------------------------------------------------------
#Checking for a String

grepl('R',var1)
grepl('Programming',var1)
grepl('Analytics',var1)
--------------------------------------------------------------------------------
#Combining two Strings

a2 <- 'Data'
a3 <- 'Science'
paste(a2,a3)
--------------------------------------------------------------------------------
#Escape Characters

jain <- "Jain university - "School of Sciences"" 
jain  

jain <- "Jain university - \"School of Sciences\""
jain
print(jain)
cat(jain)

jain1 <- "Jain university - \n\"School of Sciences\""
cat(jain1)

jain1 <- "Jain university - \t\"School of Sciences\""
cat(jain1)

jain1 <- "Jain university - \b\"School of Sciences\""
cat(jain1)

--------------------------------------------------------------------------------
# Creating a class
Vehicle <- function(type, brand, mileage) {
  structure(
    list(
      type = type,
      brand = brand,
      mileage = mileage
    ),
    class = "Vehicle"
  )
}

vehicle1 <- Vehicle("Car", "Toyota", 18)
vehicle2 <- Vehicle("Bike", "Yamaha", 45)
vehicle3 <- Vehicle("Truck", "Tata", 12)
vehicle1


numeric_vector <- c(1,2,3,4,5)
class_result <- class(numeric_vector)
print(class_result)

--------------------------------------------------------------------------------
# Assignment Operators
a <- 10
b = 3
20 -> c

# Arithmetic Operators
add  <- a + b
sub  <- a - b
mul  <- a * b
div  <- a / b
power <- a ^ b
mod   <- a %% b
int_div <- a %/% b

# Relational Operators
greater  <- a > b
less     <- a < b
equal    <- a == b
not_equal <- a != b
greater_equal <- a >= b
less_equal    <- a <= b

# Logical Operators
logic_and  <- (a > 5) & (b < 5)
logic_or   <- (a < 5) | (b < 5)
logic_not  <- !(a == b)
logic_and2 <- (a > 5) && (b < 5)
logic_or2  <- (a < 5) || (b < 5)

# Miscellaneous Operators
sequence <- 1:5
check_value <- 6 %in% sequence

sequence1 <- 1:15
check_value1 <- !(6 %in% sequence1)

--------------------------------------------------------------------------------
#Vectors

ds <- "Mathematics"

data_science <- c("Mathematics", "Statistics", "Computer science")
data_science

semesters <- c(2,4,6,5,3,1)
semesters

numbers <- 1:9
numbers

# 1. Length of a vector

length(data_science)
length(semesters)

# 2. Sorting the vectors

sort(data_science)
sort(semesters)

# 3. Accessing vectors

data_science[2]
semesters[4]

data_science[-1]
semesters[-4]

# 4. Change an existing value

data_science[1] <- "Machine Learning"
data_science

# 5. repeat vectors

repeat_each <- rep(c(1,2,3), each = 3)
repeat_each

repeat_times <- rep(c(1,2,3), times = 3)
repeat_times

# 6. Sequence numbers

seq_num <- (1:10)
seq_num

seq_num1 <- seq(from = 0, to = 100, by = 20)
seq_num1

--------------------------------------------------------------------------------  
#Matrices

matrix1 <- matrix(c(1,2,3,4,5,6), nrow = 3, ncol = 2)
matrix1

matrix2 <- matrix(c(1,2,3,4,5,6), nrow = 2, ncol = 3)
matrix2

matrix3 <- matrix(c(1,2,3,4,5,6), nrow = 2, ncol = 2)
matrix3

matrix4 <- matrix(c(1,2,3,4,5,6), nrow = 4, ncol = 2)
matrix4

updated_matrix1 <- cbind(matrix1, c(7,8,9))
updated_matrix1

updated_matrix2 <- rbind(matrix1, c(7,8,9))
updated_matrix2

elem <- updated_matrix1[c(1,3),]
elem 

#Matrix Operations
# 1. Accessing elements from a matrix

elem <- matrix1[2,1]
cat(elem)

elem1 <- matrix1[3,2]
cat(elem1)

elem2 <- matrix1[2,5]
cat(elem2)

elem3 <- matrix1[2,] 
cat(elem3)
x
elem4 <- matrix1[,2] 
cat(elem4)

# 2. Replacing individual elements of a matrix

og_mat <- matrix(1:9, nrow = 3, ncol = 3)
print(og_mat)
rep_mat <- og_mat
rep_mat[2,3] <- 12
cat("The Original matrix is:\n")
print(og_mat)
cat("The Replicated matrix is:\n")
print(rep_mat)

# 3.1 Replacing an entire row elements of a matrix

og_mat <- matrix(1:9, nrow = 3, ncol = 3)
print(og_mat)
rep_mat <- og_mat
rep_mat[2,] <- c(10,15,20)
cat("The Original matrix is:\n")
print(og_mat)
cat("The Replicated matrix is:\n")
print(rep_mat)

# 3.2 Replacing an entire column elements of a matrix
og_mat <- matrix(1:9, nrow = 3, ncol = 3)
print(og_mat)
rep_mat <- og_mat
rep_mat[,2] <- c(10,15,20)
cat("The Original matrix is:\n")
print(og_mat)
cat("The Replicated matrix is:\n")
print(rep_mat)

# 4. Removing rows and columns from a matrix

updated_matrix1
refined_matrix <- updated_matrix1[-c(2), -c(2)]
refined_matrix

refined_matrix <- updated_matrix1[-c(2),]
refined_matrix

# 5. Number of rows and columns

dim(updated_matrix1)
dim(refined_matrix)

# 6. To find the matrix length

length(updated_matrix1)
length(refined_matrix)

# 7. Combining 2 matrices

new_mat1 <- matrix(c("tony", "starc", "peter", "parker"), nrow = 2, ncol = 2)
new_mat2 <- matrix(c("robert", "downey", "tom", "holland"), nrow = 2, ncol = 2)
new_mat1
new_mat2

Comb_mat1 <- rbind(new_mat1, new_mat2)
Comb_mat1

Comb_mat2 <- cbind(new_mat1, new_mat2)
Comb_mat2

# 8. Loop through a matrix


for (i in Comb_mat1) {
  print(i)
}
--------------------------------------------------------------------------------  
# Arrays

array1 <- array(1:24, dim = c(4, 3, 3))
array1
array2 <- array(array1, dim = c(4, 3, 3))
array2

# 1. Accessing array elements

array2[2,3,2]
array2[3,1,1]

# 2. Accessing a complete row or column

array2[1,,1]
array2[c(1),,1]
array2[,c(1),3]

# 3. Checking for an element in an array

2 %in% array2

# 4. Number of rows and columns

dim(array2)

# 5. length of an array

length(array2)

# 6. Loop through an array

for (i in array2) {
  print(i)
}
--------------------------------------------------------------------------------  
