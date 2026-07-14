# import numpy as np


# ========== Lesson no 1 ==========

# my_list = [1, 2, 3, 4]

# # Numpy array
# array = np.array([1, 2, 3, 4])
# array = array * 2
# print(array)
# print(type(array))

# my_list = my_list * 2 #This will duplicate the elements of array or list

# print(my_list)


# ========== Lesson no 2 ==========

# # Dimensions
# array = np.array([[['A', 'B', 'C'], ['D', 'E', 'F'], ['G', 'H', 'I']],
#                   [['A', 'B', 'C'], ['D', 'E', 'F'], ['G', 'H', 'I']],
#                   [['A', 'B', 'C'], ['D', 'E', 'F'], ['G', 'H', 'I']]])
# print(array.ndim)
# # print(array.shape)
# print(array[0][0][0]) # known as chain indexing! normal python
# print(array[0,0,1]) # known as multidimensional indexing in numpy


import numpy as np

a = np.array(42)
b = np.array([1, 2, 3, 4, 5])
c = np.array([[1, 2, 3], [4, 5, 6]])
d = np.array([[[1, 2, 3], [4, 5, 6]], [[1, 2, 3], [4, 5, 6]]])

print(a.ndim)
print(b.ndim)
print(c.ndim)
print(d.ndim)


# ========== Lesson no 3 ==========