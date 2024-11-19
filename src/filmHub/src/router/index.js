import { createRouter, createWebHistory } from 'vue-router';
import MainPageView from '../views/MainPageView.vue';
import UserRegister from '../views/UserRegister.vue';
import UserLogin from '../views/UserLogin.vue';
import MovieDetails from '../views/MovieDetails.vue';  

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
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
