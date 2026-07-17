import pandas as pd

df = pd.read_csv("Python\Libraries\Pandas\gen1pokemon.csv", index_col="Name")

# Selection by column

# Selecting Single column
print(df["Weight"].to_string())

# Selecting multiple column
print(df[["Name", "Height", "Weight"]].to_string())


# Selection by ROWS
print(df.loc["Pikachu":"Sandslash", ["Height", "Weight"]])
# Selecting by integer location

#           from:till:steps, range of columns I like
print(df.iloc[0:11:2, 0:3])

print(df.to_string())


# Exercise

pokemon = input("Enter a Pokemon name: ")

try:
    print(df.loc[pokemon])

except:
    print(f"{pokemon} not found, enter the correct name.")