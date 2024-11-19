# firebase_config.py
import firebase_admin
from firebase_admin import credentials, firestore

import os

current_directory = os.path.dirname(os.path.abspath(__file__))

path = f"{current_directory}/firebase_key.json"

if not os.path.exists(path):
    print(f"El archivo de credenciales no se encuentra en la ruta: {path}")
else:
    print(f"Archivo encontrado: {path}")
# Inicializa Firebase Admin SDK con el archivo de credenciales de tu proyecto Firebase
cred = credentials.Certificate(path)
firebase_admin.initialize_app(cred)

# Instancia de Firestore
db = firestore.client()
