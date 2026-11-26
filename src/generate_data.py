import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Reproducibility
np.random.seed(42)

# Number of synthetic records
N_RECORDS = 2000

# Synthetic data options
divisions = [
	"Central",
	"Western",
	"Northern",
	"Eastern"
]

crime_categories = [
	"Online Fraud",
	"Phishing",
	"Identity Misuse",
	"Social Engineering",
	"Investment Scam"
]

victim_types = [
	"Individual",
	"Business"
]

report_channels = [
	"Online",
	"Phone",
	"Walk-in",
	"Email"
]

statuses = [
	"Open",
	"Under Review",
	"Closed"
]

severity_levels = [
	"Low",
	"Medium",
	"High",
	"Critical"
]

# Base date
start_date = datetime(2025, 1, 1)

records = []

for i in range(N_RECORDS):
	incident_date = start_date + timedelta(
		days=np.random.randint(0, 730)
	)

	reporting_delay = np.random.randint(0, 31)

	report_date = incident_date + timedelta(
		days=reporting_delay
	)

	record = {
		"incident_id": f"CW-{i+1:05d}",
		"report_date": report_date.date(),
		"division": np.random.choice(divisions),
		"crime_category": np.random.choice(crime_categories),
		"victim_type": np.random.choice(victim_types),
		"loss_amount": round(
			max(0, np.random.normal(2500, 1500)),
			2
		),
		"report_channel": np.random.choice(report_channels),
		"status": np.random.choice(statuses),
		"severity_level": np.random.choice(
			severity_levels,
			p=[0.40, 0.30, 0.20, 0.10]
		),
		"reporting_delay_days": reporting_delay
	}

	records.append(record)

# Create DataFrame
df = pd.DataFrame(records)

# Save Dataset
df.to_csv(
	"data/synthetic_cybercrime.csv",
	index=False
)

print(f"{len(df)} records created.")
print(df.head())
