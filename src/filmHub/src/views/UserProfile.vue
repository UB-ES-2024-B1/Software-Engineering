<template>
  <div class="profile-page">
    <HeaderPage />

    <div class="overlay"></div>



    <div class="main-content">
      <div class="shadow-overlay"></div>
      <div class="profile-box">

        <p v-if="error" class="error-message">{{ error }}</p>

        <div v-else-if="userData" class="profile-content">
          <!-- Imagen de perfil -->
          <div class="profile-image">
            <img :src="userData.img_url || require('@/assets/foto_perfil.png')" alt="Profile Picture" />
          </div>

          <div class="profile-info">
            <div class="email-div">
              <strong>Email Address:</strong><br />
              <span>{{ userData.email }}</span>
            </div>
            <div class="username-div">
              <strong>Name:</strong><br />
              <span>{{ userData.full_name }}</span>
            </div>
            <!-- Mostrar la contraseña oculta -->
            <div class="password-div">
              <strong>Password:</strong><br />
              <span>********</span>
            </div>
          </div>

          <div class="btns-div">
            <router-link to="/addMovies">
              <button class="add-btn">Add Movies</button>
            </router-link>
            <router-link to="/edit">
              <button class="modify-btn">Modify</button>
            </router-link>
          </div>
        </div>

        <div v-else class="loading-message">
          Loading profile...
        </div>
      </div>
    </div>

    <!-- Sección de películas (liked o rated) -->
    <div class="movies-section">
      <!-- Nueva capa de overlay -->
      <div class="movies-overlay"></div>
    
      <div class="movies-header">
        <button :class="{ active: showRatedMovies }" @click="toggleMovies('rated')">
          Rated Movies
        </button>
<!--
        <button :class="{ active: showRatedMovies }" @click="toggleMovies('liked')">
          Favourite Movies
        </button>
        
-->        
      </div>
    
      <div class="movies-list">
        <!-- Lista de películas -->
        <div class="movie-item" v-for="movie in displayedMovies" :key="movie.title">
          <router-link :to="`/movie/${movie.id}`">
            <img :src="movie.smallImage" :alt="movie.title" class="movie-poster" />
          </router-link>
        
          <div class="rating-likes-cover">
            <!-- Rating -->
            <div class="rating">
              <img src="@/assets/star.png" alt="Rating" class="icon" />
              <span>{{ movie.rating.toFixed(1) }}</span>
            </div>
        
            <!-- Likes -->
            <div class="likes">
              <img src="@/assets/like.png" alt="Like" class="icon" />
              <span>{{ movie.likes }}</span>
            </div>
          </div>
    
          <!-- User Rating -->
          <div class="user-rating">
            <img src="@/assets/star.png" alt="Rating" class="icon" />
            <span>{{ movie.userRating }}</span>
          </div>
        </div>
      </div>      
    </div>
    

    <FooterComponent />
  </div>
</template>




