// frontend/config.js
//export const API_BASE_URL = 'https://filmhub-backend.azurewebsites.net';
//export const API_BASE_URL = 'http://localhost:8000';  // for tests with selenium

let API_BASE_URL;

if (process.env.USE_SELE_CONFIG) {
    API_BASE_URL = 'https://filmhub-backend.azurewebsites.net';
} else {
    API_BASE_URL = 'http://localhost:8000';
}

export { API_BASE_URL };
