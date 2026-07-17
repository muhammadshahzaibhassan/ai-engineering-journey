import pandas as pd

# Data Cleaning = The process of fixing/removing:
#               => incomplete, incorrect, or irrelevant data.
#               => 75% of work done with Pandas is data cleaning.

df = pd.read_csv("Python/Libraries/Pandas/gen1pokemon.csv")

# 1. Drop irrelevant columns
df = df.drop(columns=["Legendary" , "No"])

# 2. Handle missing data and dropping rows
df = df.dropna(subset=["Type 2"])
df = df.fillna({"Type 2": "None"})

# 3. Fix inconsistent values
# column        access column        this  with  this
df["Type 1"] = df["Type 1"].replace({"Grass" : "GRASS",
                                     "Fire" : "FIRE",
                                     "Water" : "WATER"})

# 4. Standardize text
df["Name"] = df["Name"].str.lower()

# 5. Fix data types
df["Legendary"] = df["Legendary"].astype(int)

# 6. Remove duplicate values
df = df.drop_duplicates()



print(df.to_string())