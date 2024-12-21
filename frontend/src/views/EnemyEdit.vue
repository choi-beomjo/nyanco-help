<template>
    <div>
      <h1>Edit Enemy</h1>
      <form @submit.prevent="updateEnemy">
        <div>
          <label for="atk">Attack:</label>
          <input type="number" v-model="enemy.atk" id="atk" />
        </div>
        <div>
          <label for="hp">Health:</label>
          <input type="number" v-model="enemy.hp" id="hp" />
        </div>
        <div>
          <label for="range">Range:</label>
          <input type="number" v-model="enemy.range" id="range" />
        </div>
        <button type="submit">Save</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from "@/services/axios";
  
  export default {
    data() {
      return {
        enemy: {
          atk: 0,
          hp: 0,
          range: 0,
        },
      };
    },
    async created() {
      const enemyId = this.$route.params.id;
      try {
        const response = await axios.get(`/api/enemy/${enemyId}`);
        this.enemy = response.data;
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
    },
  };
  </script>
  