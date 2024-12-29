<template>
    <li>
      <strong>ID:</strong> {{ enemy.id }},
      <strong>ATK:</strong> {{ enemy.atk }},
      <strong>HP:</strong> {{ enemy.hp }},
      <strong>Range:</strong> {{ enemy.range }}
      <strong>Skills:</strong> {{ enemy.skills }}
      <button @click="$emit('edit', enemy.id)">Edit</button>
    </li>
  </template>
  
  <script>
  export default {
    props: {
      enemy: {
        type: Object,
        required: true,
      },
    },
  };
  </script>
  