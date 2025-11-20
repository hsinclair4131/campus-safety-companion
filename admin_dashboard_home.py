import streamlit as st
import pandas as pd
from datetime import datetime

# --- Supabase Backend ---
from supabase_backend import (
    get_all_sos,
    get_anonymous_reports,
    push_admin_alert,
)

# --- Tactical Page Config ---
st.set_page_config(
    page_title="Admin Dashboard - Tactical Mode",
    layout="wide",
    page_icon="🛰️"
)

# --- Tactical Styling ---
TACTICAL_CSS = """
<style>
body {
    background-color: #0d1117 !important;
    color: #e6edf3 !important;
}

[data-testid="stSidebar"] {
    background-color: #161b22 !important;
    border-right: 1px solid #1f6feb;
}

.sidebar-text {
    color: #e6edf3 !important;
}

h1, h2, h3, h4, h5, p {
    color: #e6edf3 !important;
}

.metric-box {
    background-color: #161b22;
    padding: 20px;
    border-radius: 10px;
    border-left: 4px solid #1f6feb;
}

.metric-value {
    font-size: 32px;
    font-weight: 700;
    color: #1f6feb;
}

.success-text {
    color: #00d084 !important;
    font-weight: bold;
}
</style>
"""

st.markdown(TACTICAL_CSS, unsafe_allow_html=True)

# --- Page Header ---
st.markdown("## 🛰️ Tactical Operations Dashboard")
st.markdown("<span class='success-text'>You are logged in. Authorization Level: ADMIN-1</span>", unsafe_allow_html=True)
st.write("---")

# --- Load Supabase Data ---
sos_data = get_all_sos() or []
incident_logs = get_anonymous_reports() or []

drone_count = 0               # placeholder (no drone table yet)
student_count = 0             # placeholder (add table if needed)
alert_count = len(sos_data)   # active SOS alerts

# --- Metrics Row ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("<div class='metric-box'><h4>Total Drones</h4>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric-value'>{drone_count}</div></div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='metric-box'><h4>Registered Students</h4>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric-value'>{student_count}</div></div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='metric-box'><h4>Active SOS Alerts</h4>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric-value' style='color:#ff4747;'>{alert_count}</div></div>", unsafe_allow_html=True)

with col4:
    st.markdown("<div class='metric-box'><h4>System Health</h4>", unsafe_allow_html=True)
    st.markdown("<div class='metric-value' style='color:#00d084;'>OPTIMAL</div></div>", unsafe_allow_html=True)

st.write("---")

# --- Activity Log Preview ---
st.markdown("### 📝 Recent Activity")

if len(incident_logs) == 0:
    st.info("No incident reports yet.")
else:
    df = pd.DataFrame([
        {"Timestamp": log["timestamp"], "Report": log["report"]}
        for log in incident_logs
    ])
    st.table(df)

st.write("---")

# Admin Message Sender (Optional)
st.markdown("### 📢 Send Tactical Broadcast Alert")
msg = st.text_input("Enter tactical alert message:")

if st.button("Send Tactical Alert"):
    if msg.strip():
        push_admin_alert(msg)
        st.success("🔥 Tactical Alert Broadcasted")
    else:
        st.warning("Please type a message first.")
