import streamlit as st
from PIL import Image
import os

# ------------------------------------------------------
# Page Setup
# ------------------------------------------------------
st.set_page_config(page_title="Campus Safety Companion (CSC)", page_icon="🛡️", layout="wide")

# ------------------------------------------------------
# Title
# ------------------------------------------------------
st.title("🛡️ Campus Safety Companion (CSC)")
st.markdown("Enhancing campus safety through awareness, communication, and rapid response.")

# ------------------------------------------------------
# Navigation Tabs (TOP)
# ------------------------------------------------------
tabs = st.tabs(["Home", "Alert System", "Interactive Map", "Report Activity", "Offline Fallback"])

# ------------------------------------------------------
# HOME TAB
# ------------------------------------------------------
with tabs[0]:
    st.subheader("Mission Statement")
    st.write("""
    The CSC app enhances safety, awareness, and response time during active shooter incidents 
    and other critical emergencies. It acts as a redundant, reliable communication backup 
    to the ECSU RAVE system.
    """)
    st.info("**Primary Users:** Students, Faculty, and Staff of ECSU.")

# ------------------------------------------------------
# ALERT SYSTEM TAB
# ------------------------------------------------------
with tabs[1]:
    st.subheader("Live Emergency Alerts")
    alert_placeholder = st.empty()
    if st.button("Simulate Alert"):
        alert_placeholder.error("🚨 Active threat alert in Jenkins Hall! Evacuate immediately!")
    st.caption("Alerts simulate how critical messages will appear.")

# ------------------------------------------------------
# INTERACTIVE MAP TAB
# ------------------------------------------------------
with tabs[2]:
    st.subheader("Elizabeth City State University Campus Map")

    # Add custom CSS for container appearance
    st.markdown("""
        <style>
            .map-frame {
                display: flex;
                justify-content: center;
                align-items: center;
                background-color: #f8f9fa;
                border-radius: 10px;
                padding: 10px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
                margin-top: 15px;
                margin-bottom: 20px;
            }
        </style>
    """, unsafe_allow_html=True)

    map_path = "ecsu_map.png"  # Ensure same folder as .py file

    if os.path.exists(map_path):
        ecsu_map = Image.open(map_path)
        st.markdown('<div class="map-frame">', unsafe_allow_html=True)
        st.image(ecsu_map, caption="ECSU Campus Map", use_container_width=False, width=940)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("❌ Map file not found. Please verify the file path or name.")

# ------------------------------------------------------
# REPORT ACTIVITY TAB
# ------------------------------------------------------
with tabs[3]:
    st.subheader("Anonymous Reporting")
    report = st.text_area("Describe suspicious activity or blocked exits:")
    if st.button("Submit Report"):
        st.success("Report submitted anonymously. Campus police will review immediately.")
    st.caption("Anonymous reports increase community awareness without fear of retaliation.")

# ------------------------------------------------------
# OFFLINE FALLBACK TAB
# ------------------------------------------------------
with tabs[4]:
    st.subheader("Offline Guidance")
    st.code("""
    - Shelter-in-place instructions
    - Evacuation procedures
    - Contact campus police: (252) 335-3266
    """, language="text")
