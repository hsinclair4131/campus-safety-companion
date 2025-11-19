import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# -------------------------------------------------------------
#  FIREBASE INITIALIZATION (STREAMLIT SECRETS OR LOCAL JSON)
# -------------------------------------------------------------

def get_firebase_app():
    """Initializes Firebase from Streamlit Secrets (cloud) or local JSON (PyCharm)."""

    # Already initialized?
    if firebase_admin._apps:
        return firebase_admin.get_app()

    # 1 — Streamlit Cloud Secrets
    if "serviceAccountKey" in os.environ:
        try:
            key_data = json.loads(os.environ["serviceAccountKey"])
            cred = credentials.Certificate(key_data)
            return firebase_admin.initialize_app(cred)
        except Exception as e:
            print("Streamlit Secrets Firebase Error:", e)

    # 2 — Local Development (PyCharm)
    if os.path.exists("serviceAccountKey.json"):
        cred = credentials.Certificate("serviceAccountKey.json")
        return firebase_admin.initialize_app(cred)

    raise FileNotFoundError("❌ No Firebase service account found!")

def get_db():
    """Returns Firestore client."""
    app = get_firebase_app()
    return firestore.client(app)

# -------------------------------------------------------------
# ALERT SYSTEM
# -------------------------------------------------------------
def push_alert(message: str):
    """Push emergency alert to Firestore."""
    db = get_db()
    doc = db.collection("alerts").document("latest")
    doc.set({
        "message": message,
        "active": True
    })
    return True

def get_latest_alert():
    """Reads latest emergency alert."""
    db = get_db()
    doc = db.collection("alerts").document("latest").get()
    if doc.exists:
        return doc.to_dict()
    return None

# -------------------------------------------------------------
# SOS SYSTEM
# -------------------------------------------------------------
def push_sos(latitude: float, longitude: float):
    """Students send SOS location."""
    db = get_db()
    doc = db.collection("sos_reports").document()
    doc.set({
        "lat": latitude,
        "lon": longitude,
        "timestamp": firestore.SERVER_TIMESTAMP
    })
    return True

def get_all_sos():
    """Admins read SOS reports."""
    db = get_db()
    docs = db.collection("sos_reports").order_by("timestamp", direction=firestore.Query.DESCENDING).stream()
    return [d.to_dict() for d in docs]

# -------------------------------------------------------------
# ANONYMOUS REPORTS
# -------------------------------------------------------------
def push_anonymous_report(text: str):
    db = get_db()
    doc = db.collection("anonymous_reports").document()
    doc.set({
        "report": text,
        "timestamp": firestore.SERVER_TIMESTAMP
    })
    return True

def get_anonymous_reports():
    db = get_db()
    docs = db.collection("anonymous_reports").order_by("timestamp", direction=firestore.Query.DESCENDING).stream()
    return [d.to_dict() for d in docs]
