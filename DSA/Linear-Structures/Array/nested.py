classroom = [
    [85, 90, 78], #row 1
    [72, 88, 91], #row 2
    [95, 60, 83]  #row 3
]

for row in classroom:
    for mark in row:
        print(mark, end = " ")
    print()