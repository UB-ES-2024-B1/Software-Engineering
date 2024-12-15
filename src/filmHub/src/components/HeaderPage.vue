<template>
  <header :class="['header', { scrolled, opaque: isOpaque }]">
    <div class="logo">
      <router-link to="/">
        <img :src="require('@/assets/logo.png')" alt="Logo" />
      </router-link>
    </div>

    <!-- Mostrar el botón "All Movies" solo si no estamos en páginas de registro o login -->
    <router-link v-if="!isAuthPage" to="/movies/">
      <button class="all-movies">All Movies</button>
    </router-link>

    <!-- Mostrar la barra de búsqueda solo si no estamos en páginas de registro o login -->
    <div v-if="!isAuthPage" class="search-bar">
      <!-- Conectar el input al modelo de datos -->
      <input type="text" v-model="searchInput" placeholder="Search for movies..." @keyup.enter="searchMovies" />
      <!-- Enviar el término como parámetro de consulta -->
      <router-link v-if="!isAuthPage" :to="{ path: '/movies', query: { search: searchInput } }">
        <button @click="searchMovies">Go!</button> <!-- Método de búsqueda al hacer click -->
      </router-link>
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

      <div>
        <!-- Botón Premium que abre el modal -->
        <router-link v-if="isAuthenticated" to="#">
          <button class="Btn" 
          @click.prevent="openModal"
          :class="{'premium-button': isPremium}">
            <svg class="logoIcon" height="1em" viewBox="0 0 576 512" :class="{'gold-crown': isPremium}">
              <path d="M309 106c11.4-7 19-19.7 19-34c0-22.1-17.9-40-40-40s-40 17.9-40 40c0 14.4 7.6 27 19 34L209.7 220.6c-9.1 18.2-32.7 23.4-48.6 10.7L72 160c5-6.7 8-15 8-24c0-22.1-17.9-40-40-40S0 113.9 0 136s17.9 40 40 40c.2 0 .5 0 .7 0L86.4 427.4c5.5 30.4 32 52.6 63 52.6H426.6c30.9 0 57.4-22.1 63-52.6L535.3 176c.2 0 .5 0 .7 0c22.1 0 40-17.9 40-40s-17.9-40-40-40s-40 17.9-40 40c0 9 3 17.3 8 24l-89.1 71.3c-15.9 12.7-39.5 7.5-48.6-10.7L309 106z"></path>
            </svg>
            <span class="tooltip">Premium</span>
          </button> 
        </router-link>

        <!-- Modal de Upgrade (cuando el usuario no es Premium) -->
        <div v-if="isModalOpen && !isPremium" class="modal-overlay">
          <div class="modal-content">
            <h2>UPGRADE TO PREMIUM</h2>
            <ul class="no-bullet">
              <li>Unlock the ability to create and manage custom lists for your favorite movies!</li>
            </ul>
            <div class="modal-buttons">
              <button @click="confirmPremium">Upgrade</button>
              <button @click="closeModal">Cancel</button>
            </div>
          </div>
        </div>
        
        <!-- Modal de Downgrade (cuando el usuario es Premium) -->
        <div v-if="isModalOpen && isPremium" class="modal-overlay">
          <div class="modal-content">
            <h2>Premium Downgrade</h2>
            <p>Are you sure you want to downgrade your account from Premium?</p>
            <div class="modal-buttons">
              <button @click="confirmDowngrade">Downgrade</button>
              <button @click="closeModal">Cancel</button>
            </div>
          </div>
        </div>

        <!-- Modal de confirmación de upgrade (cuando el usuario pasa a ser Premium) -->
        <div v-if="isUpgradeModalOpen" class="modal-overlay">
          <div class="modal-content">
            <h2>Premium Upgrade</h2>
            <p>Your account has been successfully upgraded to Premium!</p>
            <div class="modal-buttons">
              <button class="ok-button" @click="closeUpgradeModal">Ok</button>
            </div>
          </div>
        </div>

        <!-- Modal de confirmación de downgrade (cuando el usuario ya es Premium y hace downgrade) -->
        <div v-if="isDowngradeModalOpen" class="modal-overlay">
          <div class="modal-content">
            <h2>Premium Downgrade</h2>
            <p>Your account has been successfully downgraded from Premium.</p>
            <div class="modal-buttons">
              <button class="ok-button" @click="closeDowngradeModal">Ok</button>
            </div>
          </div>
        </div>
      </div>
      
      
      

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
import axios from 'axios';

