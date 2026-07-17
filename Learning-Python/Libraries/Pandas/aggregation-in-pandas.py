import pandas as pd

df = pd.read_csv("Python/Libraries/Pandas/gen1pokemon.csv")

# Aggregate Functions applied to the whole DataFrame
print(df.mean(numeric_only=True))
print(df.sum(numeric_only=True))
print(df.min(numeric_only=True))
print(df.max(numeric_only=True))
print(df.count())


# Aggregate Functions applied to the Single Column
print(df["Height"].mean())
print(df["Height"].sum())
print(df["Height"].min())
print(df["Weight"].max())


# Grouping

group = df.groupby("Type 1")
# print(group["Height"].mean())
print(group["Height"].sum())
print(group["Height"].min())
print(group["Height"].max())