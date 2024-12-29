<template>
    <li>
      <strong>ID:</strong> {{ skill.id }},
      <strong>Skill Name:</strong> {{ skill.skills }}
      <button @click="$emit('edit', skill.id)">Edit</button>
    </li>
  </template>
  
  <script>
  export default {
    props: {
      skill: {
        type: Object,
        required: true,
      },
    },
  };
  </script>