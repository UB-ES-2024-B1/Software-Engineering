<template>
    <div class="radio-input" :style="{ fontFamily: fontFamily, fontSize: fontSize }">
        <h3 v-if="title" class="radio-title">{{ title }}</h3>
        <label v-for="option in options" :key="option.value" class="label">
            <input type="radio" :id="option.value" :name="name" :value="option.value"
                :checked="selectedValue === option.value" @change="updateSelection" />
            <p class="text">{{ option.label }}</p>
        </label>
    </div>
</template>



<script>
    export default {
    name: 'RadioForm',
    props: {
      modelValue: String,
      options: {
        type: Array,
        required: true,
        default: () => [],
      },
      fontFamily: {
        type: String,
        default: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
      },
      name: {
        type: String,
        default: 'radio-group',
      },
      title: {
        type: String,
        default: '', // Default to no title
      },
    },
    computed: {
      selectedValue: {
        get() {
          return this.modelValue;
        },
        set(value) {
          this.$emit('update:modelValue', value);
        },
      },
    },
    methods: {
      updateSelection(event) {
        this.selectedValue = event.target.value;
      },
    },
  };
</script>  


<style scoped>
.radio-input {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

/* From Uiverse.io by Na3ar-17 */
.radio-input * {
    box-sizing: border-box;
    padding: 0;
    margin: 0;
}

.radio-input .label {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 0px 20px;
    width: 300px;
    cursor: pointer;
    height: 50px;
    position: relative;
    border-radius: 10px;
    transition: background-color 0.1s, border-color 0.1s;
}

.radio-input label::before {
    position: absolute;
    content: "";
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 220px;
    height: 45px;
    z-index: -1;
    transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    border-radius: 10px;
    border: 2px solid transparent;
}




.radio-input .label .text {
    color: #fff;
}

.radio-input .label input[type="radio"] {
    background-color: #202030;
    appearance: none;
    width: 17px;
    height: 17px;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
}

.radio-input .label input[type="radio"]:checked {
    background-color: #435dd8;
    -webkit-animation: puls 0.2s forwards;
    animation: pulse-radio 0.2s forwards;
}

.radio-input .label:has(input:checked) {
    background-color: rgba(67, 93, 216, 0.3);
    /* Fondo cuando el elemento está seleccionado */
    border: 2px solid rgb(67, 93, 216);
    /* Borde cuando el elemento está seleccionado */
    color: #fff;
}

.radio-input .label:hover {
    background-color: #00000081;
    border: 2px solid rgb(67, 93, 216);
    /* Fondo al pasar el cursor */
}

.radio-input .label .text {
    color: #bbbbbb;
}

.radio-input input[type="radio"] {
    background-color: #202030;
    appearance: none;
    width: 17px;
    height: 17px;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-right: 10px;
}

.radio-input input[type="radio"]:checked {
    background-color: #fff;
}

.radio-input .label input[type="radio"]:before {
    content: "";
    width: 6px;
    height: 6px;
    border-radius: 50%;
    transition: all 0.1s cubic-bezier(0.165, 0.84, 0.44, 1);
    background-color: #fff;
    transform: scale(0);
}

@keyframes pulse-radio {
    0% {
        box-shadow: 0 0 0 0 rgba(255, 255, 255, 0.4);
    }

    70% {
        box-shadow: 0 0 0 8px rgba(255, 255, 255, 0);
    }

    100% {
        box-shadow: 0 0 0 0 rgba(255, 255, 255, 0);
    }
}

.radio-title {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 15px;
  color: #afadad;
}

</style>