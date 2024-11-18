import { createRouter, createWebHistory } from 'vue-router';
import MainPageView from '../views/MainPageView.vue';
import UserRegister from '../views/UserRegister.vue';
import UserLogin from '../views/UserLogin.vue'; // Importa el componente de login
import AllMovies from '@/views/AllMovies.vue';

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
    path: '/login', // Nueva ruta para el login
    name: 'UserLogin',
    component: UserLogin,
  },
  {
    path: '/movies', 
    name: 'AllMovies',
    component: AllMovies,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
