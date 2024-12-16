import { createRouter, createWebHistory } from 'vue-router';
import MainPageView from '../views/MainPageView.vue';
import UserRegister from '../views/UserRegister.vue';
import UserLogin from '../views/UserLogin.vue';
import MovieDetails from '../views/MovieDetails.vue';

import UserProfile from '../views/UserProfile.vue';
import EditProfile from '../views/EditProfile.vue';

import AllMovies from '../views/AllMovies.vue';
import AddMovies from '../views/AddMovies.vue'; // Importa el componente 

import ShowReportsProfile from '@/views/ShowReportsProfile.vue';
import SearchUsers from '@/views/SearchUsers.vue';
import OtherProfiles from '@/views/OtherProfiles.vue';

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
    path: '/searchUsers',
    name: 'SearchUsers',
    component: SearchUsers,
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
  {

    path: '/reportedComments',
    name: 'ShowReportsProfile',
    component: ShowReportsProfile,
  },
  
  {
    path: '/otherProfiles/:username', // Ruta dinámica
    name: 'OtherProfiles',
    component: OtherProfiles,
    props: true, // Pasa el parámetro como "prop" al componente
  },

];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (to.hash) {
      return {
        el: to.hash, // Selecciona el elemento con el id del hash
        behavior: 'smooth', // Habilita el desplazamiento suave
      };
    } else if (savedPosition) {
      return savedPosition; // Vuelve a la posición previa al navegar hacia atrás
    } else {
      return { top: 0 }; // Vuelve al inicio si no hay hash
    }
  }
});


export default router;
