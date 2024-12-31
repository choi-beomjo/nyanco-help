<template>
    <li>
      <strong>ID:</strong> {{ character.id }},
      <strong>Name:</strong> {{ character.name }},
      <strong>ATK:</strong> {{ character.atk }},
      <strong>HP:</strong> {{ character.hp }},
      <strong>Range:</strong> {{ character.range }},
      <strong>Skills:</strong> {{ character.skills }},
      <strong>Properties</strong> {{ character.properties }}
      <button @click="$emit('edit', character.id)">Edit</button>
    </li>
  </template>
  
  <script>
  export default {
    props: {
      character: {
        type: Object,
        required: true,
      },
    },
  };
  </script>
  