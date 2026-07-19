import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_csv("Python\Libraries\Matplotlib\data.csv")
type_count = df["Type1"].value_counts(ascending=True)
plt.barh(type_count.index, type_count.values, color="#6a00ff",
                                                edgecolor="black")

plt.title("# of Pokemon by Primary Type")
plt.xlabel("Count")
plt.ylabel("Type")
plt.tight_layout()
plt.show()

