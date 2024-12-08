<template>
  <div class="cinesphere">
    <HeaderPage /> <!-- Agrega el componente HeaderPage -->
    <main class="main-content">

      <div class="container">
        <div class="search-wrapper">
          <div class="search-bar">
            <input type="text" v-model="searchQuery" @input="filterPosts" class="search-input"
              placeholder="Search reviews..." />
            <button @click="handleSearch" class="search-button">🔍</button>
          </div>
          <RadioForm v-model="selectedOption" :options="radioOptions" :fontFamily="'Arial, Helvetica, sans-serif'"
            name="movie-options" :fontSize="'15px'" :title="'Show'" id="RadioForm" />

          <div class="input-group mt-2" id="dropdown-menu">
            <label class="input-group-text" for="sortOptions">Sort By</label>
            <select class="form-select" id="sortOptions" @change="handleSortChange">
              <option value="date" selected>Date</option>
              <option value="popularity">Popularity</option>
              <option value="rating">Rating</option>
            </select>
          </div>

          <!-- Optional: Display the selected sort -->
          <p class="mt-3">Selected sort: {{ selectedSort }}</p>

        </div>


        <div class="feed">
          <div class="post" v-for="post in feed" :key="post.id">
            <div class="post-content">
              <img :src="post.moviePoster" v-if="post.moviePoster" :alt="post.movieTitle" class="movie-poster" />
              <div class="post-details">
                <div class="post-higher">
                  <div class="post-header">
                    <img :src="post.user.avatar" :alt="post.user.username" class="avatar" />
                    <div class="user-info">
                      <span class="username">{{ post.user.username }}</span>
                      <span class="timestamp">{{ post.timestamp }}</span>
                    </div>

                  </div>
                  <div class="post-actions">
                    <button :class="['action-button', post.isFollowing ? 'following' : 'not-following']"
                      @click="toggleFollow(post)">
                      {{ post.isFollowing ? 'Following' : 'Follow' }}
                    </button>
                  </div>
                </div>
                <div class="movie-info">
                  <h3 class="movie-title">{{ post.movieTitle }}</h3>
                  <div v-if="post.rating" class="rating">
                    <span v-for="n in 5" :key="n" class="star" :class="{ 'filled': n <= post.rating }">★</span>
                  </div>
                </div>
                <p class="review">{{ post.review }}</p>


              </div>
            </div>
          </div>

        </div>
        <aside class="sidebar">
          <div class="user-profile">
            <img v-if="userData" :src="userData.img_url" alt="Your profile" class="avatar" />
            <img v-else :src="require('@/assets/foto_perfil.png')" alt="Your profile" class="avatar" />
            <h2>Your Profile</h2>
            <p v-if="userData">@{{ userData.full_name }}</p>
            <p v-else>Guest</p>
            <div class="stats">
              <div class="stat">
                <span class="stat-value">{{ this.user_reviews }}</span>
                <span class="stat-label">Reviews</span>
              </div>
              <div class="stat">
                <span class="stat-value">1.2k</span>
                <span class="stat-label">Followers</span>
              </div>
              <div class="stat">
                <span class="stat-value">890</span>
                <span class="stat-label">Following</span>
              </div>
            </div>
          </div>
          <div class="trending-movies">
            <h4>Recently rated movies</h4>
            <ul>
              <li v-for="movie in trendingMovies" :key="movie.id">
                <img :src="movie.poster" :alt="movie.title" class="movie-thumbnail" />
                <div class="movie-info">
                  <span class="movie-title">{{ movie.title }}</span>
                  <div class="rating">
                    <span v-for="n in 5" :key="n" class="star" :class="{ 'filled': n <= movie.rating }">★</span>
                  </div>
                </div>
              </li>
            </ul>
          </div>
        </aside>
      </div>
    </main>
  </div>
</template>

<script>
import HeaderPage from '@/components/HeaderPage.vue'; // Importa el componente HeaderPage
import RadioForm from '@/components/RadioForm.vue'; // Importa el componente RadioForm
import axios from 'axios';
import { API_BASE_URL } from '@/config.js'; // Importa tu archivo de configuración


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

