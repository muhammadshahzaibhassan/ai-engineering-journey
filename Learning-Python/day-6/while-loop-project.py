#compund interest calculator

principle = 0
rate = 0
time = 0
# Here zeros are not allowed!!
# while principle <= 0:
#     principle = float(input("Enter the principle amount: "))
#     if principle <=0:
#         print("Principle can't be less or equal to zero.")

# while rate <= 0:
#     rate = float(input("Enter the interest rate: "))
#     if rate <=0:
#         print("Interest rate can't be less or equal to zero.")

# while time <= 0:
#     time = int(input("Enter the interest rate: "))
#     if time <=0:
#         print("Time rate can't be less or equal to zero.")


# if zeros are allowed!
while True:
    principle = float(input("Enter the principle amount: "))
    if principle < 0:
        print("Principle can't be less or equal to zero.")
    else:
        break

while True:
    rate = float(input("Enter the interest rate: "))
    if rate < 0:
        print("Interest rate can't be less or equal to zero.")
    else:
        break

while True:
    time = int(input("Enter the interest rate: "))
    if time < 0:
        print("Time rate can't be less or equal to zero.")
    else:
        break


total = principle * pow((1 + rate / 100 ), time)

print(f"Balance after {time} year/s: ${total:.2f}")



