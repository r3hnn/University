rows <- as.integer(readline(prompt = "Enter the number of rows: "))
cols <- as.integer(readline(prompt = "Enter the number of columns: "))

cat("Enter the elements of the matrix1:\n")
mat1 <- matrix(nrow = rows, ncol = cols)
for (i in 1:rows) {
  for (j in 1:cols) {
    mat1[i, j] <- as.integer(readline(prompt = paste("Element[", i, ",", j, "]: ", sep = "")))
  }
}

cat("Enter the elements of the matrix2:\n")
mat2 <- matrix(nrow = rows, ncol = cols)
for (i in 1:rows) {
  for (j in 1:cols) {
    mat2[i, j] <- as.integer(readline(prompt = paste("Element[", i, ",", j, "]: ", sep = "")))
  }
}

cat("Matrix 1:\n")
print(mat1)

cat("Matrix 2:\n")
print(mat2)

#Element wise multiplication
elem <- mat1 * mat2
cat("Element wise multiplication of mat1 and mat2 is:\n")
print(elem)

#Matrix multiplication
if(ncol(mat1) == nrow(mat2)) {
  mat_mult <- mat1 %*% mat2
  cat("Matrix multiplication of mat1 and mat2 is:\n")
  print(mat_mult)
} else {
  cat("Matrix multiplication not possible. Number of columns in mat1 must equal number of rows in mat2.\n")
}