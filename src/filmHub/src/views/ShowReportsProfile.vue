<template>
  <div class="profile-page">
    <HeaderPage />

    <div class="overlay"></div>

    <div class="main-content">
      <div class="profile-box">

        <!-- Mostrar error si no se pudo cargar la información -->
        <p v-if="error" class="error-message">{{ error }}</p>

        <!-- Modal con los reported comments del usuario-->
        <div v-else>
          <div v-if="isAdmin" class="modal-overlay-admin">
            <h2>Reported Comments</h2>
            <!-- Si el usuario es admin podrá ver todos los comments reportados de todos los usuarios-->
            <div class="admin-comments">
              <section class="vertical-bar">
                  <h3>Order by:</h3>
                  <!-- Switches para ordenar por Rating, Year y Popularity -->
                  <div class="sort-option">
                      <div class="sort-row">
                          <span>User</span>
                          <label class="switch">
                              <input type="checkbox" @change="applySwitchSorting('user', $event)" />
                              <span class="slider"></span>
                          </label>
                      </div>
                      <div class="sort-row">
                          <span>Date</span>
                          <label class="switch">
                              <input type="checkbox" @change="applySwitchSorting('date', $event)" />
                              <span class="slider"></span>
                          </label>
                      </div>
                      <div class="sort-row">
                          <span>Status</span>
                          <label class="switch">
                              <input type="checkbox" @change="applySwitchSorting('status', $event)" />
                              <span class="slider"></span>
                          </label>
                      </div>
                  </div>
              </section>

              <div class="scrollable-comments-admin">
                <div v-for="(comment, index) in allReportedComments" :key="index" class="comment-item-admin">
                  <p><strong>{{ comment.username }}:</strong> {{ comment.text }}</p>
                  <!-- Contenedor para la fecha y el badge -->
                  <div class="comment-info-container-admin">
                    <div class="comment-date-admin">
                      <p>{{ comment.date.slice(0, 10) }}</p>
                    </div>
                    <div class="submitted-badge-admin">
                      <p>{{ comment.state }}</p>
                    </div>
                  </div>
                  <hr />
                </div>
              </div>
            </div>
          </div>
          <div v-else-if="reportedComments.length > 0" class="modal-overlay">
            <h2>Reported Comments</h2>
            <div class="comments-list">
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
      isAdmin: null,
      allReportedComments: [],
      activeSorting: '', // Para almacenar el criterio activo de ordenación
      selectedYear: '',  // Para almacenar el año seleccionado si corresponde
      cancelTokenSource: null, // Para manejar la cancelación de solicitudes
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
        this.isAdmin = this.userData.is_admin;

        // Cargar comentarios reportados según el rol del usuario
        if (this.isAdmin) {
          this.fetchAllReportedComments();
        } else {
          this.showReportedComments();
        }
      })
      .catch((error) => {
        console.error('Error al obtener los datos del usuario:', error);
        this.error = 'Error fetching user data. Please try again.';
      });
  },
  methods: {
    async applySwitchSorting(criteria, event) {
      // Desmarcar todos los otros switches
      document.querySelectorAll('.switch input').forEach(input => {
        if (input !== event.target) {
          input.checked = false;
        }
      });

      // Si el switch se marca, aplica la ordenación correspondiente
      if (event.target.checked) {
        this.activeSorting = criteria;
        this.selectedYear = ''; // Resetear año si es necesario
        await this.applySorting(criteria);
      } else {
        // Si el switch se desmarca, restablece la ordenación
        this.activeSorting = '';
        await this.fetchAllReportedComments(); // Vuelve a cargar los comentarios sin ordenar
      }
    },

    // Método para aplicar la ordenación según el criterio
    async applySorting(criteria) {
      try {
        let url;

        // Manejo de cancelación de solicitudes anteriores
        if (this.cancelTokenSource) {
          this.cancelTokenSource.cancel("Operation canceled due to new request.");
        }

        this.cancelTokenSource = axios.CancelToken.source();

        // Establecer la URL según el criterio seleccionado
        if (criteria === 'user') {
          url = `${API_BASE_URL}/comments/reported/order_by_user`; // Ordenar por usuario
        } else if (criteria === 'date') {
          url = `${API_BASE_URL}/comments/reported/order_by_date`; // Ordenar por fecha
        } else if (criteria === 'status') {
          url = `${API_BASE_URL}/comments/reported/order_by_status`; // Ordenar por popularidad
        } else {
          url = `${API_BASE_URL}/comments/reported`; // Recuperar todos los comentarios sin orden
        }

        // Realizar la solicitud a la API con Axios
        const response = await axios.get(url, {
          cancelToken: this.cancelTokenSource.token,
          headers: { accept: 'application/json' },
        });

        // Resolver nombres de usuario para cada comentario
        this.allReportedComments = await Promise.all(
          response.data.map(async (comment) => {
            const username = await this.getUsername(comment.user_id);
            return {
              id: comment.id,
              text: comment.text,
              username, // Nombre de usuario obtenido
              date: comment.created_at,
              state: comment.reported,
            };
          })
        );

        console.log(`Comments sorted by ${criteria}:`, this.allReportedComments);

      } catch (error) {
        // Manejo de errores si la solicitud falla o es cancelada
        if (axios.isCancel(error)) {
          console.log("Previous request canceled:", error.message);
        } else {
          console.error("Error retrieving comments:", error);
          this.error = 'Unable to load reported comments.';
        }
      } finally {
        // Limpiar la fuente de cancelación
        this.cancelTokenSource = null;
      }
    },

    // Método para obtener todos los comentarios reportados sin aplicar un criterio de ordenación
    async fetchAllReportedComments() {
      try {
        const response = await axios.get(`${API_BASE_URL}/comments/reported`, {
          headers: { accept: 'application/json' },
        });

        // Resolver nombres de usuario para cada comentario
        this.allReportedComments = await Promise.all(
          response.data.map(async (comment) => {
            const username = await this.getUsername(comment.user_id);
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
        console.error('Error fetching all reported comments:', error);
        this.error = 'Unable to load reported comments.';
      }
    },


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


/* Modal para admin más ancho */
.modal-overlay-admin {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 90%;
  margin: 0 auto;
  padding: 20px;
  border-radius: 10px;
  background-color: rgba(0, 0, 0, 0.8);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  color: white;
}

/* Título centrado */
.modal-overlay-admin h2 {
  font-size: 1.5rem;
  font-weight: bold;
  text-align: center;
  margin-bottom: 20px;
}

/* Contenedor principal de admin */
.admin-comments {
  display: flex;
  flex-direction: row;
  gap: 5px;
  width: 120%;
}

/* Barra vertical para ordenar */
.vertical-bar {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  width:20%;
  padding: 10px;
  background-color:transparent;
  border-radius: 2px ;
  border: 0.25px solid rgba(255, 255, 255, 0.398);
  gap: 20px;
}

.vertical-bar h3 {
  font-size: 1rem;
  font-weight: bold;
  color: white;
  margin-bottom: 10px;
}

.sort-option {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.sort-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  font-size: 0.9rem;
  color: white;
  gap: 15px;
}

.switch {
  position: relative;
  display: inline-block;
  width: 34px;
  height: 20px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: 0.4s;
  border-radius: 10px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 14px;
  width: 14px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: 0.4s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: #2196F3;
}

input:checked + .slider:before {
  transform: translateX(14px);
}

/* Contenedor para comentarios */
.scrollable-comments-admin {
  flex-grow: 1;
  max-height: 400px;
  overflow-y: auto;
  padding: 10px;
  border-radius: 5px;
  background-color: #f9f9f931;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.5);
  border: 1px solid #ddd;
}

.scrollable-comments-admin::-webkit-scrollbar {
  width: 8px;
}

.scrollable-comments-admin::-webkit-scrollbar-thumb {
  background: #ccc;
  border-radius: 4px;
}

.scrollable-comments-admin::-webkit-scrollbar-thumb:hover {
  background: #aaa;
}

/* Estilo de cada comentario */
.comment-item-admin {
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



.comment-info-container-admin {
  display: flex; /* Para alinear los elementos horizontalmente */
  align-items: center; /* Asegura que estén centrados verticalmente */
  margin-left: auto; /* Empuja este contenedor hacia la derecha */
  gap: 10px; /* Espacio entre la fecha y el badge */
}

.comment-date-admin,
.submitted-badge-admin {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 5px 10px;
  border-radius: 5px;
  font-size: 0.875rem;
  font-weight: bold;
  text-transform: uppercase;
  height: auto;
  min-width: 80px;
}

.comment-date-admin {
  background-color: transparent;
  color: white;
  border: 0.5px solid white;
}

.submitted-badge-admin {
  background-color: #6ba76d;
  color: white;
  border: 0.5px solid white;
}


/* Responsive design for smaller screens */
@media (max-width: 768px) {
  .modal-overlay {
    flex-direction: column;
    align-items: center;
  }

  .vertical-bar {
    width: 100%;
    height: auto;
    margin-bottom: 20px;
  }

  .scrollable-comments-admin {
    width: 100%;
    margin-left: 0;
  }
}






</style>