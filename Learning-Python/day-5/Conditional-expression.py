#conditional expressions = A one-line shortcut for the if-else statement (ternary operator)
# Print or assign one fo two value based on a condition X if condition else Y

# age = 17
# print("You are eligible!" if age >= 18 else "You are not eligible!")
a = int(input("Enter a first number: "))
b = int(input("Enter a second number: "))
num = a if a > b else b
print(num)