<template>
    <div>
      <h1>Filter Characters</h1>
      <FilterComponent
        :skills="skills"
        :properties="properties"
        apiEndpoint="/api/character/search"
        itemType="Character"
      />
    </div>
  </template>
  
  <script>
  import FilterComponent from "@/components/common/FilterComponent.vue";
  import { fetchList } from "@/services/apiService.js";
  
  export default {
    components: { FilterComponent },
    data() {
      return {
        skills: [],
        properties: [],
      };
    },
    async created() {
      try {
        this.skills = await fetchList("/api/skill/list");
        this.properties = await fetchList("/api/property/list");
      } catch (error) {
        console.error("Error fetching skills or properties:", error);
      }
    },
  };
  </script>
  