import math


# Exercise No 1: Circumference of Circle
# radius = float(input("Enter the radius of circle: "))
# circumference = 2 * math.pi * radius
# print(f"The circumference is : {round(circumference, 3)}")


# Exercise No 2: Area of Circle
# radius = float(input("Enter the radius of circle: "))
# area = math.pi * pow(radius, 2)
# print(f"The Area is : {round(area, 3)}")

#Exercise No 3: Finding hypotenuse of the right angle triangle
# formula : c = math.sqrt((pow(a, 2)) + (pow(b, 2)))
a = float(input("Enter the side A of triangle: "))
b = float(input("Enter the side B of triangle: "))
c = math.sqrt((pow(a, 2)) + (pow(b, 2)))
print(f"The hypotenuse of triangle is: {round(c, 2)}")