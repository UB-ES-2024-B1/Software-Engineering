<template>
  <div class="home-page">
    <HeaderPage /> <!-- Componente HeaderPage -->

    <!-- Banner -->
    <section class="banner" v-if="bannerMovie">
      <div class="carousel-inner">
        <img :src="bannerMovie.image" class="d-block w-100 carousel-image" alt="Movie poster" />
        <div class="shadow-overlay"></div>

        <div class="small-cover">
          <img :src="bannerMovie.smallImage" alt="Movie Small Cover" class="small-cover-image" />
          <div class="movie-info">
            <h4>{{ bannerMovie.title }}</h4>
            <div class="info-item">
              <span class="info-title">Genres: </span> <span>{{ bannerMovie.genres.join(", ") }}</span>
            </div>
            <div class="info-item">
              <span class="info-title">Date: </span> <span>{{ bannerMovie.release_date }}</span>
            </div>
            <div class="info-item">
              <span class="info-title">Country: </span> <span>{{ bannerMovie.country }}</span>
            </div>
            <div class="rating-likes-banner">
              <div class="rating">
                <img src="@/assets/star.png" alt="Star" class="icon" />
                <span>{{ bannerMovie.rating }}</span>
              </div>
              <div class="likes">
                <img src="@/assets/like.png" alt="Like" class="icon" />
                <span>{{ bannerMovie.likes }}</span>
              </div>
            </div>
          </div>
        </div>


        <!-- Aquí agregamos las estrellas de votación -->
        <div class="star-rating-container">
          <div class="radio">
            <!-- Estrellas para la valoración -->
            <input 
              value="5" 
              name="rating" 
              type="radio" 
              id="rating-5" 
              :checked="rating === 5"
              @click="saveRating(5)" />
            <label title="5 star" for="rating-5">
              <svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 576 512">
                <path d="M316.9 18C311.6 7 300.4 0 288.1 0s-23.4 7-28.8 18L195 150.3 51.4 171.5c-12 1.8-22 10.2-25.7 21.7s-.7 24.2 7.9 32.7L137.8 329 113.2 474.7c-2 12 3 24.2 12.9 31.3s23 8 33.8 2.3l128.3-68.5 128.3 68.5c10.8 5.7 23.9 4.9 33.8-2.3s14.9-19.3 12.9-31.3L438.5 329 542.7 225.9c8.6-8.5 11.7-21.2 7.9-32.7s-13.7-19.9-25.7-21.7L381.2 150.3 316.9 18z"></path>
              </svg>
            </label>
      
            <input 
              value="4" 
              name="rating" 
              type="radio" 
              id="rating-4" 
              :checked="rating === 4"
              @click="saveRating(4)" />
            <label title="4 stars" for="rating-4">
              <svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 576 512">
                <path d="M316.9 18C311.6 7 300.4 0 288.1 0s-23.4 7-28.8 18L195 150.3 51.4 171.5c-12 1.8-22 10.2-25.7 21.7s-.7 24.2 7.9 32.7L137.8 329 113.2 474.7c-2 12 3 24.2 12.9 31.3s23 8 33.8 2.3l128.3-68.5 128.3 68.5c10.8 5.7 23.9 4.9 33.8-2.3s14.9-19.3 12.9-31.3L438.5 329 542.7 225.9c8.6-8.5 11.7-21.2 7.9-32.7s-13.7-19.9-25.7-21.7L381.2 150.3 316.9 18z"></path>
              </svg>
            </label>
      
            <input 
              value="3" 
              name="rating" 
              type="radio" 
              id="rating-3" 
              :checked="rating === 3"
              @click="saveRating(3)" />
            <label title="3 stars" for="rating-3">
              <svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 576 512">
                <path d="M316.9 18C311.6 7 300.4 0 288.1 0s-23.4 7-28.8 18L195 150.3 51.4 171.5c-12 1.8-22 10.2-25.7 21.7s-.7 24.2 7.9 32.7L137.8 329 113.2 474.7c-2 12 3 24.2 12.9 31.3s23 8 33.8 2.3l128.3-68.5 128.3 68.5c10.8 5.7 23.9 4.9 33.8-2.3s14.9-19.3 12.9-31.3L438.5 329 542.7 225.9c8.6-8.5 11.7-21.2 7.9-32.7s-13.7-19.9-25.7-21.7L381.2 150.3 316.9 18z"></path>
              </svg>
            </label>
      
            <input 
              value="2" 
              name="rating" 
              type="radio" 
              id="rating-2" 
              :checked="rating === 2"
              @click="saveRating(2)" />
            <label title="2 stars" for="rating-2">
              <svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 576 512">
                <path d="M316.9 18C311.6 7 300.4 0 288.1 0s-23.4 7-28.8 18L195 150.3 51.4 171.5c-12 1.8-22 10.2-25.7 21.7s-.7 24.2 7.9 32.7L137.8 329 113.2 474.7c-2 12 3 24.2 12.9 31.3s23 8 33.8 2.3l128.3-68.5 128.3 68.5c10.8 5.7 23.9 4.9 33.8-2.3s14.9-19.3 12.9-31.3L438.5 329 542.7 225.9c8.6-8.5 11.7-21.2 7.9-32.7s-13.7-19.9-25.7-21.7L381.2 150.3 316.9 18z"></path>
              </svg>
            </label>
      
            <input 
              value="1" 
              name="rating" 
              type="radio" 
              id="rating-1" 
              :checked="rating === 1"
              @click="saveRating(1)" />
            <label title="1 star" for="rating-1">
              <svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 576 512">
                <path d="M316.9 18C311.6 7 300.4 0 288.1 0s-23.4 7-28.8 18L195 150.3 51.4 171.5c-12 1.8-22 10.2-25.7 21.7s-.7 24.2 7.9 32.7L137.8 329 113.2 474.7c-2 12 3 24.2 12.9 31.3s23 8 33.8 2.3l128.3-68.5 128.3 68.5c10.8 5.7 23.9 4.9 33.8-2.3s14.9-19.3 12.9-31.3L438.5 329 542.7 225.9c8.6-8.5 11.7-21.2 7.9-32.7s-13.7-19.9-25.7-21.7L381.2 150.3 316.9 18z"></path>
              </svg>
            </label>
          </div>
        </div>

        <!-- Like -->
        <div class="like-container">
          <label class="container">
            <!-- Checkbox para manejar el like -->
            <input 
              type="checkbox" 
              id="like-toggle" 
              :checked="likedMovies.includes(bannerMovie.title)"  
              @change="toggleLike(bannerMovie.id, !$event.target.checked)" 
            />
            <div class="checkmark">
              <svg viewBox="0 0 256 256">
                <rect fill="none" height="256" width="256"></rect>
                <path 
                  id="heart-path" 
                  :stroke="likedMovies.includes(bannerMovie.title) ? 'red' : '#000'"  
                  d="M224.6,51.9a59.5,59.5,0,0,0-43-19.9,60.5,60.5,0,0,0-44,17.6L128,59.1l-7.5-7.4C97.2,28.3,59.2,26.3,35.9,47.4a59.9,59.9,0,0,0-2.3,87l83.1,83.1a15.9,15.9,0,0,0,22.6,0l81-81C243.7,113.2,245.6,75.2,224.6,51.9Z" 
                  stroke-width="20px" 
                  fill="none">
                </path>
              </svg>
            </div>
          </label>
        </div>


      </div>
    </section>


    <!-- Nueva zona de detalles de la película -->
    <section class="movie-details" v-if="bannerMovie">
      <div class="details-grid" style="background-color: #121212; padding: 30px; color: white;">
        <div class="detail-item">
          <h4>Description</h4>
          <p>{{ bannerMovie.description }}</p>
        </div>
      </div>
    </section>

    <section class="cast-section" v-if="bannerMovie">

      <div class="details-grid">

        <h4 class="section-title">Cast & Crew</h4>
        <div class="cards-container">
          <!-- Card for Director (Always visible as the first item) -->
          <div class="detail-card">
            <h4>Director</h4>
            <p>{{ bannerMovie.director }}</p>
          </div>

          <!-- Cards for Cast, excluding the director -->
          <div v-for="(actor, index) in bannerMovie.cast" :key="actor" class="detail-card"
            v-show="index < visibleCount">
            <h4>Actor</h4>
            <p>{{ actor }}</p>
          </div>
        </div>
        <!-- See More Button -->
        <div class="see-more-btn" v-if="bannerMovie.cast.length > 10">
          <button @click="toggleSeeMore">
            {{ showAll ? 'See Less' : 'See More' }}
            <i :class="showAll ? 'bx bx-chevron-up' : 'bx bx-chevron-down'"></i>
          </button>


        </div>
      </div>
    </section>
    <div class="trailer-title">
      <h4 class="section-title">Trailer</h4>
    </div>
    <!-- Reproductor de video -->
    <section class="video-section">

      <div v-if="bannerMovie" class="banner-video">

        <!-- Video or Image -->
        <div class="media-container">
          <VideoPlayer v-if="bannerMovie.trailer" :videoUrl="bannerMovie.trailer" />
          <img v-else :src="bannerMovie.image" :alt="bannerMovie.title" class="banner-image" />
        </div>
      </div>
    </section>

    <!-- Sección de películas relacionadas -->
    <section class="top-rated-movies">
      <h4 class="section-title" id="related-movies">Related Movies</h4>
      <div id="topRatedMoviesCarousel" class="carousel slide" data-bs-ride="carousel">
        <div class="carousel-inner">
          <!-- Primer bloque: películas 0-4 -->
          <div class="carousel-item active">
            <div class="movie-grid responsive-carousel">
              <div class="movie-item" v-for="movie in relatedMovies.slice(0, 5)" :key="movie.id">
                <router-link :to="`/movie/${movie.id}`">
                  <img :src="movie.image" :alt="movie.title" class="movie-poster" />
                </router-link>

                <div class="rating-likes-cover">
                  <div class="rating">
                    <img src="@/assets/star.png" alt="Star" class="icon" />
                    <span>{{ movie.rating }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <!-- Segundo bloque: películas 5-9 -->
          <div class="carousel-item">
            <div class="movie-grid responsive-carousel">
              <div class="movie-item" v-for="movie in relatedMovies.slice(5, 10)" :key="movie.id">
                <router-link :to="`/movie/${movie.id}`">
                  <img :src="movie.image" :alt="movie.title" class="movie-poster" />
                </router-link>
                <div class="rating-likes-cover">
                  <div class="rating">
                    <img src="@/assets/star.png" alt="Star" class="icon" />
                    <span>{{ movie.rating }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <!-- Tercer bloque: películas 10-14 -->
          <div class="carousel-item">
            <div class="movie-grid responsive-carousel">
              <div class="movie-item" v-for="movie in relatedMovies.slice(10, 15)" :key="movie.id">
                <router-link :to="`/movie/${movie.id}`">
                  <img :src="movie.image" :alt="movie.title" class="movie-poster" />
                </router-link>
                <div class="rating-likes-cover">
                  <div class="rating">
                    <img src="@/assets/star.png" alt="Star" class="icon" />
                    <span>{{ movie.rating }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <!-- Cuarto bloque: películas 15-19 -->
          <div class="carousel-item">
            <div class="movie-grid responsive-carousel">
              <div class="movie-item" v-for="movie in relatedMovies.slice(15, 20)" :key="movie.id">
                <router-link :to="`/movie/${movie.id}`">
                  <img :src="movie.image" :alt="movie.title" class="movie-poster" />
                </router-link>
                <div class="rating-likes-cover">
                  <div class="rating">
                    <img src="@/assets/star.png" alt="Star" class="icon" />
                    <span>{{ movie.rating }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- Controles del carrusel -->
        <button class="carousel-control-prev" type="button" data-bs-target="#topRatedMoviesCarousel"
          data-bs-slide="prev">
          <span class="carousel-control-prev-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Previous</span>
        </button>
        <button class="carousel-control-next" type="button" data-bs-target="#topRatedMoviesCarousel"
          data-bs-slide="next">
          <span class="carousel-control-next-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Next</span>
        </button>
      </div>
    </section>


    <FooterComponent />
  </div>
</template>

<script>
  import HeaderPage from '@/components/HeaderPage.vue';
  import axios from 'axios';
  import { API_BASE_URL } from '@/config.js';
  import FooterComponent from '@/components/FooterComponent.vue';
  import VideoPlayer from "@/components/VideoPlayer.vue";

  export default {
    name: 'MovieDetails',
    components: {
      HeaderPage,
      FooterComponent,
      VideoPlayer,
    },
    data() {
      return {
        bannerMovie: null, // Película del banner
        movies: [], // Lista de películas ordenadas
        relatedMovies: [], // Lista de películas relacionadas
        genresList: [], // Lista de géneros disponibles
        visibleCount: 9, // Inicialmente mostrar hasta 9 elementos
        showAll: false, // Para alternar entre mostrar todos los elementos o no
        userId: localStorage.getItem('user_id'), // ID del usuario
        rating: 0, // Valoración inicial
        userRatedMovies: {}, // Almacenará las películas valoradas por el usuario
        likedMovies: [] // Almacena las películas que el usuario ha marcado como "like"
      };
    },
    computed: {
      combinedCast() {
        return [this.bannerMovie.director, ...this.bannerMovie.cast];
      },
    },
    methods: {
      toggleSeeMore() {
        if (this.showAll) {
          this.visibleCount = 9; // Mostrar solo 9 (director + 2 filas de actores)
        } else {
          this.visibleCount = this.combinedCast.length; // Mostrar todos los elementos
        }
        this.showAll = !this.showAll;
      },
      async fetchTitle(title) {
        try {
          const response = await axios.get(`${API_BASE_URL}/movies/title/${title}`);
          this.bannerMovie = await generateMovieObject(response.data);
        } catch (error) {
          console.error('Error retrieving banner movie:', error);
        }
      },
      async fetchBannerMovie(id) {
        try {
          const response = await axios.get(`${API_BASE_URL}/movies/${id}`);
          this.bannerMovie = await generateMovieObject(response.data);
        } catch (error) {
          console.error('Error retrieving banner movie:', error);
        }
      },
      async fetchMovies(start, end, movies_section, movieTitle) {
        try {
          const encodedTitle = encodeURIComponent(movieTitle);
          const url = `${API_BASE_URL}/movies/sorted/related_movies/${encodedTitle}`;
          const movieObjects = [];
          const response = await axios.get(url);

          if (!response.data || response.data.length === 0) {
            console.log('No related movies found.');
            return;
          }

          const movies = response.data.slice(start, end);

          for (const movieData of movies) {
            const movieObject = movies_section === 1
              ? await generateMovieObject(movieData)
              : await generateRecentMovieObject(movieData);
            movieObjects.push(movieObject);
          }

          if (movies_section === 1) {
            this.movies = movieObjects;
          } else {
            this.relatedMovies = movieObjects;
          }
        } catch (error) {
          console.error('Error retrieving related movies:', error);
        }
      },
      async loadMovieData(movieId) {
        try {
          await this.fetchBannerMovie(movieId); // Cargar la película del banner
          if (this.bannerMovie) {
            const movieTitle = this.bannerMovie.title;
            console.log('Movie title to fetch related movies:', movieTitle);
            await this.fetchMovies(0, 50, 2, movieTitle); // Cargar películas relacionadas

            // Si la película actual está valorada, actualiza `this.rating`..
            if (this.userRatedMovies && this.userRatedMovies[this.bannerMovie.title]) {
              this.rating = this.userRatedMovies[this.bannerMovie.title];
            } else {
              // Si no está valorada, reinicia `this.rating` a 0
              this.rating = 0;
            }

            this.scrollToTop();
          }
        } catch (error) {
          console.error('Error loading movie data:', error);
        }
      },

      async saveRating(rating) {
        try {
          if (!this.userId) { // Verifica si el userId está disponible
            alert('Debes iniciar sesión para puntuar una película.'); // Muestra advertencia
            this.$router.push('/login');
            return; // Salir del método
          }
          const endpoint = `${API_BASE_URL}/movies/rate/${this.bannerMovie.id}/${this.userId}/${rating}`;
          const response = await axios.post(endpoint);
          if (response.status === 200) {
            console.log('Rating saved successfully.');
            this.rating = rating; // Actualizamos el estado local de la valoración

            // Actualizar el estado de las películas valoradas
            if (!this.userRatedMovies) {
              this.userRatedMovies = {}; // Asegurarse de que exista el objeto
            }
            this.userRatedMovies[this.bannerMovie.title] = rating; // Actualizamos localmente
          }
        } catch (error) {
          console.error('Error saving rating:', error);
        }
      },

      async toggleLike(movieId) {
        try {
          if (!this.userId) {
            console.error('User ID not found.');
            return;
          }

          // Verificar si la película ya está en likedMovies
          const isLiked = this.likedMovies.includes(this.bannerMovie.title);

          // Elegir el endpoint basado en el estado actual
          const endpoint = isLiked
            ? `${API_BASE_URL}/movies/dislike/${movieId}/${this.userId}`
            : `${API_BASE_URL}/movies/like/${movieId}/${this.userId}`;

          const response = await axios.post(endpoint);

          if (response.status === 200) {
            console.log(isLiked ? 'Movie disliked successfully.' : 'Movie liked successfully.');

            // Actualizar el estado local de likedMovies
            if (isLiked) {
              this.likedMovies = this.likedMovies.filter(title => title !== this.bannerMovie.title);
            } else {
              this.likedMovies.push(this.bannerMovie.title);
            }

            // Añadir un pequeño retraso antes de guardar la puntuación
            // Esto asegura que el like se haya procesado antes de puntuar
            setTimeout(() => {
              if (this.rating > 0) {
                this.saveRating(this.rating); // Guardar rating solo si existe uno
              }
            }, 500); // Retraso de 500ms (ajustar si es necesario)
          }
        } catch (error) {
          console.error('Error toggling like:', error.response?.data || error.message);
        }
      },

      async loadUserPreferences() {
        try {
          if (!this.userId) {
            console.error('User ID not found.');
            return;
          }
          const endpoint = `${API_BASE_URL}/movies/liked_and_rated_list/${this.userId}`;
          const response = await axios.get(endpoint);

          const data = response.data;

          // Procesar películas valoradas
          const ratedMovies = {};
          if (data.rated_movies) {
            data.rated_movies.forEach((movie) => {
              ratedMovies[movie.title] = movie.rating;
            });
          }
          this.userRatedMovies = ratedMovies;

          // Procesar películas con like
          this.likedMovies = data.liked_movies || [];
        } catch (error) {
          console.error('Error loading user preferences:', error.response?.data || error.message);
        }
      },

      scrollToTop() {
        window.scrollTo({
          top: 0,
          behavior: 'smooth',
        });
      },
    },
    mounted() {
      if (this.userId) {
        this.loadUserPreferences().then(() => {
          // Cargar datos de la película después de cargar las preferencias
          this.loadMovieData(this.$route.params.id);
        });
      } else {
        console.warn('User ID not found in localStorage.');
        this.loadMovieData(this.$route.params.id);
      }
    },
    watch: {
      '$route.params.id': {
        immediate: true,
        handler(newId) {
          console.log('Route changed, fetching new movie data for ID:', newId);
          this.loadMovieData(newId);
        },
      },
    },
  };

  function getImagePath(image) {
    if (image && image.startsWith('http')) {
      return image;
    } else {
      return require(`@/assets/${image}`);
    }
  }

  async function generateMovieObject(movieData) {
    return {
      id: movieData.id,
      image: getImagePath(movieData.image[1]),
      smallImage: getImagePath(movieData.image[0]),
      title: movieData.title,
      description: movieData.description,
      rating: movieData.rating,
      likes: movieData.likes,
      director: movieData.director,
      country: movieData.country,
      release_date: movieData.release_date,
      genres: movieData.genres.map((genre) => genre.type),
      cast: movieData.cast_members.map((cast) => cast.name),
      trailer: movieData.trailer,
    };
  }

  async function generateRecentMovieObject(movieData) {
    return {
      id: movieData.id,
      image: getImagePath(movieData.image[0]),
      rating: movieData.rating,
      likes: movieData.likes,
    };
  }
</script>




<style scoped>
body {
  background-color: #121212;
  /* Color oscuro para el fondo */
  color: white;
  /* Color del texto por defecto */
}

.home-page {
  background-color: #121212;
  /* Color oscuro para el fondo de la página */
  overflow: hidden;
  min-height: 100vh;
  /* Asegura que ocupe toda la altura de la ventana */
}

.banner-container {
  position: relative;
  /* Para que la sombra se posicione correctamente */
}

.banner {
  width: 100%;
  /* Cambia a 100% para adaptarse al ancho del contenedor padre */
  /* Oculta el desbordamiento de las imágenes */
  margin-top: 0px;
  /* Mantén esto si es necesario para tu diseño */
}

.banner-video {
  display: flex;
  justify-content: center;
  /* Center horizontally */
  align-items: center;
  /* Center vertically */
  height: 450px;
  /* Or any height that fits your layout */
}

.shadow-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 250px;
  background: linear-gradient(to top, rgba(18, 18, 18, 1), rgba(18, 18, 18, 0));
  z-index: 5;
}

/* Estilos del carrusel */
.carousel-inner img {
  width: 100%;
  height: 82vh;
  /* Cambia el tamaño aquí si lo deseas */
  object-fit: cover;
  /* Asegura que la imagen cubra todo el contenedor */
}

.carousel-control-next {
  z-index: 20;
  /* Aumenta el z-index para que estén encima de la imagen de portada */
  width: 50px;
  top: 24px;
  height: 375px;
  opacity: 0;
  border-top-right-radius: 20px;
  border-bottom-right-radius: 20px;
  background-color: rgba(255, 255, 255, 0);
  /* Fondo semi-transparente */
  transition: background-color 0.3s;
}

.carousel-control-prev {
  z-index: 20;
  /* Aumenta el z-index para que estén encima de la imagen de portada */
  top: 24px;
  width: 50px;
  height: 375px;
  opacity: 0;
  border-top-left-radius: 20px;
  border-bottom-left-radius: 20px;
  background-color: rgba(255, 255, 255, 0);
  /* Fondo semi-transparente */
  transition: background-color 0.3s;
}

.carousel-control-prev:hover,
.carousel-control-next:hover {
  background-color: rgba(0, 0, 0, 0.5);
  /* Cambio de color al pasar el mouse */
  opacity: 1;
}




.features {
  padding: 40px 20px;
  text-align: center;
}

.feature-item {
  margin: 20px;
  display: inline-block;
  width: 20%;
}


/* Estilo para la imagen pequeña */
.small-cover {
  position: absolute;
  /* Posiciona de forma absoluta */
  bottom: 3vh;
  /* Distancia desde el fondo */
  left: 27vh;
  /* Distancia desde el lado izquierdo */
  z-index: 10;
  /* Asegura que esté encima de la imagen del carrusel */
  display: flex;
  /* Usar flexbox para alinear la imagen y el texto */
  align-items: center;
  /* Centra verticalmente los elementos dentro de small-cover */
}

.small-cover-image {
  width: 350px !important;
  /* Cambia el tamaño aquí si lo deseas */
  height: 500px !important;
  /* Mantiene la proporción */
  border-radius: 15px;
  /* Bordes redondeados */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  /* Sombra para un mejor contraste */
  margin-right: 150px;
  /* Espacio entre la imagen pequeña y la caja de texto */
}

/* Estilo para la caja contenedora de la información */
.movie-info {
  background-color: rgba(0, 0, 0, 0.6);
  /* Fondo oscuro y más opaco */
  color: white;
  /* Color del texto */
  padding: 20px;
  /* Espaciado interno */
  border-radius: 10px;
  /* Bordes redondeados */
  width: 350px;
  /* Ancho mínimo de la caja */
  height: 500px;
  /* Altura mínima para la caja */
  display: flex;
  /* Usar flexbox para alinear el contenido */
  flex-direction: column;
  /* Organiza los elementos en columna */
  justify-content: flex-start;
  /* Alinea el contenido al inicio verticalmente */
  align-items: flex-start;
  /* Alinea el contenido a la izquierda horizontalmente */
  overflow: hidden;
  /* Asegura que el contenido no se desborde */
  text-align: left;
  /* Alinea el texto a la izquierda */
}

/* Alineación en una sola línea */
.info-item {
  display: flex;
  /* Usamos flexbox para alinear los elementos en la misma línea */
  margin-bottom: 30px;
  /* Espaciado entre los items */
  flex-wrap: wrap;
  /* Si es necesario, los elementos pueden romperse en la siguiente línea */
}

/* Estilo para el título */
.movie-info h4 {
  margin-bottom: 35px;
  /* Espacio entre el título y la siguiente sección */
  font-size: 1.5em;
  /* Tamaño de fuente para el título */
  font-weight: bold;
  /* Hacer que el título sea más destacable */
}

.info-title {
  font-size: 1.1em;
  /* Tamaño de fuente para los títulos */
  color: #828282;
  /* Color para diferenciar los títulos */
  margin-right: 5px;
  /* Espacio entre el título y el valor */
}

/* El contenido del valor puede tener otro estilo */
.info-item span:last-child {
  font-size: 1em;
  /* Tamaño de fuente más pequeño para el valor */
  font-weight: bold;
  /* Destacar los títulos */
  color: #d1d1d1;
  /* Color para el valor */
}


.rating-likes-banner {
  position: absolute;
  bottom: 1vh;
  right: 1vh;
  background-color: rgba(255, 255, 255, 0);
  /* Fondo oscuro semi-transparente */
  color: white;
  padding: 10px;
  border-radius: 10px;
  display: flex;
  gap: 10px;
  /* Espacio entre los elementos */
  align-items: center;
  z-index: 15;
  /* Asegura que se muestre sobre otros elementos */
}

.rating {
  display: flex;
  align-items: center;
  font-weight: bold;
}

.likes {
  display: flex;
  align-items: center;
  font-weight: bold;
}

.icon {
  width: 20px !important;
  /* Ajusta el tamaño según tus necesidades */
  height: 20px !important;
  margin-right: 5px;
  /* Espacio entre la imagen y el número */
}

.recent-movies,
.top-rated-movies {
  padding: 40px 20px;
  text-align: center;
  background-color: #121212;
  /* Color de fondo para diferenciar secciones */
  /* Margen entre secciones */
  padding-left: 50px;
  /* Espacio desde la izquierda para toda la sección */
}

.movie-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  /* Grid responsivo */
  gap: 50px;
  /* Espacio entre elementos */
  margin-left: 0;
  /* Asegura que no haya margen adicional a la izquierda */
}

.section-title {
  color: white;
  /* Cambia el color del texto */
  font-size: 20px;
  /* Cambia el tamaño de la fuente */
  text-align: left;
  /* Cambia la alineación (izquierda, centro, derecha) */
  margin-left: 2.4rem;
  /* Agrega margen a la izquierda si es necesario */
  margin-bottom: 0px;
  /* Agrega margen abajo para separarlo de la cuadrícula */
  font-weight: bold;
  
}
.trailer-title {
  padding-bottom: 2rem;
  padding-top: 2rem;
}



.rating-likes-cover {
  position: absolute;
  bottom: 315px;
  left: 15px;
  background-color: rgba(0, 0, 0, 0.6);
  /* Fondo oscuro semi-transparente */
  color: white;
  padding: 10px;
  border-radius: 10px;
  display: flex;
  gap: 2px;
  /* Espacio entre los elementos */
  align-items: center;
  z-index: 5;
  /* Asegura que se muestre sobre otros elementos */
}




/* Estilo para el carrusel */
.carousel-item {
  justify-content: center;
  /* Alinear a la izquierda (o cambiar a center si prefieres) */
  margin-top: 1.5rem;
  margin-bottom: 1.5rem;

}

/* Estilo para cada película dentro del carrusel */
.movie-item {
  width: 250px;
  /* Ajusta al tamaño deseado */
  height: 375px;
  /* Mantiene la proporción de la imagen */
  flex-direction: column;
  /* Apila el contenido verticalmente */
  align-items: center;
  /* Centra horizontalmente */
  background-color: rgba(0, 0, 0, 0.2);
  /* Cambia el color de fondo */
  border-radius: 20px;
  /* Bordes redondeados para que coincidan con el poster */

  transition: transform 0.3s;
  position: relative;
  /* Asegura que los elementos dentro se posicionen relativos a este */
}

.movie-item:hover {
  transform: scale(1.03);
  z-index: 10;
  /* Efecto de escala al pasar el cursor por encima */
}

/* Estilo para la imagen de la película */
.movie-poster {
  width: 100%;
  /* Asegúrate de que ocupen todo el ancho del contenedor */
  height: 375px !important;
  /* Mantiene la proporción de la imagen */
  border-radius: 20px;
  /* Bordes redondeados */
}



.star-rating-container {
  position: absolute;
  bottom: 25px;
  right: 150px;
  z-index: 10;
  opacity: 1;
}

.radio {
  display: flex;
  justify-content: center;
  gap: 10px;
  flex-direction: row-reverse;
}

.radio>input {
  position: absolute;
  appearance: none;
}

.radio>label {
  cursor: pointer;
  font-size: 30px;
  position: relative;
  display: inline-block;
  transition: transform 0.3s ease;
}

.radio>label>svg {
  fill: #666;
  transition: fill 0.3s ease;
}


.radio>label::before {
  top: -15px;
  left: 50%;
  transform: translateX(-50%) scale(0);
}

.radio>label::after {
  bottom: -15px;
  left: 50%;
  transform: translateX(-50%) scale(0);
}

.radio>label:hover::before,
.radio>label:hover::after {
  opacity: 1;
  transform: translateX(-50%) scale(1.5);
}

.radio>label:hover {
  transform: scale(1.2);
  animation: pulse 0.6s infinite alternate;
}

.radio>label:hover>svg,
.radio>label:hover~label>svg {
  fill: #ff9e0b;
  filter: drop-shadow(0 0 15px rgba(255, 158, 11, 0.9));
  animation: shimmer 1s ease infinite alternate;
}

.radio>input:checked+label>svg,
.radio>input:checked+label~label>svg {
  fill: #ff9e0b;
  filter: drop-shadow(0 0 15px rgba(255, 158, 11, 0.9));
  animation: pulse 0.8s infinite alternate;
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }

  100% {
    transform: scale(1.1);
  }
}

@keyframes particle-explosion {
  0% {
    opacity: 0;
    transform: scale(0.5);
  }

  50% {
    opacity: 1;
    transform: scale(1.2);
  }

  100% {
    opacity: 0;
    transform: scale(0.5);
  }
}

@keyframes shimmer {
  0% {
    filter: drop-shadow(0 0 10px rgba(255, 158, 11, 0.5));
  }

  100% {
    filter: drop-shadow(0 0 20px rgba(255, 158, 11, 1));
  }
}

.radio>input:checked+label:hover>svg,
.radio>input:checked+label:hover~label>svg {
  fill: #e58e09;
}

.radio>label:hover>svg,
.radio>label:hover~label>svg {
  fill: #ff9e0b;
}

.radio input:checked~label svg {
  fill: #ffa723;
}

.container input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0;
  width: 0;
}

