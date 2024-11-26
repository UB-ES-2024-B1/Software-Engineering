<template>
  <div class="login-page">
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
      </div>
    </div>

    <FooterComponent />
  </div>
</template>

<script>
  import HeaderPage from '@/components/HeaderPage.vue';
  import axios from 'axios';
  import { API_BASE_URL } from '@/config.js'; // Asegúrate de tener la URL base aquí
  import FooterComponent from '@/components/FooterComponent.vue';
  
  export default {
    name: 'UserLogin',
    components: {
      HeaderPage,
      FooterComponent,
    },
    data() {
      return {
        email: '', // Correo del usuario
        password: '', // Contraseña del usuario
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
  
          // Guardar el token en localStorage
          localStorage.setItem('token', response.data.access_token);
  
          // Guardar el email para futuras solicitudes
          localStorage.setItem('userEmail', this.email);
  
          // Ahora obtenemos el user_id a partir del email
          const userEmail = this.email;
          const userResponse = await axios.get(`${API_BASE_URL}/users/email/${encodeURIComponent(userEmail)}`);
          
          // Guardar el user_id en localStorage
          localStorage.setItem('user_id', userResponse.data.id);
  
          // Notificar éxito
          window.dispatchEvent(new Event('storage')); // Informa a otros componentes sobre el cambio
          this.loginError = false;
  
          // Redirigir al usuario a la página de perfil
          this.$router.push('/');
        } catch (error) {
          console.error('Error al iniciar sesión:', error);
          this.loginError = true; // Mostrar mensaje de error
        }
      },
    },
  };
  </script>
  


<style scoped>
/* Estilos específicos para el componente de login (idénticos a los de registro) */

/* Ajustes del header */
.banner {
  display: none;
}

/* Estilo principal del contenido */
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
  transition: height 0.3s ease;
  /* Transición para cambio de altura */
}

/* Expande el formulario cuando hay un error */
.login-form.expanded {
  height: 450px;
  /* Aumenta la altura solo cuando hay un error */
}

/* Estilo del mensaje de error */
.error-message {
  background-color: rgba(255, 0, 0, 0.5);
  width: 100%;
  /* Ancho completo para alinearlo al centro */
  max-width: 80%;
  /* Ajusta el ancho máximo dentro del formulario */
  color: white;
  padding: 8px;
  border-radius: 5px;
  margin: 0 auto 20px;
  /* Centra horizontalmente y añade margen inferior */
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
  background-image: url('@/assets/fondo_login.jpg');
  /* Aplicar la imagen de fondo */
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  z-index: -1;
}
</style>
