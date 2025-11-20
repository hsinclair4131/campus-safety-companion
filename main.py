import streamlit as st
from student_dashboard import student_dashboard

# REMOVE admin imports until Supabase credentials are added
# from admin_dashboard_app import admin_dashboard

st.set_page_config(
    page_title="Campus Safety Companion",
    layout="wide",
    page_icon="🛡️"
)

st.title("🛡️ Campus Safety Companion (CSC)")

mode = st.selectbox("Select App Mode:", ["Student App"])

if mode == "Student App":
    student_dashboard()

# REMOVE ADMIN ENTRY
# elif mode == "Admin Dashboard":
#     admin_dashboard()
