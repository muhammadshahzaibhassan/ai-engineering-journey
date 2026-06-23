name = input("Enter your full name: ")
# result = len(name)
# result = name.find("b") #first occurence of letter
result = name.rfind("m") #last occurence of letter
result = name.capitalize() #capitalize the first letter of string.
result = name.upper() #turn the string into uppercase letters.
result = name.lower() #turn the string into lowercase letters.
result = name.isdigit() #it returns boolean when only the complete string is numbers.
result = name.isalpha() #it returns boolean when only the complete string is alphabetial letters.
result = name.count("-") #it counts the number of occurence of a character.
result = name.replace("-") #replaces occurence of a character into another.
print(result)
