rows = int(input("Enter the number of rows: "))
columns = int(input("Enter the number of columns: "))
symbol = input("Enter the symbol for drawing the rectangle: ")


for x in range(rows):
    for y in range(columns-1):
        print(symbol, end = " ")
    print(symbol)