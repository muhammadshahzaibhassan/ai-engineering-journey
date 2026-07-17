import pandas as pd

df = pd.read_csv("Python\Libraries\Pandas\gen1pokemon.csv")

# Filtering by rows by selecting columns
tall_pokemon = df[df["Height"] >= 2]
isLegend = df[df["Legendary"] == True]
isNotLegend = df[df["Legendary"] == False]
print(tall_pokemon.to_string())
print()
print(isLegend.to_string())
print()
print(isNotLegend.to_string())
type1 = input("Enter the type 1 of Pokemon.")
type2 = input("Enter the type 2 of Pokemon.")

pokemon = df[(df["Type 1"] == type2) | (df["Type 2"] == type2)]

print(pokemon)
 