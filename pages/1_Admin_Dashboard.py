import streamlit as st
from firebase_admin import firestore

# Firestore client already initialized in main.py
db = firestore.client()

def render():
    # -------------- ACCESS CONTROL ----------------
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.error("Unauthorized. Please log in from the main page.")
        st.stop()

    st.title("🛡️ Admin Dashboard")
    st.caption("Welcome to the ECSU Campus Safety Command Center.")

    admin_email = st.session_state.get("admin_email", "Unknown")
    uid = st.session_state.get("admin_uid", None)

    st.markdown(f"### 👋 Logged in as: **{admin_email}**")

    # ---------------- QUICK METRICS ----------------
    st.write("---")
    st.subheader("📊 System Overview")

    col1, col2, col3 = st.columns(3)

    # Drones count
    drones_count = len(list(db.collection("drones").stream()))
    # Students count
    students_count = len(list(db.collection("students").stream()))
    # Active SOS alerts
    sos_count = len(list(db.collection("sos_alerts").stream()))

    col1.metric("Active Drones", drones_count)
    col2.metric("Registered Students", students_count)
    col3.metric("Live SOS Alerts", sos_count)

    # ---------------- SYSTEM LOGS PREVIEW ----------------
    st.write("---")
    st.subheader("📜 Recent System Activity")

    logs = db.collection("system_logs").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(5).stream()

    for log in logs:
        entry = log.to_dict()
        st.markdown(
            f"**{entry.get('timestamp', '')}** — {entry.get('message', 'No message')}"
        )

    st.write("---")
    st.info("Navigate using the sidebar to access Drone Fleet, Live Tracking, SOS Alerts, and Settings.")
