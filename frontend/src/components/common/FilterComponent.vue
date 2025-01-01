<template>
    <div>
      <!-- Skills Selection -->
      <div>
        <h2>Skills</h2>
        <div v-for="skill in skills" :key="skill.id">
          <label :for="'skill-' + skill.id">
            <input
              type="checkbox"
              :id="'skill-' + skill.id"
              :value="skill.id"
              v-model="selectedSkills"
            />
            {{ skill.name }}
          </label>
        </div>
      </div>
  
      <!-- Properties Selection -->
      <div>
        <h2>Properties</h2>
        <div v-for="property in properties" :key="property.id">
          <label :for="'property-' + property.id">
            <input
              type="checkbox"
              :id="'property-' + property.id"
              :value="property.id"
              v-model="selectedProperties"
            />
            {{ property.name }}
          </label>
        </div>
      </div>
  
      <!-- Filter Button -->
      <button @click="filterItems">Filter</button>
  
      <!-- Filtered Items List -->
      <div v-if="items.length > 0">
        <h2>Filtered {{ itemType }}</h2>
        <ul>
          <li v-for="item in items" :key="item.id">
            {{ item.name }} - ATK: {{ item.atk }}, HP: {{ item.hp }}
          </li>
        </ul>
      </div>
      <div v-else>
        <p>No {{ itemType.toLowerCase() }} match the selected filters.</p>
      </div>
    </div>
  </template>
  
  <script>
import axios from "@/services/axios";
export default {
    props: {
      skills: Array,
      properties: Array,
      apiEndpoint: String, // API 엔드포인트를 전달받음
      itemType: String, // 적군 또는 캐릭터 이름
    },
    data() {
      return {
        selectedSkills: [],
        selectedProperties: [],
        items: [],
      };
    },
    methods: {
      async filterItems() {
        try {
          const response = await axios.post(this.apiEndpoint, {
            skills: this.selectedSkills,
            properties: this.selectedProperties,
          });
          this.items = response.data;
        } catch (error) {
          console.error(`Error filtering ${this.itemType.toLowerCase()}s:`, error);
          alert(`Failed to fetch filtered ${this.itemType.toLowerCase()}s.`);
        }
      },
    },
  };
  </script>
  