import { createRouter, createWebHistory } from 'vue-router';
import MainPageView from '../views/MainPageView.vue';
import UserRegister from '../views/UserRegister.vue';
import UserLogin from '../views/UserLogin.vue';  
import UserProfile from '../views/UserProfile.vue';  
import EditProfile from '../views/EditProfile.vue'; 



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
    path: '/profile', 
    name: 'UserProfile',
    component: UserProfile,
  },
  {
    path: '/edit', 
    name: 'EditProfile',
    component: EditProfile,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
