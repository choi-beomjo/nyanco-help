<template>
    <div>
      <h1>Enemy List</h1>
      <div v-if="enemies.length">
        <ul>
          <li v-for="enemy in enemies" :key="enemy.id">
            <strong>ID:</strong> {{ enemy.id }},
            <strong>ATK:</strong> {{ enemy.atk }},
            <strong>HP:</strong> {{ enemy.hp }},
            <strong>Range:</strong> {{ enemy.range }}
            <strong>Range:</strong> {{ enemy.skills }}
          </li>
        </ul>
      </div>
      <div v-else>
        <p>No enemies found.</p>
      </div>
      <button @click="goBack">Back</button>
    </div>
  </template>
  
  <script>
  import axios from "@/services/axios.js"; // Axios로 API 호출
  
  export default {
    data() {
      return {
        enemies: [], // 적 데이터 저장
      };
    },
    created() {
      this.fetchEnemies(); // 페이지 생성 시 API 호출
    },
    methods: {
      async fetchEnemies() {
        try {
          const response = await axios.get("/api/enemy/list");
          this.enemies = response.data; // API 응답 저장
        } catch (error) {
          console.error("Error fetching enemies:", error);
        }
      },
      goBack() {
        this.$router.push("/"); // 홈으로 이동
      },
    },
  };
  </script>
  