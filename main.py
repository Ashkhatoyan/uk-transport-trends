# scripts/main.py

import streamlit as st
import pandas as pd
import sqlite3
import os
import plotly.express as px

st.set_page_config(page_title="🚲 London Cycleways Dashboard", layout="wide")

st.title("🚲 London Cycleways Dashboard")
st.caption("Cycleways data with visual insights")

# Connect to SQLite
db_path = os.path.join("data", "cycleways.db")
conn = sqlite3.connect(db_path)
df = pd.read_sql("SELECT * FROM cycleways", conn)
conn.close()

# Clean column names
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Convert dates
if "date" in df.columns:
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["weekday"] = df["date"].dt.day_name()

# Sidebar Filters
st.sidebar.header("📊 Filter Data")

if "location_name" in df.columns:
    locations = df["location_name"].dropna().unique().tolist()
    selected_locations = st.sidebar.multiselect("Select Locations", locations, default=locations[:5])
    df = df[df["location_name"].isin(selected_locations)]

if "date" in df.columns:
    min_date, max_date = df["date"].min(), df["date"].max()
    start_date, end_date = st.sidebar.date_input("Select Date Range", [min_date, max_date])
    df = df[(df["date"] >= pd.to_datetime(start_date)) & (df["date"] <= pd.to_datetime(end_date))]

# --- Data Table ---
st.subheader("📄 Filtered Data Preview")
st.dataframe(df, use_container_width=True)


if "date" in df.columns:
    df["date"] = pd.to_datetime(df["date"], errors="coerce")  # ensure datetime type
    st.subheader("📆 Daily Bike Count Over Time")
    daily = df.groupby("date")["count"].sum().reset_index()
    fig = px.line(daily, x="date", y="count", title="Daily Total Bike Count")
    st.plotly_chart(fig, use_container_width=True)


# --- Pie Chart: Direction Split ---
if "direction" in df.columns:
    st.subheader("🧭 Direction Breakdown")
    dir_data = df["direction"].value_counts().reset_index()
    dir_data.columns = ["Direction", "Count"]
    fig = px.pie(dir_data, names="Direction", values="Count", title="Bike Directions")
    st.plotly_chart(fig, use_container_width=True)

# --- Bar Chart: Mode Count ---
if "mode" in df.columns and "count" in df.columns:
    st.subheader("🚲 Bike Count by Mode")
    mode_counts = df.groupby("mode")["count"].sum().reset_index()
    mode_counts.columns = ["Mode", "Total Bikes"]
    fig = px.bar(mode_counts, x="Mode", y="Total Bikes", title="Total Bikes by Mode", text="Total Bikes")
    fig.update_traces(textposition='outside')
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No 'mode' and 'count' columns found to show mode count.")



st.success("✅ Dashboard loaded with extra visual insights!")
