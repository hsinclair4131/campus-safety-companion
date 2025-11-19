import streamlit as st
from firebase_admin import firestore
import time

db = firestore.client()

def render():

    # -------------------------------------------
    # ACCESS CONTROL
    # -------------------------------------------
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.error("Unauthorized. Please log in from the main page.")
        st.stop()

    st.title("🚨 Dispatcher Command Center")
    st.caption("Live emergency management, SOS routing, and dispatch operations.")

    # -------------------------------------------
    # 1. ACTIVE SOS ALERTS (REAL DATA)
    # -------------------------------------------
    st.subheader("📡 Active SOS Alerts")

    sos_docs = db.collection("sos_alerts").stream()
    sos_list = []

    for doc in sos_docs:
        x = doc.to_dict()
        sos_list.append({
            "id": doc.id,
            "lat": x.get("lat", 0),
            "lon": x.get("lon", 0),
            "severity": x.get("severity", "unknown"),
            "time": x.get("timestamp", "N/A"),
            "status": x.get("status", "active")
        })

    if len(sos_list) == 0:
        st.success("No active SOS alerts. Campus is clear.")
    else:
        for alert in sos_list:
            st.error(
                f"""
                **SOS ID:** {alert['id']}  
                **Severity:** {alert['severity']}  
                **Location:** {alert['lat']}, {alert['lon']}  
                **Time:** {alert['time']}  
                **Status:** {alert['status']}
                """,
                icon="🚨"
            )

    st.write("---")

    # -------------------------------------------
    # 2. DISPATCH ACTION PANEL
    # -------------------------------------------
    st.subheader("🎯 Dispatch Actions")

    action_col1, action_col2 = st.columns(2)

    with action_col1:
        st.markdown("#### Assign Drone to SOS")
        drone_id = st.text_input("Enter Drone ID")
        sos_id = st.text_input("Enter SOS Alert ID")

        if st.button("➤ Assign Drone"):
            if drone_id and sos_id:
                try:
                    db.collection("drones").document(drone_id).update({
                        "mission": f"SOS_RESPONSE_{sos_id}",
                        "status": "online"
                    })
                    st.success(f"Drone {drone_id} dispatched to SOS {sos_id}")
                except Exception as e:
                    st.error(f"Dispatch failed: {e}")
            else:
                st.warning("Provide both Drone ID and SOS ID.")

    with action_col2:
        st.markdown("#### Clear SOS Alert")
        sos_clear_id = st.text_input("Enter SOS ID to Clear")

        if st.button("✔ Mark SOS as Resolved"):
            if sos_clear_id:
                try:
                    db.collection("sos_alerts").document(sos_clear_id).update({
                        "status": "resolved"
                    })
                    st.success(f"SOS {sos_clear_id} marked as resolved.")
                except Exception as e:
                    st.error(f"Error resolving SOS: {e}")
            else:
                st.warning("Enter a valid SOS ID.")

    st.write("---")

    # -------------------------------------------
    # 3. DISPATCH LOGS
    # -------------------------------------------
    st.subheader("📝 Dispatch Log (Past 20 Events)")

    logs = db.collection("dispatch_logs").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(20).stream()

    for entry in logs:
        log = entry.to_dict()
        st.info(
            f"""
            🕒 **{log.get('timestamp', 'N/A')}**  
            - **Event:** {log.get('event', '')}  
            - **Details:** {log.get('details', '')}  
            """
        )

    st.write("---")

    refresh = st.checkbox("🔁 Auto-Refresh (5 sec)", True)
    if refresh:
        time.sleep(5)
        st.rerun()
