import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';


import { createApp } from 'vue';
import App from './App.vue';
import router from './router/index'; // Asegúrate de que la ruta es correcta

const app = createApp(App);
app.use(router);
app.mount('#app'); // Monta la aplicación
    