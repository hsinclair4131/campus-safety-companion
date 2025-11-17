import firebase_admin
from firebase_admin import credentials, firestore

# Placeholder – DOES NOT expose real key
cred = credentials.Certificate("firebase_key.json")

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()
