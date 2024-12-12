<template>
    <div class="home-page">
        <HeaderPage :isOpaque="true" /> <!-- Aquí importas y usas el componente HeaderPage -->

        <div class="container-wrapper">
            <!-- Barra vertical -->
            <section class="vertical-bar">
                <h3>Order by:</h3>
                <!-- Switches para ordenar por Rating, Year y Popularity -->
                <div class="sort-option">
                    <div class="sort-row">
                        <span>Rating</span>
                        <label class="switch">
                            <input type="checkbox" @change="applySwitchSorting('rating', $event)" />
                            <span class="slider"></span>
                        </label>
                    </div>
                    <div class="sort-row">
                        <span>Date</span>
                        <label class="switch">
                            <input type="checkbox" @change="applySwitchSorting('year', $event)" />
                            <span class="slider"></span>
                        </label>
                    </div>
                    <div class="sort-row">
                        <span>Popularity</span>
                        <label class="switch">
                            <input type="checkbox" @change="applySwitchSorting('popularity', $event)" />
                            <span class="slider"></span>
                        </label>
                    </div>
                </div>
            </section>

            <section class="horizontal-bar">
                <!-- Botón desplegable para "Genre" -->
                <div class="dropdown">
                    <button class="dropdown-button" @click="toggleDropdown('genre')">{{ selectedGenre || 'Genre' }}</button>
                    <ul v-show="dropdowns.genre" class="dropdown-menu">
                        <li v-for="genre in genres" :key="genre.id" @click="selectGenre(genre.type)"
                            class="dropdown-item">
                            {{ genre.type }}
                        </li>
                    </ul>
                </div>

                <!-- Botón desplegable para "Year Release" -->
                <div class="dropdown">
                    <button class="dropdown-button" @click="toggleDropdown('year')">{{ selectedYear || 'Release Year' }}</button>
                    <ul v-show="dropdowns.year" class="dropdown-menu">
                        <li v-for="year in years" :key="year" @click="selectYear(year)" class="dropdown-item">
                            {{ year }}
                        </li>
                    </ul>
                </div>
            </section>

            <div class="main-container">
                <!-- Itera sobre las filas de películas (5 por fila) -->
                <div v-for="(row, index) in sortedMovies" :key="index" class="inner-container">
                    <!-- Mostrar cada película en una fila -->
                    <div v-for="movie in row" :key="movie.id" class="movie-card">
                        <!-- Envolvemos toda la tarjeta en un router-link -->
                        <router-link :to="`/movie/${movie.id}`" class="movie-link">
                            <!-- Imagen de la película -->
                            <div class="movie-poster-wrapper">
                                <img :src="movie.smallImage" :alt="movie.title" class="movie-poster" />
                            </div>

                            <!-- Wishlist Indicator-->
                            <div v-if="wishedMovies.includes(movie.title)" class="wishlist-indicator">

                                <svg viewBox="0 0 32 32" class="wishlist-icon">
                                <g>
                                    <path
                                    d="M27 4v27a1 1 0 0 1-1.625.781L16 24.281l-9.375 7.5A1 1 0 0 1 5 31V4a4 4 4 4 1 4-4h14a4 4 4 0 1 4 4z"
                                    ></path>
                                </g>
                                </svg>
                            </div>

                            <div class="rating-likes-inline">
                                <div class="rating">
                                    <img src="@/assets/star.png" alt="Rating star" class="icon" />
                                    <span>{{ movie.rating.toFixed(1) }}</span>
                                </div>
                                <div class="likes">
                                    <img src="@/assets/like.png" alt="Like icon" class="icon" />
                                    <span>{{ movie.likes }}</span>
                                </div>
                            </div>

                            <!-- Contenedor blanco con la información -->
                            <div class="movie-info">
                                <p class="movie-title">{{ movie.title }}</p>

                                <!-- Nueva fila para mostrar el género -->
                                <p class="genre">{{ movie.genre }}</p>
                                <p class="release-date">{{ movie.releaseDate }}</p>
                            </div>
                        </router-link>
                    </div>
                </div>
            </div>
        </div>

        <FooterComponent />
    </div>
