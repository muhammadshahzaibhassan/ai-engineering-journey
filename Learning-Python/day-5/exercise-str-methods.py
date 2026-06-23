print("Rules for username:- ")
print("1. Username is no longer than 12 characters.")
print("2. Username must not contains spaces.")
print("3. Username must not contain digits.")

username = input("Enter the Username: ")
if len(username) > 12:
    print("Username is longer than 12 characters.")
elif not username.find(" ") == -1:
    print("Username should not contain spaces.")
elif username.isalpha() == False:
    print("Username should not contain digits.")
else:
    print(f"Your username is {username}")