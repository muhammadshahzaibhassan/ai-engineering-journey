# Python Temperature Converter

temperature = float(input("Enter the temperature: "))
unit = input("Is temperature in Celcius or Fahrenheit (C/F): ")

if unit == "C" or unit == "c":
    result = (temperature * 1.8) + 32
    print(f"The temperature is {round(result, 2)}° Fahrenheit.")
elif unit == "F" or unit == "f":
    result = (temperature - 32) / 1.8
    print(f"The temperature is {round(result, 2)}° Celcius.")
else:
    print(f"{unit} is an invalid unit!")
