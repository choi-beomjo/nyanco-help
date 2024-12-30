<template>
    <h1>Add Property</h1>
    <form @submit.prevent="onSubmit">
      <!-- Attack Input -->
      <div>
        <label for="name">Name: </label>
        <input type="string" id="name" v-model="property.name" />
      </div>
  
      <button type="submit">Create Property</button>
      <BackButton />
    </form>
  </template>
  
  <script>
  import axios from "@/services/axios";
  //import { fetchList } from "@/services/apiService.js";
  import BackButton from "@/components/common/BackButton.vue";
  
  export default {
    components:{
        BackButton,
    },
    data() {
        return {
            property:{
                name: "",
            },
      };
    },
    async created() {

    },
    methods: {
      async onSubmit() {
        try {
          await axios.post("/api/property", this.property);
          alert("property added successfully!");
          this.$router.push("/property-list");
        } catch (error) {
          console.error("Error adding property:", error);
          alert("Failed to add property.");
        }
      },
    },
  };
  </script>
  