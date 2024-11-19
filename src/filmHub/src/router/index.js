import { createRouter, createWebHistory } from 'vue-router';
import MainPageView from '../views/MainPageView.vue';
import UserRegister from '../views/UserRegister.vue';
import UserLogin from '../views/UserLogin.vue';
import MovieDetails from '../views/MovieDetails.vue';

import UserProfile from '../views/UserProfile.vue';
import EditProfile from '../views/EditProfile.vue';

import AllMovies from '../views/AllMovies.vue';
import AddMovies from '../views/AddMovies.vue'; // Importa el componente 



const routes = [
  {
    path: '/',
    name: 'MainPageView',
    component: MainPageView,
  },
  {
    path: '/register',
    name: 'UserRegister',
    component: UserRegister,
  },
  {
    path: '/login',
    name: 'UserLogin',
    component: UserLogin,
  },
  {

    path: '/movie/:id',
    name: 'MovieDetails',
    component: MovieDetails,
  },

  {
    path: '/profile',
    name: 'UserProfile',
    component: UserProfile,
  },
  {
    path: '/edit',
    name: 'EditProfile',
    component: EditProfile,
  },
  {

    path: '/movies',
    name: 'AllMovies',
    component: AllMovies,
  },
  {
    path: '/addMovies', // Nueva ruta para el login
    name: 'AddMovies',
    component: AddMovies,
  },

];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
