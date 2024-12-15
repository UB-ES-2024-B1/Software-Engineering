<template>
  <div class="home-page">
    <HeaderPage /> <!-- Componente HeaderPage -->

    <!-- Modal de aviso si no es premium -->
    <div v-if="showRegisterModal" class="modal-premium">
      <div class="modal-content-premium">
        <p>This feature is only available for Registered accounts.</p>
        <router-link to="/login">
          <button @click="closeRegisterModal">Ok</button>
        </router-link>
      </div>
    </div>

    <!-- Modal de aviso no hay listas creadas -->
    <div v-if="showNoListModal" class="modal-premium">
      <div class="modal-content-premium">
        <p>You have not created any lists yet.</p>
        <button @click="closeNoListModal">Ok</button>
      </div>
    </div>

    <!-- Modal de aviso pelicula anadida -->
    <div v-if="showMovieAddedModal" class="modal-premium">
      <div class="modal-content-premium">
        <p>Movie successfully added to the list!</p>
        <button @click="closeMovieAddedModal">Ok</button>
      </div>
    </div>

    <!-- Banner -->
    <section class="banner" v-if="bannerMovie">
      <div class="carousel-inner">
        <img :src="bannerMovie.image" class="d-block w-100 carousel-image" alt="Movie poster" />
        <div class="shadow-overlay"></div>


        <div class="small-cover">
          <!-- Imagen de la portada de la película -->
          <img :src="bannerMovie.smallImage" alt="Movie Small Cover" class="small-cover-image" />         

        
          <!-- Información de la película -->
          <div class="movie-info">
            <h4>{{ bannerMovie.title }}</h4>

            <!-- Modificado para redireccionarlo a AllMovies según el género -->
            <div class="info-item">
              <span class="info-title">Genres: </span> 
              <!-- <span>{{ bannerMovie.genres.join(", ") }}</span> -->
              <span>
                <span v-for="(genre, index) in bannerMovie.genres" :key="index">
                  <router-link :to="{ name: 'AllMovies', query: { genre: genre } }" class="genre-link">
                    {{ genre }}
                  </router-link>
                  <span v-if="index < bannerMovie.genres.length - 1">, </span>
                </span>
              </span>

            </div>


            <div class="info-item">
              <span class="info-title">Date: </span> <span>
                <router-link :to="{ name: 'AllMovies', query: { year: bannerMovie.release_date.slice(0,4) } }" class="genre-link">
                  {{ bannerMovie.release_date }}
                </router-link>
              </span>
            </div>
            <div class="info-item">
              <span class="info-title">Country: </span> <span>{{ bannerMovie.country }}</span>
            </div>
            <div class="rating-likes-banner">
              <div class="rating">
                <img src="@/assets/star.png" alt="Star" class="icon" />
                <span>{{ bannerMovie.rating.toFixed(1) }}</span>
              </div>
              <div class="likes">
                <img src="@/assets/like.png" alt="Like" class="icon" />
                <span>{{ bannerMovie.likes }}</span>
              </div>
            </div>

            <div tabindex="0" class="plusButton">
              <svg class="plusIcon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 30 30">
                <g mask="url(#mask0_21_345)">
                  <path d="M13.75 23.75V16.25H6.25V13.75H13.75V6.25H16.25V13.75H23.75V16.25H16.25V23.75H13.75Z"></path>
                </g>
              </svg>
            </div>

            <!-- Botón para abrir el modal -->
            <div tabindex="0" class="plusButton" @click="showAddToListModal">
              <svg class="plusIcon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 30 30">
                <g mask="url(#mask0_21_345)">
                  <path d="M13.75 23.75V16.25H6.25V13.75H13.75V6.25H16.25V13.75H23.75V16.25H16.25V23.75H13.75Z"></path>
                </g>
              </svg>
            </div>

            <!-- Modal para seleccionar la lista -->
            <div v-if="showModal" class="modal">
              <div class="modal-content">
                <h3>Add Movie to Lists:</h3>
                <ul>
                  <!-- Mostrar las listas del usuario -->
                  <li v-for="(list, index) in userLists" :key="index" class="list-item">
                    <div class="list-item-content">
                      <span class="list-name">{{ list.list_name }}</span>
                      <button type="button" @click="addMovieToList(list.list_name)" class="list-btn">
                        <svg class="add-icon" viewBox="0 0 24 24" width="16" height="16">
                          <path
                            d="M12 5v14m-7-7h14"
                            stroke="currentColor"
                            stroke-width="2"
                            fill="none"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                          />
                        </svg>
                      </button>
                    </div>
                  </li>
                </ul>
                <button type="button" @click="showModal = false" class="cancel-btn">Cancel</button>
              </div>
            </div>

          </div>
        </div>
        


        <!-- Aquí agregamos las estrellas de votación -->
        <div class="star-rating-container">
          <div class="radio">
            <!-- Estrellas para la valoración -->
            <input value="5" name="rating" type="radio" id="rating-5" :checked="rating === 5" @click="saveRating(5)" />
            <label title="5 star" for="rating-5">
              <svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 576 512">
                <path
                  d="M316.9 18C311.6 7 300.4 0 288.1 0s-23.4 7-28.8 18L195 150.3 51.4 171.5c-12 1.8-22 10.2-25.7 21.7s-.7 24.2 7.9 32.7L137.8 329 113.2 474.7c-2 12 3 24.2 12.9 31.3s23 8 33.8 2.3l128.3-68.5 128.3 68.5c10.8 5.7 23.9 4.9 33.8-2.3s14.9-19.3 12.9-31.3L438.5 329 542.7 225.9c8.6-8.5 11.7-21.2 7.9-32.7s-13.7-19.9-25.7-21.7L381.2 150.3 316.9 18z">
                </path>
              </svg>
            </label>

            <input value="4" name="rating" type="radio" id="rating-4" :checked="rating === 4" @click="saveRating(4)" />
            <label title="4 stars" for="rating-4">
              <svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 576 512">
                <path
                  d="M316.9 18C311.6 7 300.4 0 288.1 0s-23.4 7-28.8 18L195 150.3 51.4 171.5c-12 1.8-22 10.2-25.7 21.7s-.7 24.2 7.9 32.7L137.8 329 113.2 474.7c-2 12 3 24.2 12.9 31.3s23 8 33.8 2.3l128.3-68.5 128.3 68.5c10.8 5.7 23.9 4.9 33.8-2.3s14.9-19.3 12.9-31.3L438.5 329 542.7 225.9c8.6-8.5 11.7-21.2 7.9-32.7s-13.7-19.9-25.7-21.7L381.2 150.3 316.9 18z">
                </path>
              </svg>
            </label>

            <input value="3" name="rating" type="radio" id="rating-3" :checked="rating === 3" @click="saveRating(3)" />
            <label title="3 stars" for="rating-3">
              <svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 576 512">
                <path
                  d="M316.9 18C311.6 7 300.4 0 288.1 0s-23.4 7-28.8 18L195 150.3 51.4 171.5c-12 1.8-22 10.2-25.7 21.7s-.7 24.2 7.9 32.7L137.8 329 113.2 474.7c-2 12 3 24.2 12.9 31.3s23 8 33.8 2.3l128.3-68.5 128.3 68.5c10.8 5.7 23.9 4.9 33.8-2.3s14.9-19.3 12.9-31.3L438.5 329 542.7 225.9c8.6-8.5 11.7-21.2 7.9-32.7s-13.7-19.9-25.7-21.7L381.2 150.3 316.9 18z">
                </path>
              </svg>
            </label>

            <input value="2" name="rating" type="radio" id="rating-2" :checked="rating === 2" @click="saveRating(2)" />
            <label title="2 stars" for="rating-2">
              <svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 576 512">
                <path
                  d="M316.9 18C311.6 7 300.4 0 288.1 0s-23.4 7-28.8 18L195 150.3 51.4 171.5c-12 1.8-22 10.2-25.7 21.7s-.7 24.2 7.9 32.7L137.8 329 113.2 474.7c-2 12 3 24.2 12.9 31.3s23 8 33.8 2.3l128.3-68.5 128.3 68.5c10.8 5.7 23.9 4.9 33.8-2.3s14.9-19.3 12.9-31.3L438.5 329 542.7 225.9c8.6-8.5 11.7-21.2 7.9-32.7s-13.7-19.9-25.7-21.7L381.2 150.3 316.9 18z">
                </path>
              </svg>
            </label>

            <input value="1" name="rating" type="radio" id="rating-1" :checked="rating === 1" @click="saveRating(1)" />
            <label title="1 star" for="rating-1">
              <svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 576 512">
                <path
                  d="M316.9 18C311.6 7 300.4 0 288.1 0s-23.4 7-28.8 18L195 150.3 51.4 171.5c-12 1.8-22 10.2-25.7 21.7s-.7 24.2 7.9 32.7L137.8 329 113.2 474.7c-2 12 3 24.2 12.9 31.3s23 8 33.8 2.3l128.3-68.5 128.3 68.5c10.8 5.7 23.9 4.9 33.8-2.3s14.9-19.3 12.9-31.3L438.5 329 542.7 225.9c8.6-8.5 11.7-21.2 7.9-32.7s-13.7-19.9-25.7-21.7L381.2 150.3 316.9 18z">
                </path>
              </svg>
            </label>
          </div>
        </div>

        <!-- Like -->
        <div class="like-container">
          <label class="container">
            <!-- Checkbox para manejar el like -->
            <input type="checkbox" id="like-toggle" :checked="likedMovies.includes(bannerMovie.title)"
              @change="toggleLike(bannerMovie.id, !$event.target.checked)" />
            <div class="checkmark">
              <svg viewBox="0 0 256 256">
                <rect fill="none" height="256" width="256"></rect>
                <path id="heart-path" :stroke="likedMovies.includes(bannerMovie.title) ? 'red' : '#000'"
                  d="M224.6,51.9a59.5,59.5,0,0,0-43-19.9,60.5,60.5,0,0,0-44,17.6L128,59.1l-7.5-7.4C97.2,28.3,59.2,26.3,35.9,47.4a59.9,59.9,0,0,0-2.3,87l83.1,83.1a15.9,15.9,0,0,0,22.6,0l81-81C243.7,113.2,245.6,75.2,224.6,51.9Z"
                  stroke-width="20px" fill="none">
                </path>
              </svg>
            </div>
          </label>
        </div>

        <div class="wish-container"> 
          <!-- Botón de Wishlist en la esquina superior derecha -->
          <label class="ui-bookmark wishlist-button">
            <input
              type="checkbox"
              :checked="wishedMovies.includes(bannerMovie.title)"
              @change="toggleWishlist(bannerMovie.id)"
              :disabled="userRatedMovies[bannerMovie.title]" 
            />
            <div class="bookmark" :class="{ disabled: userRatedMovies[bannerMovie.title] }">
              <svg viewBox="0 0 32 32">
                <g>
                  <path
                    d="M27 4v27a1 1 0 0 1-1.625.781L16 24.281l-9.375 7.5A1 1 0 0 1 5 31V4a4 4 4 4 1 4-4h14a4 4 4 0 1 4 4z"
                  ></path>
                </g>
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
            <!-- Modificado para hacer un link hacia allMovies y que se muestren las pelis del Director-->
            <h4>Director</h4>
            <p>
              <router-link :to="{ name: 'AllMovies', query: { director: bannerMovie.director } }" class="genre-link">
                {{ bannerMovie.director }}
              </router-link>
            </p>
          </div>

          <!-- Cards for Cast, excluding the director -->
          <div v-for="(actor, index) in bannerMovie.cast" :key="actor" class="detail-card"
            v-show="index < visibleCount">
            <h4>Actor</h4>
            <p>
              <router-link :to="{ name: 'AllMovies', query: { actor: actor } }" class="genre-link">
              {{ actor }}
              </router-link>
            </p>
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


    <!-- Sección del foro de comentarios -->
     <!-- He afegit un id per linkejar els reported comments de l'admin-->
    <section id="comments-section" class="comments-section">
      <div v-if="bannerMovie">
        <h4 class="section-title">Comments</h4>
        <div class="comments-container">
          <!-- Contenedor con barra de desplazamiento -->
          <div class="scrollable-comments">
            <!-- Lista de comentarios -->
            <div v-for="(comment, index) in comments" :key="index" class="comment-item">
              <!-- Apply a gold class if the comment is from the logged-in user -->
              <p>
                <strong :class="{ 'gold-username': comment.user === userId }">{{ comment.username
                  }}</strong>: {{
                    comment.text }}
              </p>
              <!-- Button to delete the comment only visible to the logged-in user -->
              <button v-if="comment.user === userId" class="delete-comment-btn"
                @click="handleDelete(comment.id)">🗑️</button>

              <div class="comment-actions">
                <!-- Botón para contestar el comentario de otro usuario-->
                <button v-if="comment.user !== userId" class="reply-comment-btn"
                  @click="handleReply(comment.username)">
                  ↩️
                </button>

                <!-- Separador -->
                <span class="vertical-separator" v-if="comment.user !== userId"></span>

                <!-- Botón para reportar el comentario de otro usuario-->
                <button v-if="comment.user !== userId" class="report-comment-btn"
                  @click="handleReport(comment)">
                  🚩
                </button>
              </div>
            </div>
          </div>

          <!-- Botón "New Comment" -->
          <button :class="['new-comment-btn', { disabled: !loggedInUser }]" @click="handleNewComment">
            New Comment
          </button>

          <!-- Formulario para añadir un comentario -->
          <div v-if="isAddingComment" class="comment-form">
            <textarea v-model="newCommentText" placeholder="Write your comment here..."
              class="comment-textarea"></textarea>
            <div class="comment-buttons">
              <button @click="addComment" class="post-comment-btn">Post Comment</button>
              <button @click="toggleAddingComment" class="cancel-btn">Cancel</button>
            </div>
          </div>

        </div>
      </div>

      <!-- Confirmación de eliminación de comentario -->
      <div v-if="showDeleteConfirm" class="delete-modal">
        <p>Are you sure you want to delete this comment?</p>
        <div class="delete-modal-buttons">
          <button @click="deleteComment" class="delete-confirm-btn">Yes</button>
          <button @click="cancelDelete" class="delete-cancel-btn">No</button>
        </div>
      </div>

      <!-- Mensaje de alerta cuando un user no esta logged -->
      <div v-if="showAlert" class="alert-modal">
        <p>{{ alertMessage }}</p>
        <button @click="closeAlert" class="alert-close-btn">OK</button>
      </div>

      <!-- Confirmación de denuncia de comentario -->
      <div v-if="showReportConfirm" class="report-modal">
        <p>Are you sure you want to report this comment?</p>
        <div class="report-modal-buttons">
          <button @click="confirmReport" class="delete-confirm-btn">Yes</button>
          <button @click="cancelReport" class="delete-cancel-btn">Cancel</button>
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

                <!-- Wishlist Indicator -->
                <div v-if="wishedMovies.includes(movie.title)" class="wishlist-indicator">

                  <svg viewBox="0 0 32 32" class="wishlist-icon">
                    <g>
                      <path
                        d="M27 4v27a1 1 0 0 1-1.625.781L16 24.281l-9.375 7.5A1 1 0 0 1 5 31V4a4 4 4 4 1 4-4h14a4 4 4 0 1 4 4z"
                      ></path>
                    </g>
                  </svg>
                </div>


                <div class="rating-likes-cover">
                  <div class="rating">
                    <img src="@/assets/star.png" alt="Star" class="icon" />
                    <span>{{ movie.rating.toFixed(1) }}</span>
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

                <div class="rating-likes-cover">
                  <div class="rating">
                    <img src="@/assets/star.png" alt="Star" class="icon" />
                    <span>{{ movie.rating.toFixed(1) }}</span>
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

                <!-- Wishlist Indicator -->
                <div v-if="wishedMovies.includes(movie.title)" class="wishlist-indicator">

                  <svg viewBox="0 0 32 32" class="wishlist-icon">
                    <g>
                      <path
                        d="M27 4v27a1 1 0 0 1-1.625.781L16 24.281l-9.375 7.5A1 1 0 0 1 5 31V4a4 4 4 4 1 4-4h14a4 4 4 0 1 4 4z"
                      ></path>
                    </g>
                  </svg>
                </div>

                <div class="rating-likes-cover">
                  <div class="rating">
                    <img src="@/assets/star.png" alt="Star" class="icon" />
                    <span>{{ movie.rating.toFixed(1) }}</span>
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
      userId: parseInt(localStorage.getItem('user_id')), // ID del usuario
      userEmail: localStorage.getItem('userEmail'),
      rating: 0, // Valoración inicial
      userRatedMovies: {}, // Almacenará las películas valoradas por el usuario
      likedMovies: [], // Almacena las películas que el usuario ha marcado como "like"
      wishedMovies: [], // Almacenará las películas que el usuario ha añadido a la wishlist
      comments: [],
      isAddingComment: false,
      newCommentText: "",
      loggedInUser: !!localStorage.getItem('token'), // Usuario logueado
      showDeleteConfirm: false, // Controla si la confirmación de eliminación de comomment está visible
      commentToDeleteIndex: null, // Índice del comentario a eliminar
      showAlert: false, // Controla la visibilidad de la alerta
      alertMessage: "", // Mensaje dinámico de la alerta
      successMessage: "", // Mensaje de éxito
      errorMessage: "", // Mensaje de error

      showReportConfirm: false, //controla confirmación de denuncia de comentario
      commentToReport: null,

      showModal: false,  // Inicialmente, el modal está oculto
      userLists: [], // Las listas del usuario

      showRegisterModal: false,
      showNoListModal: false,
      showMovieAddedModal: false,
    };
  },
  computed: {
    combinedCast() {
      return [this.bannerMovie.director, ...this.bannerMovie.cast];
    },
  },
  methods: {

    async fetchComments() {
      console.log('Fetching comments for movie:', this.bannerMovie.id);
      try {
        const response = await axios.get(`${API_BASE_URL}/comments/threads/${this.bannerMovie.id}/comments/`, {
          headers: {
            'accept': 'application/json',
          },
        });

        if (Array.isArray(response.data)) {
          // Mapeamos los comentarios y resolvemos las promesas de usernames
          this.comments = await Promise.all(
            response.data.map(async comment => {
              const username = await this.getUsername(comment.user_id);
              return {
                id: comment.id,       // Guardar el ID del comentario
                user: comment.user_id, // Guardar el ID del usuario
                username,             // Agregar el nombre de usuario
                text: comment.text,   // Guardar el texto del comentario
              };
            })
          );
        } else {
          console.warn('Unexpected response format for comments:', response.data);
          this.comments = [];
        }
      } catch (error) {
        console.error('Error al cargar los comentarios:', error);
        this.errorMessage = 'Hubo un error al cargar los comentarios. Inténtalo de nuevo.';
      }
    },

    async getUsername(user_id) {
      try {
        const response = await axios.get(`${API_BASE_URL}/users/id/${user_id}`, {
          headers: {
            'accept': 'application/json',
          },
        });
        console.log('Username response:', response.data);
        return response.data.full_name;
      } catch (error) {
        console.error('Error fetching username:', error);
        return 'Unknown User';
      }
    },

    handleNewComment() {
      if (!this.loggedInUser) {
        this.showAlertMessage("You need to log in or register to access this feature.");
      } else {
        this.toggleAddingComment();
      }
    },

    handleDelete(commentId) {
      console.log('Deleting comment:', commentId);
      if (!this.loggedInUser) {
        this.showAlertMessage("You need to log in or register to access this feature.");
      } else {
        this.confirmDelete(commentId); // Pasa la `id` del comentario
      }
    },


    handleReply(otherUserName) {

      if (!this.loggedInUser) {
        this.showAlertMessage("You need to log in or register to access this feature.");
      } else {
        this.toggleAddingComment();
        this.newCommentText = "@" + otherUserName + " ";
      }
    },

    handleReport(comment) {
      if (!this.loggedInUser) {
        this.showAlertMessage("You need to log in or register to access this feature.");
      } else {
        // Mostrar modal de confirmación
        this.showReportConfirm = true;
        this.commentToReport = comment;
      }
    },

    confirmReport2() {
      console.log(`Reported user: ${this.userToReport}`);
      this.showAlertMessage("Comment reported successfully.");
      // Cerrar modal
      this.showReportConfirm = false;
      this.userToReport = null;
    },

    async confirmReport() {
      if (!this.commentToReport) {
        console.error("No comment selected to report.");
        this.showAlertMessage("No comment selected to report.");
        return;
      }

      try {
        console.log(`Reportando comentario con ID: ${this.commentToReport.id}`);

        // Realiza la solicitud PUT al backend
        const response = await axios.put(
          `${API_BASE_URL}/comments/${this.commentToReport.id}/status`,
          { reported: "REPORTED" }, // Payload de la solicitud
          {
            params: {
              user_id: this.userId, // Parámetro de usuario
            },
            headers: {
              accept: 'application/json',
              'Content-Type': 'application/json',
            },
          }
        );

        console.log('Respuesta del servidor:', response.data);

        // Muestra un mensaje de éxito
        this.showAlertMessage("Comment reported successfully.");

        // Opcional: Puedes actualizar los comentarios locales si es necesario
        // this.fetchComments();

      } catch (error) {
        console.error("Error reporting comment:", error);
        this.showAlertMessage("There was an error reporting the comment. Please try again.");
      } finally {
        // Cierra el modal y limpia el estado
        this.showReportConfirm = false;
        this.commentToReport = null;
      }
    },


    cancelReport() {
      // Cierra el modal sin realizar ninguna acción
      this.showReportConfirm = false;
      this.commentToReport = null;
    },


    toggleAddingComment() { //Muestra el formulario en funcion del boolean
      this.isAddingComment = !this.isAddingComment;
      if (!this.isAddingComment) {
        this.newCommentText = "";
      }
    },
    async addComment() {
      if (!Array.isArray(this.comments)) {
        this.comments = [];
      }
      const username = localStorage.getItem('userName');
      if (this.newCommentText.trim()) {
        this.comments.push({ user: username, text: this.newCommentText });
        try {
          const response = await axios.post(`${API_BASE_URL}/comments/`, null, {
            params: {
              thread_id: this.bannerMovie.id,
              user_id: localStorage.getItem('user_id'),
              text: this.newCommentText,
            },
            headers: {
              'accept': 'application/json',
            },
          });
          console.log('Comentario añadido:', response.data);
          this.successMessage = 'Comentario añadido con éxito.';
          this.newCommentText = '';
          await this.fetchComments();
        } catch (error) {
          console.error('Error al añadir el comentario:', error);
          this.errorMessage = 'No se pudo añadir el comentario. Inténtalo de nuevo.';
        }
        this.toggleAddingComment();
        this.showAlertMessage("Your comment has been successfully posted");
      }
    },
    confirmDelete(commentId) {
      this.commentToDeleteIndex = commentId;
      this.showDeleteConfirm = true; // Muestra un modal o confirmación
    },

    async deleteComment() {
      try {
        if (this.commentToDeleteIndex !== null) {
          // Realiza la llamada al backend para eliminar el comentario con la `id`
          await axios.delete(`${API_BASE_URL}/comments/${this.commentToDeleteIndex}/`, {
            headers: {
              'accept': 'application/json',
              'Authorization': `Bearer ${localStorage.getItem('token')}`, // Si es necesario autenticar
            },
          });

          // Elimina el comentario del array local
          this.comments = this.comments.filter(comment => comment.id !== this.commentToDeleteIndex);
          this.showAlertMessage('The comment has been successfully deleted');
          await this.fetchComments();
        }
      } catch (error) {
        console.error('Error when deleting the comment:', error);
        this.errorMessage = 'The comment could not be deleted. Try it again.';
      } finally {
        this.cancelDelete();
      }
    },
    cancelDelete() {
      this.commentToDeleteIndex = null;
      this.showDeleteConfirm = false;
    },

    showAlertMessage(message) {
      this.alertMessage = message;
      this.showAlert = true;
    },
    closeAlert() {
      this.showAlert = false;
      this.alertMessage = "";
    },
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

    scrollToHash() {
      const hash = this.$route.hash; // Obtén el hash de la URL
      if (hash) {
        this.$nextTick(() => {
          const element = document.querySelector(hash); // Selecciona el elemento por su ID
          if (element) {
            element.scrollIntoView({ behavior: 'smooth' }); // Desplaza suavemente
          }
        });
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

          if(this.scrollToHash()){
            this.scrollToHash()
          }else{
            this.scrollToTop();
          }
          
        }
      } catch (error) {
        console.error('Error loading movie data:', error);
      }
    },

    async saveRating(rating) {
      try {
        if (!this.userId) { // Verifica si el userId está disponible
          this.showRegisterModal = true;
          return; // Salir del método
        }

        if (this.rating === rating) {
          // Si la calificación seleccionada es la misma que la actual, deshacer la calificación
          const unrateEndpoint = `${API_BASE_URL}/movies/unrate/${this.bannerMovie.id}/${this.userId}`;
          const response = await axios.post(unrateEndpoint);
          if (response.status === 200) {
            console.log('Rating removed successfully.');
            this.rating = null; // Reiniciar el estado local de la valoración

            // Actualizar el estado de las películas valoradas
            if (this.userRatedMovies && this.bannerMovie.title in this.userRatedMovies) {
              delete this.userRatedMovies[this.bannerMovie.title];
            }
          }
        } else {
          // Si es una nueva calificación o diferente, guardar la calificación
          const rateEndpoint = `${API_BASE_URL}/movies/rate/${this.bannerMovie.id}/${this.userId}/${rating}`;
          const response = await axios.post(rateEndpoint);
          if (response.status === 200) {
            console.log('Rating saved successfully.');
            this.rating = rating; // Actualizamos el estado local de la valoración

            // Si la película está en la wishlist, quitarla automáticamente
            if (this.wishedMovies.includes(this.bannerMovie.title)) {
              console.log('Removing movie from wishlist due to rating.');
              const wishlistEndpoint = `${API_BASE_URL}/movies/nowish/${this.bannerMovie.id}/${this.userId}`;
              await axios.post(wishlistEndpoint);
              this.wishedMovies = this.wishedMovies.filter(title => title !== this.bannerMovie.title);
            }

            // Actualizar el estado de las películas valoradas
            if (!this.userRatedMovies) {
              this.userRatedMovies = {}; // Asegurarse de que exista el objeto
            }
            this.userRatedMovies[this.bannerMovie.title] = rating; // Actualizamos localmente
          }
        }

        this.loadMovieData(this.$route.params.id);

      } catch (error) {
        console.error('Error saving or removing rating:', error);
      }
    },


    async toggleLike(movieId) {
      try {
        if (!this.userId) { // Verifica si el userId está disponible
          this.showRegisterModal = true;
          return; // Salir del método
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
        }

        this.loadMovieData(this.$route.params.id);

      } catch (error) {
        console.error('Error toggling like:', error.response?.data || error.message);
      }
    },

    async toggleWishlist(movieId) {
        try {
          if (!this.userId) { // Verifica si el userId está disponible
            this.showRegisterModal = true;
            return; // Salir del método
          }

          // Verificar si la película ya está valorada
          if (this.userRatedMovies[this.bannerMovie.title]) {
            alert('No puedes añadir una película valorada a tu wishlist.');
            return; // Salir antes de cualquier otro cambio
          }

          // Verificar si la película ya está en wishedMovies
          const isWished = this.wishedMovies.includes(this.bannerMovie.title);

          // Evitar cambios visuales hasta que la base de datos responda
          const response = await axios.post(isWished
            ? `${API_BASE_URL}/movies/nowish/${movieId}/${this.userId}`
            : `${API_BASE_URL}/movies/wish/${movieId}/${this.userId}`
          );

          if (response.status === 200) {
            console.log(isWished ? 'Movie removed from wishlist.' : 'Movie added to wishlist.');

            // Actualizar el estado local sólo si la respuesta es exitosa
            if (isWished) {
              this.wishedMovies = this.wishedMovies.filter(title => title !== this.bannerMovie.title);
            } else {
              this.wishedMovies.push(this.bannerMovie.title);
            }
          }
        } catch (error) {
          console.error('Error toggling wishlist:', error.response?.data || error.message);
        }
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

          // Procesar películas en la wishlist
          this.wishedMovies = data.wished_movies || [];

          console.log('Wished Movies:', this.wishedMovies);

        } catch (error) {
          console.error('Error loading user preferences:', error.response?.data || error.message);
        }
      },

      async loadUserLists() {
        try {
          const userEmail = this.userEmail;

          if (!userEmail) {
            alert('No se ha encontrado el correo electrónico del usuario.');
            return;
          }

          const endpoint = `${API_BASE_URL}/list-type/get-lists-with-movies/${encodeURIComponent(userEmail)}`;
          const response = await axios.get(endpoint);

          // Verifica qué se devuelve en la respuesta
          console.log('Respuesta de la API:', response);

          if (response.status === 200) {
            // Accede directamente a la respuesta de las listas
            if (response.data && Array.isArray(response.data)) {
              this.userLists = response.data; // Asigna las listas directamente si son un array
              console.log('Listas asignadas:', this.userLists);
            } else {
              console.error('Las listas no están en el formato esperado');
            }
          } else {
            console.error('Error: La respuesta no es 200');
          }
        } catch (error) {
          console.error('Error al obtener las listas del usuario:', error);
        }
      },

      async showAddToListModal() {
        try {
          if (!this.userId) { 
            // Verifica si el userId está disponible
            this.showRegisterModal = true;
            return; // Salir del método
          }

          await this.loadUserLists(); // Cargar las listas del usuario

          if (this.userLists.length === 0) {
            // Si no hay listas creadas
            this.showNoListModal = true; // Muestra un mensaje en inglés
            return; // Salir del método
          }

          // Mostrar modal con las listas si hay al menos una lista
          this.showModal = true; // Hacer visible el modal
        } catch (error) {
          console.error('Error loading user lists for modal:', error);
        }
      },


      async addMovieToList(listName) {

        try {
          const userEmail = this.userEmail;

          if (!userEmail) {
            alert('No se ha encontrado el correo electrónico del usuario.');
            return;
          }

          const movieId = this.bannerMovie.id;
          const endpoint = `${API_BASE_URL}/list-type/add-movie/${encodeURIComponent(userEmail)}/${listName}/${movieId}`;
          
          const response = await axios.post(endpoint);
          
          if (response.status === 200) {
            console.log('Movie added to list successfully.');
            this.showModal = false; // Cerrar el modal después de añadir la película
            this.showMovieAddedModal = true;
          }
        } catch (error) {
          console.error('Error adding movie to list:', error.response?.data || error.message);
        }
      },

      closeRegisterModal() {
        this.showRegisterModal = false;  // Cerrar el modal de error
      },

      closeNoListModal() {
        this.showNoListModal = false;  // Cerrar el modal de error
      },

      closeMovieAddedModal() {
        this.showMovieAddedModal = false;  // Cerrar el modal de error
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
        this.scrollToHash(); // Desplazarse al hash si existe
      });
    } else {
      console.warn('User ID not found in localStorage.');
      this.loadMovieData(this.$route.params.id);
      this.scrollToHash(); // Desplazarse al hash si existe
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
    bannerMovie: {
      handler(newValue) {
        if (newValue && newValue.id) {

          this.fetchComments(); // Fetch comments when `bannerMovie` becomes available
        }
      },
      immediate: true, // Run the watcher immediately if data is already available
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
    title: movieData.title,
  };
}
</script>




