# an algorithm's execution time grows proportionally to the square of its input size n
def find_duplicates(numbers):
    for i in range(len(numbers)):
        for j in range(len(numbers)):
            if i != j and numbers[i] == numbers[j]:
                return True
    return False

numbers = [10, 22, 35, 22, 48]

result = find_duplicates(numbers)

if result:
    print("Duplicate found!")
else:
    print("No duplicate found!")

