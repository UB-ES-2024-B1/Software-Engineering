<template>
  <div class="profile-page">
    <HeaderPage />

    <div class="overlay"></div>

    <div class="main-content">
      <div class="profile-box">
        <h2 class="profile-title">Profile</h2>

        <p v-if="error" class="error-message">{{ error }}</p>

        <div v-else-if="userData" class="profile-content">
          <!-- Imagen de perfil -->
          <div class="profile-image">
            <img :src="require('@/assets/foto_perfil.png')" alt="Profile Picture" />
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
      <div class="movies-header">
        <button :class="{ active: showRatedMovies }" @click="toggleMovies('rated')">
          Rated Movies
        </button>
        <button :class="{ active: !showRatedMovies }" @click="toggleMovies('liked')">
          Liked Movies
        </button>
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

          <!-- User Rating (Nuevo contenedor) -->
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
        // Obtener la lista de películas liked y rated desde un solo endpoint
        axios
          .get(`${API_BASE_URL}/movies/liked_and_rated_list/${this.userData.id}`)
          .then((response) => {
            const likedMoviesTitles = response.data.liked_movies;
            const ratedMoviesList = response.data.rated_movies;

            // Obtener los detalles completos de las películas liked
            const likedMoviesDetails = likedMoviesTitles.map(async (movieTitle) => {
              const movieData = await this.fetchMovieDetails(movieTitle);
              return movieData ? generateMovieObject(movieData) : null;
            });

            // Obtener los detalles completos de las películas rated, incluyendo el userRating
            const ratedMoviesDetails = ratedMoviesList.map(async (movie) => {
              const movieData = await this.fetchMovieDetails(movie.title);
              return movieData
                ? generateMovieObject(movieData, movie.rating) // Pasamos el userRating
                : null;
            });

            // Esperamos que todas las promesas se resuelvan y almacenamos los resultados
            Promise.all([...likedMoviesDetails, ...ratedMoviesDetails]).then((allMovies) => {
              const allMovieDetails = allMovies.filter((movie) => movie !== null); // Filtramos los nulls (errores)
              this.likedMovies = allMovieDetails.filter((movie) =>
                likedMoviesTitles.includes(movie.title)
              );
              this.ratedMovies = allMovieDetails.filter((movie) =>
                ratedMoviesList.some((r) => r.title === movie.title)
              );

              // Determinamos cuál lista mostrar
              this.displayedMovies = this.showRatedMovies ? this.ratedMovies : this.likedMovies;
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
  height: 100vh;
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
  padding: 1rem;
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


.modify-btn {
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

.btns-div{
  position: absolute;
  display: flex;
  bottom: 2rem;
  right: 2rem;
  gap:1rem;
}

.modify-btn:hover, .add-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.email-div,
.username-div,
.password-div {
  margin-bottom: 20px;
}


/* Nueva sección de películas */
.movies-section {
  margin-top: 0px;
  padding-top: 20px;
  border-top: 2px solid #fff;
  background-color: #121212;
  width: 100%; /* Hacemos que ocupe el 100% del ancho */
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* Header para los botones de Rated y Liked */
.movies-header {
  display: flex;
  justify-content: center;
  gap: 20px; /* Espacio entre los botones */
  margin-bottom: 20px;
}

.movies-header button {
  padding: 12px 25px;
  border: none;
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
  cursor: pointer;
  font-weight: bold;
  transition: background 0.3s ease;
  border-radius: 5px; /* Bordes redondeados */
}

.movies-header button.active {
  background-color: rgba(255, 255, 255, 0.5);
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.3); /* Sombra para resaltar el botón activo */
}

/* Contenedor de la lista de películas */
.movies-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); /* Mínimo 200px por columna, ajustándose automáticamente */
  gap: 55px; /* Espacio entre las películas */
  width: 100%;
  max-width: 1200px; /* Máximo tamaño de contenedor */
  min-height: 375px; /* Máximo tamaño de contenedor */
  padding: 15px;
  box-sizing: border-box;
  background-color: rgb(0, 255, 255, 0.5);
}

/* Estilo para cada película */
.movies-list li {
  padding: 10px;
  color: white;
  background-color: rgba(0, 0, 0, 0.6);
  border-radius: 10px;
  text-align: center;
  transition: transform 0.3s ease;
}

.movies-list li:hover {
  transform: scale(1.05); /* Efecto hover */
}

/* Si las películas tienen imagenes, por ejemplo, les damos estilo */
.movies-list img {
  width: 100%;
  height: auto;
  border-radius: 5px;
  object-fit: cover; /* Para mantener la proporción de la imagen */
}


/* Estilo para cada película dentro de la lista */
.movie-item {
  width: 250px;
  /* Ajusta al tamaño deseado */
  height: 375px;
  /* Mantiene la proporción de la imagen */
  display: flex;
  flex-direction: column;
  /* Apila el contenido verticalmente */
  align-items: center;
  background-color: rgba(0, 0, 0, 0.2);
  /* Fondo oscuro semi-transparente */
  border-radius: 20px;
  transition: transform 0.3s ease-in-out;
  position: relative;
  /* Asegura que los elementos dentro se posicionen relativos a este */
}

.movie-item:hover {
  transform: scale(1.05);
  /* Aumenta ligeramente el tamaño al pasar el ratón */
}

/* Estilo para la imagen de la película */
.movie-poster {
  width: 100%;
  /* Asegúrate de que ocupen todo el ancho del contenedor */
  height: 375px !important;
  /* Mantiene la proporción de la imagen */
  border-radius: 20px !important;
  /* Bordes redondeados */
  opacity: 1;
}


.rating {
  display: flex;
  align-items: center;
  font-weight: bold;
  gap: 1px;
}

.likes {
  display: flex;
  align-items: center;
  font-weight: bold;
  gap: 1px;
}

.icon {
  width: 20px !important;
  /* Ajusta el tamaño según tus necesidades */
  height: 20px !important;
  margin-right: 5px;
  /* Espacio entre la imagen y el número */
}


.rating-likes-cover {
  position: absolute;
  top: 315px;
  left: 15px;
  background-color: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(10px);
  /* Fondo oscuro semi-transparente */
  color: white;
  padding: 10px;
  border-radius: 10px;
  display: flex;
  gap: 10px;
  /* Espacio entre los elementos */
  align-items: center;
  z-index: 5;
}

.user-rating {
  position: absolute;
  bottom: 315px;
  right: 15px;
  background-color: rgba(0, 255, 0, 0.3); /* Fondo verde claro */
  border: 1px solid green;
  border-radius: 4px;
  backdrop-filter: blur(5px);
  /* Fondo oscuro semi-transparente */
  color: white;
  padding: 10px;
  border-radius: 10px;
  display: flex;
  gap: 1px;
  /* Espacio entre los elementos */
  align-items: center;
  z-index: 5;
  /* Asegura que se muestre sobre otros elementos */
  font-weight: bold;
}



</style>