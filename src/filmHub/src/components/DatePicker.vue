<template>
    <div class="date-picker">
      <label :for="id" class="form-label">{{ label }}</label>
      <input
        :id="id"
        type="text"
        ref="datepicker"
        :placeholder="placeholder"
        :class="['form-control', inputClass]"
      />
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
        onChange: (selectedDates, dateStr) => {
          this.$emit('update:modelValue', dateStr);
        },
      });
    },
  };
  </script>
  
  <style scoped>
  
  /* Custom hover color for the month input field */
  .flatpickr-input:hover {
    border-color: #28a745 !important; /* Border color on hover */
  }
  </style>
  