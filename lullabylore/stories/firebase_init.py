import firebase_admin
from firebase_admin import credentials, firestore
import os
import environ

env = environ.Env()
env.read_env()
cred_path = env('FIREBASE_CRED_PATH')


cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

db = firestore.client()
