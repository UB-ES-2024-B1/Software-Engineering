<template>
  <div class="cinematic-profile">
    <HeaderPage />
    <!-- Hero Section -->
    <div class="hero">
      <img :src="require('@/assets/fondo_login.jpg')" alt="Favorite Movie Banner" class="hero-image" />
      <div class="hero-overlay"></div>
      <div class="hero-content">
        <h1>John Doe</h1>
        <p>Movie Enthusiast & Critic</p>
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <!-- Profile Summary -->
      <div class="profile-summary">
        <div class="user-info">
          <div class="avatar-container">
            <img :src="require('@/assets/profile-circle.svg?height=128&width=128')" alt="John Doe" class="avatar" />
            <span class="admin-badge">Admin</span>
          </div>
          <div class="user-details">
            <h2>@johndoe</h2>
            <p class="email">johndoe@example.com</p>
            <p class="stats">1,234 followers • 567 following</p>
          </div>
        </div>
        <div class="action-buttons">
          <button @click="toggleFollow" :class="['follow-button', { 'following': isFollowing }]">
            {{ isFollowing ? 'Unfollow' : 'Follow' }}
          </button>
          <button class="edit-button">
            <span class="icon">✎</span> Edit Profile
          </button>
        </div>
      </div>

      <!-- Search Bar -->
      <div class="search-container">
        <input type="text" placeholder="Search movies or users..." class="search-input" />
        <span class="search-icon">🔍</span>
      </div>

      <!-- Movie Collections -->
      <div class="movies-section">
        <!-- Nueva capa de overlay -->
        <div class="movies-overlay"></div>

        <!-- Encabezado con botones de tabs -->
        <div class="movies-header">
          <button :class="{ active: activeTab === 'rated' }" @click="toggleMovies('rated')">
            Rated Movies
          </button>

          <button :class="{ active: activeTab === 'liked' }" @click="toggleMovies('liked')">
            Favourite Movies
          </button>

          <button :class="{ active: activeTab === 'wishlist' }" @click="toggleMovies('wishlist')">
            Wishlist Movies
          </button>
        </div>

        <!-- Lista de películas -->
        <div class="movies-list">
          <div class="movie-item" v-for="movie in displayedMovies" :key="movie.id">
            <!-- Link al detalle de la película -->
            <router-link :to="`/movie/${movie.id}`">
              <img :src="movie.smallImage" :alt="movie.title" class="movie-poster" />
            </router-link>

            <!-- Rating y Likes -->
            <div class="rating-likes-cover">
              <div class="rating">
                <img src="@/assets/star.png" alt="Rating" class="icon" />
                <span>{{ movie.rating.toFixed(1) }}</span>
              </div>
              <div class="likes">
                <img src="@/assets/like.png" alt="Like" class="icon" />
                <span>{{ movie.likes }}</span>
              </div>
            </div>

            <!-- Rating del usuario si es Rated Movies -->
            <div v-if="activeTab === 'rated'" class="user-rating">
              <img src="@/assets/star.png" alt="Rating" class="icon" />
              <span>{{ movie.userRating }}</span>
            </div>

            <!-- Botón para eliminar película -->
            <button class="delete-button" @click="removeMovie(movie.id)">
              <svg class="delete-svgIcon" viewBox="0 0 448 512">
                <path
                  d="M135.2 17.7L128 32H32C14.3 32 0 46.3 0 64S14.3 96 32 96H416c17.7 0 32-14.3 32-32s-14.3-32-32-32H320l-7.2-14.3C307.4 6.8 296.3 0 284.2 0H163.8c-12.1 0-23.2 6.8-28.6 17.7zM416 128H32L53.2 467c1.6 25.3 22.6 45 47.9 45H346.9c25.3 0 46.3-19.7 47.9-45L416 128z">
                </path>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import HeaderPage from '@/components/HeaderPage.vue';
import axios from 'axios';
import { API_BASE_URL } from '@/config.js'; // Asegúrate de tener la URL base aquí
const isFollowing = ref(false)


const toggleFollow = () => {
  isFollowing.value = !isFollowing.value
}

</script>

