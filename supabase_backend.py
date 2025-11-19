import os
from supabase import create_client, Client
from datetime import datetime

# ---------------------------------------------------------------------
# SUPABASE INITIALIZATION
# ---------------------------------------------------------------------

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    raise Exception("❌ Supabase credentials missing in Streamlit Secrets!")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# ---------------------------------------------------------------------
# SEND ADMIN ALERT
# ---------------------------------------------------------------------
def push_admin_alert(message: str):
    """
    Inserts a new alert into the alerts table.
    Used by Admin Dashboard.
    """
    response = supabase.table("alerts").insert({
        "message": message,
        "timestamp": datetime.utcnow().isoformat()
    }).execute()

    return response


# ---------------------------------------------------------------------
# GET LATEST ADMIN ALERT
# ---------------------------------------------------------------------
def get_latest_alert():
    """
    Fetches the most recent alert from the alerts table.
    Used by Student Dashboard.
    """
    response = supabase.table("alerts") \
        .select("*") \
        .order("timestamp", desc=True) \
        .limit(1) \
        .execute()

    if response.data:
        return response.data[0]
    return None


# ---------------------------------------------------------------------
# SEND SOS (STUDENT)
# ---------------------------------------------------------------------
def push_sos(lat: float, lon: float):
    """
    Sends a GPS emergency SOS message.
    Inserts into sos_reports table.
    """
    response = supabase.table("sos_reports").insert({
        "lat": lat,
        "lon": lon,
        "timestamp": datetime.utcnow().isoformat()
    }).execute()

    return response


# ---------------------------------------------------------------------
# SEND ANONYMOUS REPORT
# ---------------------------------------------------------------------
def push_anonymous_report(report: str):
    """
    Inserts an anonymous report into anonymous_reports table.
    """
    response = supabase.table("anonymous_reports").insert({
        "report": report,
        "timestamp": datetime.utcnow().isoformat()
    }).execute()

    return response

