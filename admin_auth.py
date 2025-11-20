import streamlit as st
from supabase_backend import supabase

# ------------------------------------------------------
# ADMIN AUTH USING SUPABASE ONLY
# ------------------------------------------------------

def supabase_login(email, password):
    """
    Logs in via Supabase authentication table + admin_users table.
    Returns user record if authorized, otherwise None.
    """

    try:
        # 1. Try to authenticate via Supabase Auth
        auth_result = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        if not auth_result or "user" not in auth_result:
            return None

        user = auth_result["user"]
        uid = user["id"]

        # 2. Check if the user is in the admin_users table
        admin_check = (
            supabase.table("admin_users")
            .select("*")
            .eq("uid", uid)
            .execute()
        )

        if not admin_check.data:
            return None  # Not an admin

        return uid  # Authorized admin

    except Exception as e:
        print("SUPABASE LOGIN ERROR:", e)
        return None
