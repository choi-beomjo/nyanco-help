<template>
  <h1>Add Enemy</h1>
  <form @submit.prevent="onSubmit">
    <!-- Attack Input -->
    <div>
      <label for="atk">Attack:</label>
      <input type="number" id="atk" v-model="enemy.atk" />
    </div>

    <!-- Health Input -->
    <div>
      <label for="hp">Health:</label>
      <input type="number" id="hp" v-model="enemy.hp" />
    </div>

    <!-- Range Input -->
    <div>
      <label for="range">Range:</label>
      <input type="number" id="range" v-model="enemy.range" />
    </div>

    <!-- Skills Selection -->
    <div>
      <h2>Skills</h2>
      <div v-for="skill in skills" :key="skill.id">
        <label :for="'skill-' + skill.id">
          <input
            type="checkbox"
            :id="'skill-' + skill.id"
            :value="skill.id"
            v-model="enemy.skills"
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
            v-model="enemy.properties"
          />
          {{ property.name }}
        </label>
      </div>
    </div>

    <button type="submit">Create Enemy</button>
  </form>
</template>

<script>
import axios from "@/services/axios";
import { fetchList } from "@/services/apiService.js";

export default {
  data() {
    return {
      enemy: {
        atk: 0,
        hp: 0,
        range: 0,
        skills: [],
        properties: [],
      },
      skills: [],
      properties: [],
    };
  },
  async created() {
    try {
      // Fetch skills and properties for selection
      this.skills = await fetchList("/api/skill/list");
      this.properties = await fetchList("/api/property/list");
    } catch (error) {
      console.error("Error fetching skills or properties:", error);
    }
  },
  methods: {
    async onSubmit() {
      try {
        await axios.post("/api/enemy", this.enemy);
        alert("Enemy added successfully!");
        this.$router.push("/enemy-list");
      } catch (error) {
        console.error("Error adding enemy:", error);
        alert("Failed to add enemy.");
      }
    },
  },
};
</script>
