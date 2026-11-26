import pandas as pd

df = pd.read_csv("data/synthetic_cybercrime.csv")

print("=" * 50)
print("CYBERWATCH DATASET VALIDATION")
print("=" * 50)

print("\nDataset Shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 Records:")
print(df.head())

print("\nDivision Counts:")
print(df["division"].value_counts())

print("\nCrime Category Counts:")
print(df["crime_category"].value_counts())

print("\nSeverity Levels:")
print(df["severity_level"].value_counts())

print("\nTotal Financial Loss:")
print(f"FJD {df['loss_amount'].sum():,.2f}")

print("\nAverage Reporting Delay:")
print(round(df["reporting_delay_days"].mean(), 2), "days")