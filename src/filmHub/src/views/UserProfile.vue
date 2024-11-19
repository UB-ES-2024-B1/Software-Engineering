<template>
  <div class="profile-page">
    <HeaderPage />

    <div class="overlay"></div>

    <div class="main-content">
      <div class="profile-box">
        <h2 class="profile-title">Profile</h2>

        <p v-if="error" class="error-message">{{ error }}</p>

        <div v-else-if="userData" class="profile-content">
          <!-- Imagen de perfil -->
          <div class="profile-image">
            <img :src="require('@/assets/foto_perfil.png')" alt="Profile Picture" />
          </div>

          <div class="profile-info">
            <p>
              <strong>Email Address:</strong><br />
              <span>{{ userData.email }}</span>
            </p>
            <p>
              <strong>Name:</strong><br />
              <span>{{ userData.full_name }}</span>
            </p>
            <!-- Mostrar la contraseña oculta -->
            <p>
              <strong>Password:</strong><br />
              <span>********</span>
            </p>
          </div>

          <!-- Botón de modificar -->
          <div class="button-group">
            <router-link to="/edit">
              <button class="modify-btn">Modify</button>
            </router-link>
            <span class="button-spacing"></span>
            <router-link to="/addMovies">
              <button class="add-movies-btn">Add Movies</button>
            </router-link>
          </div>

        </div>

        <div v-else class="loading-message">
          Loading profile...
        </div>
      </div>
    </div>

    <footer class="footer">
      <p>&copy; 2024 Web Name. All rights reserved.</p>
    </footer>
  </div>
</template>

<script>
import HeaderPage from '@/components/HeaderPage.vue';
import axios from 'axios';
import { API_BASE_URL } from '@/config.js'; // Asegúrate de tener la URL base aquí

export default {
  name: 'UserProfile',
  components: {
    HeaderPage,
  },
  data() {
    return {
      userData: null,
      error: null,
      profileImage: '@/assets/default_profile.jpg',
    };
  },
  created() {
    const userEmail = localStorage.getItem('userEmail');
    if (!userEmail) {
      this.$router.push('/login');
      return;
    }

    // Solicitar datos del usuario
    axios
      .get(`${API_BASE_URL}/users/email/${userEmail}`)
      .then((response) => {
        this.userData = response.data;
      })
      .catch((error) => {
        console.error('Error al obtener los datos del usuario:', error);
        this.error = 'Error fetching user data. Please try again.';
      });
  },
  methods: {
    // Redirigir a la página de edición
  },
};
</script>



<style scoped>
/* Estilo general de la página */
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

/* Capa negra con opacidad */
.overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1;
}

/* Contenedor principal */
.main-content {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 80vh;
  padding: 20px;
  z-index: 10;
}

/* Caja del perfil */
.profile-box {
  display: flex;
  flex-direction: column;
  background-color: rgba(0, 0, 0, 0.6);
  padding: 40px;
  border-radius: 10px;
  width: 750px;
  height: 450px;
  align-items: center;
  color: white;
  z-index: 20;
}

/* Título del perfil */
.profile-title {
  margin-bottom: 40px;
  font-size: 28px;
  font-weight: bold;
  color: white;
  padding-right: 395px;
  z-index: 20;
}

/* Contenido del perfil (imagen + info) */
.profile-content {
  display: flex;
  width: 100%;
  align-items: center;
  justify-content: space-between;
}

/* Estilo de la imagen de perfil */
.profile-image {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding-right: 50px;
  padding-bottom: 60px;
}

.profile-image img {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  border: 0px solid white;
  object-fit: cover;

}

/* Estilo de la información del perfil */
.profile-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.profile-info p {
  margin-bottom: 60px;
  /* Espaciado entre cada línea */
  font-size: 18px;
  line-height: 1.5;
}

.profile-info strong {
  font-weight: bold;
  color: #ffffff;
}

.profile-info span {
  display: block;
  /* Fuerza a que el contenido esté en una nueva línea */
  color: #dcdcdc;
  /* Ajusta el color si es necesario */
  font-size: 16px;
  /* Asegúrate de que tenga un buen tamaño */
}


/* Footer básico */
.footer {
  background-color: #121212;
  color: #fff;
  padding: 10px;
  text-align: center;
  position: absolute;
  bottom: 0;
  width: 100%;
  z-index: 5;
}

.modify-btn {
  width: 100%;
  margin-top: 225px;
  padding: 10px;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: background 0.3s ease;
  z-index: 5;
}

.modify-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}


</style>