export default {
  name: 'ViewProfile',
  components: {
    HeaderPage, // Registra el componente HeaderPage
    RadioForm // Registra el componente RadioForm
  },
  data() {
    return {
      selectedSort: 'date', // Default sort option
      userData: null,
      profile_image: '',
      user_rated_movies: [],
      user_reviews: 0,
      trendingMovies: [],
      originalPosts: [],
      selectedOption: 'option1', // Default selected value
      radioOptions: [
        { label: 'Posts', value: 'option1' },
        { label: 'Users', value: 'option2' },// Newer
      ],
      searchQuery: '',
      feed: [],
      posts: [
        {
          id: 1,
          user: {
            username: 'moviebuff99',
            avatar: require('@/assets/foto_perfil.png')
          },
          movieTitle: 'Inception',
          moviePoster: require('@/assets/inception_banner.jpg'),
          rating: 5,
          review: "Mind-bending masterpiece! Christopher Nolan outdoes himself with this intricate plot and stunning visuals. A must-watch for any sci-fi fan.",
          timestamp: '2 hours ago',
          isFollowing: true,
        },
        {
          id: 2,
          user: {
            username: 'filmcritic22',
            avatar: require('@/assets/foto_perfil.png')
          },
          movieTitle: 'Bullet Train',
          moviePoster: require('@/assets/bulletTrain_banner.jpg'),
          rating: 5,
          review: "A timeless classic that set the standard for crime dramas. Marlon Brando's performance is unforgettable. Every frame is a masterpiece.",
          timestamp: '5 hours ago',
          isFollowing: false,
        },
        {
          id: 3,
          user: {
            username: 'cinephile42',
            avatar: require('@/assets/foto_perfil.png')
          },
          movieTitle: 'Bohemian Rhapsody',
          moviePoster: require('@/assets/bohemianRhapsody_banner.jpg'),
          rating: 4,
          review: "Tarantino's non-linear storytelling at its finest. The dialogue is sharp, the characters are unforgettable, and the soundtrack is perfect.",
          timestamp: '1 day ago',
          isFollowing: false,
        },

      ],
      users: [],
      user_list: [],

    }
  },
  methods: {
    async fetchUsers(skip = 0, limit = 100) {
      try {
        const response = await axios.get(`${API_BASE_URL}/users/`, {
          params: {
            skip: skip,
            limit: limit,
          },
        });
        return response.data;
      } catch (error) {
        console.error('Error fetching users:', error);
        return [];
      }
    },

    async fillUsers() {
      try {
        const userList = await this.fetchUsers(0, 25);
        console.log('List of USERS', userList);
        this.users = []; // Ensure `this.users` is initialized

        userList.forEach((user) => {
          this.users.push({
            id: this.users.length,
            user: {
              username: user.full_name,
              avatar: user.img_url
                ? user.img_url
                : require('@/assets/foto_perfil.png'), // Fallback avatar
            },
            isFollowing: false,
          });
        });
      } catch (error) {
        console.error('Error filling users:', error);
      }
    },

    handleSortChange(event) {
      this.selectedSort = event.target.value;
      console.log('Sort by:', this.selectedSort);

      // Add logic to sort your data based on the selected value
      if (this.selectedSort === 'date') {
        // Sort by date
      } else if (this.selectedSort === 'popularity') {
        // Sort by popularity
      } else if (this.selectedSort === 'rating') {
        // Sort by rating
      }
    },
    handleSearch() {
      console.log('Searching for:', this.searchQuery);
    },
    filterPosts() {
      const query = this.searchQuery.toLowerCase();
      this.feed = this.originalPosts.filter(feed => {
        const movieTitle = feed.movieTitle ? feed.movieTitle.toLowerCase() : '';
        const review = feed.review ? feed.review.toLowerCase() : '';
        const username = feed.user.username ? feed.user.username.toLowerCase() : '';
        return movieTitle.includes(query) || review.includes(query) || username.includes(query);
      });
    },


    toggleFollow(post) {
      post.isFollowing = !post.isFollowing;
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
    loadLastRatedMovies() {
      if (!this.userData) {
        console.error('No user data available');
        return;
      }
      // Solicitar las películas valoradas
      axios
        .get(`${API_BASE_URL}/movies/rated_list/${this.userData.id}`)
        .then(async (response) => {
          const ratedMoviesList = response.data;
          this.user_reviews = ratedMoviesList.length;
          // Tomar las últimas 3 películas valoradas
          const lastRatedMovies = ratedMoviesList.slice(-3);

          // Obtener detalles completos de las últimas 3 películas
          const ratedMoviesDetails = await Promise.all(
            lastRatedMovies.map(async (movie) => {
              const movieData = await this.fetchMovieDetails(movie.title);
              return movieData ? generateMovieObject(movieData, movie.rating) : null;
            })
          );

          // Asignar las películas valoradas filtradas a ratedMovies
          this.ratedMovies = ratedMoviesDetails.filter((movie) => movie !== null);

          // Actualizar trendingMovies con los resultados
          this.trendingMovies = this.ratedMovies.map((movie) => ({
            id: movie.id,
            title: movie.title,
            poster: movie.smallImage, // Asegúrate de usar el campo que corresponde a la portada
            rating: movie.userRating || movie.rating, // Mostrar rating del usuario si está disponible
          }));
        })
        .catch((error) => {
          console.error('Error al obtener las últimas películas valoradas:', error);
        });
    },


  },
  mounted() {
    // Keep a copy of the original posts for filtering
    this.originalPosts = [...this.feed];
  },
  created() {
    this.fillUsers();
    this.feed = this.posts;
    const userEmail = localStorage.getItem('userEmail');
    if (!userEmail) {
      return;
    }

    // Solicitar datos del usuario
    axios
      .get(`${API_BASE_URL}/users/email/${userEmail}`)
      .then((response) => {
        this.userData = response.data;

        // Verificar que userData esté disponible antes de cargar las películas valoradas
        if (this.userData) {
          // Cargar las películas valoradas y con like desde un solo endpoint
          this.loadLastRatedMovies();
        }
      })
      .catch((error) => {
        console.error('Error al obtener los datos del usuario:', error);
        this.error = 'Error fetching user data. Please try again.';
      });
  },

  watch: {
    selectedOption(newVal) {
      if (newVal === 'option1') {
        this.feed = this.posts;
        this.originalPosts = [...this.posts];
      } else {
        this.feed = this.users;
        this.originalPosts = [...this.users];
      }
    }
  }


}
</script>

<style scoped>
.cinesphere {
  background-color: #121212;
  color: #ffffff;
  font-family: Arial, sans-serif;

}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.main-content {
  padding: 20px 0;
}

.main-content .container {
  display: flex;
  gap: 20px;
  margin-top: 5rem;
}

.feed {
  flex: 1;
  max-height: 85%;
  overflow-y: auto;
}

.post {
  display: flex;
  background-color: #1a1a1a;
  border-radius: 10px;
  margin-bottom: 20px;
  padding: 15px;
  gap: 15px;
  align-items: flex-start;
}

.post-header {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  justify-content: flex-start;

}

.post-higher {
  display: flex;
  justify-content: space-between;
}


.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
}

