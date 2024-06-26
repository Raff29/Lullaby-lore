import firebase_admin
from firebase_admin import credentials, firestore
import os
from environ import Env

env = Env()
env.read_env()

cred_path = env('FIREBASE_CRED_PATH')
cred_path = os.path.join(os.path.dirname(__file__), cred_path)
                    
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

db = firestore.client()
