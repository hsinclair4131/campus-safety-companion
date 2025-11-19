import firebase_admin
from firebase_admin import auth, firestore

# Lazy-loaded Firestore client (so it doesn't crash before firebase_init runs)
_db = None

def get_db():
    global _db
    if _db is None:
        # Firestore only works AFTER firebase_init() has run in main.py
        _db = firestore.client()
    return _db


def firebase_login(email, password):
    """
    Login admin via Firebase Authentication + Firestore admin_users validation.
    """
    try:
        # Firebase Authentication lookup
        user = auth.get_user_by_email(email)
        uid = user.uid

        # Check admin authorization in Firestore
        db = get_db()
        admin_doc = db.collection("admin_users").document(uid).get()

        if not admin_doc.exists:
            return None  # Not an authorized admin

        return uid  # Success

    except Exception as e:
        print("LOGIN ERROR:", e)
        return None
