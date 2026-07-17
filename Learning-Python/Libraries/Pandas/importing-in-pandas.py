import pandas as pd
 
df = pd.read_json("Python\Libraries\Pandas\gen1pokemon.json")

print(df.to_string())