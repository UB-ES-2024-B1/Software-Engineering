<template>
  <div class="login-page">
    <HeaderPage />
    
    <!-- Capa negra con opacidad -->
    <div class="overlay"></div>

    <div class="main-content">
      <div class="login-form">
        <h2>Login</h2>
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

    <footer class="footer">
      <p>&copy; 2024 Web Name. All rights reserved.</p>
    </footer>
  </div>
</template>


<script>
// Importar el componente HeaderPage
import HeaderPage from '@/components/HeaderPage.vue';

export default {
  name: 'UserLogin',
  components: {
    HeaderPage,
  },
  data() {
    return {
      email: '',
      password: '',
    };
  },
  methods: {
    handleLogin() {
      console.log('Iniciando sesión con:', this.email);
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
}

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
  background-image: url('@/assets/fondo_login.jpg'); /* Aplicar la imagen de fondo */
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  z-index: -1;
}
</style>
