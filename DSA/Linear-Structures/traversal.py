
marks = [88, 45, 34, 23, 44, 23, 12, 34, 45, 65]
#index    0   1   2   3   4   5   6   7   8   9

# Left to Right
# way 1
# for mark in marks:
#     print(mark, end =" ") # end ="" for printing on same line.

# way 2
# for i in range(len(marks)):
#     print(marks[i])


# Right to Left
# way 1
# for mark in reversed(marks):
#     print(mark)

# way 2
# for mark in reversed(marks[::-1]):
#     print(mark)

# way 3
# for i in range(len(marks) -1, -1, -1):
#     print(marks[i])