.container {
  display: block;
  position: absolute;
  cursor: pointer;
  font-size: 18px;
  user-select: none;
  transition: 100ms;
  z-index: 10;
  top: 90%;
  left: 92%;
  width: 2em;
  height: 2em;
}

.checkmark {
  top: 0;
  left: 0;
  height: 2em;
  width: 2em;
  transition: 100ms;
  animation: dislike_effect 400ms ease;
  position: absolute;
  z-index: 2;
  /* Se asegura de que el corazón esté sobre otros elementos */
  overflow: visible; /* Esto es importante */
}

.checkmark path {
  fill: #666;
  /* Color gris por defecto */
  stroke: none;
  transition: fill 200ms ease;
  /* Añadir transición suave al cambio de color */
}

/* Efecto hover: cuando pasas el cursor por encima, el corazón se pone rojo */
.container:hover .checkmark path {
  fill: #f52121;
  filter: drop-shadow(0 0 15px rgba(96, 13, 13, 0.9)); /* Sombra dinámica */
  animation: shimmerHeart  1s ease infinite alternate; /* Animación shimmer */
}

/* El color cambia cuando está seleccionado */
.container input:checked ~ .checkmark path {
  fill: #f52121;
  filter: drop-shadow(0 0 15px rgba(96, 13, 13, 0.9)); /* Sombra dinámica */
  animation: shimmerHeart  1s ease infinite alternate; /* Animación shimmer */
}

