<template>
  <header :class="['header', { scrolled }]">
    <div class="logo">
      <router-link to="/">
        <img :src="require('@/assets/logo.png')" alt="Logo" />
      </router-link>
    </div>

    <!-- Mostrar el botón "All Movies" solo si no estamos en páginas de registro o login -->
    <router-link v-if="!isAuthPage" to="/movies">
      <button class="all-movies">All Movies</button>
    </router-link>

    <!-- Mostrar la barra de búsqueda solo si no estamos en páginas de registro o login -->
    <div v-if="!isAuthPage" class="search-bar">
      <input type="text" ref="searchInput" placeholder="Search for movies..." />
      <button @click="searchMovies">Go!</button>
    </div>

    <div class="auth-buttons">
      <!-- Mostrar el botón "Sign Up" solo si el usuario NO está autenticado -->
      <router-link v-if="!isAuthenticated" to="/register">
        <button class="sign-up">Sign Up</button>
      </router-link>

      <!-- Mostrar el botón "Login" solo si el usuario NO está autenticado -->
      <router-link v-if="!isAuthenticated" to="/login">
        <button class="login">Login</button>
      </router-link>

      <!-- Mostrar el botón "Logout" solo si el usuario está autenticado -->
      <button v-if="isAuthenticated" @click="logout" class="logout">Logout</button>
    </div>
  </header>
</template>

<script>
export default {
  name: 'HeaderPage',
  data() {
    return {
      scrolled: false, // Propiedad para controlar la opacidad
      isAuthenticated: !!localStorage.getItem('token'), // Estado de autenticación
    };
  },
  computed: {
    // Computada para verificar si estamos en las páginas de login o registro
    isAuthPage() {
      return this.$route.path === '/login' || this.$route.path === '/register';
    },
  },
  methods: {
    searchMovies() {
      const query = this.$refs.searchInput.value;
      console.log('Searching for:', query);
    },
    handleScroll() {
      // Cambia la propiedad "scrolled" dependiendo de si el scroll es mayor a 60px
      this.scrolled = window.scrollY > 60;
    },
    logout() {
      // Método para cerrar sesión
      localStorage.removeItem('token'); // Elimina el token del almacenamiento local
      this.isAuthenticated = false; // Actualiza el estado de autenticación
      this.$router.push('/'); // Redirigir a la página de inicio
    },
  },
  mounted() {
    // Agrega el evento de scroll cuando el componente se monta
    window.addEventListener('scroll', this.handleScroll);

    // Verificar el estado de autenticación al montar el componente
    this.isAuthenticated = !!localStorage.getItem('token');
  },
  beforeUnmount() {
    // Elimina el evento de scroll cuando el componente se desmonta
    window.removeEventListener('scroll', this.handleScroll);
  },
};
</script>



<style scoped>
.header {
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0));
  /* Degradado de arriba abajo */
  transition: background-color 0.3s ease;
  /* Transición suave */
  color: white;
  padding: 20px;
  /* Aumenta el padding para hacer el encabezado más alto */
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  height: 70px;
  /* Establece una altura fija si es necesario */
}

.header.scrolled {
  background-color: rgba(18, 18, 18, 0.9);
  /* Fondo completamente opaco cuando se desplaza */
}

.logo img {
  height: 80px;
  width: auto;
}

.search-bar {
  display: flex;
  align-items: center;
  flex-grow: 1;
  justify-content: center;
  margin: 0 20px;

}

.search-bar input {
  background-color: rgba(255, 255, 255, 0.3);
  color: white;
  padding: 10px;
  border: none;
  border-radius: 5px;
  width: 300px;
}

.search-bar input::placeholder {
  color: white;
  /* Cambia este color al que desees para el placeholder */
  opacity: 0.7;
  /* Opcional: Cambia la opacidad del placeholder */
}

.search-bar button {
  padding: 10px 15px;
  background-color: rgba(255, 255, 255, 0.3);
  color: white;
  border: none;
  border-radius: 5px;
  margin-left: 5px;
  cursor: pointer;
  margin-right: 240px;
}

.auth-buttons {
  display: flex;
  gap: 10px;
  /* Añade espacio entre los botones */
}

.sign-up,
.login,
.logout {
  padding: 10px 15px;
  background-color: rgba(255, 255, 255, 0.3);
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.sign-up:hover,
.login:hover,
.logout:hover {
  background-color: rgba(255, 255, 255, 0.4);
}

.all-movies {
  padding: 10px 15px;
  background-color: rgba(255, 255, 255, 0.3);
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-left: 150px;
  /* Añadir margen solo al botón */
}
</style>