<script>
function getImagePath(image) {
  if (image && image.startsWith('http')) {
    return image;
  } else if (image) {
    try {
      return require(`@/assets/${image}`);
    } catch (error) {
      console.error(`Error loading local image: ${image}`, error);
      return '';
    }
  } else {
    console.warn('No image provided');
    return '';

  }
}

async function generateMovieObject(movieData, userRating = null) {
  const movieObject = {
    id: movieData.id,
    image: getImagePath(movieData.image[1]),
    smallImage: getImagePath(movieData.image[0]),
    title: movieData.title,
    description: movieData.description,
    rating: movieData.rating,
    likes: movieData.likes,
    genre: movieData.genres.map((genre) => genre.type).join(', '),
    releaseDate: movieData.release_date.substring(0, 4),
    userRating: userRating, // Agregamos el rating del usuario, si existe
  };

  return movieObject;
}
export default {
  name: 'ViewProfile',
  components: {
    HeaderPage,

  },
  data() {
    return {
      activeTab: 'rated', // Tab activa
      showRatedMovies: true, // Controla si se muestran las valoradas o las con like
      showFavouriteMovies: false, // Controla la visualización de la lista de wishlist
      showWishlistMovies: false, // Controla la visualización de la lista de wishlist
      ratedMovies: [], // Películas valoradas
      likedMovies: [], // Películas con like
      wishedMovies: [], // Películas en la wishlist
      displayedMovies: [], // Películas que se muestran actualmente
      userData: null,
      error: null,
      profile_image: '',


      //REP eliminar
      showReportedModal: false,
      reportedComments: [],
    }
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

        // Cargar las películas valoradas y con like desde un solo endpoint
        this.loadMovies();
      })
      .catch((error) => {
        console.error('Error al obtener los datos del usuario:', error);
        this.error = 'Error fetching user data. Please try again.';
      });
  },
  methods: {

    async fetchMovieDetails(title) {
        try {
          const movieResponse = await axios.get(`${API_BASE_URL}/movies/title/${title}`);
          return movieResponse.data; // Devuelve los detalles completos de la película
        } catch (error) {
          console.error(`Error al obtener detalles de la película "${title}":`, error);
          return null; // Retorna null si hay un error
        }
      },
    loadMovies() {

      // Cargar las películas liked , rated y wished
      axios
        .get(`${API_BASE_URL}/movies/liked_list/${this.userData.id}`)
        .then((response) => {
          const likedMoviesTitles = response.data; // Listado de películas con like

          // Obtener detalles completos de las películas liked
          const likedMoviesDetails = Promise.all(
            likedMoviesTitles.map(async (movieTitle) => {
              const movieData = await this.fetchMovieDetails(movieTitle);
              return movieData ? generateMovieObject(movieData) : null;
            })
          );

          // Obtener las películas valoradas
          axios
            .get(`${API_BASE_URL}/movies/rated_list/${this.userData.id}`)
            .then((response) => {
              const ratedMoviesList = response.data;

              const ratedMoviesDetails = Promise.all(
                ratedMoviesList.map(async (movie) => {
                  const movieData = await this.fetchMovieDetails(movie.title);
                  return movieData
                    ? generateMovieObject(movieData, movie.rating)
                    : null;
                })
              );

              // Obtener las películas wishlist
              axios
                .get(`${API_BASE_URL}/movies/wished_list/${this.userData.id}`)
                .then((response) => {
                  const wishedMoviesList = response.data;

                  const wishedMoviesDetails = Promise.all(
                    wishedMoviesList.map(async (movieTitle) => {
                      const movieData = await this.fetchMovieDetails(movieTitle);
                      return movieData ? generateMovieObject(movieData) : null;
                    })
                  );

                  // Esperamos a que todas las promesas se resuelvan
                  Promise.all([likedMoviesDetails, ratedMoviesDetails, wishedMoviesDetails])
                    .then(([likedMovies, ratedMovies, wishedMovies]) => {
                      // Filtramos los valores nulos
                      this.likedMovies = likedMovies.filter((movie) => movie !== null);
                      this.ratedMovies = ratedMovies.filter((movie) => movie !== null);
                      this.wishedMovies = wishedMovies.filter((movie) => movie !== null);

                      // Ahora actualizamos la lista mostrada
                      this.displayedMovies = this.showRatedMovies
                        ? this.ratedMovies
                        : this.showFavouriteMovies
                          ? this.likedMovies
                          : this.wishedMovies;
                    })
                    .catch((error) => {
                      console.error('Error al procesar las películas wished:', error);
                    });
                })
                .catch((error) => {
                  console.error('Error al obtener las películas wished:', error);
                });
            })
            .catch((error) => {
              console.error('Error al obtener las películas rated:', error);
            });
        })
        .catch((error) => {
          console.error('Error al obtener las películas liked:', error);
        });
    },
    toggleMovies(type) {
      // Resetear todos los botones a false
      this.showRatedMovies = false;
      this.showFavouriteMovies = false;
      this.showWishlistMovies = false;

      // Activar el botón correspondiente según el tipo
      if (type === 'rated') {
        this.showRatedMovies = true;
        this.activeTab = 'rated';
      } else if (type === 'liked') {
        this.showFavouriteMovies = true;
        this.activeTab = 'liked';
      } else if (type === 'wishlist') {
        this.showWishlistMovies = true;
        this.activeTab = 'wishlist';
      }

      // Actualizar la lista mostrada inmediatamente después de cambiar el estado
      this.updateDisplayedMovies();
    },
    updateDisplayedMovies() {
      // Actualizar la lista de películas que se debe mostrar según el estado actual
      if (this.showRatedMovies) {
        this.displayedMovies = this.ratedMovies;
      } else if (this.showFavouriteMovies) {
        this.displayedMovies = this.likedMovies;
      } else if (this.showWishlistMovies) {
        this.displayedMovies = this.wishedMovies;
      }
    },


  },
  watch: {
      // Cuando cambie el estado de las películas, actualizamos la lista mostrada
      showRatedMovies() {
        this.updateDisplayedMovies();
      },
      showFavouriteMovies() {
        this.updateDisplayedMovies();
      },
      showWishlistMovies() {
        this.updateDisplayedMovies();
      }
    },

}
</script>

