<template>
    <div>
      <h1>Filter Characters</h1>
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
      <button @click="filterCharacters">Filter</button>
  
      <!-- Filtered Characters List -->
      <div v-if="characters.length > 0">
        <h2>Filtered Characters</h2>
        <ul>
          <li v-for="character in characters" :key="character.id">
            {{ character.name }} - ATK: {{ character.atk }}, HP: {{ character.hp }}
          </li>
        </ul>
      </div>
      <div v-else>
        <p>No characters match the selected filters.</p>
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
        characters: [],
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
      async filterCharacters() {
        try {
          const response = await axios.post("/api/character/search", {
            skills: this.selectedSkills,
            properties: this.selectedProperties,
          });
          this.characters = response.data;
        } catch (error) {
          console.error("Error filtering characters:", error);
          alert("Failed to fetch filtered characters.");
        }
      },
    },
  };
  </script>
  