<script>

  import HeaderPage from '@/components/HeaderPage.vue';
  import FooterComponent from '@/components/FooterComponent.vue';
  import axios from 'axios';
  import { API_BASE_URL } from '@/config.js'; // Asegúrate de tener la URL base aquí

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
    name: 'UserProfile',
    components: {
      HeaderPage,
      FooterComponent,
    },
    data() {
      return {
        userData: null,
        error: null,
        profile_image: '',
        showRatedMovies: true, // Controla si se muestran las valoradas o las con like
        ratedMovies: [], // Películas valoradas
        likedMovies: [], // Películas con like
        displayedMovies: [], // Películas que se muestran actualmente
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

          // Cargar las películas valoradas y con like desde un solo endpoint
          this.loadMovies();
        })
        .catch((error) => {
          console.error('Error al obtener los datos del usuario:', error);
          this.error = 'Error fetching user data. Please try again.';
        });
    },
    methods: {
      // Nueva función para obtener los detalles completos de una película usando el título
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
        axios
          .get(`${API_BASE_URL}/movies/liked_and_rated_list/${this.userData.id}`)
          .then((response) => {
            const likedMoviesTitles = response.data.liked_movies; // Títulos de las películas con like
            const ratedMoviesList = response.data.rated_movies; // Lista con {title, rating}

            // Obtener detalles completos de películas liked
            const likedMoviesDetails = Promise.all(
              likedMoviesTitles.map(async (movieTitle) => {
                const movieData = await this.fetchMovieDetails(movieTitle);
                return movieData ? generateMovieObject(movieData) : null;
              })
            );

            // Obtener detalles completos de películas rated
            const ratedMoviesDetails = Promise.all(
              ratedMoviesList.map(async (movie) => {
                const movieData = await this.fetchMovieDetails(movie.title);
                return movieData
                  ? generateMovieObject(movieData, movie.rating) // Incluimos el userRating
                  : null;
              })
            );

            // Esperamos a que ambas promesas terminen
            Promise.all([likedMoviesDetails, ratedMoviesDetails])
              .then(([likedMovies, ratedMovies]) => {
                // Filtramos nulls (errores) y asignamos a las listas respectivas
                this.likedMovies = likedMovies.filter((movie) => movie !== null);
                this.ratedMovies = ratedMovies.filter((movie) => movie !== null);

                // Aseguramos que una película valorada pueda estar también en la lista de liked
                const likedTitlesSet = new Set(this.likedMovies.map((movie) => movie.title));
                this.ratedMovies.forEach((movie) => {
                  if (likedTitlesSet.has(movie.title)) {
                    movie.isLiked = true; // Marcamos la película como liked
                  }
                });

                // Actualizamos la lista mostrada
                this.displayedMovies = this.showRatedMovies ? this.ratedMovies : this.likedMovies;
              })
              .catch((error) => {
                console.error('Error al procesar las películas liked y rated:', error);
              });
          })
          .catch((error) => {
            console.error('Error al obtener las películas liked y rated:', error);
          });
      },


      toggleMovies(type) {
        // Cambiar entre mostrar las películas "rated" o "liked"
        if (type === 'rated') {
          this.showRatedMovies = true;
        } else {
          this.showRatedMovies = false;
        }

        // Actualizar la lista mostrada
        this.displayedMovies = this.showRatedMovies ? this.ratedMovies : this.likedMovies;
      },
    },
    watch: {
      // Cuando cambie el estado de las películas, actualizamos la lista mostrada
      showRatedMovies(newVal) {
        this.displayedMovies = newVal ? this.ratedMovies : this.likedMovies;
      },
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
    position: relative;
    display: flex;
    flex-direction: column;
    background-color: rgba(0, 0, 0, 0.8);
    backdrop-filter: blur(5px);
    padding: 40px;
    border-radius: 10px;
    width: 750px;
    height: 350px;
    color: white;
    z-index: 20;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5); /* Mejora visual */
    border: 2px solid rgba(255, 255, 255, 0.1); /* Sutileza */
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
    padding-bottom: 0px;
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
    padding: 1rem;
    gap: 20px;
  }
  
  .profile-info p {
    margin-bottom: 60px;
    font-size: 18px;
    line-height: 1.5;
  }
  
  .profile-info strong {
    font-weight: bold;
    color: #ffffff;
  }
  
  .profile-info span {
    display: block;
    color: #dcdcdc;
    font-size: 16px;
  }
  
  /* Botones de acción */
  .modify-btn,
  .add-btn {
    width: 100%;
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
  
  .btns-div {
    position: absolute;
    display: flex;
    bottom: 2rem;
    right: 2rem;
    gap: 1rem;
  }
  
  .modify-btn:hover,
  .add-btn:hover {
    background: rgba(255, 255, 255, 0.3);
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
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-bottom: 20px;
    margin-top: 20px;
    z-index: 5;
  }
  
  .movies-header button {
    padding: 12px 25px;
    border: none;
    background:  rgba(255, 255, 255, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: white;
    cursor: pointer;
    font-weight: bold;
    transition: background-color 0.3s ease, box-shadow 0.3s ease;
    border-radius: 5px;
  }
  
  .movies-header button.active {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.6), rgba(255, 255, 255, 0.4));
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
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
    border-top-left-radius: 30px;
    z-index: 5;
  }
  
  .movie-item {
    width: 250px;
    height: 375px;
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
    width: 100%;
    height: 375px !important;
    border-radius: 20px !important;
    opacity: 1;
  }
  
  .rating-likes-cover {
    position: absolute;
    top: 315px;
    left: 15px;
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
    bottom: 315px;
    right: 15px;
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
  </style>
  