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

    export default {
        name : 'AllMoviesVew',
        components:{
            HeaderPage,
        },
        data() {
            return{
                sortedMovies: [],
            }
        },
        methods:{
            // Método para aplicar el filtro según el criterio de ordenacion
            async applySorting(criteria) {
                try{
                    // Reiniciar la lista filtrada a las películas iniciales
                    
                    let url;

                    // Aplicar el filtro basado en el criterio
                    if (criteria === "rating") {
                        url = `${API_BASE_URL}/movies/sorted/rating/`;// Endpoint para ordenar por Rating
                    } else if (criteria === "year") {
                        url = `${API_BASE_URL}/movies/sorted/release_date/`; //Endpoint para ordenar por Year
                    } else if (criteria === "popularity") {
                        url = `${API_BASE_URL}/movies/sorted/likes/`; // Endpoint para ordenar por Popularity
                    } else if (criteria === "search"){
                        const searchQuery = this.$route.query.search; // Obtén el término de búsqueda de la URL
                        console.log("Search query detected(searchQuery):", searchQuery);
                        if (!searchQuery) {
                            console.error("No search query provided!");
                            return;
                        }url = `${API_BASE_URL}/movies/search/name/${searchQuery}`; //Endpoint de búsqueda
                        console.log("Search query detected(url):", url);
                    }

                    // Realizar la solicitud a la API
                    const response = await axios.get(url);

                    //Obtener películas ordenadas
                    const movies = response.data;
                    console.log("Resposne form search endpoint(respoonse.data):", response.data);

                    // Procesar las películas para construir objetos compatibles
                    const processedMovies = await Promise.all(
                        movies.map(async (movieData) => {
                            return await generateMovieObject(movieData); // Reutiliza tu función para procesar películas
                        })
                    );

                     // Dividir las películas en filas de 5
                    this.sortedMovies = this.chunkMovies(processedMovies, 5); // Llamada a la función que divide las películas en filas de 5

                    console.log(`Movies filtered by ${criteria}:`, this.sortedMovies);
                
                }catch (error) {
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
        mounted() {
            // Detecta si hay un término de búsqueda al cargar la página
            const searchQuery = this.$route.query.search;
            if (searchQuery) {
                this.applySorting("search");
            }
        },
        //Mounted solo se ejecuta cuandoe l componente se monta por primera vez
        //Mejor usar watcher o beforeRouterUpdate, para reaccionar a los cambios de la url y ejecutar el codigo de búsqueda cada vez que el parámetro search cambia
        beforeRouteUpdate(to, from, next) {
            const searchQuery = to.query.search;
            if (searchQuery) {
                this.applySorting("search");
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

.movie-list-container {
  display: flex;
  justify-content: flex-start;
  margin-top: 20px;
  background-color: #161616;
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
  height: 100vh; /* Altura total menos el header */
  background-color: #f8f9fa; /* Fondo claro */
  padding: 20px;
  border-right: 1px solid #ccc; /* Línea vertical separadora */
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  gap: 20px; /* Espaciado entre elementos */
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
    display: flex;
    flex-direction: column; /* Apilar las filas de manera vertical */
    gap: 20px;  /* Espacio entre las filas */
    padding: 20px;
    flex: 1;
    overflow-y: auto;
    box-sizing: border-box;
    margin-left: 220px; /* Deja espacio para la barra vertical de 200px más el padding */
    margin-top: 70px;  /* Deja espacio para el header */
    width: 100%;  /* Ajusta el ancho disponible después de la barra vertical */
    background-color: rgb(0,255,0,0.5);
}

/* Estilo para las filas de películas */
.inner-container {
  display: flex; 
  justify-content: space-between; /* Distribuir las películas uniformemente en una fila */
  gap: 10px;  /* Espacio entre cada película */
  flex-wrap: wrap;  /* Ajustar las películas en múltiples filas si es necesario */
  width: 100%;  /* Asegura que las filas ocupen todo el ancho disponible */
  height: 300px;
  background-color: rgb(255,0,0,0.5);
}

/* Estilo para cada película dentro de la fila */
.movie-item {
  width: 200px;  /* Cada película ocupa el 18% del ancho del contenedor (5 películas por fila) */
  box-sizing: border-box;
  position: relative;  /* Permite ajustar el contenido de la película */
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 20px;  /* Bordes redondeados de cada película */
  background-color: rgb(0,0,255,0.5);
}

/* Estilo para las imágenes de las películas */
.movie-poster {
  width: 100%;  /* La imagen ocupa el 100% del espacio disponible */
  height: auto;  /* Mantener la proporción de la imagen */
  border-radius: 8px;  /* Bordes redondeados para las imágenes */
  object-fit: cover;  /* Hace que la imagen se recorte bien si es necesario */
  transition: transform 0.3s ease; /* Efecto de transición al pasar el mouse */
  opacity: 0;
}

/* Efecto de hover sobre las imágenes */
.movie-item:hover .movie-poster {
  transform: scale(1.05); /* Aumenta ligeramente el tamaño de la imagen cuando se pasa el ratón por encima */
}


.home-page {
  margin: 0;
  padding: 0;
  height: 100vh;
  display: flex;
  flex-direction: column; /* El header se coloca en la parte superior, el contenido debajo */
  
}


.container-wrapper {
  display: flex;
  flex: 1; /* Ocupa el resto del espacio después del header */
  background-color: rgb(255,255,0, 0.5);
}

.footer {
  background-color: #161616;
  color: white;
  text-align: center;
  padding: 20px;
  z-index: 5;
}



</style>

