file = open("Python\File-Handling\spider.txt") # Let us open the file using paths
print(file.readline()) # Let us the read the single line of the file
print(file.read()) # Let us reatd the complete file
file.close()  # Let us close the file. 
with open("spider.txt") as file: # By using "with" block, python will close file automatically so we don't have to remember to close file
    print(file.readline())