<template>
  <div class="profile-page">
    <HeaderPage />

    <!-- Modal para agregar nueva lista -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal-content">
        <h2>Create New List</h2>
        <form @submit.prevent="createNewList">
          <label for="list-name">List Name</label>
          <input
            id="list-name"
            type="text"
            v-model="newListName"
            maxlength="16" 
            placeholder="Enter list name"
            required
          />
          <div class="modal-buttons">
            <button type="submit" class="create-btn">Create List</button>
            <button type="button" @click="closeModal" class="cancel-btn">Cancel</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal to show error when the limit of 3 lists is exceeded -->
    <div v-if="showLimitModal" class="modal-limit-overlay">
      <div class="modal-limit">
        <p>You have exceeded the maximum limit of 3 lists. Please delete a list to add a new one.</p>
        <button @click="closeLimitModal">Ok</button>
      </div>
    </div>

    <!-- Modal de aviso si no es premium -->
    <div v-if="showPremiumModal" class="modal-premium">
      <div class="modal-content-premium">
        <p>This feature is only available for Premium accounts.</p>
        <button @click="closePremiumModal">Ok</button>
      </div>
    </div>

    <!-- Modal de confirmación para eliminar -->
    <div v-if="showDeleteModal" class="modal-overlay">
      <div class="modal-content">
        <p>Are you sure you want to delete the list "{{ listToDelete }}"?</p>
        <div class="modal-buttons">
          <button @click="confirmDelete" class="create-btn">Yes</button>
          <button @click="closeDeleteModal" class="cancel-btn">Cancel</button>
        </div>
      </div>
    </div>
    

    <div class="overlay"></div>

    <div class="main-content">
      <div class="shadow-overlay"></div>
      <div class="profile-box">

        <p v-if="error" class="error-message">{{ error }}</p>

        <div v-else-if="userData" class="profile-content">
          <!-- Imagen de perfil -->
          <div class="profile-image">
            <div class="profile-image-image">
              <img :src="userData.img_url || require('@/assets/foto_perfil.png')" alt="Profile Picture" />
            </div>
            <div class="extra-info">

              <div class="info-follow" @click="scrollToRatedMovies()">

                <h5>{{ ratedMovies.length }}</h5>
                <h6>Reviews</h6>

              </div>
              <div class="info-follow" @click="openPopup('followers')">
                <h5>{{ followers.length }}</h5>
                <h6>Followers</h6>
              </div>
              <div class="info-follow" @click="openPopup('following')">
                <h5>{{ following.length }}</h5>
                <h6>Following</h6>
              </div>

            </div>

          </div>

          <div class="profile-info">
            <div class="privacity-div">
              <strong>Account type:</strong><br />
              <span>{{ accountType(userData.isPublic) }} and {{ isAdmin(userData.is_admin) }}</span>
            </div>
            <div class="email-div">
              <strong>Email Address:</strong><br />
              <span>{{ userData.email }}</span>
            </div>
            <div class="username-div">
              <strong>Name:</strong><br />
              <span>{{ userData.full_name }}</span>
            </div>
            <!-- Mostrar la contraseña oculta -->
            <div class="password-div">
              <strong>Password:</strong><br />
              <span>********</span>
            </div>
          </div>

          <div class="btns-div">
            <router-link to="/addMovies">
              <button v-if="userData.is_admin" class="add-btn">Add Movies</button>
            </router-link>
            <router-link to="/edit">
              <button class="modify-btn">Modify</button>
            </router-link>
            <router-link to="/reportedComments">
              <button class="report-comments-btn">Reported comments</button>
            </router-link>
          </div>

        </div>

        <div v-else class="loading-message">
          Loading profile...
        </div>

      </div>
    </div>

    <!-- Sección de películas (liked o rated) -->
    <div class="movies-section">
      <!-- Nueva capa de overlay -->
      <div class="movies-overlay"></div>

      <div class="movies-header">
        <!-- Botones predeterminados -->
        <div class="default-buttons">
          <button :class="{ active: activeList === 'rated' }" @click="toggleMovies('rated')">
            Rated Movies
          </button>
          <button :class="{ active: activeList === 'liked' }" @click="toggleMovies('liked')">
            Favourite Movies
          </button>
          <button :class="{ active: activeList === 'wishlist' }" @click="toggleMovies('wishlist')">
            Wishlist Movies
          </button>
        </div>
      
        <!-- Botones de listas personalizadas -->
        <div class="dynamic-buttons">
          <!-- Mostrar solo las listas dinámicas si el usuario es premium -->
          <div v-if="isPremium">
            <button
              v-for="(list, index) in userLists"
              :key="index"
              class="dynamic-button"
              :class="{ active: activeList === list.name }"
              @click="selectList(list.name)"
            >
              {{ list.name }}
              <!-- Botón de eliminar que abre el modal -->
              <span class="delete-button-list" @click.stop="openDeleteModal(list.name)"></span>
            </button>
          </div>
        
          <!-- Botón de agregar nueva lista, siempre visible -->
          <button class="add-new-list-btn" @click="openAddListModal">
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
            Add New
          </button>
        </div>
        
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
          <div v-if="activeList === 'rated'" class="user-rating">
            <img src="@/assets/star.png" alt="Rating" class="icon" />
            <span>{{ movie.userRating }}</span>
          </div>

          
            <!-- Botón para eliminar película  -->
          <button class="delete-button" @click="removeMovie(movie.id)">
            <svg class="delete-svgIcon" viewBox="0 0 448 512">
              <path d="M135.2 17.7L128 32H32C14.3 32 0 46.3 0 64S14.3 96 32 96H416c17.7 0 32-14.3 32-32s-14.3-32-32-32H320l-7.2-14.3C307.4 6.8 296.3 0 284.2 0H163.8c-12.1 0-23.2 6.8-28.6 17.7zM416 128H32L53.2 467c1.6 25.3 22.6 45 47.9 45H346.9c25.3 0 46.3-19.7 47.9-45L416 128z"></path>
            </svg>
          </button>

        </div>
      </div>   
    </div>

    <!-- Aquí va el componente del popup -->
    <FollowsPopup :isVisible="isPopupVisible" :title="popupTitle" @close="closePopup">
      <div v-for="user in popupList" :key="user.id" class="user-card">
        <img :src="user.img_url || defaultImage" alt="Profile Image" class="user-image-popup" />
        <router-link :to="`/otherProfiles/${user.full_name}` " class="user-name-popup">
          <p>{{ user.full_name }}</p>
        </router-link>
        <button class="follow-btn" @click="toggleFollow(user)">
          {{ isFollowing(user) ? 'Unfollow' : 'Follow' }}
        </button>
      </div>
    </FollowsPopup>

    <FooterComponent />
  </div>
