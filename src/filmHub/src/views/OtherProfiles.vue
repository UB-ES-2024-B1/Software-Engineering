<template>
    <div class="profile-page">
        <HeaderPage />

        <div class="overlay"></div>

        <div class="main-content" v-if="!error">
            <div class="shadow-overlay"></div>
            <div class="profile-box">
                <div v-if="userData" class="profile-content">
                    <!-- Imagen de perfil -->
                    <div class="profile-image">
                        <img :src="userData.img_url || require('@/assets/foto_perfil.png')" alt="Profile Picture" />
                    </div>

                    <div class="profile-info">
                        <div class="username-div">
                            <strong>Name:</strong><br />
                            <span>{{ userData.full_name }}</span>
                        </div>

                        <!-- Información adicional: followers, reviews, followed -->
                        <div class="extra-info">
                            <div class="info-item">
                                <strong>Followers:</strong>
                                <span>125</span> <!-- Valor hardcodeado -->
                            </div>
                            <div class="info-item">
                                <strong>Reviews:</strong>
                                <span>34</span> <!-- Valor hardcodeado -->
                            </div>
                            <div class="info-item">
                                <strong>Followed:</strong>
                                <span>58</span> <!-- Valor hardcodeado -->
                            </div>

                        </div>
                        <div class="follow-button">
                            <button @click="toggleFollow">
                                {{ isFollowing ? 'Unfollow' : 'Follow' }}
                            </button>
                        </div>

                    </div>
                </div>
                <div v-else class="loading-message">
                    Loading profile...
                </div>
            </div>
        </div>

        <!-- Mostrar películas solo si el usuario existe -->
        <div class="movies-section" v-if="!error">
            <!-- Nueva capa de overlay -->
            <div class="movies-overlay"></div>

            <div class="movies-header">
                <button :class="{ active: showRatedMovies }" @click="toggleMovies('rated')">
                    Rated Movies
                </button>

                <button :class="{ active: showFavouriteMovies }" @click="toggleMovies('liked')">
                    Favourite Movies
                </button>

                <button :class="{ active: showWishlistMovies }" @click="toggleMovies('wishlist')">
                    Wishlist Movies
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

                    <!-- User Rating -->
                    <div v-if="showRatedMovies" class="user-rating">
                        <img src="@/assets/star.png" alt="Rating" class="icon" />
                        <span>{{ movie.userRating }}</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Mostrar mensaje de error si el usuario no existe -->
        <div v-if="error" class="error-container">
            <p class="error-message">{{ error }}</p>
        </div>
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
            isFollowing: false,
            userData: null,
            error: null,
            profile_image: '',
            showRatedMovies: true, // Controla si se muestran las valoradas o las con like
            showFavouriteMovies: false, // Controla la visualización de la lista de wishlist
            showWishlistMovies: false, // Controla la visualización de la lista de wishlist
            ratedMovies: [], // Películas valoradas
            likedMovies: [], // Películas con like
            wishedMovies: [], // Películas en la wishlist
            displayedMovies: [], // Películas que se muestran actualmente


            //REP eliminar
            showReportedModal: false,
            reportedComments: [],

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
            .get(`${API_BASE_URL}/users/email/${this.$route.params.username}`)
            .then((response) => {
                if (!response.data || Object.keys(response.data).length === 0) {
                    this.error = 'User does not exist.';
                    return;
                }
                this.userData = response.data;

                // Cargar las películas liked, rated y wishlist
                this.loadMovies();
            })
            .catch((error) => {
                console.error('Error al obtener los datos del usuario:', error);
                this.error = 'User does not exist.';
            });
    },

    methods: {
        toggleFollow() {
            this.isFollowing = !this.isFollowing;
        },
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

            // Cargar las películas liked , rated y wished
            axios
                .get(`${API_BASE_URL}/movies/liked_list/${this.userData.id}`)
                .then((response) => {
                    const likedMoviesTitles = response.data; // Listado de películas con like

                    // Obtener detalles completos de las películas liked
                    const likedMoviesDetails = Promise.all(
                        likedMoviesTitles.map(async (movieTitle) => {
                            const movieData = await this.fetchMovieDetails(movieTitle);
                            return movieData ? generateMovieObject(movieData) : null;
                        })
                    );

                    // Obtener las películas valoradas
                    axios
                        .get(`${API_BASE_URL}/movies/rated_list/${this.userData.id}`)
                        .then((response) => {
                            const ratedMoviesList = response.data;

                            const ratedMoviesDetails = Promise.all(
                                ratedMoviesList.map(async (movie) => {
                                    const movieData = await this.fetchMovieDetails(movie.title);
                                    return movieData
                                        ? generateMovieObject(movieData, movie.rating)
                                        : null;
                                })
                            );

                            // Obtener las películas wishlist
                            axios
                                .get(`${API_BASE_URL}/movies/wished_list/${this.userData.id}`)
                                .then((response) => {
                                    const wishedMoviesList = response.data;

                                    const wishedMoviesDetails = Promise.all(
                                        wishedMoviesList.map(async (movieTitle) => {
                                            const movieData = await this.fetchMovieDetails(movieTitle);
                                            return movieData ? generateMovieObject(movieData) : null;
                                        })
                                    );

                                    // Esperamos a que todas las promesas se resuelvan
                                    Promise.all([likedMoviesDetails, ratedMoviesDetails, wishedMoviesDetails])
                                        .then(([likedMovies, ratedMovies, wishedMovies]) => {
                                            // Filtramos los valores nulos
                                            this.likedMovies = likedMovies.filter((movie) => movie !== null);
                                            this.ratedMovies = ratedMovies.filter((movie) => movie !== null);
                                            this.wishedMovies = wishedMovies.filter((movie) => movie !== null);

                                            // Ahora actualizamos la lista mostrada
                                            this.displayedMovies = this.showRatedMovies
                                                ? this.ratedMovies
                                                : this.showFavouriteMovies
                                                    ? this.likedMovies
                                                    : this.wishedMovies;
                                        })
                                        .catch((error) => {
                                            console.error('Error al procesar las películas wished:', error);
                                        });
                                })
                                .catch((error) => {
                                    console.error('Error al obtener las películas wished:', error);
                                });
                        })
                        .catch((error) => {
                            console.error('Error al obtener las películas rated:', error);
                        });
                })
                .catch((error) => {
                    console.error('Error al obtener las películas liked:', error);
                });
        },

        toggleMovies(type) {
            // Resetear todos los botones a false
            this.showRatedMovies = false;
            this.showFavouriteMovies = false;
            this.showWishlistMovies = false;

            // Activar el botón correspondiente según el tipo
            if (type === 'rated') {
                this.showRatedMovies = true;
            } else if (type === 'liked') {
                this.showFavouriteMovies = true;
            } else if (type === 'wishlist') {
                this.showWishlistMovies = true;
            }

            // Actualizar la lista mostrada inmediatamente después de cambiar el estado
            this.updateDisplayedMovies();
        },


        updateDisplayedMovies() {
            // Actualizar la lista de películas que se debe mostrar según el estado actual
            if (this.showRatedMovies) {
                this.displayedMovies = this.ratedMovies;
            } else if (this.showFavouriteMovies) {
                this.displayedMovies = this.likedMovies;
            } else if (this.showWishlistMovies) {
                this.displayedMovies = this.wishedMovies;
            }
        },
    },

    watch: {
        // Cuando cambie el estado de las películas, actualizamos la lista mostrada
        showRatedMovies() {
            this.updateDisplayedMovies();
        },
        showFavouriteMovies() {
            this.updateDisplayedMovies();
        },
        showWishlistMovies() {
            this.updateDisplayedMovies();
        }
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
    height: 80vh;
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
    height: 350px;
    color: white;
    z-index: 20;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    /* Mejora visual */
    border: 2px solid rgba(255, 255, 255, 0.1);
    /* Sutileza */
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
    padding-bottom: 0px;
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
    gap: 20px;
}

