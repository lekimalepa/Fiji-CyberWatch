import pandas as pd


# Load dataset
df = pd.read_csv("data/synthetic_cybercrime.csv")


def total_incidents():
	return len(df)


def total_financial_loss():
	return round(df["loss_amount"].sum(), 2)


def average_reporting_delay():
	return round(
		df["reporting_delay_days"].mean(),
		2
	)


def incidents_by_division():
	return (
		df["division"]
		.value_counts()
		.sort_values(ascending=False)
	)


def incidents_by_category():
	return (
		df["crime_category"]
		.value_counts()
		.sort_values(ascending=False)
	)


def severity_distribution():
	return (
		df["severity_level"]
		.value_counts()
		.sort_values(ascending=False)
	)


print("=" * 50)
print("CYBERWATCH ANALYTICS")
print("=" * 50)

print("\nTotal Incidents:")
print(total_incidents())

print("\nTotal Financial Loss:")
print(f"FJD {total_financial_loss():,.2f}")

print("\nAverage Reporting Delay:")
print(f"{average_reporting_delay()} days")

print("\nIncidents by Division:")
print(incidents_by_division())

print("\nIncidents by Crime Category:")
print(incidents_by_category())

print("\nSeverity Distribution:")
print(severity_distribution())
print("\nMost Common Crime Category:")
print(
    incidents_by_category().idxmax()
)

print("\nHighest Reporting Division:")
print(
    incidents_by_division().idxmax()
)