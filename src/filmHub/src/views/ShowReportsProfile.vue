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

                  <!-- Para linkear con la pelicula en la que se encuentra el comentario -->
                  <router-link :to="`/movie/${comment.movie_id}#comments-section`" class="comment-link">
                    <p><strong>{{ comment.username }}:</strong> {{ comment.text }}</p>
                  </router-link>

                  <!-- Contenedor para la fecha y el badge -->
                  <div class="comment-info-container-admin">
                    <div class="comment-date-admin">
                      <p>{{ comment.date.slice(0, 10) }}</p>
                    </div>



                    <section class="horizontal-bar">
                      <!-- Botón desplegable para "REPORT" -->
                      <div class="dropdown">
                        <button class="dropdown-button" @click="toggleDropdown(index)">{{ comment.state}}</button>
                        <ul v-if="dropdowns[index]" class="dropdown-menu">
                          <li v-for="possibleState in possibleCommentsSates" :key="possibleState"  @click="selectState(possibleState)"
                              class="dropdown-item">
                                {{possibleState }}
                          </li>
                        </ul>
                      </div>
                    </section>
                  </div>

                  <!-- Modal de Confirmación -->
                  <div v-if="showConfirmation && selectedIndex === index" class="confirmation-modal">
                    <p>Are you sure you want to mark this comment as {{ selectedOption }}?</p>
                    <button @click="applyStateChange(index)" class="confirm-btn">Yes</button>
                    <button @click="cancelStateChange" class="cancel-btn">No</button>
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
                    <div>
                      <div v-if="comment.state === 'REPORTED'" class="submitted-badge">
                        <p>SUBMITTED</p>
                      </div>
                      <div v-else class="banned-badge-admin">
                        <p>{{ comment.state }}</p>
                      </div>
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

      showConfirmation: false, // Modal de confirmación visible
      selectedOption: '', // Opción seleccionada (CLEAN o BANNED)
      selectedIndex: null, // Índice del comentario que se está actualizando

      dropdowns: {} ,
      selectedState: '',
      possibleCommentsSates: ['CLEAN','REPORTED', 'BANNED' ],
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
          url = `${API_BASE_URL}/comments/reported/order_by_user/`; // Ordenar por usuario
        } else if (criteria === 'date') {
          url = `${API_BASE_URL}/comments/reported/order_by_date/`; // Ordenar por fecha
        } else if (criteria === 'status') {
          url = `${API_BASE_URL}/comments/reported/order_by_status/`; // Ordenar por popularidad
        } else {
          url = `${API_BASE_URL}/comments/reported/`; // Recuperar todos los comentarios sin orden
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
              movie_id: comment.thread_id,
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


    initializeDropdowns() {
      // Llenar dropdowns con 'false' para cada comentario
      this.allReportedComments.forEach((_, index) => {
        this.dropdowns[index] = false;
      });
    },
    toggleDropdown(index) {
      this.dropdowns[index] = !this.dropdowns[index];
    },
    selectState(state, index) {
      console.log(`Selected state: ${state}`);
      this.selectedState = state;
      this.dropdowns[index] = false;
      //metode per aplicar el canvi d'estat (canviar i fer servir endpoint per fer el put)
      this.allReportedComments[index].state = state;

    },
    handleClickOutside(event) {
      const dropdownsElements = document.querySelectorAll('.dropdown');
      let clickInsideDropdown = false;

      dropdownsElements.forEach((dropdown) => {
        if (dropdown.contains(event.target)) {
          clickInsideDropdown = true;
        }
      });

      // Si el clic es fuera de todos los dropdowns, ciérralos todos
      if (!clickInsideDropdown) {
        this.dropdowns = {};
      }
    },
  },

  async mounted() {
    document.addEventListener('click', this.handleClickOutside);
    this.initializeDropdowns();
  },
  beforeUnmount() {
    document.removeEventListener('click', this.handleClickOutside);
  },

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
  flex-direction: column;
  background-color: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(5px);
  padding: 20px;  /* Reducido el padding para que se adapte mejor en pantallas pequeñas */
  border-radius: 10px;
  width: 100%; /* Usamos el 100% del ancho disponible */
  max-width: 1000px; /* Limita el ancho máximo */
  min-width: 300px; /* Permite que el contenedor se haga pequeño en pantallas muy pequeñas */
  height: auto; /* La altura se ajustará según el contenido */
  min-height: 300px; /* Se asegura que el contenedor no se haga demasiado pequeño */
  color: white;
  z-index: 20;
  box-shadow: 0 10px 30px rgba(179, 219, 240, 0.5);

  border: 2px solid rgba(255, 255, 255, 0.1);
  box-sizing: border-box; /* Asegura que el padding no afecte el tamaño del contenedor */
  overflow: hidden; /* Evita que los elementos se salgan del contenedor */

  display: flex;
  justify-content: center; /* Centra horizontalmente */
  align-items: center; /* Centra verticalmente (si es necesario) */
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
  backdrop-filter: blur(5px);
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
.submitted-badge, .banned-badge {
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
  background-color: #bc3909;
  color: white;
  border: 0.5px solid white;
}

