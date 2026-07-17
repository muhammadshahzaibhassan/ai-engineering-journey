# Dataframe = A tabular data structure with rows and columns. 2-Dimensional Similar to an Excel Spreadsheet.

import pandas as pd

data = {
    "Name": ["Spongebob", "Patrick", "Squidward"],
    "Age": [30, 35, 50]
}

df = pd.DataFrame(data, index = ["Employee 1", "Employee 2", "Employee 3"])
# Access by index value
print(df.loc["Employee 3"])
# Access by integer value
print(df.iloc[0])

# Add a new column
#  key    = Values(equals to no of columns) 
df["Job"] = ["Cook", "N/A", "Cashier"]



# Add new rows
new_rows = pd.DataFrame([
    {"Name": "Sandy", "Age": 28, "Job": "Engineer"},
    {"Name": "Eugene", "Age": 60, "Job": "Manager"}
], index=["Employee 4", "Employee 5"])

df = pd.concat([df, new_rows])
print(df)