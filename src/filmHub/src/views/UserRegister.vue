<template>
  <div class="register-page">
    <HeaderPage />
    
    <div class="overlay"></div>

    <div class="main-content">
      <div class="register-form">
        <h2>Registration</h2>
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
import { API_BASE_URL } from '@/config.js'; // Asegúrate de que esta línea apunte a tu archivo config.js

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
    };
  },
  methods: {
    async handleSubmit() {
      // Validar que las contraseñas coincidan
      if (this.password !== this.rePassword) {
        alert('Las contraseñas no coinciden.');
        return;
      }

      const userData = {
        full_name: this.name,
        email: this.email,
        password: this.password,
      };

      try {
        const response = await axios.post(`${API_BASE_URL}/users/`, userData);
        console.log('Usuario registrado:', response.data);
        // Redirigir o mostrar un mensaje de éxito aquí
      } catch (error) {
        console.error('Error en el registro:', error);
        alert('Error en el registro: ' + error.response.data.detail);
      }
    },
  },
};
</script>

<style scoped>
/* Estilos específicos para el componente de registro */

/* Ajustes del header */
.banner {
  display: none; /* Ocultar el banner anterior */
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

/* Estilo del formulario de registro */
.register-form {
  background-color: rgba(0, 0, 0, 0.8 );
  padding: 40px;
  border-radius: 10px;
  width: 450px;
  height: 550px;
  text-align: center;
  transform: translateY(30px);
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
  color: white; /* Cambia el color del enlace */
  text-decoration: none; /* Quita el subrayado */
  font-weight: bold; /* Haz el texto más grueso */
  transition: color 0.3s ease; /* Añade una transición suave al color */
}

.register-form a:hover {
  color: white; /* Cambia el color al pasar el ratón */
  text-decoration: underline; /* Puedes agregar un subrayado al pasar el ratón si lo deseas */
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
  position: absolute; /* Para cubrir toda la página */
  top: 0;
  left: 0;
  right: 0; 
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5); /* Negro con opacidad */
  z-index: 1; /* Asegura que esté encima del fondo pero debajo del contenido */
}

/* Estilos globales para la página de registro */
.register-page {
  height: 100vh;
  margin: 0;
  padding: 0;
  font-family: 'Roboto', sans-serif;
  background-image: url('@/assets/fondo_register.jpg'); /* Aplicar la imagen de fondo solo a la página de registro */
  background-size: cover; /* Asegura que la imagen cubra todo el fondo */
  background-position: center; /* Centrar la imagen */
  background-repeat: no-repeat; /* Evita que la imagen se repita */
  z-index: -1;
}
</style>