.username {
  font-weight: bold;
}

.timestamp {
  font-size: 12px;
  color: #888;
  margin-left: 10px;
}

.post-content {
  display: flex;
  flex: 1;
  gap: 15px;
}

.movie-poster {
  width: 100px;
  height: 150px;
  object-fit: cover;
  border-radius: 10px;
  flex-shrink: 0;
}

.movie-title {
  font-size: 18px;
  margin-bottom: 5px;
}

.rating {
  margin-bottom: 10px;
}

.star {
  color: #888;
  font-size: 18px;
}

.star.filled {
  color: #ffc107;
}

.review {
  font-size: 14px;
  line-height: 1.4;
}

.post-actions {
  display: flex;
  gap: 15px;
  margin-top: auto;
  /* Push actions to the bottom */
}

.post-details {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.action-button {
  margin-left: auto;
  padding: 8px 12px;
  border-radius: 5px;
  font-size: 12px;
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s;
  border: none;
  min-width: 5wh;
  max-width: 5wh;
}

.action-button.following {
  background-color: #d21bd8;
  /* Violet for "Following" */
  color: #ffffff;
}

.action-button.following:hover {
  background-color: #b700d6;
  /* Darker violet on hover */
}

.action-button.not-following {
  background-color: #cccccc;
  /* Light gray for "Not Following" */
  color: #000000;
}

.action-button.not-following:hover {
  background-color: #b3b3b3;
  /* Darker gray on hover */
}


.sidebar {
  width: 300px;
}

.user-profile {
  background-color: #1a1a1a;
  border-radius: 10px;
  padding: 20px;
  text-align: center;
  margin-bottom: 20px;
}

.user-profile .avatar {
  width: 80px;
  height: 80px;
  margin-bottom: 10px;
}

.user-profile h2 {
  margin-bottom: 5px;
}

.user-profile p {
  color: #888;
  margin-bottom: 15px;
}

.stats {
  display: flex;
  justify-content: space-around;
}

.stat {
  text-align: center;
}

.stat-value {
  font-size: 18px;
  font-weight: bold;
  display: block;
}

.stat-label {
  font-size: 12px;
  color: #888;
}

.trending-movies {
  background-color: #1a1a1a;
  border-radius: 10px;
  padding: 20px;
}

.trending-movies h3 {
  margin-bottom: 15px;
}

.trending-movies ul {
  list-style: none;
  padding: 0;
}

.trending-movies li {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.movie-thumbnail {
  width: 60px;
  height: 90px;
  object-fit: cover;
  border-radius: 5px;
  margin-right: 10px;
}

.trending-movies .movie-info {
  flex: 1;
}

.trending-movies .movie-title {
  font-size: 14px;
  margin-bottom: 5px;
}

.trending-movies .rating {
  font-size: 12px;
}

@media (max-width: 768px) {
  .main-content .container {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
  }

  .search-bar {
    display: none;
  }
}

.search-wrapper {
  margin-bottom: 20px;
}

.search-bar {
  display: flex;
  align-items: center;
  background-color: #2c2c2c;
  border-radius: 10px;
  padding: 5px 15px;
  max-width: 400px;
  margin: 0 auto;
  /* Centers the search bar */
}

.search-input {
  background: none;
  border: none;
  color: #ffffff;
  padding: 8px;
  flex: 1;
  font-size: 14px;
  outline: none;
}

.search-button {
  background: none;
  border: none;
  color: #ff4081;
  font-size: 18px;
  cursor: pointer;
}

#RadioForm {
  margin-top: 5vh;
  margin-bottom: 5vh;
}

.input-group-text {
  background-color: #2c2c2c;
  color: #b3b3b3;
  border-color: rgb(148, 146, 146);
}

.form-select {
  background-color: #2c2c2c;
  color: #e7e5e5;
  border-color: rgb(148, 146, 146);
}
</style>