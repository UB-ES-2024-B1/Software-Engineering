<template>
  <div class="card-container">
    <div class="card-content">
      <div class="card-title">
        Movie <span>Rating</span>
      </div>


      <div class="rangeslider">
        <!-- Control de rango mínimo -->
        <input
          class="min input-ranges"
          name="range_1"
          type="range"
          min="1"
          max="5"
          step="0.05"
          v-model.number="minValue"
        />
        <!-- Control de rango máximo -->
        <input
          class="max input-ranges"
          name="range_2"
          type="range"
          min="1"
          max="5"
          step="0.05"
          v-model.number="maxValue"
        />
      </div>

      <!-- Muestra de valores actuales -->
      <div class="values">
        <div><span id="first">{{ minValue.toFixed(1) }}</span></div> -
        <div><span id="second">{{ maxValue.toFixed(1) }}</span></div>
        <div><i class='bx bx-star'></i></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RatingSlider',
  data() {
    return {
      minValue: 2.5, // Valor inicial para el rango mínimo
      maxValue: 4  // Valor inicial para el rango máximo
    };
  },
  watch: {
    // Observador para asegurar que el minValue no sea mayor que maxValue y viceversa
    minValue(value) {
      if (value > this.maxValue) {
        this.minValue = this.maxValue;
      }
    },
    maxValue(value) {
      if (value < this.minValue) {
        this.maxValue = this.minValue;
      }
    }
  }
};
</script>

<style scoped>
.card-container {
  cursor: default;
  --color-primary: #d8a101;
  --color-headline: #c0b9a9;
  --color-text: #665c45;
}

.card-content {
  width: 100%;
  max-width: 624px;
  padding: 72px 64px;
  background: #333232;
  border-radius: 20px;
  box-shadow: 0 2px 8px rgba(237, 233, 222, .12);
}

.card-content .card-title {
  font-family: inherit;
  font-size: 64px;
  font-weight: 700;
  margin: 0 0 20px 0;
  color: var(--color-headline);
}

.card-content .card-title span {
  font-weight: 500;
}

.card-content .values div, .card-content .current-range div {
  display: inline-block;
  vertical-align: top;
}

.card-content .values {
  margin-top: 20px; /* Add margin-top to move it below the sliders */
  font-weight: 500;
  color: var(--color-primary);
  text-align: center; /* Center align the values */
}

.card-content .values > div:first-child {
  margin-right: 4px;
}

.card-content .values > div:last-child {
  margin-left: 4px;
}

.card-content .slider {
  display: flex;
  justify-content: space-between;
  margin-top: 40px;
  font-size: 1.2em;
  color: var(--color-text);
}

/* Range Slider */
.input-ranges[type='range'] {
  width: 420px;
  height: 60px;
  outline: none;
}

.input-ranges[type='range'],
.input-ranges[type='range']::-webkit-slider-runnable-track,
.input-ranges[type='range']::-webkit-slider-thumb {
  -webkit-appearance: none;
  background: none;
}

.input-ranges[type='range']::-webkit-slider-runnable-track {
  width: 100%;
  height: 2px;
  background: var(--color-headline);
}

.input-ranges[type='range']::-webkit-slider-thumb {
  height: 30px;
  width: 30px;
  margin-top: -14px;
  background: #000;
  border: 2px solid var(--color-headline);
  border-radius: 50px;
  cursor: pointer;
  transition: .5s;
}

.input-ranges[type='range']::-webkit-slider-thumb:hover {
  background: #151515;
  border: 2px solid var(--color-primary);
}

.rangeslider {
  
  height: 40px;
  width: 400px;
  margin-top: -10px;
}

.values{
  display: flex;
  justify-content: center;
  align-items: center;
  margin-right: 55px;
  
}
</style>
