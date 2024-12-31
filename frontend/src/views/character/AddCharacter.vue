<template>
  <h1>Add Character</h1>
  <form @submit.prevent="onSubmit">
    <!-- Attack Input -->
    <div>
      <label for="name">Name:</label>
      <input type="string" id="name" v-model="character.name" />
    </div>

    <!-- Attack Input -->
    <div>
      <label for="atk">Attack:</label>
      <input type="number" id="atk" v-model="character.atk" />
    </div>

    <!-- Health Input -->
    <div>
      <label for="hp">Health:</label>
      <input type="number" id="hp" v-model="character.hp" />
    </div>

    <!-- Range Input -->
    <div>
      <label for="range">Range:</label>
      <input type="number" id="range" v-model="character.range" />
    </div>

    <!-- Grade Input -->
    <div>
        <label for="range">Grade:</label>
        <input type="str" id="grade" v-model="character.grade" />
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
            v-model="character.skills"
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
            v-model="character.properties"
          />
          {{ property.name }}
        </label>
      </div>
    </div>

    <button type="submit">Create Character</button>
  </form>
  <BackButton target="/character-list" />
</template>

<script>
import axios from "@/services/axios";
import { fetchList } from "@/services/apiService.js";
import BackButton from "@/components/common/BackButton.vue";

export default {
  components:{
    BackButton,
  },
  data() {
    return {
      character: {
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
        await axios.post("/api/character", this.character);
        alert("Character added successfully!");
        this.$router.push("/character-list");
      } catch (error) {
        console.error("Error adding character:", error);
        alert("Failed to add character.");
      }
    },
  },
};
</script>
