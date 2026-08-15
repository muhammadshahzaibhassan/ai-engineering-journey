with open("Python\File-Handling\spider.txt") as file:
    for line in file:
        print(line.upper()) 
# ⬆️ this will print the file, in uppercase, but in output there is a newline character.

with open("Python\File-Handling\spider.txt") as file:
    for line in file:
        print(line.strip().upper()) 
# ⬆️ this will print the file, in uppercase, but newline character is removed by the help of strip function.

