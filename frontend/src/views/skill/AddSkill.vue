<template>
    <h1>Add Property</h1>
    <form @submit.prevent="onSubmit">
      <!-- Attack Input -->
      <div>
        <label for="name">Name: </label>
        <input type="string" id="name" v-model="skill.name" />
      </div>
  
      <button type="submit">Create Skill</button>
      <BackButton />
    </form>
  </template>
  
  <script>
  import axios from "@/services/axios";
  import BackButton from "@/components/common/BackButton.vue";
  export default {
    components:{
        BackButton,
    },
    data() {
        return {
            skill:{
                name: "",
            },
      };
    },
    async created() {

    },
    methods: {
      async onSubmit() {
        try {
          await axios.post("/api/skill", this.skill);
          alert("Skill added successfully!");
          this.$router.push("/skill-list");
        } catch (error) {
          console.error("Error adding skill:", error);
          alert("Failed to add skill.");
        }
      },
    },
  };
  </script>