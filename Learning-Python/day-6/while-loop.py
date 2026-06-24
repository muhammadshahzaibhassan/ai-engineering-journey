# while loop = execute some code WHILE some condition remains true


# name = input("Enter your name: ")

# while name == "":
#     print("You did not enter name.")
#     name = input("Enter your name: ")

# print(f"Hello {name}")


# age = int(input("Enter your age: "))

# while age < 0 or not age.isdigit(age):
#     print("Age can't be 0 or negative!!")
#     age = int(input("Enter your age: "))

# print(f"You are {age} years old!")

food = input("Enter a food you like or press Q to quit.: ")

while food == "q" or food == "Q":
    while food == "" or food == " ":
        print("Field can't be left empty")
        food = input("Enter a food you like: ")


print(f"Yo! You like {food}!!")
