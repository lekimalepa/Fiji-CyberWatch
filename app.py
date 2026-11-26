import datetime

import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
	page_title="Fiji CyberWatch",
	page_icon="🚔",
	layout="wide"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

df = pd.read_csv("data/synthetic_cybercrime.csv")

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("🚔 Fiji CyberWatch")

st.sidebar.markdown("""
### About

Cybercrime Intelligence Analytics &
Decision-Support Demonstration

**Data Classification**

Synthetic Demonstration Data Only

**Project Owner**

Lekima Maka

**Technology**

- Python
- Pandas
- Streamlit
- Plotly

**Project Status**

Prototype V1.0

**Data Records**

2,000 Synthetic Records
""")

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🚔 Fiji CyberWatch")
st.markdown("""
### Data → Analysis → Interpretation → Reporting
""")
st.subheader(
	"Cybercrime Intelligence Analytics & Decision-Support Demonstration"
)

st.info(
	"Synthetic Demonstration Data Only - Not Operational Police Data"
)

st.caption(
	f"Dashboard generated on: "
	f"{datetime.datetime.now().strftime('%d %B %Y %H:%M')}"
)

# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------

total_incidents = len(df)
total_loss = df["loss_amount"].sum()
avg_delay = df["reporting_delay_days"].mean()
leading_category = (
	df["crime_category"]
	.value_counts()
	.idxmax()
)

