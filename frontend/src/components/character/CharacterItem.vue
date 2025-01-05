<template>
    <li>
      <strong>ID:</strong> {{ character.id }},
      <strong>Name:</strong> {{ character.name }},
      <strong>ATK:</strong> {{ character.atk }},
      <strong>HP:</strong> {{ character.hp }},
      <strong>Range:</strong> {{ character.range }},
      <strong>Grade:</strong> {{ character.grade }},
      <strong>Skills:</strong> {{ character.skills }},
      <strong>Properties</strong> {{ character.properties }}
      <button v-if="showEditButton" @click="$emit('edit', character.id)">Edit</button>
    </li>
  </template>
  
  <script>
  export default {
    props: {
      character: {
        type: Object,
        required: true,
      },
      showEditButton: {
        type: Boolean,
        default: true, // 기본값은 추천 버튼을 보이게 설정
    },
    },
  };
  </script>
  