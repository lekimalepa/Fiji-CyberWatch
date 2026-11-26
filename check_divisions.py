import pandas as pd

df = pd.read_csv(
    "data/synthetic_cybercrime.csv"
)

print(df["division"].unique())