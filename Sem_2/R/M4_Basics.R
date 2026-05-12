# Normal plot vs C comparison

# 1.1 Normal plot
fruits <- c("Apple", "Banana", "Cherry", "Date")
counts <- c(10, 15, 7, 12)

barplot(counts,
        names.arg = fruits,
        col = "lightblue",
        main = "Fruit Counts (Base R)",
        xlab = "Fruits",
        ylab = "Count")

# 1.2 ggplot2
library(ggplot2)

data <- data.frame(
  fruit = c("Apple", "Banana", "Cherry", "Date"),
  count = c(10, 15, 7, 12)
)

ggplot(data, aes(x = fruit, y = count)) +
  geom_bar(stat = "identity", fill = "red",color = "green") +
  labs(title = "Fruit Counts (ggplot2)",
       x = "Fruits",
       y = "Count")+
  theme_bw()

  --------------------------------------------------------------------------------
# mtcars representation
print(mtcars)
dim(mtcars)
str(mtcars)
summary(mtcars)
ggplot(mtcars, aes(x = hp, y = mpg)) +
  geom_point(aes(color = factor(cyl)), size = 1) +
  geom_smooth(method = "lm", se = TRUE) +
  labs(title = "MPG vs Horsepower", color = "Cylinders") +
  theme_classic()

ggplot(data = mtcars, aes(x = hp, y = mpg)) +
  geom_point(color = "blue") +
  geom_line(color = "red") +
  labs(title = "MPG vs Horsepower") +
  theme_light()

--------------------------------------------------------------------------------
# geom_bar()

ggplot(data = mpg, aes(x = class)) +
  geom_bar(fill = "steelblue") +
  labs(title = "Count of Vehicle Classes")

# geom_line()
ggplot(economics, aes(x = date, y = unemploy)) +
  geom_line(color = "darkgreen") +
  labs(title = "Unemployment Over Time")

--------------------------------------------------------------------------------
# goem_theme
ggplot(mtcars, aes(x = hp, y = mpg)) +
  geom_point(color = "darkred") +
  labs(title = "MPG vs Horsepower") +
  theme_linedraw()+
  theme(plot.title = element_text(face = "italic", hjust = 0.9))

--------------------------------------------------------------------------------
# annotations
ggplot(mtcars, aes(x = hp, y = mpg)) +
  geom_point() +
  annotate("text", x = 190, y = 30, label = "Peak Efficiency", color = "blue", size = 4) +
  labs(title = "MPG vs Horsepower") +
  theme_minimal()

--------------------------------------------------------------------------------
# heatmaps
library(ggplot2)
library(reshape2)
print(mtcars)
cor_data <- round(cor(mtcars), 2)
melted_cor <- melt(cor_data)

ggplot(melted_cor, aes(x = Var1, y = Var2, fill = value)) +
  geom_tile(color = "white") +
  scale_fill_gradient2(low = "blue", high = "red", mid = "white", 
                       midpoint = 0, limit = c(-1,1), name = "Correlation") +
  theme_minimal() +
  labs(title = "Correlation Heatmap of mtcars Dataset")

--------------------------------------------------------------------------------
# 1.1 scatter plot with regression line and annotation

ggplot(mtcars, aes(x = wt, y = mpg)) +
  geom_point(color = "steelblue") +
  geom_smooth(method = "lm", se = TRUE, color = "darkred") +
  annotate("text", x = 4.5, y = 25, label = "Linear Trend", size = 4) +
  labs(title = "MPG vs Weight", x = "Weight", y = "Miles Per Gallon") +
  theme_minimal()

# 1.2 combining bar plot with text labels
library(dplyr)

mpg_summary <- mpg %>%
  count(class)

ggplot(mpg_summary, aes(x = class, y = n)) +
  geom_bar(stat = "identity", fill = "skyblue") + 
  geom_text(aes(label = n), vjust = 0) +
  labs(title = "Number of Cars by Class", x = "Class", y = "Count") +
  theme_minimal()

# 1.3 heatmap with highlighted cell
ggplot(melted_cor, aes(x = Var1, y = Var2, fill = value)) +
  geom_tile(color = "white") +
  geom_text(aes(label = round(value, 2)), color = "black") +
  scale_fill_gradient2(low = "blue", high = "red", mid = "white",
                       midpoint = 0, limit = c(-1,1), name = "Corr") +
  labs(title = "Correlation Heatmap") +
  theme_minimal()

--------------------------------------------------------------------------------
# layers

library(ggplot2)
mtcars$cyl <- as.factor(mtcars$cyl)

ggplot(mtcars, aes(x = cyl, y = mpg)) +
  geom_boxplot(outlier.shape = 1, fill = "lightgreen") +
  geom_jitter(width = 0.2, alpha = 0.6, color = "darkgreen") +
  labs(title = "MPG by Number of Cylinders",
       x = "Cylinders",
       y = "Miles per Gallon") +
  theme_minimal()

ggplot(mtcars, aes(x = cyl, y = mpg)) +
  geom_boxplot(outlier.shape = 4, outlier.color = "red") +
  labs(title = "Boxplot with Asterisk-Shaped Outliers")