.profile-info p {
    margin-bottom: 60px;
    font-size: 18px;
    line-height: 1.5;
}

.profile-info strong {
    font-weight: bold;
    color: #ffffff;
}

.profile-info span {
    display: block;
    color: #dcdcdc;
    font-size: 16px;
}

/* Fondo del modal */
/* Fondo del modal */
.modal-overlay {
    width: 100%;
    align-items: center;
    justify-content: space-between;

}

/* Contenido del modal */
.modal-content {
    background-color: rgb(5, 1, 9);
    /* Fondo del modal */
    padding: 20px;
    border-radius: 10px;
    color: black;
    max-width: 600px;
    /* Ancho máximo */
    width: 90%;
    max-height: 80%;
    /* Altura máxima del modal */
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3);
    /* Sombra alrededor del modal */
    display: flex;
    flex-direction: column;
    /* Organizar contenido en columna */
    overflow: hidden;
    /* Prevenir contenido desbordado fuera del modal */
}

/* Estilo del título */
h2 {
    font-size: 1.5em;
    font-weight: bold;
    text-align: center;
    margin-bottom: 15px;
    /* Separación con los comentarios */
}

/* Contenedor con scroll exclusivo para los comentarios */
.scrollable-comments {
    max-height: 400px;
    /* Limita la altura visible a unos 6 comentarios (ajusta según el diseño). */
    overflow-y: auto;
    /* Habilita el desplazamiento vertical. */
    padding-right: 10px;
    /* Espacio para evitar superposición con la barra de desplazamiento. */
    border: 1px solid #ddd;
    /* Opcional: borde para resaltar el área. */
    width: 80%;
    padding: 10px;
    /* Añade espacio interno alrededor del contenido. */
    border-radius: 5px;
    /* Bordes redondeados. */
    background-color: #f9f9f931;
    /* Fondo claro para destacar los comentarios. */
    box-sizing: border-box;
    /* Asegura que `padding` no afecte al ancho/altura total. */
}

