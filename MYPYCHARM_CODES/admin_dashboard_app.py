# ADMIN DASHBOARD APP
import streamlit as st

# Redirect if not logged in
if "logged_in" not in st.session_state:
    st.error("You must log in first.")
    st.stop()

import streamlit as st
import pandas as pd
from datetime import datetime

# ------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------
st.set_page_config(
    page_title="CSC Admin Command Center",
    page_icon="🚨",
    layout="wide"
)

# ------------------------------------------------------
# TITLE + HEADER
# ------------------------------------------------------
st.title("🚨 CSC Admin Command Center")
st.markdown("### ECSU Police Department • Real-Time Oversight Dashboard")

st.markdown("---")

# ------------------------------------------------------
# METRICS ROW (TOP)
# ------------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Active SOS Alerts", 0)

with col2:
    st.metric("Students Being Tracked", 0)

with col3:
    st.metric("Incidents Logged Today", 0)

st.markdown("---")

# ------------------------------------------------------
# LIVE SOS FEED
# ------------------------------------------------------
st.markdown("### 🚨 Live SOS Alerts Feed")

sos_placeholder = st.empty()

if st.button("Simulate Incoming SOS Alert"):
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sos_placeholder.error(f"🚨 **SOS Triggered** at {time_now} • Student ID: 12922 • Location: Jenkins Hall")

st.caption("This area will display real-time SOS events when connected to your backend data source.")

st.markdown("---")

# ------------------------------------------------------
# GPS MAP PLACEHOLDER
# ------------------------------------------------------
st.markdown("### 📍 GPS Tracking Map")

st.info("""
The live map will display real-time student emergency locations,
movement history, and heatmap overlays.

**Next Step:** Enable Folium or PyDeck mapping.
""")

st.markdown("---")

# ------------------------------------------------------
# INCIDENT LOG PREVIEW
# ------------------------------------------------------
st.markdown("### 📝 Recent Incident Log")

# Create a placeholder table for now
sample_data = {
    "Timestamp": [datetime.now().strftime("%H:%M:%S")],
    "Type": ["System Ready"],
    "Details": ["Awaiting events..."]
}

df = pd.DataFrame(sample_data)

st.table(df)

st.caption("This table will update dynamically as reports and SOS events are logged.")

# ------------------------------------------------------
# FOOTER
# ------------------------------------------------------
st.markdown("---")
st.markdown("##### CSC Admin Dashboard • Streamlit Prototype")
