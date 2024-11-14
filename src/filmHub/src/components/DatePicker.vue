<template>
  <div class="date-picker">
    <label :for="id" class="form-label">{{ label }}</label>
    <input :id="id" type="text" ref="datepicker" :placeholder="placeholder" :class="['form-control', inputClass]" />
  </div>
</template>

<script>
import flatpickr from 'flatpickr';
import 'flatpickr/dist/flatpickr.min.css';

export default {
  name: 'DatePicker',
  props: {
    modelValue: {
      type: String,
      default: '',
    },
    label: {
      type: String,
      default: '',
    },
    id: {
      type: String,
      default: 'datepicker',
    },
    placeholder: {
      type: String,
      default: 'Select Date',
    },
    inputClass: {
      type: String,
      default: '',
    },
  },
  mounted() {
    flatpickr(this.$refs.datepicker, {
      dateFormat: 'd-m-Y',
      defaultDate: this.modelValue,
      onChange: (dateStr) => {
        this.$emit('update:modelValue', dateStr);
      },
    });
  },
};
</script>

<style scoped>
.form-control {
  background-color: #333;
  color: #636060;
  width: 100%;
  outline: 0;
  border: 1px solid rgba(105, 105, 105, 0.397);
  border-radius: 10px;
  padding: 10px 15px;
}

.form-control::placeholder {
  color: #707070;
}
</style>