import { createRouter, createWebHistory } from 'vue-router';
import MainPageView from '../views/MainPageView.vue';
import UserRegister from '../views/UserRegister.vue';
import UserLogin from '../views/UserLogin.vue'; // Importa el componente de login
import AddMovies from '../views/AddMovies.vue'; // Importa el componente de login

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
