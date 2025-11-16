import streamlit as st

st.set_page_config(page_title="CSC Launcher", page_icon="🚨", layout="centered")

st.title("CSC MULTI-APP LAUNCHER")
st.write("Choose which interface to launch:")

st.markdown("### **Student App**")
st.page_link("student_app/student_app.py", label="📱 Open Student App")

st.markdown("### **Admin Dashboard**")
st.page_link("admin_app/admin_app.py", label="🚓 Open Admin Dashboard")
