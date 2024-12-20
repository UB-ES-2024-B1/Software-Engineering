<template>
  <div class="profile-page">
    <HeaderPage />

    <div class="overlay"></div>

    <div class="main-content">
      <div class="profile-box">

        <!-- Mostrar error si no se pudo cargar la información -->
        <p v-if="error" class="error-message">{{ error }}</p>

        <!-- Formulario de edición -->
        <form v-else class="profile-edit-form" @submit.prevent="submitChanges">
          <!-- Campo de imagen de perfil -->
          <div class="form-group profile-picture-group">
            <label for="profile-picture">Profile Picture:</label>
            <div class="profile-picture-wrapper">
              <img :src="formData.profile_picture || require('@/assets/foto_perfil.png')" class="profile-picture"
                @click="handleProfilePictureClick" />
              <input id="profile-picture" type="file" ref="profilePictureInput" accept="image/*" style="display: none"
                @change="handleProfilePictureChange" />
            </div>
          </div>


          <!-- Mostrar el correo como texto en vez de un formulario -->
          <div class="form-group">
            <label for="email">Email Address:</label>
            <!-- Solo mostrar el correo sin permitir editar -->
            <p>{{ formData.email }}</p>
          </div>

          <div class="form-group">
            <label for="full_name">Name:</label>
            <input id="full_name" type="text" v-model="formData.full_name" required placeholder="Enter your name" />
          </div>

          <!-- Mostrar la contraseña -->
          <div class="form-group">
            <label for="password">Password:</label><br />
            <span>********</span>
          </div>

          <div class="form-actions">
            <button type="submit" class="save-btn">Save Changes</button>
            <router-link to="/profile">
              <button class="cancel-btn">Cancel</button>
            </router-link>
          </div>
        </form>
      </div>
    </div>
    <FooterComponent />
  </div>
</template>

<script>
import HeaderPage from '@/components/HeaderPage.vue';
import axios from 'axios';
import { API_BASE_URL } from '@/config.js';
import FooterComponent from '@/components/FooterComponent.vue';

export default {
  name: 'EditProfile',
  components: {
    HeaderPage,
    FooterComponent,
  },
  data() {
    return {
      formData: {
        email: '',
        full_name: '',
        profile_picture: '', // URL of the current profile picture
      },
      error: null,
    };
  },
  created() {
    const userEmail = localStorage.getItem('userEmail');
    if (!userEmail) {
      this.$router.push('/login');
      return;
    }

    // Initial data loading
    axios
      .get(`${API_BASE_URL}/users/email/${userEmail}`)
      .then((response) => {
        const { email, full_name, img_url } = response.data;

        // Assign the fetched values to the form
        this.formData.email = email;
        this.formData.full_name = full_name;

        // Use the provided image URL or a default image if it doesn't exist
        this.formData.profile_picture = img_url;
      })
      .catch((error) => {
        console.error('Error fetching user data:', error);
        this.error = 'Error fetching user data. Please try again.';
      });
  },

  methods: {
    handleProfilePictureClick() {
      // Trigger the file input click event
      this.$refs.profilePictureInput.click();
    },
    handleProfilePictureChange(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          // Resize the image before assigning it to formData
          this.resizeImage(e.target.result, (resizedImg) => {
            this.formData.profile_picture = resizedImg; // Update the image in the view
          });
        };
        reader.readAsDataURL(file);
      }
    },

    resizeImage(imageSrc, callback) {
      const img = new Image();
      img.onload = () => {
        // Create a canvas to resize the image
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');

        // Set the new width and height (240px in this case)
        const width = 240;
        const height = (img.height / img.width) * width; // Maintain aspect ratio

        canvas.width = width;
        canvas.height = height;

        // Draw the resized image on the canvas
        ctx.drawImage(img, 0, 0, width, height);

        // Get the resized image as a base64 string
        const resizedImage = canvas.toDataURL('image/jpeg', 0.8); // JPEG format with 80% quality
        callback(resizedImage);
      };
      img.src = imageSrc;
    },

    submitChanges() {
      // Create a FormData object to send the data
      const formData = new FormData();

      // Append the form fields
      if (this.formData.full_name) {
        formData.append('full_name', this.formData.full_name);
      }
      if (this.formData.profile_picture && this.$refs.profilePictureInput.files[0]) {
        formData.append('img', this.$refs.profilePictureInput.files[0]);
      }

      // Send the updated data to the backend using Axios
      axios
        .put(`${API_BASE_URL}/users/email/${this.formData.email}`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })
        .then(() => {
          // Redirect to the profile page after successful update
          this.$router.push('/profile');
        })
        .catch((error) => {
          console.error('Error updating user data:', error);
          this.error = 'Error updating user data. Please try again.';
        });

      // Save the updated profile picture and name to localStorage
      localStorage.setItem('userName', this.formData.full_name);
      localStorage.setItem('userImg', this.formData.profile_picture); // Save resized image
    },
  },
};
</script>