<style scoped>
.cinematic-profile {
  background-color: #000;
  color: #fff;
  font-family: Arial, sans-serif;
  min-height: 100vh;
}

.hero {
  position: relative;
  height: 50vh;
  overflow: hidden;
}

.hero-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0.5;

}

.hero-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, #000, transparent);
}

.hero-content {
  position: absolute;
  bottom: 0;
  left: 0;
  padding: 2rem;
}

.hero-content h1 {
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.hero-content p {
  font-size: 1.25rem;
  color: #ccc;
}

.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.profile-summary {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.user-info {
  display: flex;
  align-items: center;
}

.avatar-container {
  position: relative;
  margin-right: 1rem;
}

.avatar {
  width: 128px;
  height: 128px;
  border-radius: 50%;
  border: 4px solid #8b5cf6;
}

.admin-badge {
  position: absolute;
  bottom: 0;
  right: 0;
  background-color: #fbbf24;
  color: #000;
  font-size: 0.75rem;
  font-weight: bold;
  padding: 0.25rem 0.5rem;
  border-radius: 9999px;
}

.user-details h2 {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 0.25rem;
}

.email {
  color: #999;
  margin-bottom: 0.25rem;
}

.stats {
  font-size: 0.875rem;
  color: #ccc;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

.follow-button,
.edit-button {
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s;
}

.follow-button {
  background-color: #8b5cf6;
  color: #fff;
}

.follow-button.following {
  background-color: transparent;
  border: 1px solid #fff;
}

.edit-button {
  background-color: transparent;
  border: 1px solid #fff;
  color: #fff;
}

.search-container {
  position: relative;
  max-width: 600px;
  margin: 0 auto 2rem;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  border-radius: 9999px;
  background-color: #333;
  color: #fff;
  border: none;
  outline: none;
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #999;
}


.tab-button {
  background: none;
  border: none;
  color: #999;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  cursor: pointer;
  transition: color 0.3s;
}

.tab-button.active {
  color: #fff;
  border-bottom: 2px solid #8b5cf6;
}

.movie-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}

.movie-card {
  background-color: #222;
  border-radius: 0.5rem;
  overflow: hidden;
  transition: transform 0.3s;
}

.movie-card:hover {
  transform: scale(1.05);
}

.poster-container {
  position: relative;
  aspect-ratio: 2 / 3;
}

.movie-poster {
  width: 100%;
  height: 100%;
  object-fit: cover;
}


.movie-info {
  padding: 1rem;
}

.movie-info h3 {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.year {
  display: flex;
  align-items: center;
  color: #999;
  font-size: 0.875rem;
}

.icon {
  margin-right: 0.25rem;
}

.global-actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 2rem;
}

.action-button {
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s;
}

.add-movies {
  background-color: #8b5cf6;
  color: #fff;
}

.report {
  background-color: transparent;
  border: 1px solid #fff;
  color: #fff;
}

@media (max-width: 768px) {
  .profile-summary {
    flex-direction: column;
    align-items: flex-start;
  }

  .action-buttons {
    margin-top: 1rem;
  }

  .movie-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  }
}

/* Nueva sección de películas */
.movies-section {
    margin-top: 0px;
    padding-top: 20px;
    background-color: #121212;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
    z-index: 10;
  }
  
  .movies-header {
    position: absolute;
    top: px; /* 20px desde la parte superior */
    right: 363px; /* 20px desde la izquierda */
    display: flex; /* Los botones en fila */
    margin: 0 auto;
    position: relative;
    margin-top: 20px;
    z-index: 5;

}

/* Estilo base de los botones */
.movies-header button {
  padding: 10px 20px;
  background: rgba(255, 255, 255, 0.2); /* Fondo inicial transparente */
  color: white; /* Texto blanco por defecto */
  border: none;
  border-top-left-radius: 12px;
  border-top-right-radius: 12px;
  border-bottom: 2px solid transparent;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s ease; /* Suavizar transiciones */
  margin-right: 2px; /* Separación entre botones */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Sombra sutil */
}

/* El último botón no tiene margen derecho */
.movies-header button:last-child {
  margin-right: 0;
}

/* Estilo para el botón activo */
.movies-header button.active {
  background: #8b05da; /* Azul más fuerte para el fondo */
  color: white; /* Texto blanco para mejor contraste */
  border-bottom: none;
  position: relative;
  z-index: 10; /* Asegura que el botón activo se quede encima de los demás */
  box-shadow: 0 0 20px rgba(165, 4, 206, 0.8), 0 0 15px rgba(0, 0, 0, 0.3); /* Sombra azulada */
  transform: translateY(-4px); /* Eleva el botón ligeramente */
  text-shadow: 0 0 10px rgba(175, 7, 218, 0.8), 0 0 20px rgba(152, 18, 214, 0.8), 0 0 40px rgb(153, 7, 221); /* Resplandor azul */
}

/* Efecto hover */
.movies-header button:hover {
  background: #6fa3e0; /* Azul más claro cuando se pasa el ratón */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Sombra más intensa para el hover */
  transform: translateY(-2px); /* Eleva el botón al pasar el ratón */
}

/* Agregar un enfoque visual más fuerte al pasar el ratón sobre el botón activo */
.movies-header button.active:hover {
  background: #3879c0; /* Azul aún más oscuro para hover cuando está activo */
  box-shadow: 0 0 30px rgba(74, 144, 226, 1), 0 0 40px rgba(0, 0, 0, 0.4); /* Brillo más fuerte */
  transform: translateY(-6px); /* Aumenta el efecto de elevación */
  text-shadow: 0 0 15px rgba(74, 144, 226, 1), 0 0 30px rgba(74, 144, 226, 1), 0 0 50px rgba(74, 144, 226, 1); /* Brillo azul más intenso */
}



  
  /* Contenedor de la lista de películas */
  .movies-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 55px;
    width: 100%;
    max-width: 1200px;
    min-height: 375px;
    padding: 15px;
    box-sizing: border-box;
    background:rgba(255, 255, 255, 0.2);
    border-top-right-radius: 30px;
    z-index: 5;
  }
  
  .movie-item {
    position: relative; 
    width: 250px;
    height: 350px;
    display: flex;
    flex-direction: column;
    align-items: center;
    border-radius: 20px;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
    position: relative;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  }
  
  .movie-item:hover {
    transform: scale(1.05);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.5);
  }
  
  .movie-poster {
    width: 250px !important;
    height: 350px !important;
    border-radius: 20px !important;
    opacity: 1;
  }
  
  .rating-likes-cover {
    position: absolute;
    top: 295px;
    left: 10px;
    background-color: rgba(0, 0, 0, 0.4);
    backdrop-filter: blur(10px);
    color: white;
    padding: 10px;
    border-radius: 10px;
    display: flex;
    gap: 10px;
    align-items: center;
    z-index: 5;
  }
  
  .user-rating {
    position: absolute;
    bottom: 295px;
    left: 10px;
    background-color: rgba(0, 255, 0, 0.3);
    border: 1px solid green;
    backdrop-filter: blur(5px);
    color: white;
    padding: 10px;
    border-radius: 10px;
    display: flex;
    gap: 1px;
    align-items: center;
    z-index: 5;
    font-weight: bold;
  }

  .icon {
    width: 20px !important;
    /* Ajusta el tamaño según tus necesidades */
    height: 20px !important;
    margin-right: 5px;
    /* Espacio entre la imagen y el número */
  }
  
  /* Media Queries */
  @media (max-width: 768px) {
    .profile-box {
      width: 90%;
      height: auto;
      padding: 20px;
    }
  
    .profile-content {
      flex-direction: column;
      align-items: center;
      text-align: center;
    }
  
    .profile-image img {
      width: 120px;
      height: 120px;
    }
  
    .btns-div {
      flex-direction: column;
      gap: 10px;
      bottom: 1rem;
    }
  
    .movies-list {
      grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
      gap: 20px;
    }
  
    .movie-item {
      width: 150px;
      height: 225px;
    }
  
    .movie-poster {
      height: 225px !important;
    }
  
    .rating-likes-cover {
      top: 180px;
      padding: 5px;
      font-size: 12px;
    }
  
    .user-rating {
      bottom: 180px;
      padding: 5px;
      font-size: 12px;
    }
  }
  
  @media (max-width: 480px) {
    .profile-box {
      padding: 10px;
    }
  
    .movies-header button {
      padding: 8px 15px;
      font-size: 12px;
    }
  
    .movie-item {
      width: 120px;
      height: 180px;
    }
  
    .movie-poster {
      height: 180px !important;
    }
  }



