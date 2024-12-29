<template>
    <li>
      <strong>ID:</strong> {{ property.id }},
      <strong>Property Name:</strong> {{ property.name }}
      <button @click="$emit('edit', property.id)">Edit</button>
    </li>
  </template>
  
  <script>
  export default {
    props: {
      property: {
        type: Object,
        required: true,
      },
    },
  };
  </script>