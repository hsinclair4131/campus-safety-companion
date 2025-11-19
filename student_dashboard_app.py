import streamlit as st
import datetime
import random
import folium
from streamlit_folium import st_folium

# --------------------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------------------
st.set_page_config(
    page_title="CSC – Student App",
    page_icon="🛡️",
    layout="wide"
)

# --------------------------------------------------------------
# MAIN STUDENT DASHBOARD
# --------------------------------------------------------------
def student_dashboard():

    # ----------------------------------------------------------
    # HEADER
    # ----------------------------------------------------------
    st.title("🛡️ Campus Safety Companion – Student App")
    st.markdown("Your personal safety assistant for ECSU.")

    left, right = st.columns([2, 1])

    # ----------------------------------------------------------
    # CAMPUS ALERT COLOR SYSTEM
    # ----------------------------------------------------------
    with left:
        st.subheader("🚨 Campus Alert Status")

        alert_levels = {
            "Green – All Clear": "🟢 Normal operations.",
            "Yellow – Caution": "🟡 Stay alert. Something may be happening.",
            "Orange – Dangerous": "🟠 Known threat or escalation.",
            "Red – Emergency": "🔴 RUN | HIDE | FIGHT – Active threat."
        }

        current_alert = random.choice(list(alert_levels.keys()))

        st.markdown(f"### **{current_alert}**")
        st.info(alert_levels[current_alert])
        st.divider()

    # ----------------------------------------------------------
    # SOS EMERGENCY LOCATION BUTTON
    # ----------------------------------------------------------
    with left:
        st.subheader("📍 GPS Emergency SOS")

        st.markdown(
            """
            If you are in danger, press the button below to send your live
            location to campus police immediately.
            """
        )

        sos_clicked = st.button(
            "🚨 SEND SOS – SHARE LIVE LOCATION",
            type="primary",
            use_container_width=True
        )

        if sos_clicked:
            fake_lat = round(random.uniform(36.2, 36.4), 6)
            fake_lon = round(random.uniform(-76.3, -76.1), 6)

            st.error("🚨 SOS SENT TO CAMPUS POLICE!")
            st.write("**Your coordinates:**")
            st.code(f"Latitude: {fake_lat}\nLongitude: {fake_lon}")
            st.write("⏱ Timestamp:", datetime.datetime.now())

        st.divider()

    # ----------------------------------------------------------
    # ANONYMOUS REPORTING
    # ----------------------------------------------------------
    with left:
        st.subheader("🕵️ Anonymous Reporting")

        report_text = st.text_area(
            "Describe suspicious behavior, blocked exits, or any security concerns:",
            placeholder="Your report is anonymous."
        )

        if st.button("Submit Anonymous Report", use_container_width=True):
            if report_text.strip() == "":
                st.warning("Please enter a report before submitting.")
            else:
                st.success("Anonymous report sent to Campus Police.")

        st.divider()

    # ----------------------------------------------------------
    # INTERACTIVE CAMPUS MAP
    # ----------------------------------------------------------
    with left:
        st.subheader("🗺️ Interactive Campus Map")

        ecsu_lat = 36.2796
        ecsu_lon = -76.2131

        campus_map = folium.Map(location=[ecsu_lat, ecsu_lon], zoom_start=16)

        folium.Marker(
            [ecsu_lat, ecsu_lon],
            popup="ECSU — Gilchrist Hall",
            tooltip="Campus Center",
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(campus_map)

        st_folium(campus_map, width=700, height=450)

    # ----------------------------------------------------------
    # RIGHT COLUMN — NEWS + OFFLINE MODE
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

    # FOOTER
    st.divider()
    st.caption("© 2025 ECSU Campus Safety Companion – Student Application")


if __name__ == "__main__":
    student_dashboard()
