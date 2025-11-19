import os
import json
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# -------------------------------------------------------------
#  FIREBASE INITIALIZATION (STREAMLIT SECRETS OR LOCAL JSON)
# -------------------------------------------------------------

def get_firebase_app():
    """
    Initialize Firebase either from:
      1. Streamlit Cloud Secrets (RECOMMENDED)
      2. Local serviceAccountKey.json (PyCharm/local dev)
    """

    # Avoid re-initializing Firebase
    if firebase_admin._apps:
        return firebase_admin.get_app()

    # ---------------------------------------------------------
    # 1 — STREAMLIT SECRETS (CLOUD DEPLOYMENT)
    # ---------------------------------------------------------
    if "firebase" in st.secrets:
        try:
            # Streamlit stores secrets as a dictionary already
            firebase_credentials_dict = st.secrets["firebase"]

            cred = credentials.Certificate(firebase_credentials_dict)
            app = firebase_admin.initialize_app(cred)
            return app

        except Exception as e:
            st.error(f"🔥 Firebase (Streamlit secrets) init error: {e}")
            print("🔥 Firebase Streamlit secrets error:", e)

    # ---------------------------------------------------------
    # 2 — LOCAL JSON FILE (DEVELOPMENT)
    # ---------------------------------------------------------
    if os.path.exists("serviceAccountKey.json"):
        try:
            cred = credentials.Certificate("serviceAccountKey.json")
            app = firebase_admin.initialize_app(cred)
            return app

        except Exception as e:
            st.error(f"🔥 Firebase (local JSON) init error: {e}")
            print("🔥 Firebase local JSON error:", e)

    # ---------------------------------------------------------
    # 3 — NO CREDENTIALS FOUND
    # ---------------------------------------------------------
    raise FileNotFoundError("❌ Firebase credentials missing in secrets or local JSON!")


def get_db():
    """Returns Firestore client instance."""
    app = get_firebase_app()
    return firestore.client(app)


# -------------------------------------------------------------
#  ALERT SYSTEM
# -------------------------------------------------------------

def push_alert(message: str):
    """Admin pushes global emergency alert."""
    db = get_db()
    doc_ref = db.collection("alerts").document("latest")
    doc_ref.set({
        "message": message,
        "active": True
    })
    return True


def get_latest_alert():
    """Students fetch last broadcasted emergency alert."""
    db = get_db()
    doc = db.collection("alerts").document("latest").get()
    if doc.exists:
        return doc.to_dict()
    return None


# -------------------------------------------------------------
#  SOS SYSTEM
# -------------------------------------------------------------

def push_sos(latitude: float, longitude: float):
    """Students send SOS GEO location."""
    db = get_db()
    doc_ref = db.collection("sos_reports").document()
    doc_ref.set({
        "lat": latitude,
        "lon": longitude,
        "timestamp": firestore.SERVER_TIMESTAMP
    })
    return True


def get_all_sos():
    """Admins view ALL SOS reports (newest first)."""
    db = get_db()
    docs = db.collection("sos_reports") \
             .order_by("timestamp", direction=firestore.Query.DESCENDING) \
             .stream()

    return [d.to_dict() for d in docs]


# -------------------------------------------------------------
#  ANONYMOUS REPORT SYSTEM
# -------------------------------------------------------------

def push_anonymous_report(text: str):
    """Students submit anonymous reports."""
    db = get_db()
    db.collection("anonymous_reports").document().set({
        "report": text,
        "timestamp": firestore.SERVER_TIMESTAMP
    })
    return True


def get_anonymous_reports():
    """Admins retrieve anonymous reports."""
    db = get_db()
    docs = db.collection("anonymous_reports") \
             .order_by("timestamp", direction=firestore.Query.DESCENDING) \
             .stream()

    return [d.to_dict() for d in docs]
