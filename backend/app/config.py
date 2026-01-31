import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("real-estate-project-ad5bd-firebase-adminsdk-fbsvc-ea1c520fee")
firebase_admin.initialize_app(cred)