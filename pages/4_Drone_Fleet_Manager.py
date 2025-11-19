import streamlit as st
from firebase_admin import firestore
import pydeck as pdk
import time

db = firestore.client()

def render():

    # -------------------------------------------------
    # ACCESS CONTROL
    # -------------------------------------------------
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.error("Unauthorized. Please log in from the main page.")
        st.stop()

    # -------------------------------------------------
    # PAGE HEADER
    # -------------------------------------------------
    st.title("🚁 Tactical Drone Fleet Manager")
    st.caption("Real-time statuses, missions, commands, and live positioning.")

    # -------------------------------------------------
    # GLOBAL MAP MODE (from main.py)
    # -------------------------------------------------
    map_mode = st.session_state.get("map_mode", "Night")

    MAP_STYLE = (
        "mapbox://styles/mapbox/light-v9"
        if map_mode == "Day"
        else "mapbox://styles/mapbox/dark-v10"
    )

    # -------------------------------------------------
    # CUSTOM TACTICAL UI
    # -------------------------------------------------
    TACTICAL_UI = """
    <style>
    body { background-color: #0d1117; color: #e6edf3; }
    [data-testid="stSidebar"] {
        background-color: #161b22 !important;
        border-right: 1px solid #1f6feb;
    }
    h2, h3, h4, label, p { color: #e6edf3 !important; }
    .metric-box {
        background-color: #161b22;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #1f6feb;
        margin-bottom: 12px;
    }
    .batt-good { color: #00d084; font-weight: bold; }
    .batt-warn { color: #f1c40f; font-weight: bold; }
    .batt-bad { color: #ff4747; font-weight: bold; }
    .status-online { color: #00d084; font-weight: bold; }
    .status-offline { color: #ff4747; font-weight: bold; }
    </style>
    """
    st.markdown(TACTICAL_UI, unsafe_allow_html=True)

    # -------------------------------------------------
    # HELPERS
    # -------------------------------------------------
    def get_batt_class(batt):
        if batt >= 60:
            return "batt-good"
        elif batt >= 30:
            return "batt-warn"
        else:
            return "batt-bad"

    # -------------------------------------------------
    # FETCH DRONES
    # -------------------------------------------------
    def fetch_drones():
        docs = db.collection("drones").stream()
        output = []

        for d in docs:
            item = d.to_dict()
            output.append({
                "id": d.id,
                "name": item.get("name", "Drone"),
                "lat": float(item.get("lat", 0)),
                "lon": float(item.get("lon", 0)),
                "battery": int(item.get("battery", 0)),
                "status": item.get("status", "offline"),
                "mission": item.get("mission", "None")
            })

        return output

    drones = fetch_drones()

    # -------------------------------------------------
    # LAYOUT: LEFT (Info cards) | RIGHT (Map + Controls)
    # -------------------------------------------------
    left, right = st.columns([1.4, 1])

    # -------------------------------------------------
    # LEFT SIDE
    # -------------------------------------------------
    with left:
        st.markdown("### 📋 Drone Fleet Overview")

        if len(drones) == 0:
            st.warning("No drones registered.")
        else:
            for d in drones:
                batt_class = get_batt_class(d["battery"])
                status_class = "status-online" if d["status"] == "online" else "status-offline"

                st.markdown(
                    f"""
                    <div class="metric-box">
                        <b>{d['name']}</b><br>
                        <span class="{status_class}">Status: {d['status'].upper()}</span><br>
                        Mission: {d['mission']}<br>
                        Battery: <span class="{batt_class}">{d['battery']}%</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    # -------------------------------------------------
    # RIGHT SIDE
    # -------------------------------------------------
    with right:
        st.markdown("### 🗺️ Live Drone Location")

        drone_names = [d["name"] for d in drones]

        if len(drone_names) == 0:
            st.info("No drones available.")
            return

        selected = st.selectbox("Select Drone", drone_names)

        chosen = next((x for x in drones if x["name"] == selected), None)

        if chosen:
            # MAP MARKER
            point_layer = pdk.Layer(
                "ScatterplotLayer",
                data=[chosen],
                get_position="[lon, lat]",
                get_color=[30, 144, 255],
                get_radius=130,
                pickable=True
            )

            # MAP VIEW
            view_state = pdk.ViewState(
                latitude=chosen["lat"],
                longitude=chosen["lon"],
                zoom=16,
                pitch=50,
            )

            st.pydeck_chart(
                pdk.Deck(
                    map_style=MAP_STYLE,
                    initial_view_state=view_state,
                    layers=[point_layer],
                    tooltip={
                        "text": f"{chosen['name']}\nBattery: {chosen['battery']}%\nStatus: {chosen['status']}\nMission: {chosen['mission']}"
                    }
                )
            )

            st.write("---")

            # -------------------------------------------------
            # DRONE COMMANDS
            # -------------------------------------------------
            st.markdown("### 🎯 Drone Commands")

            mission = st.selectbox(
                "Assign Mission",
                [
                    "Surveillance",
                    "Perimeter Scan",
                    "Thermal Sweep",
                    "SOS Response",
                    "Escort",
                    "Recon"
                ]
            )

            if st.button("🚀 Deploy Drone"):
                if chosen["battery"] < 20:
                    st.error("❌ Battery too low for launch.")
                else:
                    db.collection("drones").document(chosen["id"]).update({
                        "status": "online",
                        "mission": mission
                    })
                    st.success(f"🛸 {chosen['name']} deployed for '{mission}'.")

            if st.button("🛬 Recall Drone"):
                db.collection("drones").document(chosen["id"]).update({
                    "status": "offline",
                    "mission": "None"
                })
                st.warning(f"📡 {chosen['name']} recalled to base.")

            if st.button("🔋 Charge Drone to 100%"):
                db.collection("drones").document(chosen["id"]).update({
                    "battery": 100
                })
                st.success(f"🔋 {chosen['name']} battery restored to 100%.")

    # -------------------------------------------------
    # AUTO REFRESH
    # -------------------------------------------------
    st.write("---")
    refresh = st.checkbox("Auto-Refresh (5 sec)", True)

    if refresh:
        time.sleep(5)
        st.rerun()
