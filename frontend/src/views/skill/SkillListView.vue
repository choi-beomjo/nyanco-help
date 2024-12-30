<template>
    <div>
      <h1>Skills List</h1>
      <div v-if="skills.length">
        <ul>
          <SkillItem
            v-for="skill in skills"
            :key="skill.id"
            :skill="skill"
            @edit="goToEdit"
          />
        </ul>
      </div>
      <div v-else>
        <p>No skills found.</p>
      </div>
      <BackButton />
      <button @click="goAdd">Add Skill</button>
    </div>
  </template>
  
  <script>
  import axios from "@/services/axios.js"; // Axios로 API 호출
  import SkillItem from "@/components/skill/SkillItem.vue";
  import BackButton from "@/components/common/BackButton.vue";

  export default {
    components:{
      SkillItem,
      BackButton,
    },
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
      goAdd(){
        this.$router.push("/skill/add");
      }
    },
  };
  </script>
  