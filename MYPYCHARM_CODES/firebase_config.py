import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# -------------------------------------------------------------
#  FIREBASE LOCAL INITIALIZATION (NO STREAMLIT SECRETS)
# -------------------------------------------------------------

def get_firebase_app():
    """
    Initializes Firebase ONLY from local serviceAccountKey.json.
    Streamlit secrets are disabled for local development.
    """

    # If Firebase already initialized → return same app
    if firebase_admin._apps:
        return firebase_admin.get_app()

    # LOCAL DEVELOPMENT MODE
    if os.path.exists("serviceAccountKey.json"):
        cred = credentials.Certificate("serviceAccountKey.json")
        return firebase_admin.initialize_app(cred)

    raise FileNotFoundError(
        "serviceAccountKey.json NOT FOUND.\n"
        "Place it in your project root next to main.py."
    )


def get_db():
    """Returns Firestore database client."""
    app = get_firebase_app()
    return firestore.client(app)


# OPTIONAL (backwards compatibility)
def firebase_init():
    return get_db()