</template>



<script>
import HeaderPage from '@/components/HeaderPage.vue'; // Importa el componente HeaderPage
import axios from 'axios';
import { API_BASE_URL } from '@/config.js'; // Importa tu archivo de configuración
import FooterComponent from '@/components/FooterComponent.vue';

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

async function generateMovieObject(movieData) {
    const movieObject = {
        id: movieData.id,
        image: getImagePath(movieData.image[1]),
        smallImage: getImagePath(movieData.image[0]),
        title: movieData.title,
        description: movieData.description,
        rating: movieData.rating,
        likes: movieData.likes,
        genre: movieData.genres.map(genre => genre.type).join(', '),
        releaseDate: movieData.release_date.substring(0, 4),
    };

    return movieObject;
}

function debounce(func, wait) {
    let timeout;
    return function (...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

export default {
    name: 'AllMovies',
    components: {
        HeaderPage,
        FooterComponent,
    },
    data() {
        return {
            sortedMovies: [],
            dropdowns: { genre: false, year: false },
            genres: [],
            years: Array.from({ length: 2024 - 2007 + 1 }, (_, i) => 2007 + i),
            selectedGenre: '',  // Aquí se guarda el género seleccionado
            selectedYear: '',   // Aquí se guarda el año seleccionado
            cancelTokenSource: null,
            activeSorting: '', // Almacena el criterio de orden activo (rating, year, popularity)
            wishedMovies: [], // Lista de películas deseadas
            userId: localStorage.getItem('user_id'), // ID del usuario
            selectedDirector: null, //Para mostrar las peliculas por Director
            selectedActor: null,
        };
    },
    methods: {
        async fetchGenres() {
            try {
                const url = `${API_BASE_URL}/genres/`;
                const response = await axios.get(url);
                this.genres = response.data;
                console.log("Fetched genres:", this.genres);
            } catch (error) {
                console.error("Error fetching genres:", error);
            }
        },
        toggleDropdown(type) {
            if (type === 'genre') {
                this.dropdowns.year = false;
            } else if (type === 'year') {
                this.dropdowns.genre = false;
            }
            this.dropdowns[type] = !this.dropdowns[type];
        },
        handleClickOutside(event) {
            const dropdownsElements = document.querySelectorAll('.dropdown');
            let clickInsideDropdown = false;

            dropdownsElements.forEach((dropdown) => {
                if (dropdown.contains(event.target)) {
                    clickInsideDropdown = true;
                }
            });

            if (!clickInsideDropdown) {
                this.dropdowns.genre = false;
                this.dropdowns.year = false;
            }
        },
        selectGenre(genre) {
            document.querySelectorAll('.switch input').forEach(input => {
                if (input !== event.target) {
                    input.checked = false;
                }
            });
            
            console.log(`Selected genre: ${genre}`);
            this.selectedGenre = genre;
            this.selectedYear = '';  // Resetear el filtro de año
            this.dropdowns.genre = false;
            this.applySorting('genre');
        },
        selectYear(year) {
            document.querySelectorAll('.switch input').forEach(input => {
                if (input !== event.target) {
                    input.checked = false;
                }
            });

            console.log(`Selected year: ${year}`);
            this.selectedYear = year;
            this.selectedGenre = '';  // Resetear el filtro de género
            this.dropdowns.year = false;
            this.applySorting('year');
        },
        applySwitchSorting(criteria, event) {
            document.querySelectorAll('.switch input').forEach(input => {
                if (input !== event.target) {
                    input.checked = false;
                }
            });

            if (event.target.checked) {
                this.activeSorting = criteria;
                this.selectedGenre = '';
                this.selectedYear = ''; 
                this.applySorting(criteria);
            } else {
                this.activeSorting = '';
                this.applySorting(''); 
            }
        },

        async filterMoviesByDirector(movies, directorName) {
            try {
                // Filtrar las películas por el nombre del director
                let directorMovies = [];
                for (const movie of movies){
                    if (movie.director === directorName){
                        directorMovies.push(movie);
                    }
                }
                return directorMovies;
            } catch (error) {
                console.error("Error filtering movies by director:", error);
                return [];
            }
        },

        async filterMoviesByActor(movies, actorName) {
            try {
                // Filtrar las películas por el nombre del actor
                let actorMovies = [];
                for (const movie of movies){
                    for (const actor of movie.cast_members){
                        if (actor.name === actorName){
                            actorMovies.push(movie);
                        }
                    }
                }
                return actorMovies;
            } catch (error) {
                console.error("Error filtering movies by director:", error);
                return [];
            }
        },

        
        async applySorting(criteria, resetSelectedYear = false) {
            try {
                let url;

                if (resetSelectedYear) {
                    this.selectedYear = '';
                }

                if (this.cancelTokenSource) {
                    this.cancelTokenSource.cancel("Operation canceled due to new request.");
                }
                this.cancelTokenSource = axios.CancelToken.source();

                if ((criteria === 'director' && this.selectedDirector) || (criteria === 'actor' && this.selectedActor)){
                    url = `${API_BASE_URL}/movies`;
                }else if (criteria === 'rating') {
                    url = `${API_BASE_URL}/movies/sorted/rating`;
                } else if (criteria === 'year') {
                    if (this.selectedYear) {
                        url = `${API_BASE_URL}/movies/release/${this.selectedYear}`;
                    } else {
                        url = `${API_BASE_URL}/movies/sorted/release_date`; // Aquí usas la URL por año
                    }
                } else if (criteria === 'popularity') {
                    url = `${API_BASE_URL}/movies/sorted/likes`;
                } else if (criteria === 'search') {
                    const searchQuery = this.$route.query.search;
                    url = `${API_BASE_URL}/movies/search/name/${searchQuery}`;
                } else if (criteria === 'genre' && this.selectedGenre) {
                    url = `${API_BASE_URL}/movies/genre/${this.selectedGenre}`;
                } else {
                    url = `${API_BASE_URL}/movies/`;
                }

                const response = await axios.get(url, {
                    cancelToken: this.cancelTokenSource.token,
                });

                let movies = response.data;

                if (criteria === 'director'){
                    // Filtra las películas por director
                    movies = await this.filterMoviesByDirector(movies, this.selectedDirector);
                }else if(criteria === 'actor'){
                    movies = await this.filterMoviesByActor(movies, this.selectedActor);
                }


                if (criteria === 'year') {
                    // Invertir el orden si estamos ordenando por año
                    movies = movies.reverse(); // Aquí invertimos el array
                }

                const processedMovies = await Promise.all(
                    movies.map(async (movieData) => {
                        return await generateMovieObject(movieData);
                    })
                );

                this.sortedMovies = this.chunkMovies(processedMovies, 5);

                console.log(`Movies filtered by ${criteria}:`, this.sortedMovies);
            

            } catch (error) {
                if (axios.isCancel(error)) {
                    console.log("Previous request canceled:", error.message);
                } else {
                    console.error("Error retrieving movies:", error);
                }
            } finally {
                this.cancelTokenSource = null;
            }
        },
        chunkMovies(movies, size) {
            const result = [];
            for (let i = 0; i < movies.length; i += size) {
                result.push(movies.slice(i, i + size));
            }
            return result;
        },
        async loadUserPreferences() {
        try {
          if (!this.userId) {
            console.error('User ID not found.');
            return;
          }
          const endpoint = `${API_BASE_URL}/movies/liked_rated_and_wished_list/${this.userId}`;
          const response = await axios.get(endpoint);

          const data = response.data;

          // Procesar películas en la wishlist
          this.wishedMovies = data.wished_movies || [];

          console.log('Wished Movies:', this.wishedMovies);

        } catch (error) {
          console.error('Error loading user preferences:', error.response?.data || error.message);
        }
      },
    },
    async mounted() {
        this.loadUserPreferences();
        document.addEventListener('click', this.handleClickOutside);
        const searchQuery = this.$route.query.search;
        const sortByYear = this.$route.query.sortByYear;
        const sortByRate = this.$route.query.sortByRate;
        const directorName = this.$route.query.director;
        const actorName = this.$route.query.actor;

        if (searchQuery) {
            this.applySorting('search');
        } else if (sortByYear) {
            this.applySorting('year');
        } else if (sortByRate) {
            this.applySorting('rating');
        } else if (directorName) {
            this.applySorting('director');
        }else if (actorName) {
            this.applySorting('actor');
        }else {
            this.applySorting('');
        }
        await this.fetchGenres();
    },
    beforeRouteUpdate(to) {
        const searchQuery = to.query.search;
        const sortByYear = to.query.sortByYear;
        const sortByRate = to.query.sortByRate;

        if (searchQuery) {
            this.applySorting('search');
        } else if (sortByYear) {
            this.applySorting('year');
        } else if (sortByRate) {
            this.applySorting('rating');
        } else {
            this.applySorting('');
        }
    },
    beforeUnmount() {
        document.removeEventListener('click', this.handleClickOutside);
    },
    watch: {
        '$route.query.search': {
            handler: debounce(function (newSearchQuery) {
                if (newSearchQuery) {
                    this.applySorting('search');
                }
            }, 300),
            immediate: true,
        },
        '$route.query.sortByYear'(newSortByYear) {
            if (newSortByYear) {
                this.applySorting('year');
            }
        },
        '$route.query.sortByRate'(newSortByRate) {
            if (newSortByRate) {
                this.applySorting('rating');
            }
        },
        '$route.query.sortByPopularity'(newSortByPopularity) {
            if (newSortByPopularity) {
                this.applySorting('popularity');
            }
        },
        '$route.query.genre': {
            immediate: true,
            handler(newGenre) {
                if (newGenre) {
                    this.selectedGenre = newGenre;
                    this.$nextTick(() => {
                        this.applySorting('genre'); // Aplicar filtro solo después de actualizar selectedGenre
                    });
                }
            },
        },
        '$route.query.director': {
            immediate: true,
            handler(newDirector) {
            if (newDirector) {
                console.log(`Filtering by director: ${newDirector}`);
                this.selectedDirector = newDirector;
                this.applySorting('director');
            }
            },
        },
        '$route.query.actor': {
            immediate: true,
            handler(newActor) {
            if (newActor) {
                console.log(`Filtering by director: ${newActor}`);
                this.selectedActor = newActor;
                this.applySorting('actor');
            }
            },
        },



    },
};
</script>




    


<style scoped>

.horizontal-bar {
    position: fixed;
    top: 70px;
    /* Justo debajo del header */
    left: 200px;
    /* Ajuste después de la barra vertical */
    width: calc(100% - 12rem);
    gap: 150px; 
    /* Ancho total menos la barra vertical */
    height: 80px; /* Reducimos la altura para un diseño más compacto */
    z-index: 999;
    /* Asegura que esté sobre el contenido, pero debajo del header */
    background-color: #121212;
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    gap: 10px; /* Espaciado entre botones */
    padding: 10px 20px;
    box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.2);
    border-bottom: 1px solid #ccc;
}

.dropdown {
    position: relative;
    margin: 20px; /* Eliminamos márgenes adicionales */
}

.dropdown-button {
    background-color: rgba(255, 255, 255, 0.1);
    color: white;
    border: none;
    border-radius: 4px;
    padding: 10px 15px; /* Botones más pequeños */
    font-size: 14px; /* Texto más pequeño */
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.dropdown-button:hover {
    background-color: rgba(255, 255, 255, 0.2);
}

.dropdown-menu {
    max-height: 10rem;
    overflow-y: auto;
    position: absolute;
    top: 100%;
    /* Muestra el menú debajo del botón */
    left: 0;
    background-color: #fff;
    color: #333;
    border: 1px solid #ddd;
    border-radius: 4px;
    box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.2);
    margin-top: 5px;
    z-index: 1000;
    list-style: none;
    padding: 10px 0;
    display: flex;
    flex-direction: column;
}


.dropdown-item {
    padding: 8px 12px;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.3s ease;
}

.dropdown-item:hover {
    background-color: #f0f0f0;
}

.dropdown-more {
    text-align: center;
    font-style: italic;
    color: #888;
    cursor: pointer;
}

@media (max-width: 768px) {
    .horizontal-bar {
        flex-direction: column;
        /* Acomoda los elementos en una columna en pantallas pequeñas */
        align-items: flex-start;
    }

    .dropdown {
        margin-bottom: 10px;
        /* Espaciado entre los botones desplegables */
    }
}


/* Estilo principal */
.vertical-bar {
    position: fixed;
    top: 70px;
    /* Altura del header */
    left: 0;
    width: 200px;
    height: 100vh;

    /* Fondo claro */
    padding: 20px;
    border-right: 1px solid #ccc;
    /* Línea vertical separadora */
    box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
    gap: 20px;
    /* Espaciado entre elementos */
    transition: width 0.3s ease;
    background-color: #121212;

}

.vertical-bar h3 {
    margin-top: 5px;
    font-size: 18px;
    color: white;
    padding-bottom: 20px;
}

button {
    width: 100%;
    padding: 10px;
    margin-bottom: 10px;
    font-size: 16px;
    background-color: rgba(255, 255, 255, 0.1);
    color: white;
    border: none;
    cursor: pointer;
    text-align: center;
    border-radius: 5px;
}

button:hover {
    background-color: rgba(255, 255, 255, 0.2);
}

/* Contenedor principal que organiza las filas */
.main-container {
    display: flex;
    flex-direction: column;
    /* Apilar las filas de manera vertical */
    gap: 20px;
    /* Espacio entre las filas */
    padding: 40px;
    flex: 1;
    overflow-y: auto;
    box-sizing: border-box;
    margin-left: 200px;
    /* Deja espacio para la barra vertical de 200px más el padding */
    margin-top: 150px;
    max-width: 100%;
    flex-wrap: wrap;
    background-color: #121212;
}

/* Estilo para cada película dentro de la fila */
.movie-item {
    width: 2    00px;
    /* Cada película ocupa el 18% del ancho del contenedor (5 películas por fila) */
    position: relative;
    /* Permite ajustar el contenido de la película */
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 20px;
    /* Bordes redondeados de cada película */
    transition: transform 0.3s ease;
    flex: 1 1 calc(20% - 10px);
    /* 5 columnas con un margen entre ellas */
    max-width: calc(20% - 10px);
    /* Asegurar un tamaño uniforme */
    box-sizing: border-box;

}

/* Estilo para las imágenes de las películas */
.movie-poster {
    opacity: 1;
    height: 100%;
    /* Establecer altura fija */
    object-fit: cover;
    /* Asegurarse de que la imagen se recorte adecuadamente si es necesario */
    width: 100%;
    /* Mantener la proporción */
}

.movie-info {
    padding: 20px 10px;
    /* Aumentamos el padding en la parte blanca para dar más espacio */
    background-color: #3a3a3a;
    text-align: left;
}

.movie-title {
    font-size: 1rem;
    font-weight: bold;
    margin-bottom: 10px;
    color: #eeeeee;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;

    /* Para manejar el desbordamiento del texto */
}


/* Efecto de hover sobre las imágenes */
.movie-item:hover {
    transform: scale(1.05);
    /* Aumenta ligeramente el tamaño de la imagen cuando se pasa el ratón por encima */
}


.home-page {
    margin: 0;
    padding: 0;
    height: 100vh;
    display: flex;
    flex-direction: column;
    /* El header se coloca en la parte superior, el contenido debajo */

}

.container-wrapper {
    justify-content: center;
    display: flex;
    flex: 1;
    /* Ocupa el resto del espacio después del header */
    background-color: #121212;
}

.rating-likes-inline {
    background-color: rgba(0, 0, 0, 0.5);
    position: absolute;
    top: 10px;
    left: 10px;
    color: white;
    padding: 0.5rem;
    border-radius: 10px;
    object-fit: contain;
    width: fit-content;
    height: fit-content;
    
}

.rating-likes-inline {
    display: flex;
    justify-content: space-between;
    /* Alineamos rating y likes a los extremos */
    margin-bottom: 10px;
}

/* Estilo para el rating y los likes */
.likes {
    margin-left: 10px;
    display: flex;
    font-weight: bold;
}

.rating {
    margin-right: 10px;
    display: flex;
    font-weight: bold;
}

.inner-container {

    display: flex;
    justify-content: flex-start;
    gap: 20px;
    /* Centrar contenido en filas incompletas */
    flex-wrap: wrap;
    /* Permitir que los elementos se ajusten */
    display: flex;
    width: 100%;
}

.movie-card {
    width: 230px;
    /* Reducir el ancho de las cartas */
    background-color: #000000;
    border-radius: 20px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    transition: transform 0.3s ease;
}


.movie-card:hover {
    transform: scale(1.05);
    /* Efecto de hover para agrandar la carta */
}

.movie-poster-wrapper {
    width: 100%;
    height: 19rem;
    /* Altura fija para la imagen */
    position: relative;
}


.icon {
    width: 18px;
    height: 18px;
    margin-right: 5px;
}

.genre {
    font-size: 0.9rem;
    color: #dadada;
    margin-bottom: 5px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.release-date {
    font-size: 0.9rem;
    color: #b6b6b6;
}

.movie-link {
    text-decoration: none;
    color: inherit;
}

.footer {
  z-index: 9999; /* El valor más alto para asegurarse de que esté por encima de otros elementos */
}



/* Contenedor de las opciones de ordenación */
.sort-option {
    display: flex;
    flex-direction: column; /* Organiza las filas de forma vertical */
    gap: 25px; /* Espaciado entre las filas */
    font-family: Arial, sans-serif;
    font-size: 1em;
    color: white;
}

/* Cada fila de texto y switch */
.sort-row {
    display: flex;
    align-items: center; /* Asegura que el texto y el botón estén alineados verticalmente */
    gap: 10px; /* Espaciado entre el texto y el botón */
}

/* Botones uniformemente alineados */
.sort-row button,
.sort-row .switch {
    margin-left: auto; /* Asegura que los botones tengan una posición consistente a la derecha */
    min-width: 50px; /* Opcional: Ajusta el ancho mínimo para mantener uniformidad */
}


/* Estilos del switch */
.switch {
    font-size: 17px;
    position: relative;
    display: inline-block;
    width: 3.5em;
    height: 2em;
}

.switch input {
    opacity: 0;
    width: 0;
    height: 0;
}

.slider {
    position: absolute;
    cursor: pointer;
    inset: 0;
    border: 2px solid #414141;
    border-radius: 50px;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.slider:before {
    position: absolute;
    content: "";
    height: 1.4em;
    width: 1.4em;
    left: 0.2em;
    bottom: 0.2em;
    background-color: white;
    border-radius: inherit;
    transition: all 0.4s cubic-bezier(0.23, 1, 0.320, 1);
}

.switch input:checked + .slider {
    box-shadow: 0 0 20px rgba(9, 117, 241, 0.8);
    border: 2px solid #0974f1;
}

.switch input:checked + .slider:before {
    transform: translateX(1.5em);
}

/* Indicador de wishlist */
.wishlist-indicator {
  position: absolute;
  top: -5px;
  right: 20px;
  display: flex; /* Centra el SVG si hay paddings */
  align-items: center;
  justify-content: center;
}

/* Escalar el icono */
.wishlist-icon {
  width: 40px; /* Aumenta el tamaño del icono */
  height: 40px;
  fill: #007bff; 
  opacity: 0.8;/* Azul para indicar que está en wishlist */

}

/* Sin hover ni interacción */
.wishlist-indicator:hover {
  cursor: default;
}


</style>
