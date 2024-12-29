<template>
    <div>
      <h1>Skills List</h1>
      <div v-if="skills.length">
        <ul>
          <li v-for="skill in skills" :key="skill.id">
            <strong>ID:</strong> {{ skill.id }},
            <strong>Skill Name:</strong> {{ skill.name }}
            <button @click="goToEdit(skill.id)">Edit</button>
          </li>
        </ul>
      </div>
      <div v-else>
        <p>No skills found.</p>
      </div>
      <button @click="goBack">Back</button>
    </div>
  </template>
  
  <script>
  import axios from "@/services/axios.js"; // Axios로 API 호출
  
  export default {
    data() {
      return {
        skills: [], // 적 데이터 저장
      };
    },
    created() {
      this.fetchSkills(); // 페이지 생성 시 API 호출
    },
    methods: {
      async fetchSkills() {
        try {
          const response = await axios.get("/api/skill/list");
          this.skills = response.data; // API 응답 저장
        } catch (error) {
          console.error("Error fetching enemies:", error);
        }
      },
      goBack() {
        this.$router.push("/"); // 홈으로 이동
      },
      goToEdit(skillId) {
        this.$router.push(`/skill/edit/${skillId}`);
      },
    },
  };
  </script>
  