<style scoped>
.genre-link {
  color: #3498db;
  text-decoration: none;
  cursor: pointer;
}

.genre-link:hover {
  text-decoration: underline;
}



/* Estilo para comentarios */
.comments-section {
  margin-top: 30px;
  padding: 20px;
  background-color: #1c1c1c;
  border-radius: 8px;
  color: #ffffff;
}

/* Título de la sección */
.section-title {
  font-size: 1.5rem;
  margin-bottom: 15px;
  text-align: center;
  color: #f5f5f5;
}

/* Contenedor de comentarios */
.comments-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;

}

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


/* Estilo para los comentarios individuales */
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

.comment-item:last-child {
  border-bottom: none;
}

/* Modal de alerta */
.alert-modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: #1c1c1c;
  color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
  z-index: 1000;
  text-align: center;
}

.alert-close-btn {
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 10px 15px;
  cursor: pointer;
  margin-top: 10px;
}

.alert-close-btn:hover {
  background-color: #0056b3;
}


/* Botón "New Comment" */
.new-comment-btn {
  background-color: #0066cc;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 10px 20px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.new-comment-btn.disabled {
  background-color: #888;
  /* Botón deshabilitado en gris */
  cursor: not-allowed;
}

.new-comment-btn:hover {
  background-color: #0055aa;
}