.scrollable-comments::-webkit-scrollbar {
    width: 8px;
    /* Ancho de la barra de desplazamiento. */
}

.scrollable-comments::-webkit-scrollbar-thumb {
    background: #ccc;
    /* Color de la barra de desplazamiento. */
    border-radius: 4px;
}

.scrollable-comments::-webkit-scrollbar-thumb:hover {
    background: #aaa;
    /* Color al pasar el cursor por la barra. */
}

/* Cada comentario dentro de su propio bloque */
.comment-item {
    width: 100%;
    /* Asegura que el comentario ocupe todo el ancho disponible */
    box-sizing: border-box;
    /* Asegura que padding y borde no afecten el tamaño */
    padding: 10px;
    /* Espacio interno para que el contenido no toque los bordes */
    border-bottom: 1px solid #eee;
    /* Línea divisoria entre comentarios */
    background-color: #2a2a2a;
    border-radius: 5px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.5);
    font-size: 1rem;
    /* Para colocar el icono de la basurita a la derecha */
    display: flex;
    /* Activa la flexbox */
    justify-content: space-between;
    /* Espaciado entre texto e icono */
    align-items: center;
    /* Centra verticalmente el contenido */
}

/* Nueva sección de películas */
.movies-section {
    margin-top: 0px;
    padding-top: 20px;
    background-color: #121212;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
    z-index: 10;
}

.movies-header {
    position: absolute;
    top: px;
    /* 20px desde la parte superior */
    right: 363px;
    /* 20px desde la izquierda */
    display: flex;
    /* Los botones en fila */
    margin: 0 auto;
    position: relative;
    margin-top: 20px;
    z-index: 5;

}

/* Estilo base de los botones */
.movies-header button {
    padding: 10px 20px;
    background: rgba(255, 255, 255, 0.2);
    /* Fondo inicial transparente */
    color: white;
    /* Texto blanco por defecto */
    border: none;
    border-top-left-radius: 12px;
    border-top-right-radius: 12px;
    border-bottom: 2px solid transparent;
    cursor: pointer;
    font-weight: bold;
    transition: all 0.3s ease;
    /* Suavizar transiciones */
    margin-right: 2px;
    /* Separación entre botones */
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    /* Sombra sutil */
}

/* El último botón no tiene margen derecho */
.movies-header button:last-child {
    margin-right: 0;
}

/* Estilo para el botón activo */
.movies-header button.active {
    background: #4a90e2;
    /* Azul más fuerte para el fondo */
    color: white;
    /* Texto blanco para mejor contraste */
    border-bottom: none;
    position: relative;
    z-index: 10;
    /* Asegura que el botón activo se quede encima de los demás */
    box-shadow: 0 0 20px rgba(74, 144, 226, 0.8), 0 0 15px rgba(0, 0, 0, 0.3);
    /* Sombra azulada */
    transform: translateY(-4px);
    /* Eleva el botón ligeramente */
    text-shadow: 0 0 10px rgba(74, 144, 226, 0.8), 0 0 20px rgba(74, 144, 226, 0.8), 0 0 40px rgba(74, 144, 226, 1);
    /* Resplandor azul */
}

/* Efecto hover */
.movies-header button:hover {
    background: #6fa3e0;
    /* Azul más claro cuando se pasa el ratón */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    /* Sombra más intensa para el hover */
    transform: translateY(-2px);
    /* Eleva el botón al pasar el ratón */
}

