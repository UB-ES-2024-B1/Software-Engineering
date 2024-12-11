<template>
    <div v-if="isVisible" class="popup-overlay" @click.self="closePopup">
      <div class="popup-content">
        <button class="close-btn" @click="closePopup">&times;</button>
        <div class="popup-header">
          <h3>{{ title }}</h3>
        </div>
        <div class="popup-body">
          <slot></slot>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'PopupComponent',
    props: {
      title: {
        type: String,
        default: 'Popup Title'
      },
      isVisible: {
        type: Boolean,
        required: true
      }
    },
    methods: {
      closePopup() {
        this.$emit('close');
      }
    }
  };
  </script>
  
  <style scoped>
  .popup-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }
  
  .popup-content {
    background: white;
    padding: 20px;
    border-radius: 8px;
    width: 90%;
    max-width: 500px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    position: relative;
  }
  
  .popup-header {
    margin-bottom: 20px;
    text-align: center;
  }
  
  .popup-body {
    max-height: 300px;
    overflow-y: auto;
  }
  
  .close-btn {
    position: absolute;
    top: 10px;
    right: 10px;
    background: transparent;
    border: none;
    font-size: 24px;
    cursor: pointer;
  }

  .user-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
}

.user-image {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
}

.user-info {
  display: flex;
  flex: 1;
  align-items: center;
  justify-content: space-between;
}

.user-name {
  font-size: 16px;
  font-weight: bold;
  margin-right: auto;
}

.follow-btn {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 5px;
  cursor: pointer;
}

.follow-btn:hover {
  background-color: #0056b3;
}
  </style>