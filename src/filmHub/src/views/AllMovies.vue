<template>
    <div class="home-page">
        <HeaderPage :isOpaque="true" /> <!-- Aquí importas y usas el componente HeaderPage -->

        <div class="container-wrapper">
            <!-- Barra vertical -->
            <section class="vertical-bar">
                <h3>Order by:</h3>
                <!-- Botones para ordenar por Rating, Year y Popularity -->

                <button @click="applySorting('rating')">Rating</button>
                <button @click="applySorting('year', true)">Year</button>
                <button @click="applySorting('popularity')">Popularity</button>

            </section>

            <section class="horizontal-bar">
                <!-- Botón desplegable para "Genre" -->
                <div class="dropdown">
                    <button class="dropdown-button" @click="toggleDropdown('genre')">Genre</button>
                    <ul v-show="dropdowns.genre" class="dropdown-menu">
                        <li v-for="genre in genres" :key="genre.id" @click="selectGenre(genre.type)"
                            class="dropdown-item">
                            {{ genre.type }}
                        </li>
                    </ul>
                </div>

                <!-- Botón desplegable para "Year Release" -->
                <div class="dropdown">
                    <button class="dropdown-button" @click="toggleDropdown('year')">Year Release</button>
                    <ul v-show="dropdowns.year" class="dropdown-menu">
                        <li v-for="year in years" :key="year" @click="selectYear(year)" class="dropdown-item">
                            {{ year }}
                        </li>
                    </ul>
                </div>
            </section>

            <div class="main-container">
                <!-- Itera sobre las filas de películas (6 por fila) -->
                <div v-for="(row, index) in sortedMovies" :key="index" class="inner-container">
                    <!-- Mostrar cada película en una fila -->
                    <div v-for="movie in row" :key="movie.id" class="movie-card">
                        <!-- Envolvemos toda la tarjeta en un router-link -->
                        <router-link :to="`/movie/${movie.id}`" class="movie-link">
                            <!-- Imagen de la película -->
                            <div class="movie-poster-wrapper">
                                <img :src="movie.smallImage" :alt="movie.title" class="movie-poster" />
                            </div>

                            <!-- Contenedor blanco con la información -->
                            <div class="movie-info">
                                <p class="movie-title">{{ movie.title }}</p>

                                <div class="rating-likes-inline">
                                    <div class="rating">
                                        <img src="@/assets/star.png" alt="Rating star" class="icon" />
                                        <span>{{ movie.rating }}</span>
                                    </div>
                                    <div class="likes">
                                        <img src="@/assets/like.png" alt="Like icon" class="icon" />
                                        <span>{{ movie.likes }}</span>
                                    </div>
                                </div>

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
    // Comprobar si la imagen es una URL
    if (image && image.startsWith('http')) {
        return image; // Retorna la URL tal cual
    } else if (image) {
        // Retorna la ruta de la imagen en assets
        try {
            return require(`@/assets/${image}`);
        } catch (error) {
            console.error(`Error loading local image: ${image}`, error);
            return ''; // Retorna una cadena vacía en caso de error
        }
    } else {
        console.warn('No image provided');
        return ''; // Retorna una cadena vacía si no hay imagen
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
            dropdowns: { genre: false, year: false, },
            genres: [], // Géneros obtenidos del backend
            years: Array.from({ length: 2024 - 2007 + 1 }, (_, i) => 2007 + i),
            selectedGenre: '', // Almacena el género seleccionado
            selectedYear: '', // Almacena el año seleccionado
            cancelTokenSource: null,
        }
    },

    methods: {
        async fetchGenres() {
            try {
                const url = `${API_BASE_URL}/genres/`; // Endpoint del backend para obtener géneros
                const response = await axios.get(url);
                this.genres = response.data; // El backend retorna un array de géneros
                console.log("Fetched genres:", this.genres);
            } catch (error) {
                console.error("Error fetching genres:", error);
            }
        },
        toggleDropdown(type) {
            if (type === 'genre') {
                this.dropdowns.year = false; // Close the "year" dropdown
            } else if (type === 'year') {
                this.dropdowns.genre = false; // Close the "genre" dropdown
            }
            this.dropdowns[type] = !this.dropdowns[type];
        },
        handleClickOutside(event) {

            // Check if the click is outside the dropdowns
            const dropdownsElements = document.querySelectorAll('.dropdown');  // Select all dropdowns
            let clickInsideDropdown = false;

            // Loop through each dropdown and check if the click is inside
            dropdownsElements.forEach((dropdown) => {
                if (dropdown.contains(event.target)) {
                    clickInsideDropdown = true;
                }
            });

            // If the click is outside all dropdowns, close them
            if (!clickInsideDropdown) {
                this.dropdowns.genre = false;
                this.dropdowns.year = false;
            }
        },
        selectGenre(genre) {
            console.log(`Selected genre: ${genre}`);
            this.selectedGenre = genre; // Guarda el género seleccionado
            this.dropdowns.genre = false; // Cierra el desplegable
            this.applySorting('genre'); // Aplica el filtro por género
        },
        selectYear(year) {
            console.log(`Selected year: ${year}`);
            this.selectedYear = year; // Guarda el año seleccionado
            this.dropdowns.year = false; // Cierra el desplegable
            this.applySorting('year'); // Aplica el filtro por año
        },

        // Método para aplicar el filtro según el criterio de ordenacion
        async applySorting(criteria, resetSelectedYear = false) {
            try {
                let url;

                if (resetSelectedYear) {
                    this.selectedYear = ""; // Reset the selected year
                }

                if (this.cancelTokenSource) {
                    // Cancel the previous request if it exists
                    this.cancelTokenSource.cancel("Operation canceled due to new request.");
                }

                // Create a new cancellation token
                this.cancelTokenSource = axios.CancelToken.source();

                // Determine the API endpoint based on the criteria
                if (criteria === "rating") {
                    url = `${API_BASE_URL}/movies/sorted/rating/`;
                } else if (criteria === "year") {
                    if (this.selectedYear) {
                        url = `${API_BASE_URL}/movies/release/${this.selectedYear}`;
                    } else {
                        url = `${API_BASE_URL}/movies/sorted/release_date/`;
                    }
                } else if (criteria === "popularity") {
                    url = `${API_BASE_URL}/movies/sorted/likes/`;
                } else if (criteria === "search") {
                    const searchQuery = this.$route.query.search;
                    url = `${API_BASE_URL}/movies/search/name/${searchQuery}`;
                } else if (criteria === "genre" && this.selectedGenre) {
                    url = `${API_BASE_URL}/movies/genre/${this.selectedGenre}`;
                } else {
                    url = `${API_BASE_URL}/movies/`;
                }

                // Make the API call with the cancel token
                const response = await axios.get(url, {
                    cancelToken: this.cancelTokenSource.token,
                });

                const movies = response.data;

                const processedMovies = await Promise.all(
                    movies.map(async (movieData) => {
                        return await generateMovieObject(movieData);
                    })
                );

                this.sortedMovies = this.chunkMovies(processedMovies, 6);

                console.log(`Movies filtered by ${criteria}:`, this.sortedMovies);
            } catch (error) {
                if (axios.isCancel(error)) {
                    console.log("Previous request canceled:", error.message);
                } else {
                    console.error("Error retrieving movies:", error);
                }
            } finally {
                // Reset the cancel token source after the request completes
                this.cancelTokenSource = null;
            }
        },


        // Función auxiliar para dividir el array en filas de 5
        chunkMovies(movies, size) {
            const result = [];
            for (let i = 0; i < movies.length; i += size) {
                result.push(movies.slice(i, i + size)); // Divide las películas en subarrays de tamaño 5
            }
            return result;
        },

    },
    async mounted() {
        document.addEventListener('click', this.handleClickOutside);
        // Detecta si hay un término de búsqueda al cargar la página sino muestra todas las pelis sin ningun orden especifico
        const searchQuery = this.$route.query.search;
        const sortByYear = this.$route.query.sortByYear;
        const sortByRate = this.$route.query.sortByRate;
        if (searchQuery) {
            this.applySorting("search");
        } else if (sortByYear) {
            this.applySorting("year");
        } else if (sortByRate) {
            this.applySorting("rating");
        } else {
            this.applySorting("");
        }
        await this.fetchGenres(); // Cargar géneros al montar el componente
    },
    //Mounted solo se ejecuta cuandoe l componente se monta por primera vez
    //Mejor usar watcher o beforeRouterUpdate, para reaccionar a los cambios de la url y ejecutar el codigo de búsqueda cada vez que el parámetro search cambia
    beforeRouteUpdate(to) {
        const searchQuery = to.query.search;
        const sortByYear = to.query.sortByYear;
        const sortByRate = to.query.sortByRate;

        if (searchQuery) {
            this.applySorting("search");
        } else if (sortByYear) {
            this.applySorting("year");
        } else if (sortByRate) {
            this.applySorting("rating");
        } else {
            this.applySorting(""); // Si no hay filtros, mostrar todas las películas
        }
    }
    ,
    beforeUnmount() {
        document.removeEventListener('click', this.handleClickOutside);
    },
    watch: {
        "$route.query.search": {
            handler: debounce(function (newSearchQuery) {
                if (newSearchQuery) {
                    this.applySorting("search");
                }
            }, 300), // 300ms de espera antes de ejecutar la búsqueda
            immediate: true, // Si quieres ejecutar el watcher al montarse
        },
        '$route.query.sortByYear'(newSortByYear) {
            if (newSortByYear) {
                this.applySorting("year");
            }
        },
        '$route.query.sortByRate'(newSortByRate) {
            if (newSortByRate) {
                this.applySorting("rating");
            }
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
    /* Ancho total menos la barra vertical */
    height: 115px;
    z-index: 999;
    /* Asegura que esté sobre el contenido, pero debajo del header */
    background-color: #121212;
    color: #fff;
    padding: 10px 20px;
    box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.2);
}

.dropdown {
    position: relative;
    /* Para posicionar el menú desplegable */
    margin: 0 10px;
}

.dropdown-button {
    background-color: rgba(255, 255, 255, 0.1);
    width: 100%;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 8px 12px;
    cursor: pointer;
    font-size: 16px;
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
    /* Alinea los elementos verticalmente */
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

}

.vertical-bar h3 {
    margin: 0;
    font-size: 18px;
    color: white;
    border-bottom: 1px solid #ccc;
    padding-bottom: 10px;
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
    padding: 20px;
    flex: 1;
    overflow-y: auto;
    box-sizing: border-box;
    margin-left: 200px;
    /* Deja espacio para la barra vertical de 200px más el padding */
    margin-top: 185px;
    max-width: 80%;
    flex-wrap: wrap;
}

/* Estilo para cada película dentro de la fila */
.movie-item {
    width: 200px;
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
    background-color: #161616;
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
    gap: 0.6rem;
    /* Centrar contenido en filas incompletas */
    flex-wrap: wrap;
    /* Permitir que los elementos se ajusten */
    display: flex;
    width: 96%;
}

.movie-card {
    width: 14rem;
    /* Reducir el ancho de las cartas */
    background-color: #000000;
    border-radius: 10px;
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
</style>
