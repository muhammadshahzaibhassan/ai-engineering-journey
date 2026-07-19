import matplotlib.pyplot as plt
import numpy as np

# scatter graph = Shows the relationship between two variables
#                 Helps to identify a correlation (+, -, None)
#                 Example: Study hours vs. Test scores 

x1 = [0, 1, 1, 2, 3, 4, 5, 6, 7, 7, 8] # Hours studied
y1 = [55, 60, 65, 52, 68, 70, 75, 78, 82, 85, 87] # Grades
x2 = [0, 1, 2, 2, 3, 4, 5, 6, 7, 8, 8] # Hours studied
y2 = [50, 58, 65, 70, 72, 78, 83, 88, 92, 95, 97] # Grades

plt.title("Test Scores")
plt.scatter(x1, y1, color="red",
                   alpha=1,
                   s=50,
                   label="Class A")

plt.title("Test Scores")
plt.scatter(x2, y2, color="blue",
                   alpha=1,
                   s=50,
                   label="Class B")

plt.xlabel("Hours Studied")
plt.ylabel("Grade")
plt.legend()
plt.show()