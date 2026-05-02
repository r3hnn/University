#Using the ggplot2 package in R write programs to create the following visualization:
#Bar chart to display marks of students.
#Scatter plot with line graph to show the relationship between study hours and marks.
#Histogram to visualize the distribution of attendance.
student_data <- data.frame(
    student = c("A","B","C","D","E","F","G","H"),
    study_hours = c(2, 3, 4, 5, 6, 3, 7, 8),
    Marks = c(50, 55, 60, 65, 70, 55, 75, 80),
    Attendence = c(75, 80, 85, 90, 95, 82, 88, 92)
)

print(student_data)

library(ggplot2)

ggplot(student_data, aes(x = student, y = Marks)) +
    geom_bar(stat = "identity", fill = "blue") +
    labs(title = "Marks of Students",
        x = "Student",
        y = "Marks") +
    theme_minimal()

ggplot(student_data, aes(x = study_hours, y = Marks))+
    geom_point(color = "red", size = 3) +
    geom_line(color = "green", size = 1)
    labs(title = "Study Hours VS Marks",
        x = "Study Hours",
        y = "Marks") +
    theme_classic()

ggplot(student_data, aes(x = Attendence)) +
    geom_histogram(binwidth = 5, fill = "orange", color = "black") +
    labs(title = "Attendace Distibution",
    x = "Attendance (%)",
    y = "Frequency") +
    theme_light()