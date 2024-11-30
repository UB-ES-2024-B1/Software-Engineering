<template>
  <div class="home-page">
    <HeaderPage /> <!-- Aquí importas y usas el componente HeaderPage -->

    <!-- Carrusel de películas -->
    <section class="banner">
      <div id="movieCarousel" class="carousel slide" data-bs-ride="carousel" data-bs-interval="5000">
        <!-- Indicators/dots -->
        <div class="carousel-indicators">
          <button v-for="(movie, index) in movies" :key="index" type="button" :data-bs-target="'#movieCarousel'"
            :data-bs-slide-to="index" :class="{ active: index === 0 }" aria-current="index === 0 ? 'true' : 'false'"
            :aria-label="'Slide ' + (index + 1)"></button>
        </div>

        <!-- The slideshow/carousel items -->
        <div class="carousel-inner">
          <div class="carousel-item" v-for="(movie, index) in movies" :class="{ active: index === 0 }" :key="index">
            <img :src="movie.image" class="d-block w-100 carousel-image" alt="Movie poster" />
            <div class="shadow-overlay"></div>

            <div class="small-cover">
              <router-link :to="`/movie/${movie.id}`">
                <img :src="movie.smallImage" alt="Movie Small Cover" class="small-cover-image" />
              </router-link>
              <div class="movie-info">
                <h5>{{ movie.title }}</h5>
                <p>{{ movie.description }}</p>
              </div>
            </div>

            <div class="rating-likes-banner">
              <div class="rating">
                <img src="@/assets/star.png" alt="Star" class="icon" />
                <span>{{ movie.rating.toFixed(1) }}</span>
              </div>
              <div class="likes">
                <img src="@/assets/like.png" alt="Like" class="icon" />
                <span>{{ movie.likes }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Left and right controls/icons -->
        <button class="carousel-control-prev-banner" type="button" data-bs-target="#movieCarousel" data-bs-slide="prev">
          <span class="carousel-control-prev-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Previous</span>
        </button>
        <button class="carousel-control-next-banner" type="button" data-bs-target="#movieCarousel" data-bs-slide="next">
          <span class="carousel-control-next-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Next</span>
        </button>
      </div>
    </section>

    <!-- Sección de películas recientes -->
    <section class="recent-movies">
      <router-link :to="{ path: '/movies', query: { sortByYear: 'year' } }" class="section-title-link">
        <h2 class="section-title">Most Recent Movies</h2>
      </router-link>
      <div id="recentMoviesCarousel" class="carousel slide" data-bs-ride="carousel">
        <div class="carousel-inner">
          <div class="carousel-item active carousel-item-lista">
            <div class="movie-grid responsive-carousel">
              <div class="movie-item" v-for="movie in recentMovies.slice(0, 5)" :key="movie.id">
                <router-link :to="`/movie/${movie.id}`">
                  <img :src="movie.image" :alt="movie.title" class="movie-poster" />
                </router-link>
                <div class="rating-likes-cover">
                  <div class="likes">
                    <img src="@/assets/like.png" alt="Like" class="icon" />
                    <span>{{ movie.likes }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="carousel-item carousel-item-lista">
            <div class="movie-grid responsive-carousel">
              <div class="movie-item" v-for="movie in recentMovies.slice(5, 10)" :key="movie.id">
                <router-link :to="`/movie/${movie.id}`">
                  <img :src="movie.image" :alt="movie.title" class="movie-poster" />
                </router-link>
                <div class="rating-likes-cover">
                  <div class="likes">
                    <img src="@/assets/like.png" alt="Like" class="icon" />
                    <span>{{ movie.likes }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="carousel-item carousel-item-lista">
            <div class="movie-grid responsive-carousel">
              <div class="movie-item" v-for="movie in recentMovies.slice(10, 15)" :key="movie.id">
                <router-link :to="`/movie/${movie.id}`">
                  <img :src="movie.image" :alt="movie.title" class="movie-poster" />
                </router-link>
                <div class="rating-likes-cover">
                  <div class="likes">
                    <img src="@/assets/like.png" alt="Like" class="icon" />
                    <span>{{ movie.likes }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="carousel-item carousel-item-lista">
            <div class="movie-grid responsive-carousel">
              <div class="movie-item" v-for="movie in recentMovies.slice(15, 20)" :key="movie.id">
                <router-link :to="`/movie/${movie.id}`">
                  <img :src="movie.image" :alt="movie.title" class="movie-poster" />
                </router-link>
                <div class="rating-likes-cover">
                  <div class="likes">
                    <img src="@/assets/like.png" alt="Like" class="icon" />
                    <span>{{ movie.likes }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- Controles -->
        <button class="carousel-control-prev" type="button" data-bs-target="#recentMoviesCarousel" data-bs-slide="prev">
          <span class="carousel-control-prev-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Previous</span>
        </button>
        <button class="carousel-control-next" type="button" data-bs-target="#recentMoviesCarousel" data-bs-slide="next">
          <span class="carousel-control-next-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Next</span>
        </button>
      </div>
    </section>
    <!-- Sección de películas mejor valoradas -->
    <section class="top-rated-movies">
      <router-link :to="{ path: '/movies', query: { sortByRate: 'rating' } }" class="section-title-link">
        <h2 class="section-title">Top Valorated Movies</h2>
      </router-link>
      <div id="topRatedMoviesCarousel" class="carousel slide" data-bs-ride="carousel">
        <div class="carousel-inner">
          <div class="carousel-item active carousel-item-lista">
            <div class="movie-grid responsive-carousel">
              <div class="movie-item" v-for="movie in topRatedMovies.slice(0, 5)" :key="movie.id">
                <router-link :to="`/movie/${movie.id}`">
                  <img :src="movie.image" :alt="movie.title" class="movie-poster" />
                </router-link>
                <div class="rating-likes-cover">
                  <div class="rating">
                    <img src="@/assets/star.png" alt="Star" class="icon" />
                    <span>{{ movie.rating.toFixed(1) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="carousel-item carousel-item-lista">
            <div class="movie-grid responsive-carousel">
              <div class="movie-item" v-for="movie in topRatedMovies.slice(5, 10)" :key="movie.id">
                <router-link :to="`/movie/${movie.id}`">
                  <img :src="movie.image" :alt="movie.title" class="movie-poster" />
                </router-link>
                <div class="rating-likes-cover">
                  <div class="rating">
                    <img src="@/assets/star.png" alt="Star" class="icon" />
                    <span>{{ movie.rating.toFixed(1) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="carousel-item carousel-item-lista">
            <div class="movie-grid responsive-carousel">
              <div class="movie-item" v-for="movie in topRatedMovies.slice(10, 15)" :key="movie.id">
                <router-link :to="`/movie/${movie.id}`">
                  <img :src="movie.image" :alt="movie.title" class="movie-poster" />
                </router-link>
                <div class="rating-likes-cover">
                  <div class="rating">
                    <img src="@/assets/star.png" alt="Star" class="icon" />
                    <span>{{ movie.rating.toFixed(1) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="carousel-item carousel-item-lista">
            <div class="movie-grid responsive-carousel">
              <div class="movie-item" v-for="movie in topRatedMovies.slice(15, 20)" :key="movie.id">
                <router-link :to="`/movie/${movie.id}`">
                  <img :src="movie.image" :alt="movie.title" class="movie-poster" />
                </router-link>
                <div class="rating-likes-cover">
                  <div class="rating">
                    <img src="@/assets/star.png" alt="Star" class="icon" />
                    <span>{{ movie.rating.toFixed(1) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- Controles -->
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
import HeaderPage from '@/components/HeaderPage.vue'; // Importa el componente HeaderPage
import axios from 'axios';
import { API_BASE_URL } from '@/config.js'; // Importa tu archivo de configuración
import FooterComponent from '@/components/FooterComponent.vue';

function getImagePath(image) {
  // Comprobar si la imagen es una URL
  if (image && image.startsWith('http')) {
    return image; // Retorna la URL tal cual
  } else {
    // Retorna la ruta de la imagen en assets
    return require(`@/assets/${image}`);
  }
}

async function generateMovieObject(movieData) {
  const movieObject = {
    id: movieData.id,
    image: getImagePath(movieData.image[1]),
    smallImage: getImagePath(movieData.image[0]),
    title: movieData.title,
    description: movieData.description,
    rating: movieData.rating,
    likes: movieData.likes
  };

  return movieObject;
}

async function generateRecentMovieObject(movieData) {
  const movieObject = {
    id: movieData.id,
    image: getImagePath(movieData.image[0]),
    rating: movieData.rating,
    likes: movieData.likes
  };

  return movieObject;
}

export default {
  name: 'MainPageView',
  components: {
    HeaderPage,
    FooterComponent,
  },
  data() {
    return {
      movies: [],

      recentMovies: [],

      topRatedMovies: [],

    };
  },
  methods: {


    async fetchMovies(start, end, movies_section) {
      try {
        let url;

        // Seleccionar la URL en función de la sección
        if (movies_section === 1) { 
          url = `${API_BASE_URL}/movies/sorted/likes`; 
        } else if (movies_section === 2) { 
          url = `${API_BASE_URL}/movies/sorted/release_date`; 
        } else { 
          url = `${API_BASE_URL}/movies/sorted/rating`; 
        }

        const movieObjects = [];
        const response = await axios.get(url);
        let movies = response.data; 

        // Ordenar de más reciente a más antiguo si es movies_section === 2
        if (movies_section === 2) {
          movies = movies.reverse(); 
        }

        // Limitar a las primeras películas
        const topMovies = movies.slice(start, end);

        for (let i = 0; i < topMovies.length; i++) {
          const movieData = topMovies[i];

          let movieObject;

          if (movies_section === 1) {
            movieObject = await generateMovieObject(movieData);
          } else {
            movieObject = await generateRecentMovieObject(movieData);
          }

          if (movieObject) movieObjects.push(movieObject);
        }

        // Asignar las películas al estado correspondiente
        if (movies_section === 1) {
          this.movies = movieObjects;
        } else if (movies_section === 2) {
          this.recentMovies = movieObjects;
        } else {
          this.topRatedMovies = movieObjects;
        }

      } catch (error) {
        console.error("Error retrieving movies:", error);
      }
    },




    navigateToMovie(movieId) {
      console.log(`Navigating to movie with ID: ${movieId}`);
    },
  },
  created() {
    this.fetchMovies(0, 9, 1);
    this.fetchMovies(0, 20, 2);
    this.fetchMovies(0, 20, 3);
  },
};
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
  overflow: hidden;
  /* Oculta el desbordamiento de las imágenes */
  margin-top: 0px;
  /* Mantén esto si es necesario para tu diseño */
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
  height: 600px;
  /* Cambia el tamaño aquí si lo deseas */
  object-fit: cover;
  /* Asegura que la imagen cubra todo el contenedor */
}



.carousel-control-prev-banner,
.carousel-control-next-banner {
  z-index: 20;
  /* Aumenta el z-index para que estén encima de la imagen de portada */
  width: 50px;
  /* Ancho de los botones */
  opacity: 1;
  /* Opacidad inicial */
  background-color: rgba(255, 255, 255, 0);
  /* Fondo transparente */
  transition: background-color 0.3s;
  border: none;
  /* Eliminar el borde */
  outline: none;
  /* Eliminar el contorno que aparece al hacer clic */
}

.carousel-control-prev-banner:focus,
.carousel-control-next-banner:focus {
  outline: none;
  /* Asegúrate de que no haya contorno al enfocarlo */
}

/* Posicionamiento de los controles */
.carousel-control-prev-banner,
.carousel-control-next-banner {
  position: absolute;
  /* Asegúrate de que se posicione correctamente */
  top: 50%;
  /* Centrado vertical */
  transform: translateY(-50%);
  /* Ajuste para centrar verticalmente */
  opacity: 0.5;
}

/* Posición de los botones */
.carousel-control-prev-banner {
  left: 5px;
  /* Ajusta según sea necesario */
}

.carousel-control-next-banner {
  right: 5px;
  /* Ajusta según sea necesario */
}

.carousel-control-prev-banner:hover,
.carousel-control-next-banner:hover {
  opacity: 1;
  /* Cambio de color al pasar el mouse */
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


.carousel-indicators {
  position: absolute;
  z-index: 15;
  /* Asegúrate de que los indicadores estén por encima de otros elementos */
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
  bottom: 50px;
  /* Distancia desde el fondo */
  left: 60px;
  /* Distancia desde el lado izquierdo */
  z-index: 10;
  /* Asegura que esté encima de la imagen del carrusel */
  display: flex;
  /* Usar flexbox para alinear la imagen y el texto */
  align-items: center;
  /* Centra verticalmente los elementos dentro de small-cover */
}

.small-cover-image {
  width: 250px !important;
  /* Cambia el tamaño aquí si lo deseas */
  height: 350px !important;
  /* Mantiene la proporción */
  border-radius: 15px;
  /* Bordes redondeados */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  /* Sombra para un mejor contraste */
  margin-right: 20px;
  /* Espacio entre la imagen pequeña y la caja de texto */
}

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
  height: 350px;
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

.movie-info h5 {
  margin: 0;
  /* Elimina el margen por defecto del encabezado */
  font-weight: bold;
}

.movie-info p {
  margin-top: 20px;
  /* Añade un margen entre el título y la descripción */
}

.rating-likes-banner {
  position: absolute;
  bottom: 50px;
  right: 40px;
  background-color: rgba(0, 0, 0, 0.6);
  /* Fondo oscuro semi-transparente */
  color: white;
  padding: 10px;
  border-radius: 10px;
  display: flex;
  gap: 10px;
  /* Espacio entre los elementos */
  align-items: center;
  z-index: 5;
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
  padding: 20px 20px;
  text-align: center;
  background-color: #121212;
  /* Color de fondo para diferenciar secciones */
  margin: 0;
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
  margin-left: 0px;
  /* Agrega margen a la izquierda si es necesario */
  margin-bottom: 0px;
  /* Agrega margen abajo para separarlo de la cuadrícula */
  font-weight: bold;
  
}

/* Para el enlace */
.section-title-link {
  text-decoration: none; /* Quita el subrayado del router-link */
  color: inherit; /* Evita el color azul predeterminado */
}


.section-title-link:hover {
  text-decoration: underline; 
  color: white; 
}


.movie-item:hover {
  transform: scale(1.03);
  z-index: 10;
  /* Efecto de escala al pasar el cursor por encima */
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
.carousel-item{
  justify-content: center;
  /* Alinear a la izquierda (o cambiar a center si prefieres) */
  align-items: flex-start;
  /* Alinea las películas al inicio */
}

.carousel-item-lista {
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

/* Estilo para la imagen de la película */
.movie-poster {
  width: 100%;
  /* Asegúrate de que ocupen todo el ancho del contenedor */
  height: 375px !important;
  /* Mantiene la proporción de la imagen */
  border-radius: 20px;
  /* Bordes redondeados */
}

</style>