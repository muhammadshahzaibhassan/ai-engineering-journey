# O(n)   uses more memory
def duplicates_fast(numbers):
    seen = set() #empty step

    for number in numbers:
        if number in seen:
            return True
        seen.add(number)
    return False
numbers = [10, 22, 35, 22, 48]

result = duplicates_fast(numbers)
if result:
    print("Duplicate Found(fast).")
else:
    print("No Duplicates.")