.new-comment-btn:hover:not(.disabled) {
  background-color: #0055aa;
}

/* Formulario para añadir comentario */
.comment-form {
  width: 100%;
  max-width: 600px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

/* Textarea de comentarios */
.comment-textarea {
  width: 100%;
  height: 80px;
  resize: none;
  border: none;
  border-radius: 5px;
  padding: 10px;
  font-size: 1rem;
  color: #000;
}

/* Botones del formulario */
.comment-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.post-comment-btn {
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 8px 15px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.3s;
}

.post-comment-btn:hover {
  background-color: #218838;
}

.cancel-btn {
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 8px 15px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.3s;
}

.cancel-btn:hover {
  background-color: #c82333;
}

/* Estilos para eliminación de comentarios */
/* Botón de eliminar comentario */
.delete-comment-btn {
  background: transparent;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  color: #ff4d4d;
  /* Rojo para el botón */
  margin-left: auto;
  transition: color 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.delete-comment-btn:hover {
  color: #e60000;
  /* Rojo más oscuro al pasar el cursor */

}

/* Modal de confirmación de eliminación */
.delete-modal,
.report-modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: #2a2a2a;
  padding: 20px;
  border-radius: 8px;
  color: #ffffff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  z-index: 1000;
  text-align: center;
}

.delete-modal-buttons,
.report-modal-buttons {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 15px;
}

.delete-confirm-btn {
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 8px 15px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.3s;
}

.delete-confirm-btn:hover {
  background-color: #218838;
}

.delete-cancel-btn {
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 8px 15px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.3s;
}

.delete-cancel-btn:hover {
  background-color: #c82333;
}



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

  transition: transform ease 0.3s;

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
  right: 125px;
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

.like-container {
  position: absolute;
  bottom: 59px;
  right: 100px;
  z-index: 10;
  opacity: 1;
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
  overflow: visible;
  /* Esto es importante */
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
  filter: drop-shadow(0 0 15px rgba(96, 13, 13, 0.9));
  /* Sombra dinámica */
  animation: shimmerHeart 1s ease infinite alternate;
  /* Animación shimmer */
}

/* El color cambia cuando está seleccionado */
.container input:checked~.checkmark path {
  fill: #f52121;
  filter: drop-shadow(0 0 15px rgba(96, 13, 13, 0.9));
  /* Sombra dinámica */
  animation: shimmerHeart 1s ease infinite alternate;
  /* Animación shimmer */
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
    filter: drop-shadow(0 0 10px rgba(255, 13, 13, 0.5));
    /* Sombra roja suave */
  }

  100% {
    filter: drop-shadow(0 0 20px rgba(255, 13, 13, 1));
    /* Sombra roja más intensa */
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

.banner-image {
  width: 112rem;
  height: 63rem;
}

#related-movies {
  margin-left: -0.2rem;
}

.gold-username {
  color: gold;
}

.wish-container {
  position: absolute;
  bottom: 21px;
  right: 375px;
  z-index: 10;
  opacity: 1;
}

/* From Uiverse.io by Galahhad */ 
.ui-bookmark {
  --icon-size: 33px;
  --icon-secondary-color: rgb(100, 100, 100, 1);
  --icon-hover-color: rgba(0, 157, 255, 1);
  --icon-primary-color: rgba(0, 157, 255, 1);
  --icon-circle-border: 1px solid var(--icon-primary-color);
  --icon-circle-size: 35px;
  --icon-anmt-duration: 0.3s;
}

.ui-bookmark input {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  display: none;
}

.ui-bookmark .bookmark {
  width: var(--icon-size);
  height: auto;
  fill: var(--icon-secondary-color);
  cursor: pointer;
  -webkit-transition: 0.2s;
  -o-transition: 0.2s;
  transition: 0.2s;
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  -webkit-box-pack: center;
  -ms-flex-pack: center;
  justify-content: center;
  -webkit-box-align: center;
  -ms-flex-align: center;
  align-items: center;
  position: relative;
  -webkit-transform-origin: top;
  -ms-transform-origin: top;
  transform-origin: top;
}

.ui-bookmark .bookmark.disabled {
  pointer-events: none; /* Deshabilita cualquier interacción */
  opacity: 0; /* Visualmente más claro para indicar que está deshabilitado */
  cursor: not-allowed; /* Cambia el cursor para reforzar que no se puede interactuar */
}

.bookmark::after {
  content: "";
  position: absolute;
  width: 10px;
  height: 10px;
  -webkit-box-shadow: 0 30px 0 -4px var(--icon-primary-color),
    30px 0 0 -4px var(--icon-primary-color),
    0 -30px 0 -4px var(--icon-primary-color),
    -30px 0 0 -4px var(--icon-primary-color),
    -22px 22px 0 -4px var(--icon-primary-color),
    -22px -22px 0 -4px var(--icon-primary-color),
    22px -22px 0 -4px var(--icon-primary-color),
    22px 22px 0 -4px var(--icon-primary-color);
  box-shadow: 0 30px 0 -4px var(--icon-primary-color),
    30px 0 0 -4px var(--icon-primary-color),
    0 -30px 0 -4px var(--icon-primary-color),
    -30px 0 0 -4px var(--icon-primary-color),
    -22px 22px 0 -4px var(--icon-primary-color),
    -22px -22px 0 -4px var(--icon-primary-color),
    22px -22px 0 -4px var(--icon-primary-color),
    22px 22px 0 -4px var(--icon-primary-color);
  border-radius: 50%;
  -webkit-transform: scale(0);
  -ms-transform: scale(0);
  transform: scale(0);
}

.bookmark::before {
  content: "";
  position: absolute;
  border-radius: 50%;
  border: var(--icon-circle-border);
  opacity: 0;
}

/* actions */

.ui-bookmark:hover .bookmark {
  fill: var(--icon-hover-color);
}

.ui-bookmark input:checked + .bookmark::after {
  -webkit-animation: circles var(--icon-anmt-duration)
    cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
  animation: circles var(--icon-anmt-duration)
    cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
  -webkit-animation-delay: var(--icon-anmt-duration);
  animation-delay: var(--icon-anmt-duration);
}

.ui-bookmark input:checked + .bookmark {
  fill: var(--icon-primary-color);
  -webkit-animation: bookmark var(--icon-anmt-duration) forwards;
  animation: bookmark var(--icon-anmt-duration) forwards;
  -webkit-transition-delay: 0.3s;
  -o-transition-delay: 0.3s;
  transition-delay: 0.3s;
}

.ui-bookmark input:checked + .bookmark::before {
  -webkit-animation: circle var(--icon-anmt-duration)
    cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
  animation: circle var(--icon-anmt-duration)
    cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
  -webkit-animation-delay: var(--icon-anmt-duration);
  animation-delay: var(--icon-anmt-duration);
}

@-webkit-keyframes bookmark {
  50% {
    -webkit-transform: scaleY(0.6);
    transform: scaleY(0.6);
  }

  100% {
    -webkit-transform: scaleY(1);
    transform: scaleY(1);
  }
}

@keyframes bookmark {
  50% {
    -webkit-transform: scaleY(0.6);
    transform: scaleY(0.6);
  }

  100% {
    -webkit-transform: scaleY(1);
    transform: scaleY(1);
  }
}

@-webkit-keyframes circle {
  from {
    width: 0;
    height: 0;
    opacity: 0;
  }

  90% {
    width: var(--icon-circle-size);
    height: var(--icon-circle-size);
    opacity: 1;
  }

  to {
    opacity: 0;
  }
}

@keyframes circle {
  from {
    width: 0;
    height: 0;
    opacity: 0;
  }

  90% {
    width: var(--icon-circle-size);
    height: var(--icon-circle-size);
    opacity: 1;
  }

  to {
    opacity: 0;
  }
}

@-webkit-keyframes circles {
  from {
    -webkit-transform: scale(0);
    transform: scale(0);
  }

  40% {
    opacity: 1;
  }

  to {
    -webkit-transform: scale(0.8);
    transform: scale(0.8);
    opacity: 0;
  }
}

@keyframes circles {
  from {
    -webkit-transform: scale(0);
    transform: scale(0);
  }

  40% {
    opacity: 1;
  }

  to {
    -webkit-transform: scale(0.8);
    transform: scale(0.8);
    opacity: 0;
  }
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



.plusButton {
  /* Config start */
  --plus_sideLength: 2rem;
  --plus_topRightTriangleSideLength: 0.9rem;
  /* Config end */
  position: absolute;
  bottom: 2vh;
  left: 70.5vh;
  display: flex;
  justify-content: center;
  align-items: center;
  border: 1px solid white;
  width: var(--plus_sideLength);
  height: var(--plus_sideLength);
  background-color: rgb(0,0,0,0);
  overflow: hidden;
  position: absolute;
  border-radius: 25%;
}

.plusButton::before {
  position: absolute;
  content: "";
  top: 0;
  right: 0;
  width: 0;
  height: 0;
  border-width: 0 var(--plus_topRightTriangleSideLength) var(--plus_topRightTriangleSideLength) 0;
  border-style: solid;
  border-color: transparent white transparent transparent;
  transition-timing-function: ease-in-out;
  transition-duration: 0.2s;
}

.plusButton:hover {
  cursor: pointer;
}

.plusButton:hover::before {
  --plus_topRightTriangleSideLength: calc(var(--plus_sideLength) * 2);
}

.plusButton:focus-visible::before {
  --plus_topRightTriangleSideLength: calc(var(--plus_sideLength) * 2);
}

.plusButton>.plusIcon {
  fill: white;
  width: calc(var(--plus_sideLength) * 0.7);
  height: calc(var(--plus_sideLength) * 0.7);
  z-index: 1;
  transition-timing-function: ease-in-out;
  transition-duration: 0.2s;
}

.plusButton:hover>.plusIcon {
  fill: black;
  transform: rotate(180deg);
}

.plusButton:focus-visible>.plusIcon {
  fill: black;
  transform: rotate(180deg);
}



/* Estilo para el modal */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5); /* Fondo semi-transparente */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: #1c1c1c;
  padding: 20px;
  border-radius: 8px;
  width: 300px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
}

