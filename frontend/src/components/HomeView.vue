<template>
  <div>
    <h1>Welcome to the Home Page</h1>

    <!-- 로그인 상태 확인 -->
    <LoginForm v-if="!isLoggedIn" @login-success="handleLogin" />

    <div v-else>
      <p>Hello, {{ username }}!</p>
      <button @click="goToPosts">Go to Posts</button>
      <button @click="logout">Logout</button>
      <div>
        <button @click="goToEnemyList">View Enemy List</button>
        <button @click="goToSkillList">View Skill List</button>
        <button @click="goToPropertyList">View Property List</button>
        <button @click="goToCharacterList">View Character List</button>
      </div>
      </div>
  </div>
</template>

<script>
import LoginForm from "@/views/auth/LoginForm.vue";

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
      // 로그아웃 시 토큰 제거 및 리다이렉트
      localStorage.clear();
      this.isLoggedIn = false;
      this.username = "";
      this.$router.push("/login");
    },
    goToEnemyList() {
      this.$router.push("/enemy-list"); // 적 리스트 페이지로 이동
    },
    goToSkillList() {
      this.$router.push("/skill-list"); // 적 리스트 페이지로 이동
    },
    goToPropertyList() {
      this.$router.push("/property-list"); // 적 리스트 페이지로 이동
    },
    goToCharacterList() {
      this.$router.push("/character-list"); // 적 리스트 페이지로 이동
    },
  },
};
</script>