.banned-badge{
  background-color: #248c28b7;
  color: white;
  border: 0.5px solid white;
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


.modal-overlay-admin {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: auto; /* Ajusta el ancho al contenido, pero no será más grande de max-width */
  max-width: 1000px; /* Limita el ancho máximo para pantallas grandes */
  min-width: 600px; /* Establece un ancho mínimo para que no se haga muy pequeño */
  margin: 0 auto;
  padding: 30px; /* Aumenta el padding para que no esté tan pegado */
  border-radius: 10px;
  background-color: transparent; /* Más saturación para mayor visibilidad */
  color: white;
  box-sizing: border-box; /* Asegura que el padding y borde no afecten el tamaño */
  overflow: hidden; /* Evita que los elementos sobresalgan */
  border: 0px; /* Añade borde para más visibilidad */
}

/* Media Queries para pantallas más pequeñas */
@media (max-width: 768px) {
  .modal-overlay-admin {
    width: 90%; /* Ajusta al 90% del ancho de la pantalla */
    min-width: 500px; /* Ajusta el tamaño mínimo en pantallas más pequeñas */
    padding: 20px; /* Reduce el padding para pantallas medianas */
  }
}

@media (max-width: 480px) {
  .modal-overlay-admin {
    width: 95%; /* Ajusta al 95% en pantallas más pequeñas */
    min-width: 400px; /* Ancho mínimo en pantallas de muy baja resolución */
    padding: 15px; /* Ajusta aún más el padding */
  }
}

/* Título centrado */
.modal-overlay-admin h2 {
  font-size: 1.5rem;
  font-weight: bold;
  text-align: center;
  margin-bottom: 20px;
  /* Ajusta el tamaño del título para pantallas más pequeñas */
}

/* Ajuste del título en pantallas más pequeñas */
@media (max-width: 768px) {
  .modal-overlay-admin h2 {
    font-size: 1.3rem;
  }
}

@media (max-width: 480px) {
  .modal-overlay-admin h2 {
    font-size: 1.1rem;
  }
}
/* Contenedor principal de admin */
.admin-comments {
  display: flex;
  flex-direction: row;
  gap: 5px;
  width: auto; /* Ajusta el ancho al contenido */
  min-width: 500px; /* Asegura que el contenedor tenga un ancho mínimo */
  padding: 10px;
  border-radius: 0px;
  box-sizing: border-box; /* Asegura que padding no afecte el tamaño */
  flex-wrap: wrap; /* Permite que los contenedores se acomoden en pantalla más pequeña */
  border: 0px;

  background-color: transparent; /* Más saturación para mayor visibilidad */
}

/* Contenedor azul más oscuro */
.vertical-bar {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
  width: 120px; /* Ancho fijo, puedes ajustarlo según el espacio */
  padding: 10px;
  background-color: transparent; /* Más saturación para mayor visibilidad */
  border-radius: 0px;
  border: 0px;
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

  background-color:transparent;
}

.sort-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  font-size: 0.9rem;
  color: white;
  gap: 15px;

  background-color: transparent;
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
  background-color: #b8ecf3c1;
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
  flex-grow: 1; /* Toma el espacio restante */
  max-height: 400px;
  overflow-y: auto;
  padding: 10px;
  border-radius: 5px;
  background-color: tr;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.5);
  border: 0.20px solid #dddddd75;
  margin-left: 10px; /* Espaciado entre contenedor azul y rosa claro */
}

/* Estilo del scrollbar */
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

/* Media Queries para pantallas más pequeñas */
@media (max-width: 768px) {
  .admin-comments {
    flex-direction: column; /* Ajuste para pantallas más pequeñas */
    align-items: center;
  }

  .vertical-bar,
  .scrollable-comments-admin {
    width: 100%; /* Se ajustan al ancho completo */
    margin: 10px 0; /* Espaciado entre los contenedores */
  }

  .vertical-bar {
    min-width: 100%; /* Asegura que el contenedor azul ocupe todo el ancho */
    max-width: 100%;
  }
}

