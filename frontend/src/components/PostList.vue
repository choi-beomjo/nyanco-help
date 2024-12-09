<template>
  <div>
    <h1>Posts</h1>
    <ul>
      <li v-for="post in posts" :key="post.id">
        {{ post.title }} - {{ post.contents }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      posts: [],
    };
  },
  async mounted() {
    const response = await fetch("http://localhost:8000/api/board/post-all");
    this.posts = await response.json();
  },
};
</script>
