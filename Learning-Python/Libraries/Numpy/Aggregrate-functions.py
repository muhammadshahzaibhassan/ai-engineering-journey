import numpy as np

# Aggregrate Functions = Summarize data and typically returns a single value.

array = np.array([[1, 2, 3, 4, 5], 
                  [6, 7, 8, 9, 10]])

# print(np.sum(array)) # For addition
# print(np.mean(array)) # For finding mean of array
# print(np.std(array)) # For standard deviation
# print(np.var(array)) # For variance
# print(np.min(array)) # For minimum value in array
# print(np.max(array)) # For maximum value in array
# print(np.argmin(array)) # For position of minimum value in array
# print(np.argmax(array)) # For position of maximum value in array
value = int(input("Enter the value for axis: "))
print(np.sum(array, axis = value))


