# represents logarithmic time complexity, which describes an algorithm whose execution time grows very slowly as the input size (n) increases
def find_name(names, target):
    left = 0
    right = len(names) - 1

    while left <= right:
        middle = (left + right) // 2

        if names[middle] == target:
            return middle
        
        elif names[middle] < target:
            left = middle + 1

        else:
            right = middle - 1

    return - 1

names = ['Ava', 'Emma', 'Jackson', 'Liam', 'Lucas', 'Mia', 'Noah', 'Oliver', 'Olivia', 'Sophia']

target_name = "Ava"

result = find_name(names, target_name)

if result != -1:
    print(f"Found '{target_name}' at index {result + 1}")
else:
    print("Not found!")