# O(n^2)
def has_duplicates_slow(numbers):
    for i in range(len(numbers)):
        for j in range(len(numbers)):
            if i != j and numbers[i] == numbers[j]:
                return True
    return False

numbers = [10, 22, 35, 22, 48]

result = has_duplicates_slow(numbers)
if result:
    print("Duplicate Found(slow).")
else:
    print("No Duplicates.")
