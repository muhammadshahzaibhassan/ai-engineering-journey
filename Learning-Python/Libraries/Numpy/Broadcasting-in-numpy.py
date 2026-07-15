'''
Broadcasting allows Numpy to perform operations on arrays with different shapes by vitrually expanding dimensions so they match the larger array's shape.
'''
import numpy as np

# first = np.array([1, 2, 3])
# second = np.array([4, 5, 6])

# print(first + second)

# matrix = np.array([[1, 2], [3, 4]])
# print(matrix) # To print matrix
# print(np.sum(matrix, axis=0)) # for sum of columns
# print(np.sum(matrix, axis=1)) # for sum of rows


# array1 = np.array([[1, 2, 3, 4],
#                    [5, 6, 7, 8],
#                    [9, 10, 11, 12],
#                    [13, 14, 15,16]])

# array2 = np.array([[1], [2], [3], [4]])

# print(array1.shape)
# print(array2.shape)

# print(array1 * array2)

array1 = np.array([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]])
array2 = np. array([[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]])

print(array1.shape)
print(array2.shape)
print(array1 * array2)