# Python weight converter

weight = float(input("Enter your weight: "))
unit = input("Kilograms or Pounds? (K or L): ")

if unit == "K" or unit == "k":
    result = weight * 2.205
    new_unit = "Lbs."
    unit_name = "Pounds"
    print(f"Your weight in {unit_name} is {round(result, 3)} {new_unit}")
elif unit == "L" or unit == "l":
    result = weight / 2.205
    new_unit = "Kgs."
    unit_name = "Kilograms"
    print(f"Your weight in {unit_name} is {round(result, 3)} {new_unit}")
else:
    print(f"{unit} is not valid!!!")
