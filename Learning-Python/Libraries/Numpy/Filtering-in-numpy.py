'''
Filtering = Refers to the process of selectiong elements from an array that match a given condition
'''

import numpy as np

ages = np.array([[21, 17, 19, 20, 16, 30, 18, 65],
                 [39, 22, 15, 99, 18, 19, 20, 21]])

teenagers = ages[ages > 18] # filtering teenagers group from class
# print(teenagers)
adults = ages[(ages >= 18) & (ages < 65)] # filtering adults group from class
# print(adults)
seniors = ages[ages >= 65] # filtering seniors group from class
# print(seniors)
even = ages[ages % 2 == 0] # filtering even group of ages from class
# print(even)
odd = ages[ages % 2 != 0] # filtering odd group of ages from class
# print(odd)

# If we want to preserve the original shape of the array, we use a function which is called "Wear Function"  

#               conditions, array, fill value)
adult = np.where(ages >= 18, ages, 0 )
print(adult)