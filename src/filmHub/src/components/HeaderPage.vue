<template>
  <header :class="['header', { scrolled, opaque: isOpaque }]">
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
      <!-- Conectar el input al modelo de datos -->
      <input type="text" v-model="searchInput" placeholder="Search for movies..." />
      <!-- Enviar el término como parámetro de consulta -->
      <router-link v-if="!isAuthPage" :to="{ path: '/movies', query: { search: searchInput } }">
        <button>Go!</button>
      </router-link>
    </div>
    <div class="auth-buttons">
      <!-- Mostrar el botón "Sign Up" solo si el usuario NO está autenticado y no estamos en la página de registro -->
      <router-link v-if="!isAuthenticated && $route.path !== '/register'" to="/register">
        <button class="sign-up">Sign Up</button>
      </router-link>

      <!-- Mostrar el botón "Login" solo si el usuario NO está autenticado y no estamos en la página de login -->
      <router-link v-if="!isAuthenticated && $route.path !== '/login'" to="/login">
        <button class="login">Login</button>
      </router-link>

      <!-- Mostrar el botón "Profile" solo si el usuario está autenticado y no estamos en la página de perfil -->
      <router-link v-if="isAuthenticated && $route.path !== '/profile' && $route.path !== '/edit'" to="/profile">
        <img class="profile-image" :src="profileImage" alt="Profile" />
      </router-link>

      <!-- Mostrar el botón "Logout" solo si el usuario está autenticado -->
      <button v-if="isAuthenticated" @click="logout" class="logout">Logout</button>

    </div>
  </header>
</template>

<script>
export default {
  name: 'HeaderPage',
  props: {
    isOpaque: {
      type: Boolean,
      default: false, // Por defecto, el header será transparente
    },
  },
  data() {
    return {
      searchInput: "",
      scrolled: false, // Propiedad para controlar la opacidad
      isAuthenticated: !!localStorage.getItem('token'), // Estado de autenticación
      profileImage: require('@/assets/foto_perfil.png')
    };
  },
  computed: {
    isAuthPage() {
      return this.$route.path === '/login' || this.$route.path === '/register';
    },
  },
  methods: {  
    handleScroll() {
      this.scrolled = window.scrollY > 60;
    },
    logout() {
      // Elimina el token del almacenamiento local
      localStorage.removeItem('token');
      this.isAuthenticated = false; // Actualiza el estado de autenticación
      // Redirige al inicio para forzar una actualización de la vista
      this.$router.push('/');
    },
  },
  mounted() {
    window.addEventListener('scroll', this.handleScroll);
    this.isAuthenticated = !!localStorage.getItem('token');
  },
  beforeUnmount() {
    window.removeEventListener('scroll', this.handleScroll);
  },
};
</script>

<style scoped>
.header {
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0));
  transition: background-color 0.3s ease;
  color: white;
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  height: 70px;
}

.header.scrolled {
  background-color: rgba(18, 18, 18, 0.9);
}
.header.opaque {
  background-color: rgba(18, 18, 18, 1); /* Completamente opaco */
}

.logo img {
  height: 80px;
  width: auto;
}

.auth-buttons {
  display: flex;
  gap: 10px;
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

.profile-image {
  width: 45px;
  height: 45px;
  border-radius: 50%; /* Hace que la imagen sea circular */
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  margin-right: 20px;
}

.profile-image:hover {
  transform: scale(1.1); /* Aumenta el tamaño ligeramente al pasar el cursor */
  box-shadow: 0 0 5px rgba(255, 255, 255, 0.5); /* Añade un efecto de sombra */
}

.sign-up:hover,
.login:hover,
.logout:hover,
.all-movies:hover {
  background-color: rgba(255, 255, 255, 0.4);
}
</style>
