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
export default {
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    handleLogin() {
      if (this.username === "admin" && this.password === "password") {
        this.$emit("login-success");
      } else {
        alert("Invalid credentials!");
      }
    },
  },
};
</script>
