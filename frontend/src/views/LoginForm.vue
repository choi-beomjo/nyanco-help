<template>
  <div>
    <h2>Login</h2>
    <form @submit.prevent="handleLogin">
      <label>Username:</label>
      <input v-model="username" type="text" required />
      <label>Password:</label>
      <input v-model="password" type="password" required />
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script>
import { login } from "@/services/authService";

export default {
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    async handleLogin() {
        try {
            const response = await login(this.username, this.password);

            const { access_token, token_type, username } = response;
            localStorage.setItem("token", access_token);
            localStorage.setItem("token_type", token_type);
            localStorage.setItem("username", username);

            alert(`Welcome ${username}!`); // 성공 메시지
            this.$router.push("/");
            this.$emit("login-success");
        } catch (error) {
            alert(error.message); // 실패 메시지
        }
    },
  },
};
</script>
