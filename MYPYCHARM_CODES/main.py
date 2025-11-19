import streamlit as st
from admin_auth import firebase_login
from firebase_config import get_firebase_app, get_db

# ---------------------------------------
# INITIALIZE FIREBASE
# ---------------------------------------
get_firebase_app()   # Initialize Firebase app
db = get_db()        # Initialize Firestore client

# ---------------------------------------
# PAGE CONFIG
# ---------------------------------------
st.set_page_config(
    page_title="ECSU Campus Safety - Admin",
    layout="wide",
    page_icon="🛡️"
)

# ---------------------------------------
# SESSION STATE
# ---------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "admin_uid" not in st.session_state:
    st.session_state.admin_uid = None

if "map_mode" not in st.session_state:
    st.session_state["map_mode"] = "Night"   # Default tactical mode

# ---------------------------------------
# LOGIN SCREEN
# ---------------------------------------
if not st.session_state.logged_in:

    st.title("🔐 Admin Login Portal")
    st.caption("Restricted: ECSU Campus Safety Officials Only")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        uid = firebase_login(email, password)

        if uid:
            st.session_state.logged_in = True
            st.session_state.admin_uid = uid
            st.success("Login successful! Loading dashboard...")
            st.rerun()
        else:
            st.error("Invalid login or admin not authorized.")

    st.stop()

# ---------------------------------------
# GLOBAL DAY/NIGHT MODE
# ---------------------------------------
st.sidebar.markdown("### 🌓 Map Mode")
mode = st.sidebar.radio(
    "Toggle display mode:",
    ["Day", "Night"],
    horizontal=True
)
st.session_state["map_mode"] = mode

# ---------------------------------------
# HEADER
# ---------------------------------------
st.title("🛡️ ECSU Campus Safety - Admin System")
st.success("Welcome, administrator!")

# ---------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------
page = st.sidebar.selectbox(
    "**Navigation**",
    [
        "Dashboard",
        "GPS Live Map",
        "Dispatcher Center",
        "Drone Fleet Manager"
    ]
)

# ---------------------------------------
# ROUTING FUNCTION
# ---------------------------------------
def load_page(module_path):
    module = __import__(module_path, fromlist=["render"])
    module.render()   # each page must define render()

# ---------------------------------------
# ROUTING – LOAD REQUESTED MODULE
# ---------------------------------------
def load_page(module_path):
    module = __import__(module_path, fromlist=["render"])
    module.render()

if page == "Dashboard":
    load_page("pages.1_Admin_Dashboard")

elif page == "GPS Live Map":
    load_page("pages.2_GPS_Live_Map")

elif page == "Dispatcher Center":
    load_page("pages.3_Dispatcher_Center")

elif page == "Drone Fleet Manager":
    load_page("pages.4_Drone_Fleet_Manager")
