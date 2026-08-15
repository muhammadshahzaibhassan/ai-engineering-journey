with open("Python\File-Handling\spider.txt") as file:
    for line in file:
        print(line.upper()) 
# ⬆️ this will print the file, in uppercase, but in output there is a newline character.
print("")
print("==================================================================================")
print("")


with open("Python\File-Handling\spider.txt") as file:
    for line in file:
        print(line.strip().upper()) 
# ⬆️ this will print the file, in uppercase, but newline character is removed by the help of strip function.
print("")
print("==================================================================================")
print("")


file = open("Python\File-Handling\spider.txt")
lines = file.readlines()
file.close()
lines.sort()
print(lines)
# ⬆️ the lines have been sorted alphabetically, so they're no longer in ​the order that they were in the file. ​Second, we can see that Python displays a newline character using "\n" symbol ​when printing a list of strings.

print("")
print("==================================================================================")
print("")
