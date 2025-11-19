import os
from supabase import create_client, Client

# -------------------------------------------------------------
#  INITIALIZE SUPABASE
# -------------------------------------------------------------

def get_supabase() -> Client:
    url = os.environ.get("SUPABASE_URL")
    anon = os.environ.get("SUPABASE_ANON_KEY")

    if not url or not anon:
        raise RuntimeError("❌ Missing Supabase credentials in Streamlit Secrets.")

    return create_client(url, anon)

supabase = get_supabase()


# -------------------------------------------------------------
# ALERT SYSTEM  (Admin pushes, students read)
# -------------------------------------------------------------

def push_alert(message: str):
    data = {
        "message": message,
        "active": True
    }

    response = supabase.table("alerts").insert(data).execute()
    return response


def get_latest_alert():
    response = (
        supabase
        .table("alerts")
        .select("*")
        .order("timestamp", desc=True)
        .limit(1)
        .execute()
    )

    if response.data:
        return response.data[0]
    return None


# -------------------------------------------------------------
# SOS SYSTEM (Students send GPS SOS)
# -------------------------------------------------------------

def push_sos(latitude: float, longitude: float):
    data = {
        "lat": latitude,
        "lon": longitude,
        "timestamp": "now()"
    }

    return supabase.table("sos_reports").insert(data).execute()


def get_all_sos():
    response = (
        supabase
        .table("sos_reports")
        .select("*")
        .order("timestamp", desc=True)
        .execute()
    )
    return response.data


# -------------------------------------------------------------
# ANONYMOUS REPORTS
# -------------------------------------------------------------

def push_anonymous_report(text: str):
    data = {
        "report": text,
        "timestamp": "now()"
    }
    return supabase.table("anonymous_reports").insert(data).execute()


def get_anonymous_reports():
    response = (
        supabase
        .table("anonymous_reports")
        .select("*")
        .order("timestamp", desc=True)
        .execute()
    )
    return response.data
