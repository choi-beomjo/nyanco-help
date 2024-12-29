<template>
    <form @submit.prevent="onSubmit">
      <!-- Attack Input -->
      <div>
        <label for="atk">Attack:</label>
        <input
          type="number"
          id="atk"
          v-model="localEnemy.atk"
        />
      </div>
  
      <!-- Health Input -->
      <div>
        <label for="hp">Health:</label>
        <input
          type="number"
          id="hp"
          v-model="localEnemy.hp"
        />
      </div>
  
      <!-- Range Input -->
      <div>
        <label for="range">Range:</label>
        <input
          type="number"
          id="range"
          v-model="localEnemy.range"
        />
      </div>
    <!--
      <div>
        <h2>Skills</h2>
        <div v-for="skill in skills" :key="skill.id">
          <label :for="'skill-' + skill.id">
            <input
              type="checkbox"
              :id="'skill-' + skill.id"
              :value="skill.id"
              v-model="localEnemy.skills"
            />
            {{ skill.name }}
          </label>
        </div>
      </div>
    -->
  
    <button type="submit">Save</button>
    </form>
  </template>
  
  <script>
  export default {
    props: {
      enemy: {
        type: Object,
        required: true,
      },
      skills: {
        type: Array,
        required: true,
      },
    },
    emits: ["submit"],
    data() {
      return {
        localEnemy: { ...this.enemy }, // enemy 객체의 복사본 생성
      };
    },
    methods: {
      onSubmit() {
        console.info("Enemy INfo ",this.localEnemy);
        this.$emit("submit", this.localEnemy); // 부모 컴포넌트에 수정된 enemy 전달
      },
    },
  };
  </script>
  