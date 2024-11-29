import cloudinary from 'cloudinary';

// Configura tus credenciales de Cloudinary
cloudinary.config({
  cloud_name: 'dt2flsyai',   // Reemplaza con tu cloud name
  api_key: '837635363457355',         // Reemplaza con tu API Key
  api_secret: 'HFR8SGyqX239kIb8YYTE6Wc_A50',   // Reemplaza con tu API Secret
});

async function subirImagen(filePath) {
  try {
    // Subir la imagen a Cloudinary
    const result = await cloudinary.v2.uploader.upload(filePath, {
      folder: 'imagenes-perfil',  // Opcional, puedes organizar tus imágenes en carpetas
      use_filename: true,         // Usa el nombre original del archivo
      unique_filename: false,     // Si prefieres un nombre único, ponlo como true
    });

    // Guarda el public_id y la URL de la imagen
    const publicId = result.public_id;
    const imageUrl = result.url;

    console.log('Imagen subida correctamente:', imageUrl);
    console.log('Public ID:', publicId); // Aquí obtienes el public_id

    return { publicId, imageUrl };  // Devuelve el public_id y la URL de la imagen subida
  } catch (error) {
    console.error('Error subiendo la imagen:', error);
  }
}


// Función para eliminar un archivo de Cloudinary
async function eliminarImagen(publicId) {
  try {
    // Elimina el archivo usando el public_id
    const result = await cloudinary.v2.uploader.destroy(publicId);
    
    if (result.result === "ok") {
      console.log("Imagen eliminada correctamente.");
    } else {
      console.log("No se pudo eliminar la imagen:", result);
    }
  } catch (error) {
    console.error("Error eliminando la imagen:", error);
  }
}

subirImagen('src/filmHub/src/assets/logo.png');