.delete-button {
  position: absolute;
  bottom: 290px;
  right: 15px;
  min-width: 40px;
  min-height: 40px;
  width: 40px;
  height: 40px;
  margin-bottom: 10px;
  border-radius: 50%;
  background-color: rgb(20, 20, 20, 0.8);
  backdrop-filter: blur(10px);
  border: none;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.164);
  cursor: pointer;
  transition-duration: 0.3s;
  overflow: hidden;
}

.delete-svgIcon {
  width: 15px;
  transition-duration: 0.3s;
}

.delete-svgIcon path {
  fill: white;
}

.delete-button:hover {
  width: 90px;
  border-radius: 50px;
  transition-duration: 0.3s;
  background-color: rgb(255, 69, 69);
  align-items: center;
}

.delete-button:hover .delete-svgIcon {
  width: 20px;
  transition-duration: 0.3s;
  transform: translateY(60%);
  -webkit-transform: rotate(360deg);
  -moz-transform: rotate(360deg);
  -o-transform: rotate(360deg);
  -ms-transform: rotate(360deg);
  transform: rotate(360deg);
}

.delete-button::before {
  display: none;
  content: "Delete";
  color: white;
  transition-duration: 0.3s;
  font-size: 2px;
}

.delete-button:hover::before {
  display: block;
  padding-right: 10px;
  font-size: 13px;
  opacity: 1;
  transform: translateY(0px);
  transition-duration: 0.3s;
}
</style>