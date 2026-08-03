def sum_positive_numbers(n):
    if n < 1:
        return 0
    total = 0
    for i in range(1, n + 1):
        total += i
    return total


print(sum_positive_numbers(3))   # Should be 6
print(sum_positive_numbers(5))   # Should be 15