/* Agregar un enfoque visual más fuerte al pasar el ratón sobre el botón activo */
.movies-header button.active:hover {
    background: #3879c0;
    /* Azul aún más oscuro para hover cuando está activo */
    box-shadow: 0 0 30px rgba(74, 144, 226, 1), 0 0 40px rgba(0, 0, 0, 0.4);
    /* Brillo más fuerte */
    transform: translateY(-6px);
    /* Aumenta el efecto de elevación */
    text-shadow: 0 0 15px rgba(74, 144, 226, 1), 0 0 30px rgba(74, 144, 226, 1), 0 0 50px rgba(74, 144, 226, 1);
    /* Brillo azul más intenso */
}




/* Contenedor de la lista de películas */
.movies-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 55px;
    width: 100%;
    max-width: 1200px;
    min-height: 375px;
    padding: 15px;
    box-sizing: border-box;
    background: rgba(255, 255, 255, 0.2);
    border-top-right-radius: 30px;
    z-index: 5;
}

.movie-item {
    position: relative;
    width: 250px;
    height: 350px;
    display: flex;
    flex-direction: column;
    align-items: center;
    border-radius: 20px;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
    position: relative;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.movie-item:hover {
    transform: scale(1.05);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.5);
}

.movie-poster {
    width: 250px !important;
    height: 350px !important;
    border-radius: 20px !important;
    opacity: 1;
}

.rating-likes-cover {
    position: absolute;
    top: 295px;
    left: 10px;
    background-color: rgba(0, 0, 0, 0.4);
    backdrop-filter: blur(10px);
    color: white;
    padding: 10px;
    border-radius: 10px;
    display: flex;
    gap: 10px;
    align-items: center;
    z-index: 5;
}

.user-rating {
    position: absolute;
    bottom: 295px;
    left: 10px;
    background-color: rgba(0, 255, 0, 0.3);
    border: 1px solid green;
    backdrop-filter: blur(5px);
    color: white;
    padding: 10px;
    border-radius: 10px;
    display: flex;
    gap: 1px;
    align-items: center;
    z-index: 5;
    font-weight: bold;
}

.icon {
    width: 20px !important;
    /* Ajusta el tamaño según tus necesidades */
    height: 20px !important;
    margin-right: 5px;
    /* Espacio entre la imagen y el número */
}

/* Media Queries */
@media (max-width: 768px) {
    .profile-box {
        width: 90%;
        height: auto;
        padding: 20px;
    }

    .profile-content {
        flex-direction: column;
        align-items: center;
        text-align: center;
    }

    .profile-image img {
        width: 120px;
        height: 120px;
    }

    .btns-div {
        flex-direction: column;
        gap: 10px;
        bottom: 1rem;
    }

    .movies-list {
        grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
        gap: 20px;
    }

    .movie-item {
        width: 150px;
        height: 225px;
    }

    .movie-poster {
        height: 225px !important;
    }

    .rating-likes-cover {
        top: 180px;
        padding: 5px;
        font-size: 12px;
    }

    .user-rating {
        bottom: 180px;
        padding: 5px;
        font-size: 12px;
    }
}

@media (max-width: 480px) {
    .profile-box {
        padding: 10px;
    }

    .movies-header button {
        padding: 8px 15px;
        font-size: 12px;
    }

    .movie-item {
        width: 120px;
        height: 180px;
    }

    .movie-poster {
        height: 180px !important;
    }
}


.error-container {
    display: flex;
    justify-content: center;
    /* Center horizontally */
    align-items: center;
    /* Center vertically */
    height: 100vh;
    /* Full viewport height */
    text-align: center;
}

.error-message {
    padding: 20px;
    background-color: #f8d7da;
    border: 1px solid #f5c2c7;
    color: #842029;
    border-radius: 5px;
    font-size: 1.5rem;
    font-weight: bold;
}

.profile-info {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 10px;
    text-align: center;
}

.extra-info {
    display: flex;
    justify-content: space-between;
    gap: 20px;
    margin-top: 10px;
    font-size: 14px;
    font-weight: bold;
}

.extra-info .info-item {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.follow-button {
    margin-top: 15px;
    text-align: center;
}

.follow-button button {
    padding: 8px 16px;
    background-color: #007bff;
    /* Color azul */
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 14px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.follow-button button:hover {
    background-color: #0056b3;
    /* Azul más oscuro al pasar el mouse */
}

.follow-button button:active {
    background-color: #003f7f;
    /* Azul aún más oscuro al hacer clic */
}
</style>