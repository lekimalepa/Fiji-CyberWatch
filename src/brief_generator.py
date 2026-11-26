import pandas as pd

# Load dataset
df = pd.read_csv("data/synthetic_cybercrime.csv")

# Basic calculations
current_incidents = len(df)
total_loss = df["loss_amount"].sum()
avg_delay = df["reporting_delay_days"].mean()
top_category = df["crime_category"].value_counts().idxmax()
top_division = df["division"].value_counts().idxmax()

# Generate brief
print("=" * 60)
print("CYBERWATCH INTELLIGENCE REPORTING MODULE")
print("=" * 60)

print("\n1. Observation")
print(f"{current_incidents} synthetic cybercrime records were analysed.")

print("\n2. Comparison")
print(f"The largest recorded category was {top_category}.")

print("\n3. Interpretation")
print(
	"The concentration within the leading category may indicate "
	"an area for further analytical review."
)

print("\n4. Analytical Limitation")
print(
	"The results are based entirely on synthetic demonstration data "
	"and do not represent actual crime activity."
)

print("\n5. Analyst Consideration")
print(
	f"{top_division} recorded the highest incident volume and may warrant "
	"additional review within this demonstration."
)

print("\nAdditional Statistics")
print(f"Total Financial Loss: FJD {total_loss:,.2f}")
print(f"Average Reporting Delay: {avg_delay:.2f} days")
