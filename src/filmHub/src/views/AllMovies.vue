<template>
    <div class="home-page">
        <HeaderPage /> <!-- Aquí importas y usas el componente HeaderPage -->
        
        <div class="container-wrapper">
            <!-- Barra vertical -->
            <section class="vertical-bar">
                <h3>Order by:</h3>
                <!-- Botones para ordenar por Rating, Year y Popularity -->
                <button @click="applySorting('rating')">Rating</button>
                <button @click="applySorting('year')">Year</button>
                <button @click="applySorting('popularity')">Popularity</button>
            </section>

            <section class="horizontal-bar">
                <!-- Botón desplegable para "Genre" -->
                <div class="dropdown">
                    <button class="dropdown-button" @click="toggleDropdown('genre')">Genre</button>
                    <ul v-show="dropdowns.genre" class="dropdown-menu">
                        <li
                        v-for="genre in paginatedGenres"
                        :key="genre.id"
                        @click="selectGenre(genre.type)"
                        class="dropdown-item"
                        >
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
                    <li
                    v-for="year in years"
                    :key="year"
                    @click="selectYear(year)"
                    class="dropdown-item"
                    >
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
                        <img :src="movie.image" :alt="movie.title" class="movie-poster" />
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
        } else if(image){
            // Retorna la ruta de la imagen en assets
            try {
                return require(`@/assets/${image}`);
            } catch (error) {
                console.error(`Error loading local image: ${image}`, error);
                return ''; // Retorna una cadena vacía en caso de error
            }
        }else {
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
        name : 'AllMoviesVew',
        components:{
            HeaderPage,
        },
        data() {
            return{
                sortedMovies: [],
                dropdowns: {genre: false,year: false,},
                genres: [], // Géneros obtenidos del backend
                currentGenrePage: 0,
                genresPerPage: 5,
                years: Array.from({ length: 2024 - 2007 + 1 }, (_, i) => 2007 + i),
                selectedGenre: '', // Almacena el género seleccionado
                selectedYear: '', // Almacena el año seleccionado
            }
        },computed: {
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

        methods:{
            async fetchGenres(){
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
            async applySorting(criteria) {
                try {
                    let url;

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
            // Detecta si hay un término de búsqueda al cargar la página sino muestra odas las pelis sin ningun orden especifico
            const searchQuery = this.$route.query.search;
            if (searchQuery) {
                this.applySorting("search");
            }else{
                this.applySorting("");
            }
            await this.fetchGenres(); // Cargar géneros al montar el componente
        },
        //Mounted solo se ejecuta cuandoe l componente se monta por primera vez
        //Mejor usar watcher o beforeRouterUpdate, para reaccionar a los cambios de la url y ejecutar el codigo de búsqueda cada vez que el parámetro search cambia
        beforeRouteUpdate(to, from, next) {
            const searchQuery = to.query.search;
            if (searchQuery) {
                this.applySorting("search");
            }else{
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
        },

    };
</script>


<style scoped>

.horizontal-bar {
    position: fixed;
    top: 70px; /* Justo debajo del header */
    left: 200px; /* Ajuste después de la barra vertical */
    width: calc(100% - 200px); /* Ancho total menos la barra vertical */
    z-index: 999; /* Asegura que esté sobre el contenido, pero debajo del header */
    background-color: #333;
    color: #fff;
    padding: 10px 20px;
    box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.2);
}

.dropdown {
    position: relative; /* Para posicionar el menú desplegable */
    margin: 0 10px;
}

.dropdown-button {
    background-color: #444;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 8px 12px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.3s ease;
}
.dropdown-button:hover {
    background-color: #555;
}

.dropdown-menu {
    position: absolute;
    top: 100%; /* Muestra el menú debajo del botón */
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
    flex-direction: column; /* Alinea los elementos verticalmente */
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
        flex-direction: column; /* Acomoda los elementos en una columna en pantallas pequeñas */
        align-items: flex-start;
    }

    .dropdown {
        margin-bottom: 10px; /* Espaciado entre los botones desplegables */
    }
}


.movie-list-container {
  display: flex;
  justify-content: flex-start;
  margin-top: 20px;
}

.movie-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.movie-row {
  display: flex;
  justify-content: flex-start;
  gap: 20px;
}

.movie-item {
  width: 18%;
  text-align: center;
}

.movie-item img {
  width: 100%;
  height: auto;
  border-radius: 5px;
  cursor: pointer;
}

.movie-item img:hover {
  transform: scale(1.05); /* Efecto hover */
  transition: transform 0.3s ease;
}


/* Estilo principal */
.vertical-bar {
  position: fixed;
  top: 70px; /* Altura del header */
  left: 0;
  width: 200px;
  height: calc(100vh - 70px); /* Altura total menos el header */
  background-color: #f8f9fa; /* Fondo claro */
  padding: 20px;
  border-right: 1px solid #ccc; /* Línea vertical separadora */
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  gap: 20px; /* Espaciado entre elementos */
  transition: width 0.3s ease;
}

.vertical-bar h3 {
  margin: 0;
  font-size: 18px;
  color: #333;
  border-bottom: 1px solid #ccc;
  padding-bottom: 10px;
}

button {
    width: 100%;
    padding: 10px;
    margin-bottom: 10px;
    font-size: 16px;
    background-color: #007bff;
    color: white;
    border: none;
    cursor: pointer;
    text-align: center;
}

button:hover {
    background-color: #0056b3;
}
/* Contenedor principal que organiza las filas */
.main-container {
    margin-top: 200px; /* 70px del header + 50px de la barra horizontal */
    margin-left: 220px; /* 200px de la barra vertical + 20px extra */
    padding: 20px;
    width: calc(100% - 220px); /* Ancho restante después de la barra vertical */
    height: calc(100vh - 120px); /* Altura restante después del header y la barra horizontal */
    overflow-y: auto;
}
/* Estilo para las filas de películas */
.inner-container {
  display: flex;
  justify-content: space-between; /* Distribuir las películas uniformemente en una fila */
  gap: 10px; /* Espacio entre cada película */
  flex-wrap: wrap; /* Ajustar las películas en múltiples filas si es necesario */
  width: 100%; /* Asegura que las filas ocupen todo el ancho disponible */
}

/* Estilo para cada película dentro de la fila */
.movie-item {
  width: 18%; /* Cada película ocupa el 18% del ancho del contenedor (5 películas por fila) */
  box-sizing: border-box;
  position: relative; /* Permite ajustar el contenido de la película */
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Estilo para las imágenes de las películas */
.movie-poster {
  width: 100%; /* La imagen ocupa el 100% del espacio disponible */
  height: auto; /* Mantener la proporción de la imagen */
  border-radius: 8px; /* Bordes redondeados para las imágenes */
  object-fit: cover; /* Hace que la imagen se recorte bien si es necesario */
  transition: transform 0.3s ease; /* Efecto de transición al pasar el mouse */
}

/* Efecto de hover sobre las imágenes */
.movie-item:hover .movie-poster {
  transform: scale(1.05); /* Aumenta ligeramente el tamaño de la imagen cuando se pasa el ratón por encima */
}

/* Añadir un borde sutil a las imágenes de las películas */
.movie-item {
  border-radius: 10px; /* Bordes redondeados de cada película */
  overflow: hidden; /* Asegura que el contenido de la película no se desborde */
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); /* Sombra suave alrededor de cada película */
}



.home-page {
  margin: 0;
  padding: 0;
  height: 100vh;
  display: flex;
  flex-direction: column; /* El header se coloca en la parte superior, el contenido debajo */
}
/* Contenedor del contenido y barra horizontal */
.content-wrapper {
    margin-left: 200px; /* Espacio para la barra vertical */
    flex: 1;
    display: flex;
    flex-direction: column;
}

.footer {
  background-color: #161616;
  color: white;
  text-align: center;
  padding: 20px;
}



</style>

