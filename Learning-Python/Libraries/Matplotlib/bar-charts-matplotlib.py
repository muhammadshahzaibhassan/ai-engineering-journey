import matplotlib.pyplot as plt
import numpy as np

# Bar chart = compare categories of data by representing each category with bar. 

categories = np.array(["Grains", "Fruit", "Vegetables", "Protien", "Dairy", "Sweets"])
values = np.array([4, 3, 2, 5, 3, 1])

# Vertical Bar Chart
# plt.bar(categories, values)
# Horizontal Bar Chart
plt.barh(categories, values)
plt.title("Daily Consumption")
plt.xlabel("Food")
plt.ylabel("Consumption")
plt.show()

