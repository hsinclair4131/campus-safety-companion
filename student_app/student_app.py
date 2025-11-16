import streamlit as st
from PIL import Image
import os

st.set_page_config(page_title="Campus Safety Companion", page_icon="🛡️", layout="wide")

st.title("🛡️ Campus Safety Companion (CSC)")
st.markdown("Mobile Student Interface")

tabs = st.tabs(["Home", "Alerts", "Map", "Report", "Offline"])

with tabs[0]:
    st.subheader("Welcome to the CSC Student App")
    st.write("This is the mobile-facing Streamlit version of the safety app.")

with tabs[1]:
    st.subheader("Emergency Alerts")
    if st.button("Simulate Alert"):
        st.error("🚨 Active threat detected! Seek safety immediately.")

with tabs[2]:
    st.subheader("Campus Map")
    map_path = "ecsu_map.png"
    if os.path.exists(map_path):
        st.image(map_path, caption="ECSU Campus Map", width=900)
    else:
        st.warning("Map not uploaded yet.")

with tabs[3]:
    st.subheader("Report Suspicious Activity (Anonymous)")
    msg = st.text_area("Describe what you saw")
    if st.button("Submit Report"):
        st.success("Report received.")

with tabs[4]:
    st.subheader("Offline Emergency Instructions")
    st.write("""
    - Lock doors  
    - Turn off lights  
    - Silence phones  
    - Call ECSU Police: (252) 335-3266  
    """)

