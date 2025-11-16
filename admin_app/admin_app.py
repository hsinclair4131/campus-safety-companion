import streamlit as st
import pandas as pd
from datetime import datetime

from streamlit_folium import st_folium
import folium

# Page config stays OUTSIDE the function
st.set_page_config(
    page_title="CSC Admin Dashboard",
    page_icon="🚓",
    layout="wide"
)

def admin_dashboard():
    st.title("🚓 CSC ADMIN DASHBOARD")
    st.markdown("ECSU Police & Dispatch Control Panel")

    tabs = st.tabs(["Live Alerts", "Reports", "User Locations", "System Logs"])

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
    with tabs[2]:
        st.subheader("📍 Real-time GPS Tracking – Command Center Map")

        # ECSU center coords
        ecsu_lat, ecsu_lon = 36.2796, -76.2130

        # Create tactical map
        map_admin = folium.Map(
            location=[ecsu_lat, ecsu_lon],
            zoom_start=17,
            tiles="CartoDB dark_matter",   # Tactical theme
            control_scale=True
        )

        # --- Create LayerGroups ---
        sos_layer = folium.FeatureGroup(name="🚨 Student SOS Alerts")
        police_layer = folium.FeatureGroup(name="🚓 Police Patrol Units")
        zones_layer = folium.FeatureGroup(name="🛑 Restricted / Threat Zones")

        # --- Example SOS Alerts (Prototypes) ---
        example_users = [
            {"name": "Student A", "lat": 36.2799, "lon": -76.2135},
            {"name": "Student B", "lat": 36.2804, "lon": -76.2128},
            {"name": "Student C", "lat": 36.2788, "lon": -76.2141},
        ]

        for u in example_users:
            folium.CircleMarker(
                location=[u["lat"], u["lon"]],
                radius=10,
                color="red",
                fill=True,
                fill_color="red",
                fill_opacity=0.9,
                popup=f"🚨 SOS from {u['name']}"
            ).add_to(sos_layer)

        # --- Police HQ Marker ---
        folium.Marker(
            location=[36.2792, -76.2140],
            popup="🚓 Campus Police HQ",
            icon=folium.Icon(color="blue", icon="star")
        ).add_to(police_layer)

        # --- Hazard Zone Example ---
        folium.Polygon(
            locations=[
                [36.2795, -76.2135],
                [36.2790, -76.2131],
                [36.2787, -76.2137],
            ],
            color="orange",
            fill=True,
            fill_opacity=0.3,
            popup="⚠ Potential Risk Area"
        ).add_to(zones_layer)

        # Add layers to the map
        sos_layer.add_to(map_admin)
        police_layer.add_to(map_admin)
        zones_layer.add_to(map_admin)

        # Enable layer toggles
        folium.LayerControl(collapsed=False).add_to(map_admin)

        # Render map in Streamlit (large)
        st_folium(
            map_admin,
            width=1400,
            height=750
        )

    # --------------------------------------------------------------------
    # SYSTEM LOGS
    # --------------------------------------------------------------------
    with tabs[3]:
        st.subheader("System Logs")
        st.write("All admin activities will be tracked here.")

# ------------------------------
# MAIN EXECUTION
# ------------------------------
if __name__ == "__main__":
    admin_dashboard()

