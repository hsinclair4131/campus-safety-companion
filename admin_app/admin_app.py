import streamlit as st
import pandas as pd
from datetime import datetime

from streamlit_folium import st_folium
import folium

# Page config
st.set_page_config(
    page_title="CSC Admin Dashboard",
    page_icon="🚓",
    layout="wide"
)

def admin_dashboard():
    st.title("🚓 CSC ADMIN DASHBOARD")
    st.markdown("ECSU Police & Dispatch Control Panel")

    tabs = st.tabs([
        "Live Alerts",
        "Reports",
        "User Locations",
        "System Logs",
        "Drone Deployment — A.L.I.C.E."
    ])

    # --------------------------------------------------------------------
    # LIVE ALERTS
    # --------------------------------------------------------------------
    with tabs[0]:
        st.subheader("Send Emergency Broadcast")
        alert = st.text_input("Enter alert message:")
        
        if st.button("Send Alert"):
            st.error(f"🚨 ALERT BROADCASTED: {alert}")
            st.success("Alert pushed to student app.")

    # --------------------------------------------------------------------
    # REPORTS
    # --------------------------------------------------------------------
    with tabs[1]:
        st.subheader("Incoming Anonymous Reports")
        st.info("This is where submitted student reports will appear.")

    # --------------------------------------------------------------------
    # USER LOCATIONS – COMMAND CENTER MAP
    # --------------------------------------------------------------------
       # --------------------------------------------------------------------
    # USER LOCATIONS – COMMAND CENTER MAP
    # --------------------------------------------------------------------
    with tabs[2]:
        st.subheader("📍 Real-time GPS Tracking – Command Center Map")

        # Day/Night Toggle
        mode = st.radio(
            "Select Map Mode:",
            ["🌙 Night Ops", "☀️ Day Ops"],
            horizontal=True
        )

        if mode == "🌙 Night Ops":
            map_tiles = "CartoDB dark_matter"
        else:
            map_tiles = "CartoDB positron"  # clean white daytime map

        # Campus center coords
        ecsu_lat, ecsu_lon = 36.2796, -76.2130

        # Tactical map WITH mode toggle
        map_admin = folium.Map(
            location=[ecsu_lat, ecsu_lon],
            zoom_start=17,
            tiles=map_tiles,
            control_scale=True
        )


    # --------------------------------------------------------------------
    # SYSTEM LOGS
    # --------------------------------------------------------------------
    with tabs[3]:
        st.subheader("System Logs")
        st.write("All admin activities will be tracked here.")

    # --------------------------------------------------------------------
    # DRONE DEPLOYMENT — A.L.I.C.E.
    # --------------------------------------------------------------------
    with tabs[4]:
        st.subheader("🛸 Drone Deployment — Managed by A.L.I.C.E.")
        st.markdown("Autonomous UAV Command Center")

        # Drone registry
        drone_ids = [f"Drone {i+1}" for i in range(10)]

        drone_data = pd.DataFrame({
            "Drone ID": drone_ids,
            "Status": ["Idle", "Charging", "In-Flight", "Idle", "Returning",
                       "Offline", "In-Flight", "Charging", "Idle", "Idle"],
            "Mission": [
                "None", "None", "Surveillance", "None", "Return to Base",
                "None", "Perimeter Scan", "None", "None", "None"
            ],
            "Battery (%)": [96, 45, 78, 83, 52, 0, 67, 39, 90, 88]
        })

        st.markdown("### Registered UAV Units")
        st.dataframe(drone_data, use_container_width=True)

        # ------------------------------------------
        # DEPLOY DRONE (with battery check)
        # ------------------------------------------
        st.markdown("---")
        st.markdown("## 🚀 Deploy Drone (A.L.I.C.E. Safety Pre-check)")

        selected_drone = st.selectbox("Select UAV", drone_ids)
        mission = st.selectbox("Mission Type", [
            "Surveillance",
            "Escort",
            "SOS Response",
            "Thermal Sweep",
            "Perimeter Scan",
            "Recon",
            "Payload Delivery"
        ])

        if st.button("Deploy Drone"):
            drone_row = drone_data[drone_data["Drone ID"] == selected_drone].iloc[0]
            battery = drone_row["Battery (%)"]

            if battery < 20:
                st.error(f"❌ Deployment Denied — {selected_drone} battery at {battery}%.")
                st.warning("A.L.I.C.E.: Drone must be charged before launch.")
            elif drone_row["Status"] not in ["Idle", "Charging"]:
                st.error(f"❌ Deployment Denied — {selected_drone} not available.")
            else:
                st.success(f"🛸 {selected_drone} launching for **{mission}** mission.")
                st.info("A.L.I.C.E. executing autonomous routing and telemetry.")

        # ------------------------------------------
        # RECOVER DRONE
        # ------------------------------------------
        st.markdown("---")
        st.markdown("## 🛬 Recover Drone")

        recover_drone = st.selectbox("Select UAV to Recover", drone_ids)

        if st.button("Recover Selected Drone"):
            st.warning(f"📡 A.L.I.C.E. issuing RTB for {recover_drone}...")
            st.success(f"🛸 {recover_drone} successfully recovered. Status: **Idle**")

        # ------------------------------------------
        # CHARGE DRONE
        # ------------------------------------------
        st.markdown("## 🔋 Charge Drone")

        charge_drone = st.selectbox("Select UAV to Charge", drone_ids)

        if st.button("Charge Selected Drone"):
            st.info(f"🔌 Charging initiated for {charge_drone}...")
            st.success(f"🔋 {charge_drone} battery restored to 100%")

        # ------------------------------------------
        # EMERGENCY GLOBAL RECALL
        # ------------------------------------------
        st.markdown("---")
        st.markdown("## 🚨 Emergency Recall (All UAVs)")

        if st.button("Recall ALL Drones Immediately"):
            st.error("⚠ EMERGENCY RECALL ACTIVATED")
            st.warning("A.L.I.C.E.: Broadcasting universal RTB command...")
            st.success("🛸 All drones returning to base.")

# ------------------------------
# MAIN
# ------------------------------
if __name__ == "__main__":
    admin_dashboard()
