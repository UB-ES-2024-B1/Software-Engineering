<template>
  <div class="home-page">
    <HeaderPage /> <!-- Aquí importas y usas el componente HeaderPage -->

    <!-- Carrusel de películas -->
    <section class="banner">
      <div id="movieCarousel" class="carousel slide" data-bs-ride="carousel" data-bs-interval="5000">
        <!-- Indicators/dots -->
        <div class="carousel-indicators">
          <button
            v-for="(movie, index) in movies"
            :key="index"
            type="button"
            :data-bs-target="'#movieCarousel'"
            :data-bs-slide-to="index"
            :class="{ active: index === 0 }"
            aria-current="index === 0 ? 'true' : 'false'"
            :aria-label="'Slide ' + (index + 1)"
          ></button>
        </div>

        <!-- The slideshow/carousel items -->
        <div class="carousel-inner">
          <div
            class="carousel-item"
            v-for="(movie, index) in movies"
            :class="{ active: index === 0 }"
            :key="index"
          >
            <img :src="movie.image" class="d-block w-100 carousel-image" alt="Movie poster" />
            <div class="shadow-overlay"></div> 

            <div class="small-cover">
              <img :src="movie.smallImage" alt="Movie Small Cover" class="small-cover-image" />
              <div class="movie-info">
                <h5>{{ movie.title }}</h5>
                <p>{{ movie.description }}</p>
              </div>
            </div>

            <div class="rating-likes-banner">
              <div class="rating">
                <img src="@/assets/star.png" alt="Star" class="icon" />
                <span>{{ movie.rating }}</span>
              </div>
              <div class="likes">
                <img src="@/assets/like.png" alt="Like" class="icon" />
                <span>{{ movie.likes }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Left and right controls/icons -->
        <button
          class="carousel-control-prev-banner"
          type="button"
          data-bs-target="#movieCarousel"
          data-bs-slide="prev"
        >
          <span class="carousel-control-prev-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Previous</span>
        </button>
        <button
          class="carousel-control-next-banner"
          type="button"
          data-bs-target="#movieCarousel"
          data-bs-slide="next"
        >
          <span class="carousel-control-next-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Next</span>
        </button>
      </div>
    </section>

    <!-- Sección de películas recientes -->
    <section class="recent-movies">
      <h2 class="section-title">Películas Más Recientes</h2>
      <div id="recentMoviesCarousel" class="carousel slide" data-bs-ride="carousel">
        <div class="carousel-inner">
          <div class="carousel-item active">
            <div class="movie-grid">
              <div class="movie-item" v-for="movie in recentMovies.slice(0, 5)" :key="movie.id">
                <img :src="movie.image" :alt="movie.title" class="movie-poster" />
                <div class="rating-likes-cover">
                  <div class="likes">
                    <img src="@/assets/like.png" alt="Like" class="icon" />
                    <span>{{ movie.likes }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="carousel-item">
            <div class="movie-grid">
              <div class="movie-item" v-for="movie in recentMovies.slice(5, 10)" :key="movie.id">
                <img :src="movie.image" :alt="movie.title" class="movie-poster" />
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
      <h2 class="section-title">Películas Mejor Valoradas</h2>
      <div id="topRatedMoviesCarousel" class="carousel slide" data-bs-ride="carousel">
        <div class="carousel-inner">
          <div class="carousel-item active">
            <div class="movie-grid">
              <div class="movie-item" v-for="movie in topRatedMovies.slice(0, 5)" :key="movie.id">
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
          <div class="carousel-item">
            <div class="movie-grid">
              <div class="movie-item" v-for="movie in topRatedMovies.slice(5, 10)" :key="movie.id">
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
        <!-- Controles -->
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
      <p>&copy; 2024 Web Name. All rights reserved.</p>
      <div class="socials">
        <a href="#">Facebook</a>
        <a href="#">Twitter</a>
        <a href="#">Instagram</a>
      </div>
    </footer>
  </div>
</template>

<script>
import HeaderPage from '@/components/HeaderPage.vue'; // Importa el componente HeaderPage

export default {
  name: 'MainPageView',
  components: {
    HeaderPage, // Registra el componente
  },
  data() {
    return {
      movies: [

        {
          id: 1,
          image: require('@/assets/avatarTheWayOfWater_banner.jpg'),
          smallImage: require('@/assets/avatarTheWayOfWater_cover.jpg'), // Nueva imagen pequeña
          title: 'Avatar: The Way of Water',
          description: 'James Cameron returns to the world of Pandora. Set a decade plus after events of the first film, this breathtaking new movie tells the story of the Sully family and introduces audiences to the majestic ocean tulkun.',
          rating: 3.7, // Rating de la película
          likes: 29, // Número de "likes"
        },
        {
          id: 2,
          image: require('@/assets/dunePartTwo_banner.jpg'),
          smallImage: require('@/assets/dunePartTwo_cover.jpg'), // Nueva imagen pequeña
          title: 'Dune: Part Two ',
          description: 'Paul Atreides unites with Chani and the Fremen while on a warpath of revenge against the conspirators who destroyed his family. Facing a choice between the love of his life and the fate of the known universe, he endeavors to prevent a terrible future only he can foresee.',
          rating: 4.3, // Rating de la película
          likes: 39, // Número de "likes"
        },
        {
          id: 3,
          image: require('@/assets/spider-manNoWayHome_banner.jpg'),
          smallImage: require('@/assets/spider-manNoWayHome_cover.jpg'), // Nueva imagen pequeña
          title: 'Spider-Man: No Way Home',
          description: 'When Peter Parker secret identity is discovered, he turns to Doctor Strange to make the world forget that he is Spider-Man.',
          rating: 1.9, // Rating de la película
          likes: 8, // Número de "likes"
        },
        {
          id: 4,
          image: require('@/assets/barbie_banner.jpg'),
          smallImage: require('@/assets/barbie_cover.jpg'), // Nueva imagen pequeña
          title: 'Barbie',
          description: 'Living in Barbie Land is about being a perfect being in a perfect place. Unless you have a total existential crisis. Or you are a Ken.',
          rating: 4.0, // Rating de la película
          likes: 32, // Número de "likes"
        },
        {
          id: 5,
          image: require('@/assets/warForThePlanetOfTheApes_banner.jpg'),
          smallImage: require('@/assets/warForThePlanetOfTheApes_cover.jpg'), // Nueva imagen pequeña
          title: 'War for the Planet of the Apes',
          description: 'Caesar and his apes face an army of humans in a battle that will determine the fate of both species and the future of the planet.',
          rating: 2.4, // Rating de la película
          likes: 17, // Número de "likes"
        },
        {
          id: 6,
          image: require('@/assets/deadpool&wolverine_banner.jpg'),
          smallImage: require('@/assets/deadpool&wolverine_cover.jpg'), // Nueva imagen pequeña
          title: 'Deadpool & Wolverine',
          description: 'Marvel Studios presents its biggest mistake to date. His escapades as Deadpool are in the past, and an apathetic Wade Wilson goes about his day with reluctance. When his world is threatened, he reluctantly puts on the suit to convince Wolverine that... Come on, watch the movie.',
          rating: 4.7, // Rating de la película
          likes: 53, // Número de "likes"
        },
        {
          id: 7,
          image: require('@/assets/theBatman_banner.jpg'),
          smallImage: require('@/assets/theBatman_cover.jpg'), // Nueva imagen pequeña
          title: 'The Batman',
          description: 'A murderer threatens Gotham elite and Batman sets out to unmask him: he must fit the pieces of the puzzle, forge new alliances and punish corruption.',
          rating: 3.2, // Rating de la película
          likes: 25, // Número de "likes"
        },
        {
          id: 8,
          image: require('@/assets/kunfuPanda4_banner.jpg'),
          smallImage: require('@/assets/kunfuPanda4_cover.jpg'), // Nueva imagen pequeña
          title: 'Kung Fu Panda 4',
          description: 'Po and his new ally face a sorceress who wants to take their Staff of Wisdom from them.',
          rating: 2.8, // Rating de la película
          likes: 21, // Número de "likes"
        },
      ],
  
      recentMovies: [
        // Aquí añades tus películas más recientes
        {
          id: 1,
          image: require('@/assets/theNun_cover.jpg'),
          rating: 3.0,
          likes: 5, 
        },
        {
          id: 2,
          image: require('@/assets/up_cover.jpg'),
          rating: 2.8,
          likes: 8,
        },
        {
          id: 3,
          image: require('@/assets/theMeg_cover.jpg'),
          rating: 4.1,
          likes: 11,
        },
        {
          id: 4,
          image: require('@/assets/inception_cover.jpg'),
          rating: 3.4,
          likes: 13,
        },
        {
          id: 5,
          image: require('@/assets/furiosaMadMaxSaga_cover.jpg'),
          rating: 5,
          likes: 87,
        },
        {
          id: 6,
          image: require('@/assets/theFallGuy_cover.jpg'),
          rating: 3.2, 
          likes: 25, 
        },
        {
          id: 7,
          image: require('@/assets/napoleon_cover.jpg'),
          rating: 2.8, 
          likes: 21, 
        },
        {
          id: 8,
          image: require('@/assets/uncharted_cover.jpg'),
          rating: 4.8,
          likes: 79,
        },
        {
          id: 9,
          image: require('@/assets/bulletTrain_cover.jpg'),
          rating: 4.7,
          likes: 63,
        },
        {
          id: 10,
          image: require('@/assets/ratatouille_cover.jpg'),
          rating: 4.7,
          likes: 63,
        },
      ],

      topRatedMovies: [
        // Aquí añades tus películas más recientes
        {
          id: 1,
          image: require('@/assets/toyStory4_cover.jpg'),
          rating: 5,
          likes: 87,
        },
        {
          id: 2,
          image: require('@/assets/dunkirk_cover.jpg'),
          rating: 4.8,
          likes: 79,
        },
        {
          id: 3,
          image: require('@/assets/oppenheimer_cover.jpg'),
          rating: 4.7,
          likes: 63,
        },
        {
          id: 4,
          image: require('@/assets/jumanjiTheNextLevel_cover.jpg'),
          rating: 3.9,
          likes: 25, 
        },
        {
          id: 5,
          image: require('@/assets/bohemianRhapsody_cover.jpg'),
          rating: 2.8, 
          likes: 21, 
        },
        {
          id: 6,
          image: require('@/assets/theHungerGamesTheBalladOfSongbirdsAndSnakes_cover.jpg'),
          rating: 4.7,
          likes: 63,
        },
        {
          id: 7,
          image: require('@/assets/coco_cover.jpg'),
          rating: 3.0,
          likes: 5, 
        },
        {
          id: 8,
          image: require('@/assets/incredibles2_cover.jpg'),
          rating: 2.8,
          likes: 8,
        },
        {
          id: 9,
          image: require('@/assets/jurassicWorldFallenKingdom_cover.jpg'),
          rating: 4.1,
          likes: 11,
        },
        {
          id: 10,
          image: require('@/assets/cars3_cover.jpg'),
          rating: 3.4,
          likes: 13,
        },
      ],

    };
  },
  methods: {
    navigateToMovie(movieId) {
      console.log(`Navigating to movie with ID: ${movieId}`);
    },
  },
};
</script>

<style scoped>

body {
  background-color: #121212; /* Color oscuro para el fondo */
  color: white; /* Color del texto por defecto */
}

.home-page {
  background-color: #121212; /* Color oscuro para el fondo de la página */
  min-height: 100vh; /* Asegura que ocupe toda la altura de la ventana */
}

.banner-container {
  position: relative; /* Para que la sombra se posicione correctamente */
}

.banner {
  width: 100%; /* Cambia a 100% para adaptarse al ancho del contenedor padre */
  overflow: hidden; /* Oculta el desbordamiento de las imágenes */
  margin-top: 0px; /* Mantén esto si es necesario para tu diseño */
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
  height: 600px; /* Cambia el tamaño aquí si lo deseas */
  object-fit: cover; /* Asegura que la imagen cubra todo el contenedor */
}



.carousel-control-prev-banner,
.carousel-control-next-banner {
  z-index: 20; /* Aumenta el z-index para que estén encima de la imagen de portada */
  width: 50px; /* Ancho de los botones */
  opacity: 1; /* Opacidad inicial */
  background-color: rgba(255, 255, 255, 0); /* Fondo transparente */
  transition: background-color 0.3s;
  border: none; /* Eliminar el borde */
  outline: none; /* Eliminar el contorno que aparece al hacer clic */
}

.carousel-control-prev-banner:focus,
.carousel-control-next-banner:focus {
  outline: none; /* Asegúrate de que no haya contorno al enfocarlo */
}

/* Posicionamiento de los controles */
.carousel-control-prev-banner,
.carousel-control-next-banner {
  position: absolute; /* Asegúrate de que se posicione correctamente */
  top: 50%; /* Centrado vertical */
  transform: translateY(-50%); /* Ajuste para centrar verticalmente */
  opacity: 0.5;
}

/* Posición de los botones */
.carousel-control-prev-banner {
  left: 5px; /* Ajusta según sea necesario */
}

.carousel-control-next-banner {
  right: 5px; /* Ajusta según sea necesario */
}

.carousel-control-prev-banner:hover,
.carousel-control-next-banner:hover {
  opacity: 1; /* Cambio de color al pasar el mouse */
}

.carousel-control-next {
  z-index: 20; /* Aumenta el z-index para que estén encima de la imagen de portada */
  width: 50px;
  opacity: 0;
  border-top-right-radius: 20px;
  border-bottom-right-radius: 20px;
  background-color: rgba(255, 255, 255, 0); /* Fondo semi-transparente */
  transition: background-color 0.3s;
}

.carousel-control-prev {
  z-index: 20; /* Aumenta el z-index para que estén encima de la imagen de portada */
  width: 50px;
  opacity: 0;
  border-top-left-radius: 20px;
  border-bottom-left-radius: 20px;
  background-color: rgba(255, 255, 255, 0); /* Fondo semi-transparente */
  transition: background-color 0.3s;
}

.carousel-control-prev:hover,
    .carousel-control-next:hover {
        background-color: rgba(255, 255, 255, 0.1); /* Cambio de color al pasar el mouse */
        opacity: 1;
}


.carousel-indicators {
  position: absolute;
  z-index: 15; /* Asegúrate de que los indicadores estén por encima de otros elementos */
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
  position: absolute; /* Posiciona de forma absoluta */
  bottom: 50px; /* Distancia desde el fondo */
  left: 60px; /* Distancia desde el lado izquierdo */
  z-index: 10; /* Asegura que esté encima de la imagen del carrusel */
  display: flex; /* Usar flexbox para alinear la imagen y el texto */
  align-items: center; /* Centra verticalmente los elementos dentro de small-cover */
}

.small-cover-image {
  width: 250px !important; /* Cambia el tamaño aquí si lo deseas */
  height: 350px !important; /* Mantiene la proporción */
  border-radius: 15px; /* Bordes redondeados */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3); /* Sombra para un mejor contraste */
  margin-right: 20px; /* Espacio entre la imagen pequeña y la caja de texto */
}

.movie-info {
  background-color: rgba(0, 0, 0, 0.6); /* Fondo oscuro y más opaco */
  color: white; /* Color del texto */
  padding: 20px; /* Espaciado interno */
  border-radius: 10px; /* Bordes redondeados */
  width: 350px; /* Ancho mínimo de la caja */
  height: 350px; /* Altura mínima para la caja */
  display: flex; /* Usar flexbox para alinear el contenido */
  flex-direction: column; /* Organiza los elementos en columna */
  justify-content: flex-start; /* Alinea el contenido al inicio verticalmente */
  align-items: flex-start; /* Alinea el contenido a la izquierda horizontalmente */
  overflow: hidden; /* Asegura que el contenido no se desborde */
  text-align: left; /* Alinea el texto a la izquierda */
}

.movie-info h5 {
  margin: 0; /* Elimina el margen por defecto del encabezado */
  font-weight: bold;
}

.movie-info p {
  margin-top: 20px; /* Añade un margen entre el título y la descripción */
}

.rating-likes-banner {
  position: absolute;
  bottom: 50px;
  right: 40px;
  background-color: rgba(0, 0, 0, 0.6); /* Fondo oscuro semi-transparente */
  color: white;
  padding: 10px;
  border-radius: 10px;
  display: flex;
  gap: 10px; /* Espacio entre los elementos */
  align-items: center;
  z-index: 5; /* Asegura que se muestre sobre otros elementos */
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
  width: 20px !important; /* Ajusta el tamaño según tus necesidades */
  height: 20px !important;
  margin-right: 5px; /* Espacio entre la imagen y el número */
}

.recent-movies, .top-rated-movies {
  padding: 40px 20px;
  text-align: center;
  background-color: #121212; /* Color de fondo para diferenciar secciones */
  margin: 10px 0; /* Margen entre secciones */
  padding-left: 50px; /* Espacio desde la izquierda para toda la sección */
}

.movie-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); /* Grid responsivo */
  gap: 50px; /* Espacio entre elementos */
  margin-left: 0; /* Asegura que no haya margen adicional a la izquierda */
}