.container input:checked~.checkmark {
  animation: like_effect 400ms ease;
}


/* Animaciones para el efecto de like/dislike */
@keyframes like_effect {
  0% {
    transform: scale(0);
  }

  50% {
    transform: scale(1.2);
  }

  100% {
    transform: scale(1);
  }
}

@keyframes dislike_effect {
  0% {
    transform: scale(0);
  }

  50% {
    transform: scale(1.2);
  }

  100% {
    transform: scale(1);
  }
}

/* Animación para el efecto de brillo (shimmer) con sombra roja para el corazón */
@keyframes shimmerHeart {
  0% {
    filter: drop-shadow(0 0 10px rgba(255, 13, 13, 0.5)); /* Sombra roja suave */
  }

  100% {
    filter: drop-shadow(0 0 20px rgba(255, 13, 13, 1)); /* Sombra roja más intensa */
  }
}



.detail-item {
  margin: 10px;
  display: inline-block;
  width: 100%;
}

.detail-item p {
  margin-top: 1.5rem;
  font-size: 1.1em;
  color: #d1d1d1;
}

.detail-item h4 {
  font-size: 1.5em;
  font-weight: bold;
}



.detail-card h4 {
  font-size: 1.2em;
  color: #f5f5f5;
  margin-bottom: 10px;
}

