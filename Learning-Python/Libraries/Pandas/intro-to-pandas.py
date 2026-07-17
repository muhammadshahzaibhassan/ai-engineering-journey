import pandas as pd

# Series = A pandas 1-Dimensional labeled array that can hold any data type. Think of it like a single column in a spreadsheet (1-Dimensional)

data = [100, 102, 104, 200, 202]
data1 = [100.3, 102.32, 104]
data2 = ["A", "B", "C"]
#                               Labels
series = pd.Series(data, index=["a", "b", "c", "d", "e"])
#           #accessing by location by index value
print(series.loc["b"])
#           #accessing by location by integer value
print(series.iloc[2])
#         can reassign the value too
print(series)
series.loc["b"] = 300
print(series)


