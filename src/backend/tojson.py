import firebase_admin
from firebase_admin import credentials, firestore
import json
import sqlite3

# Conexión a tu base de datos SQLite
conn = sqlite3.connect('src/backend/filmhub_database.db')
cursor = conn.cursor()

db_tables = ['castmember', 'genre', 'movie', 'moviecast', 'moviegenre', 'user']
def process_row(row, column_names):
    processed_row = {}
    for col_name, value in zip(column_names, row):
        if isinstance(value, str):  # Si el valor es una cadena
            try:
                # Intentar convertir la cadena en una lista (si es una cadena JSON)
                processed_row[col_name] = json.loads(value) if value.startswith('[') and value.endswith(']') else value
            except json.JSONDecodeError:
                processed_row[col_name] = value
        else:
            processed_row[col_name] = value
    return processed_row

for t in db_tables:
    # Exportar tabla
    cursor.execute(f"SELECT * FROM {t}")  # Cambia 'user' por el nombre de tu tabla
    column_names = [description[0] for description in cursor.description]
    rows = cursor.fetchall()

    # Procesar las filas y convertir las cadenas que representan listas en listas reales
    data = [process_row(row, column_names) for row in rows]

    # Guardar en el archivo JSON
    with open((f'{t}.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print("Datos exportados a f'{t}.json'.")
# Cerrar la conexión
conn.close()


