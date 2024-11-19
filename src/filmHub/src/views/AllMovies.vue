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
                        <li v-for="genre in paginatedGenres" :key="genre.id" @click="selectGenre(genre.type)"
                            class="dropdown-item">
                            {{ genre.type }}
                        </li>
                        <li v-if="canShowMoreGenres" @click="nextGenrePage()" class="dropdown-more">
                            Show more...
                        </li>
                        <li v-if="canShowLessGenres" @click="previousGenrePage()" class="dropdown-more">
                            Show previous...
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
                <!-- Itera sobre las filas de películas (5 por fila) -->
                <div v-for="(row, index) in sortedMovies" :key="index" class="inner-container">
                    <!-- Mostrar cada película en una fila -->
                    <div v-for="movie in row" :key="movie.id" class="movie-item">
                        <!-- Imagen de la película -->
                        <div class="movie-poster-wrapper">
                            <!-- Contenedor para el rating y los likes -->
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
                            <img :src="movie.smallImage" :alt="movie.title" class="movie-poster" />
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Pie de Página -->
        <footer class="footer">
            <p>&copy; 2024 FilmHub Enterpise. All rights reserved.</p>
            <div class="socials">
                <a href="#">FilmHub Enterpise</a>
            </div>
        </footer>
    </div>
</template>



<script>
import HeaderPage from '@/components/HeaderPage.vue'; // Importa el componente HeaderPage
import axios from 'axios';
import { API_BASE_URL } from '@/config.js'; // Importa tu archivo de configuración

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
        likes: movieData.likes
    };

    return movieObject;
}

export default {
    name: 'AllMoviesVew',
    components: {
        HeaderPage,
    },
    data() {
        return {
            sortedMovies: [],
            dropdowns: { genre: false, year: false, },
            genres: [], // Géneros obtenidos del backend
            currentGenrePage: 0,
            genresPerPage: 5,
            years: Array.from({ length: 2024 - 2007 + 1 }, (_, i) => 2007 + i),
            selectedGenre: '', // Almacena el género seleccionado
            selectedYear: '', // Almacena el año seleccionado
        }
    }, computed: {
        paginatedGenres() {
            const start = this.currentGenrePage * this.genresPerPage;
            const end = start + this.genresPerPage;
            return this.genres.slice(start, end);
        },
        canShowMoreGenres() {
            return (this.currentGenrePage + 1) * this.genresPerPage < this.genres.length;
        },
        canShowLessGenres() {
            return this.currentGenrePage > 0;
        },
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
            this.dropdowns[type] = !this.dropdowns[type];
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
        nextGenrePage() {
            if (this.canShowMoreGenres) this.currentGenrePage++;
        },
        previousGenrePage() {
            if (this.canShowLessGenres) this.currentGenrePage--;
        },

        // Método para aplicar el filtro según el criterio de ordenacion
        async applySorting(criteria, resetSelectedYear = false) {
            try {
                let url;

                if (resetSelectedYear) {
                    this.selectedYear = ""; // Reinicia el año seleccionado
                }

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
                    if (!searchQuery) {
                        console.error("No search query provided!");
                        return;
                    }
                    url = `${API_BASE_URL}/movies/search/name/${searchQuery}`;
                } else if (criteria === "genre" && this.selectedGenre) {
                    url = `${API_BASE_URL}/movies/genre/${this.selectedGenre}`;
                } else {
                    url = `${API_BASE_URL}/movies/`;
                }

                const response = await axios.get(url);
                const movies = response.data;

                const processedMovies = await Promise.all(
                    movies.map(async (movieData) => {
                        return await generateMovieObject(movieData);
                    })
                );

                this.sortedMovies = this.chunkMovies(processedMovies, 5);

                console.log(`Movies filtered by ${criteria}:`, this.sortedMovies);
            } catch (error) {
                console.error("Error retrieving movies:", error);
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
    beforeRouteUpdate(to, from, next) {
        const searchQuery = to.query.search;
        const sortByYear = this.$route.query.sortByYear;
        const sortByRate = this.$route.query.sortByRate;
        if (searchQuery) {
            this.applySorting("search");
        } else if (sortByYear) {
            this.applySorting("year");
        } else if (sortByRate) {
            this.applySorting("rating");
        } else {
            this.applySorting("");//Si se aprieta el boton allMove se recarga la pagina con la informacion inicial
        }
        next(); //llamar a next() para que la navegación continúe
    },
    watch: {
        // Observar los cambios en el parámetro 'search' en la URL
        "$route.query.search": function (newSearchQuery, oldSearchQuery) {
            if (newSearchQuery !== oldSearchQuery) {
                this.applySorting("search"); // Ejecutar la búsqueda cada vez que cambie el parámetro 'search'
            }
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
    width: calc(100% - 200px);
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
    /* Altura total menos el header */
    background-color: #f8f9fa;
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
    /* Deja espacio para el header */
    width: 100%;
    /* Ajusta el ancho disponible después de la barra vertical */
    background-color: #121212;

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
    
    object-fit: cover;
    /* Hace que la imagen se recorte bien si es necesario */
    opacity: 1;

    height: auto;
    border-radius: 10px;
    height: 350px; /* Establecer altura fija */
    object-fit: cover; /* Asegurarse de que la imagen se recorte adecuadamente si es necesario */
    width: 100%; /* Mantener la proporción */
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
    display: flex;
    flex: 1;
    /* Ocupa el resto del espacio después del header */
    background-color: #161616;
}

.footer {
    background-color: #161616;
    color: white;
    text-align: center;
    padding: 20px;
    z-index: 5;
}


/* Contenedor de rating y likes en una línea */
.rating-likes-inline {
    position: absolute;
    top: 10px;
    left: 10px;
    background-color: rgba(0, 0, 0, 0.7);
    /* Fondo semitransparente */
    color: white;
    padding: 5px 10px;
    border-radius: 10px;
    display: flex;
    /* Cambiado para alinear en línea */
    gap: 10px;
    /* Espacio entre el rating y los likes */
    align-items: center;
    /* Asegura que estén alineados verticalmente */
    z-index: 10;
    /* Asegura que esté sobre la imagen */
}

/* Estilo para el rating y los likes */
.rating-likes-inline .rating,
.rating-likes-inline .likes {
    display: flex;
    align-items: center;
    gap: 5px;
    /* Espacio entre el ícono y el texto */
}



.inner-container {
    display: flex;
    justify-content: flex-start;
    /* Centrar contenido en filas incompletas */
    gap: 10px;
    /* Espaciado consistente entre elementos */
    flex-wrap: wrap;
    /* Permitir que los elementos se ajusten */
}



.movie-poster-wrapper {
    position: relative;
    
}

.rating-likes-inline {
    position: absolute;
    top: 10px;
    left: 10px;
    background-color: rgba(0, 0, 0, 0.5);
    color: white;
    padding: 5px;
    border-radius: 5px;
    object-fit: contain;
    width:16px;
    height:16px;
}

.icon {
    width: 16px;
    height: 16px;
    margin-right: 5px;
}


</style>
