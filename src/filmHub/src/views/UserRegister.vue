<template>
  <div class="register-page">
    <HeaderPage />

    <div class="overlay"></div>

    <div class="main-content">
      <!-- Clase condicional 'expanded' que se activa si 'passwordError' o 'emailError' es true -->
      <div :class="['register-form', { 'expanded': passwordError || emailError }]">
        <h2>Registration</h2>

        <!-- Mensaje de error de contraseñas no coincidentes -->
        <p v-if="passwordError" class="error-message">
          Passwords do not match. Try again.
        </p>
        
        <!-- Mensaje de error de email ya registrado -->
        <p v-if="emailError" class="error-message">
          Email already registered. Try again.
        </p>

        <form @submit.prevent="handleSubmit">
          <div>
            <input type="text" id="name" v-model="name" placeholder="First and last name" required />
          </div>
          <div>
            <input type="email" id="email" v-model="email" placeholder="example@email.com" required />
          </div>
          <div>
            <input type="password" id="password" v-model="password" placeholder="Password" required />
          </div>
          <div>
            <input type="password" id="rePassword" v-model="rePassword" placeholder="Repeat Password" required />
          </div>
          <button type="submit">REGISTER</button>
          <p>Already have an account?
            <router-link to="/login" class="create-account-link">Sign in</router-link>
          </p>
        </form>
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
import { API_BASE_URL } from '@/config.js';

export default {
  name: 'UserRegister',
  components: {
    HeaderPage,
  },
  data() {
    return {
      name: '',
      email: '',
      password: '',
      rePassword: '',
      passwordError: false, // Estado para mostrar o esconder el mensaje de error de contraseñas
      emailError: false,    // Estado para mostrar o esconder el mensaje de error de email
    };
  },
  methods: {
    async handleSubmit() {
      // Restablecer los mensajes de error antes de verificar condiciones
      this.passwordError = false;
      this.emailError = false;

      // Validar que las contraseñas coincidan
      if (this.password !== this.rePassword) {
        this.passwordError = true; // Muestra el mensaje de error de contraseñas
        return; // Sale de la función para evitar otros errores simultáneos
      }

      const userData = {
        full_name: this.name,
        email: this.email,
        password: this.password,
      };

      try {
        const response = await axios.post(`${API_BASE_URL}/users/`, userData);
        console.log('Usuario registrado:', response.data);
        this.$router.push('/login');
      } catch (error) {
        console.error('Error en el registro:', error);
        
        // Verificar si el error es debido a un email ya registrado
        if (error.response && error.response.data.detail === 'Email already registered') {
          this.emailError = true; // Muestra solo el mensaje de error de email
        }
      }
    },
  },
};
</script>
  

<style scoped>
/* Estilo del formulario de registro */
.register-form {
  background-color: rgba(0, 0, 0, 0.8);
  padding: 40px;
  border-radius: 10px;
  width: 450px;
  height: 550px;
  text-align: center;
  transform: translateY(30px);
  z-index: 10;
  transition: height 0.3s ease; /* Transición para cambio de altura */
}

/* Expande el formulario cuando hay un error */
.register-form.expanded {
  height: 600px; /* Aumenta la altura solo cuando hay un error */
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

/* Resto de los estilos, no cambian */
.main-content {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  padding: 20px;
  z-index: 10;
}

.register-form h2 {
  margin-bottom: 30px;
  color: #fff;
  font-weight: bold;
}

.register-form input {
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

.register-form input:focus {
  border-color: white;
  outline: none;
}

.register-form button {
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

.register-form button:hover {
  background: rgba(255, 255, 255, 0.3);
}

.register-form p {
  margin-top: 10px;
  color: rgba(255, 255, 255, 0.8);
}

.register-form a {
  color: white;
  text-decoration: none;
  font-weight: bold;
  transition: color 0.3s ease;
}

.register-form a:hover {
  color: white;
  text-decoration: underline;
}

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

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0; 
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1;
}

.register-page {
  height: 100vh;
  margin: 0;
  padding: 0;
  font-family: 'Roboto', sans-serif;
  background-image: url('@/assets/fondo_register.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  z-index: -1;
}
</style>
