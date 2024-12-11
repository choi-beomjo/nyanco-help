<template>
  <div>
    <h1>Welcome to the Home Page</h1>
    <LoginForm v-if="!isLoggedIn" @login-success="isLoggedIn = true" />
    <button v-if="isLoggedIn" @click="goToPosts">Go to Posts</button>
  </div>
</template>

<script>
import LoginForm from "@/components/LoginForm.vue";

export default {
  components: { LoginForm },
  data() {
    return {
      isLoggedIn: false,
    };
  },
  methods: {
    goToPosts() {
      this.$router.push("/posts");
    },
  },
};
</script>
