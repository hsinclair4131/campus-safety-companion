import streamlit as st
from admin_app.admin_app import admin_dashboard
from student_app.student_app import student_dashboard

# ------------------------------
# APP SELECTOR
# ------------------------------

st.set_page_config(
    page_title="Campus Safety Companion",
    layout="wide",
    page_icon="🛡️"
)

st.title("🛡️ Campus Safety Companion (CSC)")

st.markdown("Choose which interface you want to open:")

mode = st.selectbox(
    "Select App Mode:",
    ["Student App", "Admin Dashboard"]
)

if mode == "Student App":
    student_dashboard()

elif mode == "Admin Dashboard":
    admin_dashboard()
