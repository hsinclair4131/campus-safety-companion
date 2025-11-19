import streamlit as st
import datetime
import random
import folium
from streamlit_folium import st_folium

# Supabase backend
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
# AUTO REFRESH EVERY 5 SECONDS (SAFE METHOD)
# --------------------------------------------------------------
st.markdown(
    "<meta http-equiv='refresh' content='5'>",
    unsafe_allow_html=True
)

# --------------------------------------------------------------
# MAIN STUDENT DASHBOARD
# --------------------------------------------------------------
def student_dashboard():

    st.title("🛡️ Campus Safety Companion – Student App")
    st.markdown("Your personal safety assistant for ECSU.")

    left, right = st.columns([2, 1])

    # ----------------------------------------------------------
    # LIVE ADMIN ALERTS (REAL-TIME)
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
    # SOS EMERGENCY BUTTON → SEND LIVE DATA
    # ----------------------------------------------------------
    with left:
        st.subheader("📍 GPS Emergency SOS")

        st.markdown("""
            If you are in danger, press the button below to send your
            **live location** to campus police immediately.
        """)

        sos_clicked = st.button(
            "🚨 SEND SOS – SHARE LIVE LOCATION",
            type="primary",
            use_container_width=True
        )

        if sos_clicked:
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

        report_text = st.text_area(
            "Describe suspicious behavior, blocked exits, or concerns:",
            placeholder="Your report is anonymous."
        )

        if st.button("Submit Anonymous Report", use_container_width=True):
            if report_text.strip() == "":
                st.warning("Please enter a report first.")
            else:
                push_anonymous_report(report_text)
                st.success("Anonymous report sent to Campus Police.")

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
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(campus_map)

        st_folium(campus_map, width=700, height=450)

    # ----------------------------------------------------------
    # RIGHT COLUMN — LIVE NEWS + OFFLINE MODE
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