/* Estilo de cada comentario */
.comment-item-admin {
  width: auto; /* El contenedor negro ocupa todo el ancho disponible */
  box-sizing: border-box;
  padding: 10px;
  border-bottom: 1px solid #eee;
  background-color: #2a2a2a;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.5);
  font-size: 1rem;
  display: flex; /* Usamos flex para alinear los elementos internos horizontalmente */
  justify-content: flex-end; /* Alineamos los elementos a la izquierda */
  align-items: center; /* Centrado vertical */
  gap: 0; /* Aseguramos que no haya espacio entre los elementos */
}

.comment-link, .comment-info-container-admin {
  margin: 0; /* Elimina cualquier margen entre los elementos internos */
  padding: 0; /* Elimina padding adicional, si lo hay */
}


.comment-info-container-admin {
  display: flex;
  align-items: center;
  margin-left: 0; /* Elimina el margen izquierdo */
  background-color: transparent;
  padding: 5px 10px; /* Añadimos algo de padding al contenedor azul */
  border-radius: 4px; /* Bordes redondeados */
}

.comment-info-container-admin .date,
.comment-info-container-admin .status {
  white-space: nowrap; /* Evita que el texto se divida en varias líneas */
}

.comment-date-admin,
.submitted-badge-admin, .banned-badge-admin, .comment-state {
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
  background-color: #bc3909;
  color: white;
  border: 0.5px solid white;
}

.banned-badge-admin{
  background-color: #248c28b7;
  color: white;
  border: 0.5px solid white;
}

html {
  scroll-behavior: smooth;
}

.comment-link {
  font-family: 'Arial', sans-serif;
  color: #ffffffd7;
  text-decoration: none;
  font-size: 1.1rem;
  padding: 5px 10px;
  border-radius: 4px;
  transition: all 0.3s ease;
  display: block; /* Cambiado a block para evitar espacios */
  background-color: transparent;
  
  /* Ancho fijo para el contenedor de comentario */
  width: 450px; /* Cambia este valor si necesitas un ancho diferente */
  height: auto; /* Altura ajustada al contenido */
  max-height: 300px; /* Límite máximo de altura */
  overflow-y: auto; /* Permite desplazamiento si el contenido excede el max-height */
  box-sizing: border-box; /* Incluye el padding dentro del tamaño total */
}

.comment-link:hover {
  color: #fff; /* Cambia el color del texto a blanco al pasar el mouse */
  background-color: #2a4152; /* Fondo azul claro al pasar el mouse */
  text-decoration: none; /* Asegura que no haya subrayado */
}

.comment-link:active {
  background-color: #2980b9; /* Fondo más oscuro al hacer clic */
}

.comment-link:focus {
  outline: 2px solid #2980b9; /* Borde azul alrededor al hacer foco */
  outline-offset: 2px; /* Asegura que el borde no quede pegado al texto */
}

/* Contenedor principal del dropdown */
.dropdown-container {
  position: relative;
  display: inline-block;
}

/* Botón principal del dropdown */
.dropdown-button {
  background-color: #2a4152;
  color: white;
  padding: 8px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  text-transform: uppercase;
  text-align: center;
}
.dropdown-button:hover {
  background-color: #45a049;
}

/* Contenido del dropdown (inicialmente oculto) */
.dropdown-content {
  display: none;
  position: absolute;
  background-color: #f1f1f1;
  min-width: 160px;
  z-index: 1;
  border-radius: 5px;
  box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.2);
}

/* Estilo para los enlaces dentro del dropdown */
.dropdown-content a {
  color: black;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
  border-radius: 5px;
}

/* Estilo cuando se pasa el ratón sobre un enlace */
.dropdown-content a:hover {
  background-color: #ddd;
}

/* Mostrar el contenido del dropdown cuando el ratón está sobre el botón */
.dropdown:hover .dropdown-content {
  display: block;
}

/* Modal de confirmación */
.confirmation-modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: white;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
  text-align: center;
  z-index: 2000;
}

.confirm-btn {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 8px 15px;
  margin: 5px;
  cursor: pointer;
  border-radius: 3px;
}

.cancel-btn {
  background-color: #f44336;
  color: white;
  border: none;
  padding: 8px 15px;
  margin: 5px;
  cursor: pointer;
  border-radius: 3px;
}

.dropdown-menu {
    max-height: 10rem;
    overflow-y: auto;
    position: absolute;
    top: 100%;
    /* Muestra el menú debajo del botón */
    left: 0;
    background-color: #fff;
    color: #333;
    border: 1px solid #ddd;
    border-radius: 4px;
    box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.2);
    margin-top: 5px;
    z-index: 1000;
    list-style: none;
    padding: 10px 0;
    display: flex;
    flex-direction: column;
}


.dropdown-item {
    padding: 8px 12px;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.3s ease;
}

.dropdown-item:hover {
    background-color: #f0f0f0;
}


</style>