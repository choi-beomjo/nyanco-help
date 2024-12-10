<template>
  <div>
    <h1>Welcome to the Home Page</h1>
    <button @click="goToPosts">Go to Posts</button>
  </div>
</template>

<script>
export default {
  methods: {
    goToPosts() {
      this.$router.push("/posts");
    },
  },
};
</script>
