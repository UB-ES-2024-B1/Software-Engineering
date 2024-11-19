// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyBT-6u8mmpu2G6x9yIRnbqWfcpM0f80zrc",
  authDomain: "filmhub-136b9.firebaseapp.com",
  projectId: "filmhub-136b9",
  storageBucket: "filmhub-136b9.firebasestorage.app",
  messagingSenderId: "513396322903",
  appId: "1:513396322903:web:6aa150b96d1e7e6efd6912",
  measurementId: "G-JT3905BT10"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

export { app, analytics };