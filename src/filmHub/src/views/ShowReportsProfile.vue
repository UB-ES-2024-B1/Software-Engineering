<template>
  <div class="profile-page">
    <HeaderPage />

    <div class="overlay"></div>

    <div class="main-content">
      <div class="profile-box">

        <!-- Mostrar error si no se pudo cargar la información -->
        <p v-if="error" class="error-message">{{ error }}</p>

        <!-- Modal con los reported comments del usuario-->
        <div v-else class="modal-overlay">
          <h2>Reported Comments</h2>
          <div v-if="reportedComments.length > 0" class="comments-list">
            <!-- Contenedor con scroll solo para los comentarios -->
            <div class="scrollable-comments">
              <div v-for="(comment, index) in reportedComments" :key="index" class="comment-item">
                <p><strong>{{ comment.username }}:</strong> {{ comment.text }}</p>

                <!-- Contenedor para la fecha y el badge -->
                <div class="comment-info-container">
                  <div class="comment-date">
                    <p>{{ comment.date.slice(0, 10) }}</p>
                  </div>
                  <div class="submitted-badge">
                    <p>{{ comment.state }}</p>
                  </div>
                </div>

                <hr />
              </div>
            </div>
          </div>
          <div v-else class="no-comments">
            <p>No comments have been reported by you.</p>
          </div>
          <router-link to="/profile">
            <button class="close-modal-btn">Cancel</button>
          </router-link>

        </div>
      </div>
    </div>
    <FooterComponent />
  </div>
</template>

<script>

import HeaderPage from '@/components/HeaderPage.vue';
import FooterComponent from '@/components/FooterComponent.vue';
import axios from 'axios';
import { API_BASE_URL } from '@/config.js'; // Asegúrate de tener la URL base aquí

export default {
  name: 'ShowReportsProfile',
  components: {
    HeaderPage,
    FooterComponent,
  },
  data() {
    return {
      userData: null,
      error: null,
      reportedComments: [],
    }
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

        // Cargar las películas valoradas y con like desde un solo endpoint
        this.showReportedComments();
      })
      .catch((error) => {
        console.error('Error al obtener los datos del usuario:', error);
        this.error = 'Error fetching user data. Please try again.';
      });
  },
  methods: {
    async showReportedComments() {
      try {
        const userId = this.userData.id; // Asegúrate de tener el ID del usuario cargado
        const response = await axios.get(`${API_BASE_URL}/comments/reported_by_user/${userId}/`, {
          headers: {
            accept: 'application/json',
          },
        });

        // Mapeamos los comentarios y resolvemos los nombres de usuario
        this.reportedComments = await Promise.all(
          response.data.map(async (comment) => {
            const username = await this.getUsername(comment.user_id);
            console.log('Username a:', username);
            return {
              id: comment.id,
              text: comment.text,
              username, // Nombre de usuario obtenido
              date: comment.created_at,
              state: comment.reported,
            };
          })
        );
      } catch (error) {
        console.error('Error fetching reported comments:', error);
        this.error = 'Unable to load reported comments.';
      }
    },

    async getUsername(userId) {
      try {
        const response = await axios.get(`${API_BASE_URL}/users/id/${userId}`, {
          headers: {
            accept: 'application/json',
          },
        });
        return response.data.full_name || 'Unknown User'; // Asegúrate de manejar usuarios sin nombre
      } catch (error) {
        console.error('Error fetching username:', error);
        return 'Unknown User';
      }
    },
  }

}


</script>

<style scoped>
.profile-page {
  display: flex;
  flex-direction: column;
  height: 100vh;
  /* Asegura que el contenedor ocupe toda la altura de la ventana */
  margin: 0;
  padding: 0;
  background-image: url('@/assets/fondo_login.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  z-index: -1;
}

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
  flex-grow: 1;
  /* Hace que este contenedor crezca para ocupar el espacio disponible */
  padding: 20px;
  z-index: 10;
}

.footer-component {
  margin-top: auto;
  /* Asegura que el footer se quede pegado al fondo */
}

/* Caja del perfil */
.profile-box {
  position: relative;
  display: flex;
  flex-direction: column;
  background-color: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(5px);
  padding: 40px;
  border-radius: 10px;
  width: 750px;
  height: 580px;
  color: white;
  z-index: 20;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  /* Mejora visual */
  border: 2px solid rgba(255, 255, 255, 0.1);
  /* Sutileza */
}

.modal-overlay {
  width: 100%;
  align-items: center;
  justify-content: space-between;
}

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
  box-sizing: border-box;
  padding: 10px;
  border-bottom: 1px solid #eee;
  background-color: #2a2a2a;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.5);
  font-size: 1rem;
  display: flex;
  justify-content: space-between; /* Distribuye espacio entre el contenido principal y el contenedor derecho */
  align-items: center; /* Centrado vertical */
}

.comment-info-container {
  display: flex; /* Para alinear los elementos horizontalmente */
  align-items: center; /* Asegura que estén centrados verticalmente */
  margin-left: auto; /* Empuja este contenedor hacia la derecha */
  gap: 10px; /* Espacio entre la fecha y el badge */
}


.comment-date,
.submitted-badge {
  display: inline-flex; /* Ambos elementos se comportan igual */
  align-items: center; /* Centrado vertical */
  justify-content: center; /* Centrado horizontal */
  padding: 5px 10px; /* Espaciado interno */
  border-radius: 5px; /* Bordes redondeados */
  font-size: 0.875rem; /* Tamaño de fuente igual */
  font-weight: bold; /* Negrita */
  text-transform: uppercase; /* Texto en mayúsculas */
  height: auto; /* Ajusta la altura automáticamente */
  min-width: 80px; /* Tamaño mínimo igual */
}

.comment-date {
  background-color: transparent; /* Fondo transparente */
  color: white; /* Texto blanco */
  border: 0.5px solid white; /* Bordes blancos */
}

.submitted-badge {
  background-color: #6ba76d; /* Fondo verde */
  color: white; /* Texto blanco */
  border: 0.5px solid white; /* Bordes blancos */
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
  align-items: center;
}

.close-modal-btn:hover {
  background-color: #d32f2f;
  /* Cambiar color al pasar el mouse */
}

h2 {
  font-size: 1.5em;
  font-weight: bold;
  text-align: center;
  margin-bottom: 15px;
  /* Separación con los comentarios */
}
</style>