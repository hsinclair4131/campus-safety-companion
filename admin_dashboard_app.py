# ADMIN DASHBOARD APP — FULL BACKEND INTEGRATED
import streamlit as st
import pandas as pd
from datetime import datetime

# 🔥 IMPORT FIREBASE BACKEND
from firebase_backend import (
    push_alert,
    get_latest_alert,
    push_sos,
    get_all_sos,
    get_anonymous_reports
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
# TITLE + HEADER
# ------------------------------------------------------
st.title("🚨 CSC Admin Command Center")
st.markdown("### ECSU Police Department • Real-Time Oversight Dashboard")
st.markdown("---")

# ------------------------------------------------------
# METRICS ROW
# ------------------------------------------------------
col1, col2, col3 = st.columns(3)

# SOS alerts – REAL DATA COUNT
sos_data = get_all_sos()
active_sos_count = len(sos_data)

# Students being tracked (currently same as SOS count)
tracked_students = active_sos_count

# Incident logs from anonymous reports
incident_logs = get_anonymous_reports()
incident_count = len(incident_logs)

with col1:
    st.metric("Active SOS Alerts", active_sos_count)

with col2:
    st.metric("Students Being Tracked", tracked_students)

with col3:
    st.metric("Incidents Logged Today", incident_count)

st.markdown("---")

# ------------------------------------------------------
#  🔥 REAL-TIME SOS FEED
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
#  🔥 SEND MANUAL ADMIN ALERT (BRODCAST TO STUDENT APP)
# ------------------------------------------------------
st.markdown("### 📢 Send Emergency Broadcast Alert")

alert_message = st.text_input("Enter alert message:")

if st.button("Send Broadcast Alert"):
    if alert_message.strip():
        push_alert(alert_message)
        st.success("🔥 ALERT BROADCASTED TO STUDENTS (LIVE)")
    else:
        st.warning("Please enter a message before sending.")

st.markdown("---")

# ------------------------------------------------------
#  🔥 GPS MAP PLACEHOLDER (NEXT STEP: LIVE LOCATION MAP)
# ------------------------------------------------------
st.markdown("### 📍 GPS Tracking Map")

st.info("""
Live map will show real-time student emergency locations.\n
Next step: Integrate Folium or PyDeck with Firestore sos_reports.
""")

st.markdown("---")

# ------------------------------------------------------
#  🔥 REAL INCIDENT LOG PREVIEW
# ------------------------------------------------------
st.markdown("### 📝 Recent Incident Reports (Anonymous)")

if len(incident_logs) == 0:
    st.info("No reports submitted yet.")
else:
    table_data = []
    for log in incident_logs:
        table_data.append({
            "Timestamp": log.get("timestamp", ""),
            "Report": log.get("report", "")
        })
    
    df = pd.DataFrame(table_data)
    st.table(df)

st.caption("Incident logs update in real time as students submit reports.")

# ------------------------------------------------------
# FOOTER
# ------------------------------------------------------
st.markdown("---")
st.markdown("##### CSC Admin Dashboard • Connected to Live Firebase Backend")
