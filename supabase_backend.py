import os
from supabase import create_client, Client
from datetime import datetime

# ---------------------------------------------------------
# SUPABASE INITIALIZATION (PUBLIC CLIENT)
# ---------------------------------------------------------

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    raise Exception("❌ Supabase credentials missing in Streamlit Secrets!")

# Public client (correct for Streamlit Apps)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# ---------------------------------------------------------
# SEND ADMIN ALERT
# ---------------------------------------------------------
def push_admin_alert(message: str):
    response = supabase.table("alerts").insert({
        "message": message,
        "timestamp": datetime.utcnow().isoformat()
    }).execute()
    return response

# ---------------------------------------------------------
# GET LATEST ADMIN ALERT
# ---------------------------------------------------------
def get_latest_alert():
    response = (
        supabase.table("alerts")
        .select("*")
        .order("timestamp", desc=True)
        .limit(1)
        .execute()
    )
    return response.data[0] if response.data else None

# ---------------------------------------------------------
# SEND SOS REPORT
# ---------------------------------------------------------
def push_sos(lat: float, lon: float):
    response = supabase.table("sos_reports").insert({
        "lat": lat,
        "lon": lon,
        "timestamp": datetime.utcnow().isoformat()
    }).execute()
    return response

# ---------------------------------------------------------
# SEND ANONYMOUS REPORT
# ---------------------------------------------------------
def push_anonymous_report(report: str):
    response = supabase.table("anonymous_reports").insert({
        "report": report,
        "timestamp": datetime.utcnow().isoformat()
    }).execute()
    return response

