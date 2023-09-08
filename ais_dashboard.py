# import necessary libraries
import streamlit as st
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt
import seaborn as sns
from aisexplorer.AIS import AIS
import plotly.express as px

df = pd.DataFrame(AIS(return_df=True).get_area_data("USEC"))

# Streamlit app starts here
st.title("AIS Vessels Dashboard")

# Draw the Mapbox Map
st.subheader("Map of East Coast Vessels")

# Set the map default location
map_center = {"latitude": 38.7128, "longitude": -73.0100}
map_data = df[["LAT", "LON"]]

# Convert LAT and LON to numeric, dropping any rows with unconvertible data
df['LAT'] = pd.to_numeric(df['LAT'], errors='coerce')
df['LON'] = pd.to_numeric(df['LON'], errors='coerce')
df.dropna(subset=['LAT', 'LON'], inplace=True)

# Rename the columns for compatibility with st.map
map_data = df.rename(columns={"LAT": "lat", "LON": "lon"})

# Draw the map
st.map(map_data)
# First row: Two columns for bar charts
col1, col3 = st.columns([1, 1])

# First Chart: Count by Country
col1.subheader("Count by Country")
country_count = df['COUNTRY'].value_counts().reset_index()
country_count.columns = ['COUNTRY', 'COUNT']
country_count = country_count.sort_values(by='COUNT', ascending=False)
fig1 = px.bar(country_count, x='COUNTRY', y='COUNT', title="Count by Country")
col1.plotly_chart(fig1, use_container_width=True)

# Third Chart: Count by TYPE_SUMMARY
col3.subheader("Count by TYPE_SUMMARY")
type_count = df['TYPE_SUMMARY'].value_counts().reset_index()
type_count.columns = ['TYPE_SUMMARY', 'COUNT']
type_count = type_count.sort_values(by='COUNT', ascending=False)
fig3 = px.bar(type_count, x='TYPE_SUMMARY', y='COUNT', title="Count by TYPE_SUMMARY")
col3.plotly_chart(fig3, use_container_width=True)

# Second row: One column for scatter plot
col2 = st.columns([1])

# Second Chart: Scatter plot of LENGTH and WIDTH
col2[0].subheader("Scatter plot of LENGTH and WIDTH")
fig2 = px.scatter(df, x='LENGTH', y='WIDTH')
col2[0].plotly_chart(fig2, use_container_width=True)