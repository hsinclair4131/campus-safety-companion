import streamlit as st
import pydeck as pdk
import pandas as pd
import time
from firebase_admin import firestore

db = firestore.client()

def render():

    # -------------------------------------------------
    # ACCESS CONTROL
    # -------------------------------------------------
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.error("Unauthorized. Please log in from the main page.")
        st.stop()

    st.title("🎯 Tactical GPS Command Center")
    st.caption("Real-time tracking interface for drones, students, and emergency operations.")

    # -------------------------------------------------
    # MAP MODE (GLOBAL)
    # -------------------------------------------------
    map_mode = st.session_state.get("map_mode", "Night")

    MAP_STYLE = (
        "mapbox://styles/mapbox/light-v9"
        if map_mode == "Day"
        else "mapbox://styles/mapbox/dark-v10"
    )

    # -------------------------------------------------
    # SIDEBAR TACTICAL CONTROL PANEL
    # -------------------------------------------------
    st.sidebar.title("🛠 Tactical Control Panel")

    mode = st.sidebar.radio("🌓 Map Display Mode", ["Day", "Night"])
    st.session_state["map_mode"] = mode

    # Toggle layers
    show_drones = st.sidebar.checkbox("🚁 Drone Layer", True)
    show_students = st.sidebar.checkbox("🧍 Student Layer", True)
    show_sos = st.sidebar.checkbox("🚨 SOS Alerts", True)
    show_heatmap = st.sidebar.checkbox("🔥 Heatmap Layer", False)
    show_zones = st.sidebar.checkbox("📡 Restricted Zones", False)

    # Thermal filter (visual only)
    thermal_mode = st.sidebar.checkbox("🌡 Thermal Mode (visual filter)", False)

    refresh_rate = st.sidebar.slider("🔁 Auto-Refresh (sec)", 1, 10, 3)

    # -------------------------------------------------
    # AUTO REFRESH
    # -------------------------------------------------
    time.sleep(refresh_rate)

    # -------------------------------------------------
    # FIRESTORE DATA FETCHES
    # -------------------------------------------------

    def fetch_drones():
        docs = db.collection("drones").stream()
        output = []
        for d in docs:
            x = d.to_dict()
            output.append({
                "lat": float(x.get("lat", 0)),
                "lon": float(x.get("lon", 0)),
                "name": x.get("name", "Drone"),
                "battery": x.get("battery", 0),
                "mission": x.get("mission", "None"),
                "color": [0, 150, 255]  # tactical blue
            })
        return pd.DataFrame(output)

    def fetch_students():
        docs = db.collection("students").stream()
        output = []
        for s in docs:
            x = s.to_dict()
            output.append({
                "lat": float(x.get("lat", 0)),
                "lon": float(x.get("lon", 0)),
                "name": x.get("name", "Student"),
                "status": x.get("status", "active"),
                "color": [0, 255, 0]  # green
            })
        return pd.DataFrame(output)

    def fetch_sos():
        docs = db.collection("sos_alerts").stream()
        output = []
        for s in docs:
            x = s.to_dict()
            output.append({
                "lat": float(x.get("lat", 0)),
                "lon": float(x.get("lon", 0)),
                "name": f"SOS ({x.get('severity','')})",
                "color": [255, 50, 50]  # red
            })
        return pd.DataFrame(output)

    drones_df = fetch_drones()
    students_df = fetch_students()
    sos_df = fetch_sos()

    # -------------------------------------------------
    # BUILD MAP LAYERS
    # -------------------------------------------------
    layers = []

    # DRONES
    if show_drones and not drones_df.empty:
        layers.append(
            pdk.Layer(
                "ScatterplotLayer",
                data=drones_df,
                get_position=["lon", "lat"],
                get_color="color",
                get_radius=110,
                pickable=True,
            )
        )

    # STUDENTS
    if show_students and not students_df.empty:
        layers.append(
            pdk.Layer(
                "ScatterplotLayer",
                data=students_df,
                get_position=["lon", "lat"],
                get_color="color",
                get_radius=80,
                pickable=True,
            )
        )

    # SOS ALERTS
    if show_sos and not sos_df.empty:
        layers.append(
            pdk.Layer(
                "ScatterplotLayer",
                data=sos_df,
                get_position=["lon", "lat"],
                get_color="color",
                get_radius=160,
                pickable=True,
            )
        )

    # HEATMAP
    if show_heatmap:
        combined = pd.concat([drones_df, students_df, sos_df], ignore_index=True)
        if not combined.empty:
            layers.append(
                pdk.Layer(
                    "HeatmapLayer",
                    data=combined,
                    get_position=["lon", "lat"],
                    get_weight=1,
                )
            )

    # POLYGON ZONES
    if show_zones:
        polygon_data = [{
            "coordinates": [[[-76.2533, 36.2850], [-76.2530, 36.2854], [-76.2526, 36.2851]]],
            "fill_color": [200, 0, 200, 80]
        }]
        layers.append(
            pdk.Layer(
                "PolygonLayer",
                data=polygon_data,
                get_polygon="coordinates",
                get_fill_color="fill_color",
                pickable=True
            )
        )

    # -------------------------------------------------
    # VIEW STATE CENTERING
    # -------------------------------------------------
    all_points = pd.concat([drones_df, students_df, sos_df], ignore_index=True)

    if not all_points.empty:
        center_lat = all_points["lat"].mean()
        center_lon = all_points["lon"].mean()
    else:
        center_lat = 36.2855
        center_lon = -76.2529

    view_state = pdk.ViewState(
        latitude=center_lat,
        longitude=center_lon,
        zoom=16,
        pitch=50,
    )

    # -------------------------------------------------
    # RENDER MAP
    # -------------------------------------------------
    deck = pdk.Deck(
        map_style=MAP_STYLE,
        initial_view_state=view_state,
        layers=layers,
        tooltip={"text": "{name}"}
    )

    # Thermal override (visual only)
    if thermal_mode:
        deck = deck.update(
            parameters={"effects": [{"type": "brightness", "brightness": 2}]}
        )

    st.pydeck_chart(deck)

    # -------------------------------------------------
    # EVENT FEED PANEL
    # -------------------------------------------------
    st.subheader("📝 Event Feed (Coming Soon)")
    st.info("Live dispatch events, drone launches, and SOS alerts will appear here.")
