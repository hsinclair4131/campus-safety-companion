# ADMIN DASHBOARD (SUPABASE BACKEND VERSION)
import streamlit as st
import pandas as pd
from datetime import datetime

# 🔥 IMPORT SUPABASE BACKEND (NOT FIREBASE)
from supabase_backend import (
    push_admin_alert,     # replaces push_alert
    get_latest_alert,
    push_sos,
    get_all_sos,          # NEW — we will define below
    get_anonymous_reports # NEW — we will define below
)

# ------------------------------------------------------
# REDIRECT IF NOT LOGGED IN
# ------------------------------------------------------
if "logged_in" not in st.session_state:
    st.error("You must log in first.")
    st.stop()

# ------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------
st.set_page_config(
    page_title="CSC Admin Command Center",
    page_icon="🚨",
    layout="wide"
)

# ------------------------------------------------------
# HEADER
# ------------------------------------------------------
st.title("🚨 CSC Admin Command Center")
st.markdown("### ECSU Police Department • Real-Time Oversight Dashboard")
st.markdown("---")

# ------------------------------------------------------
# LOAD DATA FROM SUPABASE
# ------------------------------------------------------
sos_data = get_all_sos() or []
incident_logs = get_anonymous_reports() or []

active_sos_count = len(sos_data)
tracked_students = active_sos_count
incident_count = len(incident_logs)

# ------------------------------------------------------
# METRICS ROW
# ------------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Active SOS Alerts", active_sos_count)

with col2:
    st.metric("Students Being Tracked", tracked_students)

with col3:
    st.metric("Incidents Logged Today", incident_count)

st.markdown("---")

# ------------------------------------------------------
# LIVE SOS FEED
# ------------------------------------------------------
st.markdown("### 🚨 Live SOS Alerts Feed")

if active_sos_count == 0:
    st.info("No active SOS alerts at this time.")
else:
    for sos in sos_data:
        ts = sos.get("timestamp", "")
        lat = sos.get("lat", "")
        lon = sos.get("lon", "")
        st.error(f"🚨 **SOS Triggered** • Location: ({lat}, {lon}) • Time: {ts}")

st.markdown("---")

# ------------------------------------------------------
# SEND MANUAL BROADCAST ALERT (USES SUPABASE)
# ------------------------------------------------------
st.markdown("### 📢 Send Emergency Broadcast Alert")

alert_message = st.text_input("Enter alert message:")

if st.button("Send Broadcast Alert"):
    if alert_message.strip():
        push_admin_alert(alert_message)  # SUPABASE VERSION
        st.success("🔥 ALERT BROADCASTED TO STUDENTS (LIVE)")
    else:
        st.warning("Please enter a message before sending.")

st.markdown("---")

# ------------------------------------------------------
# INCIDENT LOG PREVIEW
# ------------------------------------------------------
st.markdown("### 📝 Recent Incident Reports (Anonymous)")

if len(incident_logs) == 0:
    st.info("No reports submitted yet.")
else:
    df = pd.DataFrame([
        {
            "Timestamp": log.get("timestamp", ""),
            "Report": log.get("report", "")
        }
        for log in incident_logs
    ])
    st.table(df)

st.caption("Incident logs update in real time as students submit reports.")

st.markdown("---")
st.markdown("##### CSC Admin Dashboard • Connected to Supabase Backend")

