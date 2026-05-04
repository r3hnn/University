#Arithmetic Operators
num1 <- as.integer(readline(prompt = "Enter 1st number: "))
num2 <- as.integer(readline(prompt = "Enter 2nd number: "))

add <- num1 + num2
sub <- num1 - num2
mul <- num1 * num2
div <- num1 / num2
mod_div <- num1 %% num2

cat("The sum is: ", add, "\n")
cat("The difference is: ", sub, "\n")
cat("The product is: ", mul, "\n")
cat("The quotient is: ", div, "\n")
cat("The remainder is: ", mod_div, "\n")

#Logical Operators
a <- TRUE
b <- FALSE

cat("a AND b: ", a && b)
cat("a OR b: ", a || b)
cat("NOT a: ", !a)