.detail-card p {
  font-size: 1em;
  color: #bdbdbd;
  margin: 0;
}

.cast-section .details-grid .cards-container {
  background-color: #121212;
  padding: 30px;
  color: white;
  display: grid;
  gap: 20px;
  grid-template-columns: repeat(5, 1fr);
  /* 5 cards per row */
  max-width: 100%;
  overflow: hidden;

  /* Hide the overflow by default */
}



.detail-card {
  background-color: #1e1e1e;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  text-align: center;
  transition: 0.2s;
}

.detail-card:hover {
  transform: scale(1.05);
}

.see-more-btn {
  grid-column: span 5;
  text-align: right;
  margin-right: 1.5rem;
}

.see-more-btn button {
  background-color: #00000000;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  font-weight: bold;
}

.see-more-btn button:hover {
  color: #949494;
}

.media-container {
  display: flex;
  justify-content: center;
  /* Center horizontally */
  align-items: center;
  /* Center vertically */
  width: 100%;
  height: 100%;
}

.video-section {
  text-align: center;
  padding-top: 18rem;
  padding-bottom: 18rem;
}

.banner-video iframe {
  max-width: 100%;
  /* Ensure the video/image doesn't overflow */
  max-height: 100%;
  /* Ensure the video/image doesn't overflow */
}

.banner-image{
  width: 112rem;
  height: 63rem;
}

#related-movies {
  margin-left: -0.2rem;
}
</style>