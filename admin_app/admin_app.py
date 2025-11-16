import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="CSC Admin Dashboard", page_icon="🚓", layout="wide")

st.title("🚓 CSC ADMIN DASHBOARD")
st.markdown("ECSU Police & Dispatch Control Panel")

tabs = st.tabs(["Live Alerts", "Reports", "User Locations", "System Logs"])

# --- LIVE ALERTS ---
with tabs[0]:
    st.subheader("Send Emergency Broadcast")
    alert = st.text_input("Enter alert message:")
    
    if st.button("Send Alert"):
        st.error(f"🚨 ALERT BROADCASTED: {alert}")
        st.success("Alert pushed to student app.")

# --- REPORTS ---
with tabs[1]:
    st.subheader("Incoming Anonymous Reports")
    st.info("This is where submitted student reports will appear.")

# --- GPS ---
with tabs[2]:
    st.subheader("Real-time GPS (Prototype)")
    st.write("Live map will be displayed here in full build.")

# --- LOGS ---
with tabs[3]:
    st.subheader("System Logs")
    st.write("All admin activities will be tracked here.")

