<template>
    <div>
      <h1>Filter Enemies</h1>
      <!-- Skills Selection -->
      <div>
        <h2>Skills</h2>
        <div v-for="skill in skills" :key="skill.id">
          <label :for="'skill-' + skill.id">
            <input
              type="checkbox"
              :id="'skill-' + skill.id"
              :value="skill.id"
              v-model="selectedSkills"
            />
            {{ skill.name }}
          </label>
        </div>
      </div>
  
      <!-- Properties Selection -->
      <div>
        <h2>Properties</h2>
        <div v-for="property in properties" :key="property.id">
          <label :for="'property-' + property.id">
            <input
              type="checkbox"
              :id="'property-' + property.id"
              :value="property.id"
              v-model="selectedProperties"
            />
            {{ property.name }}
          </label>
        </div>
      </div>
  
      <!-- Filter Button -->
      <button @click="filterEnemies">Filter</button>
  
      <!-- Filtered Enemies List -->
      <div v-if="enemies.length > 0">
        <h2>Filtered Enemies</h2>
        <ul>
          <li v-for="enemy in enemies" :key="enemy.id">
            {{ enemy.name }} - ATK: {{ enemy.atk }}, HP: {{ enemy.hp }}
          </li>
        </ul>
      </div>
      <div v-else>
        <p>No enemies match the selected filters.</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "@/services/axios";
  import { fetchList } from "@/services/apiService.js";
  
  export default {
    data() {
      return {
        skills: [],
        properties: [],
        selectedSkills: [],
        selectedProperties: [],
        enemies: [],
      };
    },
    async created() {
      try {
        // Fetch skills and properties
        this.skills = await fetchList("/api/skill/list");
        this.properties = await fetchList("/api/property/list");
      } catch (error) {
        console.error("Error fetching skills or properties:", error);
      }
    },
    methods: {
      async filterEnemies() {
        try {
          const response = await axios.post("/api/enemy/search", {
            skills: this.selectedSkills,
            properties: this.selectedProperties,
          });
          this.enemies = response.data;
        } catch (error) {
          console.error("Error filtering enemies:", error);
          alert("Failed to fetch filtered enemies.");
        }
      },
    },
  };
  </script>
  