</template>



<script>
  import HeaderPage from '@/components/HeaderPage.vue';
  import FooterComponent from '@/components/FooterComponent.vue';
  import FollowsPopup from '@/components/FollowsPopup.vue';
  import axios from 'axios';
  import { API_BASE_URL } from '@/config.js';

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
    };

    if (userRating !== null) {
      movieObject.userRating = userRating; // Solo se agrega si está presente
    }

    return movieObject;
  }


  export default {
    name: 'UserProfile',
    components: {
      HeaderPage,
      FooterComponent,
      FollowsPopup,
    },
    data() {
      return {
        userData: null,
        error: null,
        profile_image: '',
        activeList: 'rated',
        showRatedMovies: true, // Controla si se muestran las valoradas o las con like
        showFavouriteMovies: false,
        showWishlistMovies: false,
        ratedMovies: [], // Películas valoradas
        likedMovies: [], // Películas con like
        wishedMovies: [], // Películas en la wishlist
        displayedMovies: [], // Películas que se muestran actualmente
        isPremium: false, // Inicializamos en `false` por defecto

        // Datos para el modal
        showModal: false,
        newListName: '', // Nombre de la nueva lista

        // Listas predeterminadas (no deben añadirse a `userLists`).
        defaultLists: ['Rated', 'Favourite', 'Wishlist'], 

        // Aquí irán las listas creadas por el usuario.
        userLists: [], 
        showLimitModal: false,
        showPremiumModal: false,  // Para mostrar el modal de error
        showDeleteModal: false,
        listToDelete: null,

        followers: [], // Lista de seguidores
        following: [], // Lista de seguidos
        isPopupVisible: false,
        popupTitle: '',
        popupList: [],
        defaultImage: require('@/assets/foto_perfil.png'), // Ruta a una imagen por defecto

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
        .get(`${API_BASE_URL}/users/email/${userEmail}`)
        .then((response) => {
          this.userData = response.data;

          // Actualizar el estado de `isPremium` desde los datos recibidos
          this.isPremium = response.data.is_premium;

          // Cargar las películas valoradas, con like y en wishlist
          this.loadMovies();
          this.loadLists();
        })
        .catch((error) => {
          console.error('Error al obtener los datos del usuario:', error);
          this.error = 'Error fetching user data. Please try again.';
        });

      // Cargar la lista de seguidores
      this.loadFollowers();
      this.loadFollowing();
    },
    methods: {

      isAdmin(isAdmin) {
        if(isAdmin){
          return 'Admin';
        }
        else{
          return 'User';
        }
      },

      accountType(accType){
        if(accType === 'public'){
          return 'Public';
        }
        else if(accType === 'private'){ 
          return 'Private';
        }

        return 'Only Followers';
      },

      scrollToRatedMovies() {
        this.toggleMovies('rated'); // Cambiar a la vista de Rated Movies
        this.$nextTick(() => {
          const ratedSection = this.$refs.ratedMoviesSection;
          if (ratedSection) {
            ratedSection.scrollIntoView({ behavior: 'smooth' }); // Desplazamiento suave
          }
        });
      },

      isFollowing(user) {
        return this.following.some(followingUser => followingUser.id === user.id);
      },

      openPopup(type) {
        if (type === 'followers') {
          this.popupTitle = 'Followers';
          this.popupList = this.followers;
        } else if (type === 'following') {
          this.popupTitle = 'Following';
          this.popupList = this.following;
        }
        this.isPopupVisible = true;
      },

      closePopup() {
        this.isPopupVisible = false;
      },

      async toggleFollow(user) {
        const url = `${API_BASE_URL}/users/${this.isFollowing(user) ? 'unfollow' : 'follow'}/${user.id}`;
        const token = localStorage.getItem('token');
        try {
          await axios.post(
            url,
            {},
            {
              headers: {
                Authorization: `Bearer ${token}`,
                Accept: 'application/json',
              },
            }
          );
          this.loadFollowing(); // Recarga la lista para reflejar los cambios
          this.loadFollowers(); // Recarga la lista para reflejar los cambios
        } catch (error) {
          console.error(this.isFollowing(user) ? 'Error unfollowing user:' : 'Error following user:', error);
        }
      },

      async fetchMovieDetails(title) {
        try {
          const movieResponse = await axios.get(`${API_BASE_URL}/movies/title/${title}`);
          return movieResponse.data; // Devuelve los detalles completos de la película
        } catch (error) {
          console.error(`Error al obtener detalles de la película "${title}":`, error);
          return null; // Retorna null si hay un error
        }
      },

      async loadFollowers() {
        // Obtener la lista de seguidores
        const url = `${API_BASE_URL}/users/followers/${localStorage.getItem('user_id')}`;

        // Make the GET request
        axios.get(url, {
          headers: {
            'accept': 'application/json'
          }
        })
          .then(response => {
            // Handle the response
            this.followers = response.data;
            if (this.popupTitle === 'Followers') {
              this.popupList = this.followers;
            }
            else {
              this.popupList = this.following;
            }

          })
          .catch(error => {
            // Handle the error
            console.error('Error occurred:', error);
          });

      },

      async loadFollowing() {
        // Obtener la lista de seguidos
        const url = `${API_BASE_URL}/users/followed/${localStorage.getItem('user_id')}`;

        // Make the GET request
        axios.get(url, {
          headers: {
            'accept': 'application/json'
          }
        })
          .then(response => {
            // Handle the response
            this.following = response.data;
            if (this.popupTitle === 'Following') {
              this.popupList = this.following;
            }
            else {
              this.popupList = this.followers;
            }


          })
          .catch(error => {
            // Handle the error
            console.error('Error occurred:', error);
          });

      },


      loadMovies() {
        // Cargar las películas liked, rated y wished
        axios
          .get(`${API_BASE_URL}/movies/liked_list/${this.userData.id}`)
          .then((response) => {
            const likedMoviesTitles = response.data;

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

                    Promise.all([likedMoviesDetails, ratedMoviesDetails, wishedMoviesDetails])
                      .then(([likedMovies, ratedMovies, wishedMovies]) => {
                        this.likedMovies = likedMovies.filter((movie) => movie !== null);
                        this.ratedMovies = ratedMovies.filter((movie) => movie !== null);
                        this.wishedMovies = wishedMovies.filter((movie) => movie !== null);

                        this.updateDisplayedMovies();
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

      loadLists() {
        if (!this.userData) {
          console.error('Error: No se han cargado los datos del usuario.');
          return;
        }

        console.log('Email enviado al backend:', this.userData.email); // Añadido para depuración

        axios
          .get(`${API_BASE_URL}/list-type/email/${this.userData.email}`)
          .then((response) => {
            console.log('Listas obtenidas del backend:', response.data);
            
            // Listas creadas por el usuario obtenidas del backend
            const userCreatedLists = response.data.map((list) => ({
              name: list.name,
              id: list.id,
            }));

            // Aseguramos que `userLists` contenga solo una copia de las listas predeterminadas
            const defaultLists = [
            ];
            // Actualizamos `userLists` fusionando listas predeterminadas con las del backend
            this.userLists = [
              ...defaultLists, // Listas predeterminadas
              ...userCreatedLists, // Listas del backend
            ];
          })
          .catch((error) => {
            console.error('Error al obtener las listas del usuario:', error);
          });
      },


      toggleMovies(type) {
        this.activeList = type; // Actualizamos la lista activa

        // Actualizamos las variables para las listas predeterminadas
        this.showRatedMovies = type === 'rated';
        this.showFavouriteMovies = type === 'liked';
        this.showWishlistMovies = type === 'wishlist';

        // Actualizamos las películas mostradas
        switch (type) {
          case 'rated':
            this.displayedMovies = this.ratedMovies;
            break;
          case 'liked':
            this.displayedMovies = this.likedMovies;
            break;
          case 'wishlist':
            this.displayedMovies = this.wishedMovies;
            break;
          default:
            console.warn('Tipo de lista desconocido:', type);
        }
      },


      updateDisplayedMovies() {
        this.displayedMovies = this.showRatedMovies
          ? this.ratedMovies
          : this.showFavouriteMovies
          ? this.likedMovies
          : this.wishedMovies;
      },

      removeMovie(movieId) {
        switch (this.activeList) {
          case 'rated':
            this.unrateMovie(movieId);
            break;
          case 'liked':
            this.dislikeMovie(movieId);
            break;
          case 'wishlist':
            this.removeFromWishlist(movieId);
            break;
          default:
            // Si es una lista personalizada
            if (this.userLists.some(list => list.name === this.activeList)) {
              this.removeMovieFromDynamicList(movieId);
            } else {
              console.warn('Lista activa no reconocida.');
            }
        }
      },

      async unrateMovie(movieId) {
        try {
          await axios.post(`${API_BASE_URL}/movies/unrate/${movieId}/${this.userData.id}`);
          this.ratedMovies = this.ratedMovies.filter((movie) => movie.id !== movieId);
          this.updateDisplayedMovies();
        } catch (error) {
          console.error('Error al descalificar la película:', error);
        }
      },

      async dislikeMovie(movieId) {
        try {
          await axios.post(`${API_BASE_URL}/movies/dislike/${movieId}/${this.userData.id}`);
          this.likedMovies = this.likedMovies.filter((movie) => movie.id !== movieId);
          this.updateDisplayedMovies();
        } catch (error) {
          console.error('Error al marcar la película como dislike:', error);
        }
      },

      async removeFromWishlist(movieId) {
        try {
          await axios.post(`${API_BASE_URL}/movies/nowish/${movieId}/${this.userData.id}`);
          this.wishedMovies = this.wishedMovies.filter((movie) => movie.id !== movieId);
          this.updateDisplayedMovies();
        } catch (error) {
          console.error('Error al eliminar la película de la wishlist:', error);
        }
      },

      async removeMovieFromDynamicList(movieId) {
        try {
          // Llamada al endpoint para eliminar de la lista activa
          const response = await axios.delete(
            `${API_BASE_URL}/list-type/remove-movie/${this.userData.email}/${this.activeList}/${movieId}`
          );

          if (response.status === 200) {
            // Actualizar las películas de la lista activa
            this.displayedMovies = this.displayedMovies.filter(movie => movie.id !== movieId);
          } else {
            alert('No se pudo eliminar la película. Inténtalo de nuevo.');
          }
        } catch (error) {
          console.error(`Error al eliminar la película "${movieId}" de la lista "${this.activeList}":`, error);
          alert('Hubo un error al intentar eliminar la película.');
        }
      },


      openAddListModal() {
        if (this.isPremium) {
          if (this.userLists.length >= 3) {
          // Si ya hay 3 listas, muestra el modal de error
          this.showLimitModal = true;
          this.closeModal();
          return;
          }else{
            this.showModal = true; // Mostrar el modal
          }
        } else {
          this.showPremiumModal = true; // Mostrar el modal si no es premium
        }
      },

      closeModal() {
        this.showModal = false; // Cerrar el modal
        this.newListName = ''; // Limpiar el campo de texto
      },

      async createNewList() {

        if (this.newListName.trim() === '') {
          alert('Please enter a valid list name.');
          return;
        }

        const listExists = this.userLists.some(
          (list) => list.name.toLowerCase() === this.newListName.toLowerCase()
        );
        if (listExists) {
          alert('A list with this name already exists.');
          return;
        }

        try {
          const response = await axios.post(
            `${API_BASE_URL}/list-type/${this.userData.email}/${this.newListName.trim()}`
          );

          this.userLists.push({
            name: this.newListName.trim(),
            id: response.data.id,
          });

          this.newListName = '';
          this.closeModal();
        } catch (error) {
          console.error('Error al crear la nueva lista:', error);
          alert('There was an error creating the list. Please try again.');
        }
      },   

          // Función para cerrar el modal de error
      closeLimitModal() {
        this.showLimitModal = false;  // Cerrar el modal de error
      },

      closePremiumModal() {
        this.showPremiumModal = false;  // Cerrar el modal de error
      },
      

      async loadMoviesFromList(listName) {
        try {
          const userEmail = localStorage.getItem('userEmail');
          if (!userEmail) {
            console.error('User email not found');
            return;
          }

          const response = await axios.get(`${API_BASE_URL}/list-type/movies/${userEmail}/${listName}`);

          // Suponiendo que la respuesta contiene una lista de películas
          const movies = response.data.map(movie => generateMovieObject(movie));

          // Actualizar las películas mostradas según la lista seleccionada
          this.displayedMovies = movies;
        } catch (error) {
          console.error('Error al cargar las películas de la lista:', error);
        }
      },

      // Método para manejar la selección de una lista
      async selectList(listName) {
        this.activeList = listName; // Actualiza la lista activa a la nueva lista personalizada

        try {
          const response = await axios.get(
            `${API_BASE_URL}/list-type/movies/${this.userData.email}/${listName}`
          );

          this.displayedMovies = await Promise.all(
            response.data.map(async (movieTitle) => {
              const movieData = await this.fetchMovieDetails(movieTitle);
              return movieData ? generateMovieObject(movieData) : null;
            })
          ).then((movies) => movies.filter((movie) => movie !== null));
        } catch (error) {
          console.error(`Error al cargar las películas de la lista "${listName}":`, error);
          alert('Hubo un error al cargar las películas de esta lista. Por favor, inténtalo de nuevo.');
        }
      },

      async deleteList(listName) {
        try {
          const userEmail = localStorage.getItem('userEmail');
          if (!userEmail) {
            console.error('No user email found');
            return;
          }

          // Realiza la solicitud DELETE al servidor
          await axios.delete(`${API_BASE_URL}/list-type/${userEmail}/${listName}`);
          this.$router.go(); // Recarga si estás en UserProfile

          // Actualiza las listas en el frontend
          this.userLists = this.userLists.filter(list => list.name !== listName);

          console.log(`List "${listName}" deleted successfully.`);
        } catch (error) {
          console.error('Error deleting the list:', error);
          alert('An error occurred while deleting the list. Please try again.');
        }
      },

      openDeleteModal(listName) {
        this.listToDelete = listName; // Guarda la lista seleccionada
        this.showDeleteModal = true; // Muestra el modal
      },
      
      // Cerrar el modal
      closeDeleteModal() {
        this.listToDelete = null; // Limpia la lista seleccionada
        this.showDeleteModal = false; // Oculta el modal
      },
      
      // Confirmar eliminación de la lista
      async confirmDelete() {
        if (this.listToDelete) {
          await this.deleteList(this.listToDelete); // Llama al método de eliminar
        }
        this.closeDeleteModal(); // Cierra el modal después de eliminar
      },
      
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
    flex-direction: column;
    background-color: rgba(0, 0, 0, 0.8);
    backdrop-filter: blur(5px);
    padding: 20px;  /* Reducido el padding para que se adapte mejor en pantallas pequeñas */
    border-radius: 10px;
    width: 100%; /* Usamos el 100% del ancho disponible */
    max-width: 1000px; /* Limita el ancho máximo */
    min-width: 300px; /* Permite que el contenedor se haga pequeño en pantallas muy pequeñas */
    height: auto; /* La altura se ajustará según el contenido */
    min-height: 300px; /* Se asegura que el contenedor no se haga demasiado pequeño */
    color: white;
    z-index: 20;
    box-shadow: 0 10px 30px rgba(179, 219, 240, 0.5);

    border: 2px solid rgba(255, 255, 255, 0.1);
    box-sizing: border-box; /* Asegura que el padding no afecte el tamaño del contenedor */
    overflow: hidden; /* Evita que los elementos se salgan del contenedor */

    display: flex;
    justify-content: center; /* Centra horizontalmente */
    align-items: center; /* Centra verticalmente (si es necesario) */
  }
  
  /* Contenido del perfil (imagen + info) */
  .profile-content {
    display: flex; /* Disposición horizontal de los contenedores en pantallas grandes */
    flex-wrap: wrap; /* Permite que los elementos pasen a la siguiente línea si es necesario */
    gap: 0px; /* Espacio entre los elementos */
    box-sizing: border-box;
    width: 100%;

    background-color: transparent;
  }
  
  /* Estilo de la imagen de perfil */
  .profile-image {
    flex: 1; /* Ocupa la mitad del contenedor */
    min-width: 250px; /* Ancho mínimo para la imagen */
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column; /* Apilar los elementos de arriba hacia abajo */
    padding-right: 50px;
    background-color: transparent;
    position: relative; /* Necesario para el posicionamiento absoluto dentro */
    width: 100%;
    gap: 0px;  
  }
  
  .profile-image-image {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%; /* Asegura que la imagen ocupe todo el ancho de su contenedor */
    flex: 0 0 65%; /* El contenedor de la imagen ocupa el 65% del espacio de profile-image */
    margin-bottom: 10px;

    background-color: transparent;
  }

  .profile-image-image img {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    border: 0px solid white;
    object-fit: cover;
  }

  .extra-info {
    display: flex;
    justify-content: space-evenly; /* Distribuye los elementos horizontalmente */
    align-items: center; /* Centra los elementos verticalmente */
    flex: 0 0 35%; /* El contenedor extra-info ocupa el 35% restante del espacio */
    padding: 2vh;
    background-color: transparent;
    width: 100%;
    box-sizing: border-box;
  }

  .info-follow {
    width: 25%; /* Los elementos de info-follow ocupan un 25% del espacio cada uno */
    height: 9vh;
    padding: 2vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 0 20px;
    background: rgba(0, 0, 0, 0.8);
    background: linear-gradient(135deg, rgb(48, 47, 47), rgba(0, 0, 0, 0.8));
    border-radius: 10%;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    cursor: pointer;
    transition: transform 0.3s ease;
    
  }

  .info-follow:hover {
    transform: scale3d(1.1, 1.1, 1.1);
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
    flex: 1; /* Ocupa la mitad del contenedor */
    min-width: 250px; /* Ancho mínimo para la información */
    display: flex;
    flex-direction: column;
    padding: 1rem;
    gap: 20px;
    text-align: center;

    background-color: transparent;
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
  margin-bottom: 15px; /* Separación con los comentarios */
}

/* Lista de comentarios */
.comments-list {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
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

/* Botón para cerrar el modal */
.close-modal-btn {
  margin-top: 15px;
  padding: 10px 20px;
  background-color: #f44336;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
}

.close-modal-btn:hover {
  background-color: #d32f2f; /* Cambiar color al pasar el mouse */
}







  
  /* Botones de acción */
  .add-btn,
.modify-btn,
.report-comments-btn {
  width: 150px;
  /* Misma anchura para todos los botones */
  height: 50px;
  /* Misma altura para todos los botones */
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: background 0.3s ease;
  text-align: center;
  background-color: #0f0f0f;
}
  
.btns-div {
  display: flex;
  justify-content: center;
  gap: 1rem;
  background-color: yellow;
  margin-top: 60px; /* Espacio entre los botones y los otros contenedores */
  width: 100%; /* Ocupa todo el ancho disponible */
  box-sizing: border-box;

  background-color: transparent;
}

.modify-btn:hover,
.report-comments-btn:hover,
.add-btn:hover {
  background: rgba(255, 255, 255, 0.3);
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
  position: relative;
  display: flex;
  top: px; /* 20px desde la parte superior */
  margin: 0 auto;
  margin-top: 20px;
  z-index: 5;
  align-items: left; /* Alinea los botones verticalmente */
}

.default-buttons {
  display: flex;
  gap: 0px;
  margin-right: 0px; /* Espacio entre los botones predeterminados y los nuevos */
  align-items: center; /* Alinea los botones verticalmente */
  max-width: 500px;  /* Cambia este valor según el tamaño que desees */
  flex-shrink: 0; /* Esto evita que los botones se reduzcan de tamaño */
}

.default-buttons button {
  padding: 10px 20px;
  background: rgba(255, 255, 255, 0.2); /* Fondo inicial transparente */
  color: white; /* Texto blanco por defecto */
  border: none;
  border-top-left-radius: 12px;
  border-top-right-radius: 12px;
  border-bottom: 2px solid transparent;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s ease; /* Suavizar transiciones */
  margin-right: 2px; /* Separación entre botones */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Sombra sutil */
}

.add-new-list-btn {
  padding: 10px 20px;
  background: rgba(255, 255, 255, 0.2); /* Fondo inicial transparente */
  color: white; /* Texto blanco por defecto */
  border: none;
  border-top-left-radius: 12px;
  border-top-right-radius: 12px;
  border-bottom: 2px solid transparent;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s ease; /* Suavizar transiciones */
  margin-right: 2px; /* Separación entre botones */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Sombra sutil */
}

/* Efecto hover */
.add-new-list-btn:hover {
  background: #95e06f; /* Azul más claro cuando se pasa el ratón */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Sombra más intensa para el hover */
  transform: translateY(-2px); /* Eleva el botón al pasar el ratón */
}


/* El último botón no tiene margen derecho */
.movies-header button:last-child {
  margin-right: 2px;
}

.movies-header button:first-child {
  margin-left: 0px;
}

/* Estilo para el botón activo */
.movies-header button.active {
  background: #4a90e2; /* Azul más fuerte para el fondo */
  color: white; /* Texto blanco para mejor contraste */
  border-bottom: none;
  position: relative;
  z-index: 10; /* Asegura que el botón activo se quede encima de los demás */
  box-shadow: 0 0 20px rgba(74, 144, 226, 0.8), 0 0 15px rgba(0, 0, 0, 0.3); /* Sombra azulada */
  transform: translateY(-4px); /* Eleva el botón ligeramente */
  text-shadow: 0 0 10px rgba(74, 144, 226, 0.8), 0 0 20px rgba(74, 144, 226, 0.8), 0 0 40px rgba(74, 144, 226, 1); /* Resplandor azul */
}

/* Efecto hover */
.default-buttons button:hover {
  background: #6fa3e0; /* Azul más claro cuando se pasa el ratón */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Sombra más intensa para el hover */
  transform: translateY(-2px); /* Eleva el botón al pasar el ratón */
}

.movies-header button.active:hover {
  background: #3879c0; /* Azul aún más oscuro para hover cuando está activo */
  box-shadow: 0 0 30px rgba(74, 144, 226, 1), 0 0 40px rgba(0, 0, 0, 0.4); /* Brillo más fuerte */
  transform: translateY(-6px); /* Aumenta el efecto de elevación */
  text-shadow: 0 0 15px rgba(74, 144, 226, 1), 0 0 30px rgba(74, 144, 226, 1), 0 0 50px rgba(74, 144, 226, 1); /* Brillo azul más intenso */
}

/* Estilos para el contenedor de botones personalizados (listas nuevas) */

.dynamic-buttons {

display: flex;
gap: 0px; /* Espacio entre los botones dinámicos */
align-items: center; /* Alinea los botones verticalmente */
margin-left: 0px; /* Empuja los botones dinámicos hacia la derecha */
flex-wrap: nowrap;  /* Asegura que no haya salto de línea entre los botones */
}

.dynamic-button {

position: relative; /* Necesario para posicionar el botón de eliminar */
background: rgba(255, 255, 255, 0.2); /* Fondo inicial transparente */
color: white; /* Texto blanco por defecto */
border: none;
border-top-left-radius: 12px;
border-top-right-radius: 12px;
border-bottom: 2px solid transparent;
cursor: pointer;
font-weight: bold;
transition: all 0.3s ease; /* Suavizar transiciones */
margin-right: 2px; /* Separación entre botones */
box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Sombra sutil */
padding: 10px 20px;
}

.dynamic-button:hover {
background: #6fa3e0; /* Azul más claro cuando se pasa el ratón */
box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Sombra más intensa para el hover */
transform: translateY(-2px); /* Eleva el botón al pasar el ratón */
}

/* Asegura que el primer botón de la lista no se mueva */
.dynamic-buttons button:last-child {
margin-left: 0;
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
  background:rgba(255, 255, 255, 0.2);
  border-top-right-radius: 30px;
  border-top-left-radius: 30px;
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



.delete-button {
  position: absolute;
  bottom: 290px;
  right: 15px;
  min-width: 40px;
  min-height: 40px;
  width: 40px;
  height: 40px;
  margin-bottom: 10px;
  border-radius: 50%;
  background-color: rgb(20, 20, 20, 0.8);
  backdrop-filter: blur(10px);
  border: none;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.164);
  cursor: pointer;
  transition-duration: 0.3s;
  overflow: hidden;
}

.delete-svgIcon {
  width: 15px;
  transition-duration: 0.3s;
}

.delete-svgIcon path {
  fill: white;
}

.delete-button:hover {
  width: 90px;
  border-radius: 50px;
  transition-duration: 0.3s;
  background-color: rgb(255, 69, 69);
  align-items: center;
}

.delete-button:hover .delete-svgIcon {
  width: 20px;
  transition-duration: 0.3s;
  transform: translateY(60%);
  -webkit-transform: rotate(360deg);
  -moz-transform: rotate(360deg);
  -o-transform: rotate(360deg);
  -ms-transform: rotate(360deg);
  transform: rotate(360deg);
}

.delete-button::before {
  display: none;
  content: "Delete";
  color: white;
  transition-duration: 0.3s;
  font-size: 2px;
}

.delete-button:hover::before {
  display: block;
  padding-right: 10px;
  font-size: 13px;
  opacity: 1;
  transform: translateY(0px);
  transition-duration: 0.3s;
}



.Btn {
  position: absolute;
  width: 45px; /* Ancho mayor para mostrar la curva más notoria */
  height: 45px; /* Altura del botón */
  border: none;
  background: rgba(0, 195, 255, 0);
  background-size: 250%;
  background-position: left;
  display: flex;
  align-items: center;
  justify-content: center;
  transition-duration: 0.5s;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.11);
  margin-left: 124px;
  margin-bottom: 200px;
  border-radius: 25px;
  cursor: default;

}

.logoIcon {
  fill: blue;
  opacity: 0;
}


.gold-crown {
  fill: gold; /* Cambia el color de la corona a dorado */
  opacity: 1;
}

.gold-border img{
  border: 0px solid gold; /* Borde dorado */
}


/* Modal styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10000;
}

.modal-content {
  background-color: #1c1c1c;
  color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  max-width: 400px;
  width: 100%;
}

.modal-content h2 {
  text-align: center;
  font-size: 1.5rem;
  margin-bottom: 15px;
}

.modal-content form {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.modal-content label {
  font-size: 14px;
  font-weight: bold;
}

.modal-content input {
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
  font-size: 14px;
  outline: none;
}

.modal-content input:focus {
  border-color: #4CAF50;
}

.modal-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.cancel-btn,
.create-btn {
  padding: 10px 15px;
  border-radius: 5px;
  font-size: 14px;
  cursor: pointer;
}

.cancel-btn {
  background-color: #f44336; /* Rojo para cancelar */
  color: white;
  border: none;
}

.cancel-btn:hover {
  background-color: #e53935;
}

.create-btn {
  background-color: #4CAF50; /* Verde para crear lista */
  color: white;
  border: none;
}

.create-btn:hover {
  background-color: #45a049;
}


.delete-button-list {
  position: absolute;
  top: 5px;
  right: 5px;
  background-color: rgba(255, 0, 0, 0.5);
  border: none;
  border-radius: 2px;
  width: 10px;
  height: 10px;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Inicialmente, la cruz no es visible */
.delete-button-list::after {
  content: ''; /* La cruz se genera con este pseudo-elemento */
  width: 8px;
  height: 1.5px;
  background-color: transparent;
  position: absolute;
  transform: rotate(45deg);
  transition: background-color 0.3s, transform 0.3s;
}

.delete-button-list::before {
  content: '';
  width: 8px;
  height: 1.5px;
  background-color: transparent;
  position: absolute;
  transform: rotate(-45deg);
  transition: background-color 0.3s, transform 0.3s;
}

/* Hover: Cambia el color de fondo y muestra la cruz */
.delete-button-list:hover {
  background-color: rgba(255, 0, 0, 1);
}

.delete-button-list:hover::after,
.delete-button-list:hover::before {
  background-color: white;
}

/* Estilos para el botón de eliminar (oculto por defecto) */
.dynamic-button .delete-button-list {
  position: absolute;
  top: 5px;
  right: 5px;
  width: 10px;
  height: 10px;
  background-color: rgb(255, 0, 0, 0.5);
  border-radius: 25%;
  cursor: pointer;
  opacity: 0; /* Lo ocultamos por defecto */
  transition: opacity 0.3s ease; /* Transición suave */
}

/* Cuando el ratón pase por encima de la lista, el botón de eliminar aparecerá */
.dynamic-button:hover .delete-button-list {
  opacity: 1; /* Lo hacemos visible */
}

/* Estilo del contorno para el botón de eliminar */
.delete-button-list::before {
  color: white;
  font-weight: bold;
  font-size: 18px;
  text-align: center;
  line-height: 20px;
}



/* Estilos del modal de error */
.modal-limit-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5); /* Fondo translúcido */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-limit {
  background-color: #1c1c1c;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  width: 300px;
}

.modal-limit p {
  margin-bottom: 20px;
  font-size: 16px;
  color:white;
}

.modal-limit button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
}

.modal-limit button:hover {
  background-color: #0056b3;
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

.user-image-popup {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
}

.user-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px;
  margin-bottom: 10px;
  border: none;
  border-radius: 8px;
  background-color: #0f0f0f;
}

.user-name {
  flex: 1;
  font-size: 16px;
  font-weight: bold;
  color: rgb(255, 255, 255);
  margin-right: 10px;
}

.user-name-popup {
    font-size: 16px;
    font-weight: bold;
    color: rgb(255, 255, 255);
    margin-right: 10px;
    text-decoration: none;
    flex:1;
    
}

.user-name-popup:hover {
    text-decoration: underline;
}


.follow-btn {
  background-color: #5d0d92;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 5px;
  cursor: pointer;
}

.follow-btn:hover {
  background-color: #2d0349;
}


</style>