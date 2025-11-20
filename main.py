import streamlit as st
from student_dashboard import student_dashboard

st.set_page_config(
    page_title="Campus Safety Companion",
    layout="wide",
    page_icon="🛡️"
)

st.title("🛡️ Campus Safety Companion (CSC)")

st.markdown("Choose which interface you want to open:")

mode = st.selectbox(
    "Select App Mode:",
    ["Student App"]    # REMOVE admin option for now
)

# Always load student app
student_dashboard()

# NOTE:
# Admin dashboard is temporarily disabled
# until supabase admin system is fully built.