<style scoped>
/* Estilos generales iguales a los de profile */
.profile-page {
  height: 100vh;
  margin: 0;
  padding: 0;
  background-image: url('@/assets/fondo_login.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  z-index: -1;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1;
}

.main-content {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  padding: 20px;
  z-index: 10;
}

.profile-box {

    position: relative;
    display: flex;
    flex-direction: column;
    background-color: rgba(0, 0, 0, 0.8);
    backdrop-filter: blur(5px);
    padding: 40px;
    border-radius: 10px;
    width: 750px;
    height: 550px;
    color: white;
    z-index: 20;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5); /* Mejora visual */
    border: 2px solid rgba(255, 255, 255, 0.1); /* Sutileza */
    margin-bottom: 146px;

}



/* Campo de foto de perfil */
.profile-picture-group {
  display: flex;
  flex-direction: column;
  align-items: left;
  margin-bottom: 20px;
}

.profile-picture-wrapper {
  position: relative;
  cursor: pointer;
  display: flex;
  justify-content: left;
  align-items: center;
}

.profile-picture {
  width: 120px;
  /* Ajusta el tamaño según lo necesario */
  height: 120px;
  /* Asegúrate de que sea cuadrado */
  border-radius: 50%;
  /* Esto hace que la imagen sea circular */
  object-fit: cover;
  /* Asegura que la imagen se ajuste sin distorsión */
  border: 2px solid white;
  /* Opcional: borde blanco */
  transition: transform 0.3s;
  /* Animación al pasar el cursor */
}

.profile-picture:hover {
  transform: scale(1.1);
}




/* Estilo de formulario */
.profile-edit-form {
  display: flex;
  flex-direction: column;
  gap: 10px;
}



.form-group label {
  font-weight: bold;
  color: white;
  margin-bottom: 5px;
}

.form-group input {
  width: 100%;
  padding: 8px;
  margin-bottom: 0px;
  border: 1px solid gray;
  border-radius: 5px;
  transition: border-color 0.3s ease;
  background: #1f1f1f;
  opacity: 0.7;
  color: white;
}

.form-group input:focus {
  border-color: #1fb115;
}

/* Botones de acción */
.form-actions {
  display: flex;
  justify-content: space-between;
  gap: 10px;
}

.save-btn {
  width: 75;
  margin-top: 15px;
  padding: 10px;
  background: rgba(0, 255, 0, 0.3);
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: background 0.3s ease;
  z-index: 5;
}

.save-btn:hover {
  background: rgba(0, 255, 0, 0.4);

}

.cancel-btn {
  width: 75;
  margin-top: 15px;
  padding: 10px;
  background: rgba(255, 0, 0, 0.3);
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: background 0.3s ease;
  z-index: 5;
}

.cancel-btn:hover {
  background: rgba(255, 0, 0, 0.4);

}
</style>
