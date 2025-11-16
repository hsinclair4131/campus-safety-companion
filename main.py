import streamlit as st
from admin_app.admin_app import admin_dashboard
from student_app.student_app import student_home

st.set_page_config(page_title="Campus Safety Companion", layout="wide")

st.title("Campus Safety Companion (CSC)")

menu = st.sidebar.selectbox(
    "Choose App View",
    ["Student App", "Admin Dashboard"]
)

if menu == "Student App":
    student_home()

elif menu == "Admin Dashboard":
    admin_dashboard()

