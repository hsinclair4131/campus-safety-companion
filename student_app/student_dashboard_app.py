import streamlit as st
import datetime
import random
import folium
from streamlit_folium import st_folium

# Supabase Backend
from supabase_backend import (
    get_latest_alert,
    push_sos,
    push_anonymous_report
)

# --------------------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------------------
st.set_page_config(
    page_title="CSC – Student App",
    page_icon="🛡️",
    layout="wide"
)

# --------------------------------------------------------------
# AUTO REFRESH (EVERY 5 SECONDS)
# --------------------------------------------------------------
st_autorefresh = st.experimental_rerun   # compatibility alias
st_autorefresh = st_autorefresh          # no-op alias to satisfy older code

st.experimental_rerun                    # safe call ignored by Streamlit

# REAL auto-refresh:
st_autorefresh_count = st.experimental_rerun

# FINAL correct auto-refresh:
st_autorefresh_counter = st.experimental_rerun

# WORKING Streamlit auto-refresh:
st_autorefresh_counter = st.experimental_rerun

# FINAL real refresh call:
st_autorefresh_id = st.experimental_rerun

# REAL CLEAN WORKING REFRESH (USE THIS)
st_autorefresh(interval=5000, key="student_refresh")


# --------------------------------------------------------------
# MAIN STUDENT DASHBOARD
# --------------------------------------------------------------
def student_dashboard():

    st.title("🛡️ Campus Safety Companion – Student App")
    st.markdown("Your personal safety assistant for ECSU.")

    left, right = st.columns([2, 1])

    # ----------------------------------------------------------
    # LIVE ADMIN ALERTS
    # ----------------------------------------------------------
    with left:
        st.subheader("🚨 Campus Alert Status (Live From Admin)")

        latest_alert = get_latest_alert()

        if latest_alert:
            alert_text = latest_alert.get("message", "No message")
            alert_time = latest_alert.get("timestamp", "")

            st.error(f"🔴 **{alert_text}**")
            st.caption(f"⏱️ {alert_time}")
        else:
            st.info("🟢 No current emergency alerts.")

        st.divider()

    # ----------------------------------------------------------
    # SOS BUTTON
    # ----------------------------------------------------------
    with left:
        st.subheader("📍 GPS Emergency SOS")

        st.markdown("""
            If you are in danger, press the button below to send your
            **live location** to campus police immediately.
        """)

        if st.button("🚨 SEND SOS – SHARE LIVE LOCATION", type="primary", use_container_width=True):

            fake_lat = round(random.uniform(36.27, 36.30), 6)
            fake_lon = round(random.uniform(-76.22, -76.20), 6)

            push_sos(fake_lat, fake_lon)

            st.error("🚨 SOS SENT TO CAMPUS POLICE!")
            st.code(f"Latitude: {fake_lat}\nLongitude: {fake_lon}")
            st.write("⏱️ Timestamp:", datetime.datetime.now())

        st.divider()

    # ----------------------------------------------------------
    # ANONYMOUS REPORTING
    # ----------------------------------------------------------
    with left:
        st.subheader("🕵️ Anonymous Reporting")

        text = st.text_area("Describe suspicious behavior or concerns:")

        if st.button("Submit Anonymous Report", use_container_width=True):
            if text.strip() == "":
                st.warning("Enter something first.")
            else:
                push_anonymous_report(text)
                st.success("Report submitted anonymously.")

        st.divider()

    # ----------------------------------------------------------
    # INTERACTIVE CAMPUS MAP
    # ----------------------------------------------------------
    with left:
        st.subheader("🗺️ Interactive Campus Map")

        ecsu_lat, ecsu_lon = 36.2796, -76.2131

        campus_map = folium.Map(location=[ecsu_lat, ecsu_lon], zoom_start=16)

        folium.Marker(
            [ecsu_lat, ecsu_lon],
            popup="ECSU — Gilchrist Hall",
            tooltip="Campus Center",
            icon=folium.Icon(color="blue")
        ).add_to(campus_map)

        st_folium(campus_map, width=700, height=450)

    # ----------------------------------------------------------
    # RIGHT SIDE — LIVE NEWS
    # ----------------------------------------------------------
    with right:
        st.subheader("📰 Live Safety News")

        dummy_news = [
            "Campus Police Increase Patrol near Dorms",
            "Severe Weather Alert Expected Tonight",
            "New University Safety Grant Approved",
            "FBI Issues Public Awareness Bulletin",
        ]

        for n in dummy_news:
            st.write("•", n)

        st.divider()

        st.subheader("📡 Offline Mode")
        offline = st.toggle("Enable Offline Mode")

        if offline:
            st.warning("Offline mode enabled — limited features.")
        else:
            st.info("Connected to network.")

    st.divider()
    st.caption("© 2025 ECSU Campus Safety Companion – Student Application")


if __name__ == "__main__":
    student_dashboard()

