#Using the ggplot2 package in R write progras to create the following visualization:
#Line Graph to display the trend of sales across different months.
#Box plot to visualize the distribution of profit across different regions.
#Density plot to show the distribution of sales values.
library(ggplot2)
sales_data <- data.frame(
    Month = c("Jan", "Feb", "Mar", "Apr", "May", "Jun"),
    Sales = c(200, 250, 300, 280, 320, 350),
    Profit = c(50, 60, 80, 70, 90, 100),
    Region = c("North", "South", "East", "West", "North", "South")
)

print(sales_data)

ggplot(sales_data, aes(x = Month, y = Sales)) +
    geom_line(color = "steelblue", size = 1, group = 1) +
    labs(title = "Monthly Sales Trend",
        x = "Month",
        y = "Sale") +
    theme_light()

ggplot(sales_data, aes(x = Region, y = Profit, fill = Region)) +
    geom_boxplot() + 
    labs(title = "Profit Distribution by Region",
        x = "Region",
        y = "Profit") +
    theme_classic()

ggplot(sales_data, aes(x = Sales)) +
    geom_density(fill = "green", alpha = 0.8) +
    labs(title = "Density plot for Sales",
        x = "Sales",
        y = "Density") +
    theme_classic()