st.markdown("## Executive Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
	st.metric(
		"Incident Reports Analysed",
		f"{total_incidents:,}"
	)

with col2:
	st.metric(
		"Reported Financial Impact",
		f"FJD {total_loss:,.0f}"
	)

with col3:
	st.metric(
		"Average Reporting Delay",
		f"{avg_delay:.1f} Days"
	)

with col4:
	st.metric(
		"Leading Category",
		leading_category
	)

# --------------------------------------------------
# FILTERS
# --------------------------------------------------

st.sidebar.header("Filters")

selected_division = st.sidebar.multiselect(
	"Division",
	options=df["division"].unique(),
	default=df["division"].unique()
)

selected_category = st.sidebar.multiselect(
	"Crime Category",
	options=df["crime_category"].unique(),
	default=df["crime_category"].unique()
)

filtered_df = df[
	(df["division"].isin(selected_division))
	&
	(df["crime_category"].isin(selected_category))
]

# --------------------------------------------------
# TABS
# --------------------------------------------------

tab1, tab2, tab3, tab4 = st.tabs(
	[
		"Overview",
		"Trends",
		"Geographic Explorer",
		"Intelligence Reporting"
	]
)

# ==================================================
# TAB 1 OVERVIEW
# ==================================================

with tab1:

	st.header("Overview")

	category_counts = (
		filtered_df["crime_category"]
		.value_counts()
		.reset_index()
	)

	category_counts.columns = [
		"Crime Category",
		"Incidents"
	]

	fig = px.bar(
		category_counts,
		x="Crime Category",
		y="Incidents",
		title="Incidents by Crime Category"
	)

	st.plotly_chart(
		fig,
		use_container_width=True
	)

# ==================================================
# TAB 2 TRENDS
# ==================================================

with tab2:

	st.header("Trend Analysis")

	filtered_df["report_date"] = pd.to_datetime(
		filtered_df["report_date"]
	)

	monthly = (
		filtered_df
		.groupby(
			filtered_df["report_date"]
			.dt.to_period("M")
		)
		.size()
		.reset_index(name="Incidents")
	)

	monthly["report_date"] = (
		monthly["report_date"]
		.astype(str)
	)

	fig2 = px.line(
		monthly,
		x="report_date",
		y="Incidents",
		markers=True,
		title="Monthly Incident Trend"
	)

	st.plotly_chart(
		fig2,
		use_container_width=True
	)

# ==================================================
# TAB 3 DIVISIONS
# ==================================================

with tab3:

	st.header("🗺️ Geographic Explorer")

	st.caption(
		"Division-level Cybercrime Visualisation"
	)

	summary = (
		filtered_df
		.groupby("division")
		.agg(
			Incidents=("incident_id", "count"),
			Financial_Loss=("loss_amount", "sum"),
			Average_Delay=("reporting_delay_days", "mean"),
			Average_Loss=("loss_amount", "mean")
		)
		.reset_index()
	)

	summary["Financial_Loss"] = summary["Financial_Loss"].round(2)
	summary["Average_Loss"] = summary["Average_Loss"].round(2)
	summary["Average_Delay"] = summary["Average_Delay"].round(1)
	summary = summary.sort_values(
		by="Incidents",
		ascending=False
	)

	division_map = folium.Map(
		location=[-17.8, 180.0],
		zoom_start=6
	)

	division_colors = {
		"Central": "#2563eb",
		"Western": "#f97316",
		"Northern": "#16a34a",
		"Eastern": "#9333ea"
	}

	division_coordinates = {
		"Central": (-18.1248, 178.4501),
		"Western": (-17.7765, 177.4350),
		"Northern": (-16.4333, 179.3667),
		"Eastern": (-17.7134, -178.0650)
	}

	for _, division in summary.iterrows():
		division_name = division["division"]
		latitude, longitude = division_coordinates[division_name]
		if longitude < 0:
			longitude += 360

		color = division_colors[division_name]
		popup = (
			f"<strong>{division_name} Division</strong><br>"
			f"Incidents: {division['Incidents']:,}<br>"
			f"Financial Loss: FJD "
			f"{division['Financial_Loss']:,.2f}<br>"
			f"Average Delay: {division['Average_Delay']:.1f} days"
		)

		folium.CircleMarker(
			location=[latitude, longitude],
			radius=10,
			color=color,
			weight=2,
			fill=True,
			fill_color=color,
			fill_opacity=0.8,
			tooltip=f"{division_name} Division",
			popup=folium.Popup(popup, max_width=300)
		).add_to(division_map)

	st_folium(
		division_map,
		width=1000,
		height=600
	)

	st.subheader(
		"Division Intelligence Summary"
	)

	st.dataframe(
		summary,
		use_container_width=True
	)

	st.subheader("Geographic Intelligence Notes")

	if summary.empty:
		st.info(
			"No records match the selected filters, so "
			"division insights are unavailable."
		)
	else:
		highest_reporting = summary.iloc[0]
		highest_loss = summary.loc[
			summary["Financial_Loss"].idxmax()
		]
		lowest_delay = summary.loc[
			summary["Average_Delay"].idxmin()
		]

		st.info(
			f"Highest reporting division: "
			f"{highest_reporting['division']} "
			f"({highest_reporting['Incidents']:,} incidents)\n\n"
			f"Highest total loss: {highest_loss['division']} "
			f"(FJD {highest_loss['Financial_Loss']:,.2f})\n\n"
			f"Lowest average reporting delay: {lowest_delay['division']} "
			f"({lowest_delay['Average_Delay']:.1f} days)"
		)

# ==================================================
# TAB 4 REPORTING
# ==================================================

with tab4:

	st.header("Intelligence Reporting Module")

	top_category = (
		filtered_df["crime_category"]
		.value_counts()
		.idxmax()
	)

	top_division = (
		filtered_df["division"]
		.value_counts()
		.idxmax()
	)

	st.subheader("Observation")

	st.write(
		f"{len(filtered_df)} synthetic records were analysed."
	)

	st.subheader("Comparison")

	st.write(
		f"The most common category was "
		f"'{top_category}'."
	)

	st.subheader("Interpretation")

	st.write(
		"The concentration within the leading "
		"category may indicate an area for "
		"further analytical review."
	)

	st.subheader("Analytical Limitation")

	st.write(
		"This application uses synthetic data "
		"for demonstration purposes only and "
		"does not represent actual police data."
	)

	st.subheader("Analyst Consideration")

	st.write(
		f"{top_division} recorded the highest "
		f"incident volume within the selected "
		f"records."
	)
