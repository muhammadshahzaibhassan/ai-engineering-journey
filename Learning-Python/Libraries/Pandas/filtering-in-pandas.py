import pandas as pd

data = [100, 102, 104, 200, 202]

series = pd.Series(data, index=["a", "b", "c", "d", "e"])

# Filtering
print(series[series >= 200])

calories = {"Day 1": 1750,
            "Day 2": 2100,
            "Day 3": 1700}

series = pd.Series(calories)
# Accessing by index
series.loc["Day 3"] += 500
print(series.loc["Day 3"])
print()
print(series[series >= 2000])


# Homework

names = ["Bulbasaur", "Ibysaur", "Venusaur", "Charmander", "Charmeleon", "Charizard"]

series = pd.Series(names, index=[1, 2, 3, 4, 5, 6])

print(series)