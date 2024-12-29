<template>
    <button @click="goBack">Back</button>
  </template>
  
  <script>
  export default {
    methods: {
      goBack() {
        this.$router.push(this.target);
      },
    },
    props: {
      target: {
        type: String,
        default: "/",
      },
    },
  };
  </script>
  