# firebase_backend.py
# 🔥 Unified Firestore backend for Admin + Student Apps

from firebase_config import get_db
from firebase_admin import firestore


# -------------------------------------------------------------
# ADMIN → STUDENT : SEND EMERGENCY ALERT
# -------------------------------------------------------------
def send_alert(message: str):
    db = get_db()
    db.collection("alerts").document("current").set({
        "message": message,
        "timestamp": firestore.SERVER_TIMESTAMP
    })
    return True


# -------------------------------------------------------------
# STUDENT → ADMIN : SEND SOS COORDINATES
# -------------------------------------------------------------
def send_sos(uid: str, lat: float, lon: float):
    db = get_db()
    db.collection("sos_alerts").document(uid).set({
        "lat": lat,
        "lon": lon,
        "timestamp": firestore.SERVER_TIMESTAMP
    })
    return True


# -------------------------------------------------------------
# ADMIN SIDE : GET ALL SOS ALERTS
# -------------------------------------------------------------
def get_all_sos():
    db = get_db()
    docs = db.collection("sos_alerts").stream()
    return [
        {
            "uid": d.id,
            **d.to_dict()
        }
        for d in docs
    ]


# -------------------------------------------------------------
# STUDENT → ADMIN : SEND ANONYMOUS REPORT
# -------------------------------------------------------------
def send_report(text: str):
    db = get_db()
    db.collection("reports").add({
        "text": text,
        "timestamp": firestore.SERVER_TIMESTAMP
    })
    return True


# -------------------------------------------------------------
# ADMIN SIDE : LIST ALL REPORTS
# -------------------------------------------------------------
def get_reports():
    db = get_db()
    docs = db.collection("reports").order_by("timestamp").stream()
    return [d.to_dict() for d in docs]


# -------------------------------------------------------------
# STUDENT SIDE : READ LIVE ALERT STATUS
# -------------------------------------------------------------
def get_current_alert():
    db = get_db()
    doc = db.collection("alerts").document("current").get()

    if doc.exists:
        return doc.to_dict()

    return {"message": "All Clear", "timestamp": None}
