<template>
  <div class="home-container">
    <h1>Welcome to the Home Page</h1>

    <!-- 로그인 상태 확인 -->
    <LoginForm v-if="!isLoggedIn" @login-success="handleLogin" />

    <div v-else>
      <p class="user-info">Hello, {{ username }}!</p>

      <div class="home-button-group">
        <button class="home-button-nav" @click="goToPosts">Go to Posts</button>
        <button class="home-button-danger" @click="logout">Logout</button>
      </div>

      <div class="home-button-group">
        <button class="home-button" @click="goToEnemyList">View Enemy List</button>
        <button class="home-button" @click="goToSkillList">View Skill List</button>
        <button class="home-button" @click="goToPropertyList">View Property List</button>
        <button class="home-button" @click="goToCharacterList">View Character List</button>
      </div>
    </div>
  </div>
</template>

<script>
import LoginForm from "@/views/auth/LoginForm.vue";
import "@/assets/css/HomeView.css"; // 새로운 스타일 적용

export default {
  components: { LoginForm },
  data() {
    return {
      isLoggedIn: false,
      username: "",
    };
  },
  mounted() {
    // 새로 고침 시 토큰 확인
    const token = localStorage.getItem("token");
    const username = localStorage.getItem("username");

    if (token && username) {
      this.isLoggedIn = true;
      this.username = username;
    }
  },
  methods: {
    handleLogin() {
      this.isLoggedIn = true;
      this.username = localStorage.getItem("username");
    },
    goToPosts() {
      this.$router.push("/posts");
    },
    logout() {
      localStorage.clear();
      this.isLoggedIn = false;
      this.username = "";
      this.$router.push("/login");
    },
    goToEnemyList() {
      this.$router.push("/enemy-list");
    },
    goToSkillList() {
      this.$router.push("/skill-list");
    },
    goToPropertyList() {
      this.$router.push("/property-list");
    },
    goToCharacterList() {
      this.$router.push("/character-list");
    },
  },
};
</script>
