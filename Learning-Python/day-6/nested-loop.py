# nested loop = A loop within another loop (outer, inner)
#               outer_loop:
#                   inner_loop:
for x in range(3):
    for y in range(1, 10):
        print(y, end = " ")
    print()
