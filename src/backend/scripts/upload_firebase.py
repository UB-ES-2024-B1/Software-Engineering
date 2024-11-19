import firebase_admin
from firebase_admin import credentials, firestore
import json
import os

# Inicializar Firebase
current_directory = os.path.dirname(os.path.abspath(__file__))

cred = credentials.Certificate(f'{current_directory}/firebase_key.json')
firebase_admin.initialize_app(cred)

# Inicializar la base de datos Firestore
db = firestore.client()
lista = ['user', 'genre','moviecast','castmember','moviegenre', 'movie']
for i in lista:

    ruta = f"{current_directory}/{i}.json"
    # Cargar los datos desde el archivo JSON
    with open(f"{ruta}", 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Subir los datos a Firestore
    for d in data:
        # Crear un documento en la colección i
        db.collection(i).add(d)

    print("Datos de movie subidos a Firestore.")