.section-title {
  color: white; /* Cambia el color del texto */
  font-size: 20px; /* Cambia el tamaño de la fuente */
  text-align: left; /* Cambia la alineación (izquierda, centro, derecha) */
  margin-left: 0px; /* Agrega margen a la izquierda si es necesario */
  margin-bottom: 20px; /* Agrega margen abajo para separarlo de la cuadrícula */
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
  background-color: rgba(0, 0, 0, 0.6); /* Fondo oscuro semi-transparente */
  color: white;
  padding: 10px;
  border-radius: 10px;
  display: flex;
  gap: 2px; /* Espacio entre los elementos */
  align-items: center;
  z-index: 5; /* Asegura que se muestre sobre otros elementos */
}


/* Estilo para el carrusel */
.carousel-item {
  justify-content: flex-start; /* Alinear a la izquierda (o cambiar a center si prefieres) */
  align-items: flex-start; /* Alinea las películas al inicio */
}

/* Estilo para cada película dentro del carrusel */
.movie-item {
  width: 250px; /* Ajusta al tamaño deseado */
  height: 350px; /* Mantiene la proporción de la imagen */
  flex-direction: column; /* Apila el contenido verticalmente */
  align-items: center; /* Centra horizontalmente */
  background-color: rgba(0, 0, 0, 0.2); /* Cambia el color de fondo */
  border-radius: 20px; /* Bordes redondeados para que coincidan con el poster */

  transition: transform 0.3s;
  position: relative; /* Asegura que los elementos dentro se posicionen relativos a este */
}

/* Estilo para la imagen de la película */
.movie-poster {
  width: 100% ; /* Asegúrate de que ocupen todo el ancho del contenedor */
  height: 350px !important; /* Mantiene la proporción de la imagen */
  border-radius: 20px; /* Bordes redondeados */
}

</style>
  