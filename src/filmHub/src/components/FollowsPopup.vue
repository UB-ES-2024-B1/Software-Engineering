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

.popup-header {
    color: white;
}
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
    background: rgb(27, 26, 26);
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

</style>