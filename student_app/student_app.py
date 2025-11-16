import streamlit as st
import datetime
import random

# ------------------------------
# CONFIG (stays OUTSIDE function)
# ------------------------------
st.set_page_config(
    page_title="CSC – Student App",
    layout="wide",
    page_icon="🛡️"
)

def student_dashboard():
    # ------------------------------
    # HEADER
    # ------------------------------
    st.title("🛡️ Campus Safety Companion – Student App")
    st.markdown("Your personal safety assistant for ECSU.")

    # ------------------------------
    # LAYOUT COLUMNS
    # ------------------------------
    left, right = st.columns([2, 1])

    # ------------------------------
    # COLOR ALERT SYSTEM
    # ------------------------------
    with left:
        st.subheader("🚨 Campus Alert Status")

        alert_levels = {
            "Green – All Clear": "🟢 Situation normal.",
            "Yellow – Caution": "🟡 Be alert. Potential risk nearby.",
            "Orange – Dangerous": "🟠 Active threat reported.",
            "Red – Emergency": "🔴 RUN | HIDE | FIGHT – ACTIVE THREAT"
        }

        current_alert = random.choice(list(alert_levels.keys()))

        st.markdown(f"### **{current_alert}**")
        st.info(alert_levels[current_alert])

        st.divider()

    # ------------------------------
    # SOS EMERGENCY SECTION
    # ------------------------------
    with left:
        st.subheader("📍 GPS Emergency SOS")

        st.markdown(
            """
            Press the button below to send your location to campus police
            immediately during an emergency.
            """
        )

        sos_trigger = st.button(
            "🚨 SEND SOS – SHARE LIVE LOCATION",
            type="primary",
            use_container_width=True
        )

        if sos_trigger:
            fake_lat = round(random.uniform(36.2, 36.4), 6)
            fake_lon = round(random.uniform(-76.3, -76.1), 6)

            st.error("🚨 SOS SENT TO CAMPUS POLICE!")
            st.write("**Your coordinates:**")
            st.code(f"Latitude: {fake_lat}\nLongitude: {fake_lon}")
            st.write("⏱️ Timestamp:", datetime.datetime.now())

        st.divider()

    # ------------------------------
    # ANONYMOUS REPORTING
    # ------------------------------
    with left:
        st.subheader("🕵️ Anonymous Reporting")

        report_text = st.text_area(
            "Submit a concern or suspicious activity (completely anonymous):",
            placeholder="Describe what you saw…"
        )

        if st.button("Submit Anonymous Report", use_container_width=True):
            if report_text.strip() == "":
                st.warning("Please enter a report before submitting.")
            else:
                st.success("Your anonymous report has been sent to campus dispatch.")

        st.divider()

        # ------------------------------
    # CAMPUS MAP (LIVE INTERACTIVE)
    # ------------------------------
    with left:
        st.subheader("🗺️ Interactive Campus Map")

        # Import mapping tools
        import folium
        from streamlit_folium import st_folium

        # Center of ECSU Campus
        ecsu_lat = 36.2796
        ecsu_lon = -76.2131

        # Create folium map
        campus_map = folium.Map(location=[ecsu_lat, ecsu_lon], zoom_start=16)

        # Add a marker (Gilchrist Hall)
        folium.Marker(
            [ecsu_lat, ecsu_lon],
            popup="ECSU — Gilchrist Hall",
            tooltip="Campus Center",
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(campus_map)

        # Render the interactive map
        st_folium(campus_map, width=700, height=450)


    # ------------------------------
    # RIGHT COLUMN – NEWS + OFFLINE MODE
    # ------------------------------
    with right:
        st.subheader("📰 Live Safety News Feed")

        st.markdown(
            """
            Latest headlines from AP News & Google News  
            *(Live API integration coming soon)*
            """
        )

        dummy_news = [
            "Campus Police Increases Patrol Around Dorms",
            "Severe Weather Alert: Thunderstorms Expected Tonight",
            "State Officials Announce New Campus Security Grants",
            "FBI Releases Public Safety Awareness Report"
        ]

        for n in dummy_news:
            st.write("•", n)

        st.divider()

        # Offline toggle
        st.subheader("📡 Offline Mode")

        offline = st.toggle("Enable offline mode")

        if offline:
            st.warning("Offline mode enabled – some features may be unavailable.")
        else:
            st.info("You are connected.")

if __name__ == "__main__":
    student_dashboard()
    
   

    # ------------------------------
    # FOOTER
    # ------------------------------
    st.divider()
    st.caption("© 2025 ECSU Campus Safety Companion – Student Application")
