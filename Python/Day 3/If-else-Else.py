# if = Do some code only IF some condition is True
#       Else do something else

age = int(input("Enter your age: "))

if age >= 18 and age <=60:
    print("You are now signed up!")
elif age > 60:
    print("You are too old to sign up!")
elif age < 0:
    print("Invalid age!")
else:
    print("You are too young for signing up!")  