from supabase import create_client
import os
from datetime import datetime

# -------------------------------------------------------
# INITIALIZE SUPABASE FROM STREAMLIT SECRETS
# -------------------------------------------------------

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_ANON_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# -------------------------------------------------------
# ALERT SYSTEM
# -------------------------------------------------------

def get_latest_alert():
    """Retrieve the newest alert"""
    response = supabase.table("alerts").select("*").order("timestamp", desc=True).limit(1).execute()
    
    if response.data:
        return response.data[0]
    return None


# -------------------------------------------------------
# SOS LOCATION
# -------------------------------------------------------

def push_sos(lat, lon):
    """Send student SOS coordinates"""
    supabase.table("sos_reports").insert({
        "latitude": lat,
        "longitude": lon,
        "timestamp": datetime.utcnow().isoformat()
    }).execute()


# -------------------------------------------------------
# ANONYMOUS REPORTS
# -------------------------------------------------------

def push_anonymous_report(report_text):
    """Submit anonymous report"""
    supabase.table("anonymous_reports").insert({
        "report": report_text,
        "timestamp": datetime.utcnow().isoformat()
    }).execute()
