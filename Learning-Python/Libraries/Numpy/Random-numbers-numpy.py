import numpy as np

# For Integers.
#                          (seed=1) to generate the same result repeatedly.
# rng = np.random.default_rng(seed=1)
#   value.datatype(range, no of random.no)
# print(rng.integers(low=1, high=100, size = 3)) # output will be 1 dimensional
# print(rng.integers(low=1, high=100, size = (3, 4))) # output will be 2 dimensional, (x, y) where x is no of rows and y is no of columns.


# For Float values     (range)
print(np.random.uniform(low=-1, high=1, size=3)) # 1 Dimensional Array



# How to shuffle an array!!

rng = np.random.default_rng()
array = np.array([1, 2, 3, 4, 5])
rng.shuffle(array)
print(array)

fruits = np.array(["🍎", "🍊", "🍌", "🍓", "🥝", "🍇"])

fruits = rng.choice(fruits, size=(3, 3))
print(fruits)