.modal-content ul {
  list-style: none;
  padding: 0;
}

.modal-content li {
  margin: 10px 0;
}

.modal-content {
  padding: 20px;
}

.list-item {
  margin: 5px 0;
  display: flex;
  justify-content: space-between; /* Espacia los elementos a los extremos */
  align-items: center;
}

.list-item-content {
  display: flex;
  align-items: center;
  justify-content: space-between; /* Alinea nombre de lista y botón en los extremos */
  width: 100%; /* Hace que ocupe todo el espacio disponible */
}

.list-name {
  font-weight: bold; /* Para destacar el nombre de la lista */
  margin-right: 5px; /* Espacio entre el nombre de la lista y el botón */
  margin-left: 25px;
  margin-top: 10px;
}

.list-btn {
  background: none;
  border: none;
  cursor: pointer;
  height: 30px;
  width: 30px;
  background-color: #4CAF50;
  border-radius: 25%;
  margin-right: 30px;
  display: flex;  /* Flexbox para centrar el contenido */
  justify-content: center;  /* Centra el ícono horizontalmente */
  align-items: center;   /* Centra el ícono verticalmente */
}

/* Estilos para el contenedor del icono */
.add-icon {
  width: 20px;   /* Cambia el tamaño del icono */
  height: 20px;  /* Cambia el tamaño del icono */
  fill: #ffffff; /* Cambia el color de relleno del icono */
  transition: fill 0.3s ease; /* Añade una transición suave al color */
  color: #ffffff;
  justify-content: center;
  font-weight: bold;
}

/* Modificación de color del icono cuando el usuario pasa el ratón por encima del botón */
.list-btn:hover .add-icon {
  fill: #4caf4fbf; /* Cambia el color cuando el ratón pasa sobre el botón */
}

.list-btn:hover {
  background-color: #45a049;
}



.cancel-btn {
  background-color: #f44336; /* Rojo para cancelar */
  color: white;
  border: none;
}

.cancel-btn:hover {
  background-color: #e53835bc;
}



/* Estilos del modal de error */
.modal-premium {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5); /* Fondo translúcido */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 100;
}

.modal-content-premium {
  background-color: #1c1c1c;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  width: 300px;
}

.modal-content-premium p {
  margin-bottom: 20px;
  font-size: 16px;
  color:white;
}

.modal-content-premium button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
}

.modal-content-premium button:hover {
  background-color: #0056b3;
}

</style>