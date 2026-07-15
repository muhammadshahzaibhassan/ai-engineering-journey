import numpy as np

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
# Dimensions of numpy array
# 0 dimensional array
# a = np.array(42)
# 1 dimensional array
# b = np.array([1, 2, 3, 4, 5])
# 2 dimensional array
# c = np.array([[1, 2, 3], [4, 5, 6]])
# 3 dimensional array
# d = np.array([[[1, 2, 3], [4, 5, 6]], 
            #   [[7, 8, 9], [10, 11, 12]],
            #   [[13, 14, 15], [16, 17, 18]]])

# # print(c[1, 1]) # accessing element in 2-D array
# index1 = int(input("Enter the first index: "))
# index2 = int(input("Enter the second index: "))
# index3 = int(input("Enter the third index: "))
# print(d[index1, index2, index3])


# print(a.ndim)
# print(b.ndim)
# print(c.ndim)
# print(d.ndim)


# ========== Lesson no 3 ==========
# Slicing Array
array = np.array([[1,2,3,4], 
                 [5,6,7,8], 
                 [9,10,11,12], 
                 [13,14,15,16]])

# array[start:end:step] Row selection
# print(array[::-2])
# column selection 
# array(no.of.row:, )
# print(array[:, 0:3])

# row and column selection
# array[row start:row end, column start:column end]
print(array[0:2, 2:4])
