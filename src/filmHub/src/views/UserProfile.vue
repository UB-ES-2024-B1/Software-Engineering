<template>

  <div class="login-page">

  <div class="profile-page">

    <HeaderPage />

    <div class="overlay"></div>

    <div class="main-content">

      <div :class="['login-form', { 'expanded': loginError }]">
        <h2>Login</h2>

        <!-- Mensaje de error si el login falla -->
        <p v-if="loginError" class="error-message">
          User not registered. Please try again.
        </p>

        <form @submit.prevent="handleLogin">
          <div>
            <input type="email" id="email" v-model="email" placeholder="example@email.com" required />
          </div>
          <div>
            <input type="password" id="password" v-model="password" placeholder="Password" required />
          </div>
          <button type="submit">LOGIN</button>
          <p>Don't have an account?
            <router-link to="/register" class="create-account-link">Create account</router-link>
          </p>
        </form>
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
        <
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

  name: 'UserLogin',

  name: 'UserProfile',

  components: {
    HeaderPage,
  },
  data() {
    return {

      email: '',
      password: '',
      loginError: false, // Estado para mostrar o esconder el mensaje de error
    };
  },
  methods: {
    async handleLogin() {
      try {
        // Usar FormData para enviar los datos en el formato adecuado
        const formData = new FormData();
        formData.append('username', this.email); // OAuth2PasswordRequestForm espera 'username'
        formData.append('password', this.password); // Y también espera 'password'

        // Realizar la solicitud POST al backend para el login
        const response = await axios.post(`${API_BASE_URL}/login/`, formData, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        });
        // Si la solicitud tiene éxito, almacenar el token en localStorage
        localStorage.setItem('token', response.data.access_token);
        // Redirigir al usuario a la página principal
        this.$router.push('/');

        // Asegúrate de que los componentes parent puedan actualizar el estado
        window.dispatchEvent(new Event('storage')); // Para informar a otros componentes del cambio
        this.loginError = false; // Reiniciar el error en caso de éxito
      } catch (error) {
        console.error('Error al iniciar sesión:', error);
        this.loginError = true; // Muestra el mensaje de error
      }
    },

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

  height: 100vh;

  padding: 20px;
  z-index: 10;
}


/* Estilo del formulario de login */
.login-form {
  background-color: rgba(0, 0, 0, 0.8);
  padding: 40px;
  border-radius: 10px;
  width: 450px;
  height: 400px;
  text-align: center;
  transform: translateY(20px);
  z-index: 10;
  transition: height 0.3s ease; /* Transición para cambio de altura */
}

/* Expande el formulario cuando hay un error */
.login-form.expanded {
  height: 450px; /* Aumenta la altura solo cuando hay un error */
}

/* Estilo del mensaje de error */
.error-message {
  background-color: rgba(255, 0, 0, 0.5);
  width: 100%; /* Ancho completo para alinearlo al centro */
  max-width: 80%; /* Ajusta el ancho máximo dentro del formulario */
  color: white;
  padding: 8px;
  border-radius: 5px;
  margin: 0 auto 20px; /* Centra horizontalmente y añade margen inferior */
  text-align: center;
  z-index: 30;
}

/* Estilo del resto del formulario */
.login-form h2 {
  margin-bottom: 30px;
  color: #fff;
  font-weight: bold;
}

.login-form input {
  width: 80%;
  padding: 15px;
  margin-bottom: 20px;
  border: 1px solid gray;
  border-radius: 5px;
  transition: border-color 0.3s ease;
  background: #1f1f1f;
  opacity: 0.7;
  color: white;
}

.login-form input:focus {
  border-color: white;
  outline: none;
}

.login-form button {
  width: 80%;
  margin-top: 15px;
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

.login-form button:hover {
  background: rgba(255, 255, 255, 0.3);
}

.login-form p {
  margin-top: 10px;
  color: rgba(255, 255, 255, 0.8);
}

.login-form a {
  color: white;
  text-decoration: none;
  font-weight: bold;
  transition: color 0.3s ease;
}

.login-form a:hover {
  color: white;
  text-decoration: underline;
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

  bottom: 20;
  width: 100%;
  height: 200px;
  z-index: 5;
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

/* Estilos globales para la página de login */
.login-page {
  height: 100vh;
  margin: 0;
  padding: 0;
  font-family: 'Roboto', sans-serif;
  background-image: url('@/assets/fondo_login.jpg');
  /* Aplicar la imagen de fondo */
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  z-index: -1;
}

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
