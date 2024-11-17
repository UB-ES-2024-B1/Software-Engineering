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
            <h6>Director:</h6>
            <p>{{ bannerMovie.director }}</p>
            <h6>Country:</h6>
            <p>{{ bannerMovie.country }}</p>
            <h6>Date:</h6>
            <p>{{ bannerMovie.release_date }}</p>
          </div>
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
    </section>

    <!-- Nueva zona de detalles de la película -->
    <section class="movie-details" v-if="bannerMovie">
      <div class="details-grid" style="background-color: #121212; padding: 30px; color: white;">
        <div class="detail-item">
          <p>{{ bannerMovie.description }}</p>
        </div>
      </div>
    </section>

    <!-- Sección de películas relacionadas -->
    <section class="top-rated-movies">
      <h2 class="section-title">Related Movies</h2>
      <div id="topRatedMoviesCarousel" class="carousel slide" data-bs-ride="carousel">
        <div class="carousel-inner">
          <!-- Primer bloque: películas 0-4 -->
          <div class="carousel-item active">
            <div class="movie-grid responsive-carousel">
              <div class="movie-item" v-for="movie in relatedMovies.slice(0, 5)" :key="movie.id">
                <img :src="movie.image" :alt="movie.title" class="movie-poster" />
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
                <img :src="movie.image" :alt="movie.title" class="movie-poster" />
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
                <img :src="movie.image" :alt="movie.title" class="movie-poster" />
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
                <img :src="movie.image" :alt="movie.title" class="movie-poster" />
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
        <button class="carousel-control-prev" type="button" data-bs-target="#topRatedMoviesCarousel" data-bs-slide="prev">
          <span class="carousel-control-prev-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Previous</span>
        </button>
        <button class="carousel-control-next" type="button" data-bs-target="#topRatedMoviesCarousel" data-bs-slide="next">
          <span class="carousel-control-next-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Next</span>
        </button>
      </div>
    </section>
    

    <!-- Pie de Página -->
    <footer class="footer">
      <p>&copy; 2024 FilmHub Enterprise. All rights reserved.</p>
      <div class="socials">
        <a href="#">FilmHub Enterprise</a>
      </div>
    </footer>
  </div>
</template>

<script>
  import HeaderPage from '@/components/HeaderPage.vue';
  import axios from 'axios';
  import { API_BASE_URL } from '@/config.js';
  
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
  
  export default {
    name: 'MovieDetails',
    components: { HeaderPage },
    data() {
      return {
        bannerMovie: null, // Nueva propiedad para la película del banner
        movies: [], // Lista de películas ordenadas
        relatedMovies: [], // Lista de películas relacionadas
      };
    },
    methods: {
      async fetchBannerMovie(id) {
        try {
          const response = await axios.get(`${API_BASE_URL}/movies/${id}`);
          this.bannerMovie = await generateMovieObject(response.data);
        } catch (error) {
          console.error('Error retrieving banner movie:', error);
        }
      },
      async fetchMovies(start, end, movies_section) {
        try {
          const url =
            movies_section === 1
              ? `${API_BASE_URL}/movies/sorted/likes/`
              : `${API_BASE_URL}/movies/sorted/rating/`;
          const movieObjects = [];
          const response = await axios.get(url);
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
          console.error('Error retrieving movies:', error);
        }
      },
    },
    created() {
      const movieId = this.$route.params.id; // ID de la película desde la URL
      this.fetchBannerMovie(movieId); // Carga la película para el banner
      this.fetchMovies(0, 50, 2); // Carga las películas mejor valoradas
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

.carousel-control-next {
  z-index: 20;
  /* Aumenta el z-index para que estén encima de la imagen de portada */
  width: 50px;
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
  width: 50px;
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

.footer {
  background-color: #161616;
  color: white;
  text-align: center;
  padding: 20px;
}

/* Estilo para la imagen pequeña */
.small-cover {
  position: absolute;
  /* Posiciona de forma absoluta */
  bottom: 50px;
  /* Distancia desde el fondo */
  left: 200px;
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
  height: 450px !important;
  /* Mantiene la proporción */
  border-radius: 15px;
  /* Bordes redondeados */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  /* Sombra para un mejor contraste */
  margin-right: 100px;
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
  height: 450px;
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

/* Estilo para el título */
.movie-info h4 {
  margin-bottom: 35px; /* Espacio entre el título y la siguiente sección */
  font-size: 1.5em; /* Tamaño de fuente para el título */
  font-weight: bold; /* Hacer que el título sea más destacable */
}

/* Estilo para los subtítulos (h6) */
.movie-info h6 {
  margin-bottom: 7px; /* Espacio entre cada subtítulo y el contenido */
  font-size: 1.1em; /* Tamaño de fuente para los subtítulos */
  font-weight: normal; /* Hacer que el subtítulo sea más ligero */
  color: #f0f0f0; /* Color más suave para los subtítulos */
}

/* Estilo para los párrafos (p) */
.movie-info p {
  margin-bottom: 35px; /* Espacio entre los párrafos */
  font-size: 1em; /* Tamaño de fuente para los párrafos */
  color: #d1d1d1; /* Color más suave para el texto */
}

.rating-likes-banner {
  position: absolute;
  bottom: 60px;
  right: 530px;
  background-color: rgba(0, 0, 0, 0.6);
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
  margin: 10px 0;
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
  margin-bottom: 20px;
  /* Agrega margen abajo para separarlo de la cuadrícula */
  font-weight: bold;
}

/* 
.movie-item:hover {
  transform: scale(1.05); 
}

*/


.rating-likes-cover {
  position: absolute;
  bottom: 290px;
  left: 20px;
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
  justify-content: flex-start;
  /* Alinear a la izquierda (o cambiar a center si prefieres) */
  align-items: flex-start;
  /* Alinea las películas al inicio */
}

/* Estilo para cada película dentro del carrusel */
.movie-item {
  width: 250px;
  /* Ajusta al tamaño deseado */
  height: 350px;
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
  height: 350px !important;
  /* Mantiene la proporción de la imagen */
  border-radius: 20px;
  /* Bordes redondeados */
}

</style>