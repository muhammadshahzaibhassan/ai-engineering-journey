#collection = single "variable" used to store multiple values
#   List    = [] ordered and changeable. Duplicate OK
#   Set     = {} unordered and immutable, but Add/Remove OK. No Duplicates
#   Tuple   = () ordered and unchangeable. Duplicates OK. FASTER.


fruits = ["apple", "banana", "cherry", "date", "elderberry"]
# methods for collections
# print(dir(fruits))


# for fruit in fruits:
#     print(fruit)



# append() - Add to End
fruits = ["apple", "banana", "cherry"]
fruits.append("date")
print(fruits)  # ['apple', 'banana', 'cherry', 'date']



# insert() - Add at Specific Position
fruits = ["apple", "banana", "cherry"]
fruits.insert(1, "grape")  # Insert at index 1
print(fruits)  # ['apple', 'grape', 'banana', 'cherry']



# remove() - Remove Specific Item
fruits = ["apple", "banana", "cherry"]
fruits.remove("banana")
print(fruits)  # ['apple', 'cherry']



# pop() - Remove Last Item (or specific index)
fruits = ["apple", "banana", "cherry"]
last = fruits.pop()  # Removes and returns last item
print(last)    # 'cherry'
print(fruits)  # ['apple', 'banana']



# Remove specific index:
second = fruits.pop(1)  # Removes index 1
print(second)  # 'banana'
print(fruits)  # ['apple']



# index() - Find Position
fruits = ["apple", "banana", "cherry"]
position = fruits.index("banana")
print(position)  # 1



# count() - Count Occurrences
fruits = ["apple", "banana", "apple", "cherry"]
count = fruits.count("apple")
print(count)  # 2



# sort() - Sort the List
fruits = ["banana", "apple", "cherry", "date"]
fruits.sort()
print(fruits)  # ['apple', 'banana', 'cherry', 'date']



# Sort in reverse:
fruits.sort(reverse=True)
print(fruits)  # ['date', 'cherry', 'banana', 'apple']



# reverse() - Reverse Order
fruits = ["apple", "banana", "cherry"]
fruits.reverse()
print(fruits)  # ['cherry', 'banana', 'apple']



# extend() - Add Multiple Items
fruits = ["apple", "banana"]
more_fruits = ["cherry", "date"]
fruits.extend(more_fruits)
print(fruits)  # ['apple', 'banana', 'cherry', 'date']



# You can also extend with any iterable:
fruits.extend(["elderberry", "fig"])
print(fruits)  # ['apple', 'banana', 'cherry', 'date', 'elderberry', 'fig']



# clear() - Remove All Items
fruits = ["apple", "banana", "cherry"]
fruits.clear()
print(fruits)  # []



# copy() - Create a Copy
fruits = ["apple", "banana", "cherry"]
new_fruits = fruits.copy()
print(new_fruits)  # ['apple', 'banana', 'cherry']



# Without copy, both variables point to same list:
fruits2 = fruits
fruits.append("date")
print(fruits2)  # ['apple', 'banana', 'cherry', 'date'] - Also changed!