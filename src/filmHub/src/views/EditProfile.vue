<template>
  <div class="profile-page">
    <HeaderPage />

    <div class="overlay"></div>

    <div class="main-content">
      <div class="profile-box">
        <h2 class="profile-title">Edit Profile</h2>

        <!-- Mostrar error si no se pudo cargar la información -->
        <p v-if="error" class="error-message">{{ error }}</p>

        <!-- Formulario de edición -->
        <form v-else class="profile-edit-form" @submit.prevent="submitChanges">
          <div class="form-group">
            <label for="email">Email Address:</label>
            <input
              id="email"
              type="email"
              v-model="formData.email"
              required
              placeholder="Enter your email"
            />
          </div>

          <div class="form-group">
            <label for="full_name">Name:</label>
            <input
              id="full_name"
              type="text"
              v-model="formData.full_name"
              required
              placeholder="Enter your name"
            />
          </div>

          <div class="form-group">
            <label for="password">Password:</label>
            <input
              id="password"
              type="password"
              v-model="formData.password"
              required
              placeholder="Enter your password"
            />
          </div>

          <div class="form-actions">
            <button type="submit" class="save-btn">Save Changes</button>
            <router-link to="/profile" class="cancel-btn">Cancel</router-link>
          </div>
        </form>
      </div>
    </div>

    <footer class="footer">
      <p>&copy; 2024 Web Name. All rights reserved.</p>
    </footer>
  </div>
</template>

<script>
import HeaderPage from '@/components/HeaderPage.vue';
import axios from 'axios';
import { API_BASE_URL } from '@/config.js';

export default {
  name: 'EditProfile',
  components: {
    HeaderPage,
  },
  data() {
    return {
      formData: {
        email: '',
        full_name: '',
        password: '',
      },
      error: null,
    };
  },
  created() {
    const userEmail = localStorage.getItem('userEmail');
    if (!userEmail) {
      this.$router.push('/login');
      return;
    }

    // Carga inicial de los datos del usuario
    axios
      .get(`${API_BASE_URL}/users/email/${userEmail}`)
      .then((response) => {
        const { email, full_name } = response.data;
        this.formData.email = email;
        this.formData.full_name = full_name;
      })
      .catch((error) => {
        console.error('Error al obtener los datos del usuario:', error);
        this.error = 'Error fetching user data. Please try again.';
      });
  },
  methods: {
    submitChanges() {
      // Actualizar datos del usuario en el backend
      axios
        .put(`${API_BASE_URL}/users/email/${this.formData.email}`, this.formData)
        .then(() => {
          this.$router.push('/profile');
        })
        .catch((error) => {
          console.error('Error al actualizar los datos del usuario:', error);
          this.error = 'Error updating user data. Please try again.';
        });
    },
  },
};
</script>

<style scoped>
/* Estilos generales iguales a los de profile */
.profile-page {
  height: 100vh;
  margin: 0;
  padding: 0;
  background: linear-gradient(135deg, #1e3c72, #2a5298);
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

.main-content {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 80vh;
  padding: 20px;
  z-index: 10;
}

.profile-box {
  display: flex;
  flex-direction: column;
  background-color: rgba(0, 0, 0, 0.6);
  padding: 40px;
  border-radius: 10px;
  width: 750px;
  height: 450px;
  color: white;
  z-index: 20;
}

.profile-title {
  margin-bottom: 30px;
  font-size: 28px;
  font-weight: bold;
  text-align: center;
}

/* Estilo de formulario */
.profile-edit-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group label {
  font-weight: bold;
  color: white;
  margin-bottom: 5px;
}

.form-group input {
  width: 100%;
  padding: 8px;
  border-radius: 5px;
  border: 1px solid #444;
  background-color: #3e3e3e;
  color: white;
  font-size: 16px;
}

.form-group input:focus {
  border-color: #1fb115;
}

/* Botones de acción */
.form-actions {
  display: flex;
  justify-content: space-between;
  gap: 10px;
}

.save-btn {
  background-color: #ffcc00;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  flex: 1;
}

.save-btn:hover {
  background-color: #e6b800;
}

.cancel-btn {
  text-align: center;
  background-color: #ccc;
  color: black;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  text-decoration: none;
  flex: 1;
}

.cancel-btn:hover {
  background-color: #b3b3b3;
}

/* Footer básico */
.footer {
  background-color: #121212;
  color: #fff;  
  padding: 10px;
  text-align: center;
  position: absolute;
  bottom: 0;
  width: 100%;
  z-index: 5;
}

</style>
