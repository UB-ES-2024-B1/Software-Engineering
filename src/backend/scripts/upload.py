import cloudinary
import cloudinary.uploader
import cloudinary.api
from io import BytesIO

# Configura tus credenciales de Cloudinary
cloudinary.config(
    cloud_name="dt2flsyai",  # Reemplaza con tu cloud_name
    api_key="837635363457355",  # Reemplaza con tu api_key
    api_secret="HFR8SGyqX239kIb8YYTE6Wc_A50"  # Reemplaza con tu api_secret
)

# Función para subir imágenes desde un archivo
def subir_imagen_desde_archivo(file):
    """
    Sube una imagen a Cloudinary directamente desde un archivo.
    :param file: Archivo en formato BytesIO o similar
    :return: Diccionario con el public_id y la URL de la imagen
    """
    try:
        # Subir la imagen directamente a Cloudinary
        result = cloudinary.uploader.upload(
            file,
            folder="imagenes-perfil",  # Opcional: Carpeta en Cloudinary
            use_filename=False,         # Usa el nombre original del archivo
            unique_filename=False      # Si prefieres un nombre único, ponlo en True
        )
        
        # Obtener public_id y URL de la imagen
        public_id = result["public_id"]
        image_url = result["url"]

        print("Imagen subida correctamente:", image_url)
        print("Public ID:", public_id)

        return {"public_id": public_id, "url": image_url}

    except Exception as e:
        print("Error subiendo la imagen:", e)

# Función para eliminar imágenes
def eliminar_imagen(public_id):
    """
    Elimina una imagen en Cloudinary usando su public_id.
    :param public_id: El ID público de la imagen
    """
    try:
        result = cloudinary.uploader.destroy(public_id)
        
        if result["result"] == "ok":
            print("Imagen eliminada correctamente.")
        else:
            print("No se pudo eliminar la imagen:", result)
    except Exception as e:
        print("Error eliminando la imagen:", e)