export default {
  name: 'HeaderPage',
  props: {
    isOpaque: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      searchInput: "",
      scrolled: false,
      isAuthenticated: !!localStorage.getItem('token'),
      isModalOpen: localStorage.getItem('isModalOpen') === 'true',
      isUpgradeModalOpen: localStorage.getItem('isUpgradeModalOpen') === 'true',
      isDowngradeModalOpen: localStorage.getItem('isDowngradeModalOpen') === 'true',
      isPremium: false, // Lo inicializamos a falso y lo actualizamos desde el backend
    };
  },
  computed: {
    isAuthPage() {
      return this.$route.path === '/login' || this.$route.path === '/register';
    },
    profileImage() {
      const storedImage = localStorage.getItem('userImg');
      if (storedImage === 'null' || storedImage === 'undefined') {
        return require('@/assets/foto_perfil.png');
      }
      return storedImage;
    },
  },
  methods: {
    async fetchUserData() {
      const userEmail = localStorage.getItem('userEmail');
      if (!userEmail) {
        console.error('Usuario no autenticado');
        return;
      }

      try {
        const response = await axios.get(`/users/email/${userEmail}`);
        if (response.status === 200) {
          const userData = response.data;
          this.isPremium = userData.is_premium; // Actualizamos el estado
        } else {
          console.error('Error al obtener los datos del usuario:', response.data);
        }
      } catch (error) {
        console.error('Error de red al obtener los datos del usuario:', error);
      }
    },
    searchMovies() {
      if (this.searchInput) {
        this.$router.push({ path: '/movies', query: { search: this.searchInput } });
        console.log('Searching for:', this.searchInput);
      }
    },
    handleScroll() {
      this.scrolled = window.scrollY > 60;
    },
    logout() {
      localStorage.removeItem('token');
      localStorage.removeItem('userEmail');
      localStorage.removeItem('userImg');
      localStorage.removeItem('userName');
      localStorage.removeItem('user_id');
      this.isAuthenticated = false;
      this.isPremium = false; // Restablecemos el estado
      window.dispatchEvent(new Event('storage'));
      this.$router.push('/');
    },
    openModal() {
      this.isModalOpen = true;
      localStorage.setItem('isModalOpen', 'true');
    },
    closeModal() {
      this.isModalOpen = false;
      localStorage.setItem('isModalOpen', 'false');
    },
    closeUpgradeModal() {
      this.isUpgradeModalOpen = false;
      localStorage.setItem('isUpgradeModalOpen', 'false');
    },
    closeDowngradeModal() {
      this.isDowngradeModalOpen = false;
      localStorage.setItem('isDowngradeModalOpen', 'false');
    },
    async confirmPremium() {
      const userEmail = localStorage.getItem('userEmail');
      if (!userEmail) {
        this.$router.push('/login');
        return;
      }

      try {
        const response = await axios.put(`/users/upgrade_premium/${userEmail}`);
        if (this.$route.name === 'UserProfile') {
          this.$router.go(); // Recarga solo si estás en UserProfile
        }
        if (response.status === 200) {
          this.isPremium = true;
          this.isUpgradeModalOpen = true;
          localStorage.setItem('isUpgradeModalOpen', 'true');
        } else {
          console.error('Error al actualizar a Premium:', response.data);
        }
      } catch (error) {
        console.error('Error de red:', error);
      }

      this.closeModal();
    },
    async confirmDowngrade() {
      const userEmail = localStorage.getItem('userEmail');
      if (!userEmail) {
        this.$router.push('/login');
        return;
      }

      try {
        const response = await axios.put(`/users/downgrade_premium/${userEmail}`);
        if (this.$route.name === 'UserProfile') {
          this.$router.go(); // Recarga solo si estás en UserProfile
        }
        if (response.status === 200) {
          this.isPremium = false;
          this.isDowngradeModalOpen = true;
          localStorage.setItem('isDowngradeModalOpen', 'true');
        } else {
          console.error('Error al cancelar Premium:', response.data);
        }
      } catch (error) {
        console.error('Error de red:', error);
      }

      this.closeModal();
    },
  },
  async mounted() {
    window.addEventListener('scroll', this.handleScroll);
    this.isAuthenticated = !!localStorage.getItem('token');

    if (this.isAuthenticated) {
      await this.fetchUserData(); // Obtenemos la información del usuario al montar
    }

    if (localStorage.getItem('isModalOpen') === 'true') {
      this.isModalOpen = true;
    }
    if (localStorage.getItem('isUpgradeModalOpen') === 'true') {
      this.isUpgradeModalOpen = true;
    }
    if (localStorage.getItem('isDowngradeModalOpen') === 'true') {
      this.isDowngradeModalOpen = true;
    }
  },
  beforeUnmount() {
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

.header.opaque {
  background-color: rgba(18, 18, 18, 1);
  /* Completamente opaco */
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
  margin-right: 180px;
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
.logout:hover,
.all-movies:hover {
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

.profile-image:hover {
  transform: scale(1.1);
  /* Aumenta el tamaño ligeramente al pasar el cursor */
  box-shadow: 0 0 5px rgba(255, 255, 255, 0.5);
  /* Añade un efecto de sombra */
}

.profile-image {
  width: 45px;
  height: 45px;
  border-radius: 50%;
  /* Hace que la imagen sea circular */
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  margin-right: 20px;
}




.Btn {
  width: 60px; /* Ancho mayor para mostrar la curva más notoria */
  height: 45px; /* Altura del botón */
  border: none;
  background: linear-gradient(-50deg, rgb(39, 107, 255), rgb(112, 186, 255), rgb(39, 107, 255));
  background-size: 250%;
  background-position: left;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition-duration: 0.5s;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.11);
  margin-right: 10px;

  border-radius: 25px  0 25px;

}


.logoIcon {
  fill: white;
}

.tooltip {
  position: absolute;
  bottom: -10px; 
  opacity: 0;
  background: linear-gradient(to right, rgb(39, 107, 255), rgb(108, 184, 255));
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition-duration: 0.2s;
  pointer-events: none;
  letter-spacing: 0.5px;
}


.tooltip::before {
  position: absolute;
  content: "";
  width: 10px;
  height: 10px;
  background: linear-gradient(45deg, rgb(39, 107, 255), rgb(108, 184, 255));
  background-size: 1000%;
  background-position: center;
  transform: rotate(45deg);
  top: -15%; 
  transition-duration: 0.3s;
}


.Btn:hover .tooltip {
  bottom: -30px; 
  opacity: 1;
  transition-duration: 0.3s;
  
}


.Btn:hover {
  background-position: right;
  transition-duration: .5s;
}



/* Overlay del modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

/* Contenido del modal */
.modal-content {
  background: #1c1c1c;
  color: #fff;
  padding: 20px;
  border-radius: 8px;
  max-width: 500px;
  width: 80%;
  text-align: center;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
}

/* Título y descripción */
.modal-content h2 {
  margin-bottom: 20px;
  font-size: 1.5rem;
  font-weight: bold;
}

.modal-content p {
  font-size: 1rem;
  margin-bottom: 20px;
  line-height: 1.5;
}

/* Botones */
.modal-buttons {
  display: flex;
  justify-content: center;
  gap: 250px;
  margin-top: 20px;
}

/* Botón Confirmar (Upgrade) */
.modal-buttons button:first-child {
  background-color: #28a745; /* Verde similar al de confirmación */
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.modal-buttons button:first-child:hover {
  background-color: #218838; /* Verde más oscuro al pasar el mouse */
}

/* Botón Cancelar */
.modal-buttons button:last-child {
  background-color: #dc3545; /* Rojo similar al de cancelación */
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.modal-buttons button:last-child:hover {
  background-color: #c82333; /* Rojo más oscuro al pasar el mouse */
}

/* Botón Ok (Modal de Confirmación) */
.modal-buttons button.ok-button {
  background-color: #007bff; /* Azul para el botón Ok */
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.modal-buttons button.ok-button:hover {
  background-color: #0056b3; /* Azul más oscuro al pasar el mouse */
}

/* Quitar el punto de la lista */
.no-bullet {
  list-style: none; /* Elimina los puntos */
  padding: 0;
  margin: 0;
}


.premium-button {
  border: 3px solid gold; /* Borde dorado */
  background-color: #f5c42d; /* Fondo dorado (opcional) */
  color: white; /* Color del texto */
  font-weight: bold; /* Texto en negrita */
  transition: all 0.3s ease; /* Efecto de transición */
}

.premium-button:hover {
  background-color: gold; /* Fondo dorado cuando pasa el mouse */
  color: black; /* Color de texto negro en hover */
}

.gold-crown {
  fill: gold; /* Cambia el color de la corona a dorado */
}

  

</style>
