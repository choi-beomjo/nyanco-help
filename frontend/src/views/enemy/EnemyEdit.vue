<template>
  <div class="enemy-edit-container">
    <h1>Edit Enemy</h1>
    <form @submit.prevent="onSubmit">
      <!-- Name Input -->
      <div class="form-group">
        <label for="name">Name:</label>
        <input type="text" id="name" v-model="enemy.name" />
      </div>

      <!-- Attack Input -->
      <div class="form-group">
        <label for="atk">Attack:</label>
        <input type="number" id="atk" v-model="enemy.atk" />
      </div>

      <!-- Health Input -->
      <div class="form-group">
        <label for="hp">Health:</label>
        <input type="number" id="hp" v-model="enemy.hp" />
      </div>

      <!-- Range Input -->
      <div class="form-group">
        <label for="range">Range:</label>
        <input type="number" id="range" v-model="enemy.range" />
      </div>

      <!-- Skills Selection -->
      <div>
        <h2>Skills</h2>
        <div class="checkbox-group">
          <label v-for="skill in skills" :key="skill.id" :for="'skill-' + skill.id">
            <input type="checkbox" :id="'skill-' + skill.id" :value="skill.id" v-model="enemy.skills" />
            {{ skill.name }}
          </label>
        </div>
      </div>

      <!-- Properties Selection -->
      <div>
        <h2>Properties</h2>
        <div class="checkbox-group">
          <label v-for="property in properties" :key="property.id" :for="'property-' + property.id">
            <input type="checkbox" :id="'property-' + property.id" :value="property.id" v-model="enemy.properties" />
            {{ property.name }}
          </label>
        </div>
      </div>

      <button type="submit">Save</button>
    </form>
    <BackButton target="/enemy-list" />
  </div>
</template>

<script>
import axios from "@/services/axios";
import { fetchList } from "@/services/apiService.js";
import BackButton from "@/components/common/BackButton.vue";
import "@/assets/css/EnemyEdit.css"; // CSS 적용

export default {
  components: {
    BackButton,
  },
  data() {
    return {
      enemy: {
        name: "",
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
    const enemyId = this.$route.params.id;
    try {
      const response = await axios.get(`/api/enemy/${enemyId}`);
      this.enemy = response.data;

      this.skills = await fetchList("/api/skill/list");
      this.properties = await fetchList("/api/property/list");

      this.enemy.skills = this.enemy.skills.map((skill) => skill.id);
      this.enemy.properties = this.enemy.properties.map((property) => property.id);
    } catch (error) {
      console.error("Error fetching enemy:", error);
    }
  },
  methods: {
    async updateEnemy() {
      const enemyId = this.$route.params.id;
      try {
        await axios.put(`/api/enemy/${enemyId}`, this.enemy);
        alert("Enemy updated successfully!");
        this.$router.push("/enemy-list");
      } catch (error) {
        console.error("Error updating enemy:", error);
        alert("Failed to update enemy.");
      }
    },
    onSubmit() {
      this.updateEnemy();
    },
  },
};
</script>
