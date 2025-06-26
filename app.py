import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium

# -----------------------
# Dummy Site Data Loader
# -----------------------
def load_site_data():
    data = {
        'Site ID': ["A1", "A2", "A3", "A4"],
        'Latitude': [40.7128, 36.7783, 39.7392, 34.0522],
        'Longitude': [-74.0060, -119.4179, -104.9903, -118.2437],
        'Solar Score (0–100)': [82, 75, 88, 69],
        'Distance to Road (km)': [3.5, 8.2, 1.1, 2.7],
        'Flood Risk': ["Low", "High", "Medium", "Low"]
    }
    return pd.DataFrame(data)

# ---------------------
# Simple Filter Logic
# ---------------------
def filter_sites(df, min_solar, max_distance, flood_ok):
    return df[(df['Solar Score (0–100)'] >= min_solar) &
              (df['Distance to Road (km)'] <= max_distance) &
              (df['Flood Risk'].isin(flood_ok))]

# ---------------------
# App UI and Logic
# ---------------------
st.set_page_config(page_title="Paces Site Selector", layout="wide")

st.markdown("""
    <h1 style='text-align: center;'>Where Should We Build? 🌍</h1>
    <h4 style='text-align: center; color: gray;'>A mini site screening demo inspired by Paces (YC S22)</h4>
    <hr style='margin-top: 10px;'>
""", unsafe_allow_html=True)

# Sidebar filters
with st.sidebar:
    st.header("🔍 Filter Criteria")
    solar_score = st.slider("Minimum Solar Score", 0, 100, 70)
    distance_limit = st.slider("Max Distance to Road (km)", 1, 10, 5)
    flood_risks = st.multiselect("Allowable Flood Risk", ["Low", "Medium", "High"], default=["Low", "Medium"])

# Load and filter data
site_df = load_site_data()
filtered_df = filter_sites(site_df, solar_score, distance_limit, flood_risks)

st.success(f"{len(filtered_df)} site(s) match your criteria")
st.dataframe(filtered_df, use_container_width=True)

st.markdown("### 📍 Site Map")
m = folium.Map(location=[38.5, -97.0], zoom_start=5)
for _, row in filtered_df.iterrows():
    popup = f"Site: {row['Site ID']}<br>Solar: {row['Solar Score (0–100)']}<br>Risk: {row['Flood Risk']}"
    folium.Marker(location=[row['Latitude'], row['Longitude']], tooltip=row['Site ID'], popup=popup).add_to(m)

st_folium(m, width=1000, height=500)

# Footer
st.markdown("""
---
<p style='text-align: center;'>Built with ❤️ by Bhargav Mylavarapu • Inspired by @Paces (YC S22)</p>
""", unsafe_allow_html=True)
