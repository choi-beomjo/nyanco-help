<template>
    <div class="filter-container">
      <!-- Skills Selection -->
      <h2>Skills</h2>
      <div class="checkbox-group">
        <div v-for="skill in skills" :key="skill.id">
          <label :for="'skill-' + skill.id">
            <input
              type="checkbox"
              :id="'skill-' + skill.id"
              :value="skill.id"
              v-model="selectedSkills"
            />
            <span v-html="getSkillIcon(skill.name)"></span>
            <span>{{ skill.name }}</span>
          </label>
        </div>
      </div>
  
      <!-- Properties Selection -->
      <h2>Properties</h2>
      <div class="checkbox-group">
       
          <label
          v-for="property in properties"
          :key="property.id"
          :for="'property-' + property.id"
          :style="{ backgroundColor: getPropertyColor(property.name), color: getTextColor(property.name) }"
          class="property-label"
        >
            <input
              type="checkbox"
              :id="'property-' + property.id"
              :value="property.id"
              v-model="selectedProperties"
            />
            
            <span>{{ property.name }}</span>
          </label>

      </div>
  
      <!-- Filter Button -->
      <button @click="filterItems">Filter</button>
  
      <!-- Filtered Items List -->
    <div class="filtered-list" v-if="items.length > 0">
      <h2>Filtered {{ itemType }}</h2>
      <ul>
        <li v-for="item in items" :key="item.id">
          <strong>{{ item.name }}</strong>
          <div>ATK: {{ item.atk }}, HP: {{ item.hp }}</div>

          <!-- 스킬 리스트 -->
          <div class="skill-list">
            <span v-for="skill in item.skills" :key="skill.id" class="skill-tag">
              {{ skill.name }}
            </span>
          </div>

          <!-- 속성 리스트 -->
          <div class="property-list">
            <span v-for="property in item.properties" :key="property.id" class="property-tag">
              {{ property.name }}
            </span>
          </div>
        </li>
      </ul>
    </div>

    <div v-else class="no-items">
      <p>No {{ itemType.toLowerCase() }} match the selected filters.</p>
    </div>
    </div>
  </template>
  
  <script>
import axios from "@/services/axios";
import "@/assets/css/FilterComponent.css";
import { useIconAndColor } from "@/composables/useIconAndColor.js";
export default {
    props: {
      skills: Array,
      properties: Array,
      apiEndpoint: String, // API 엔드포인트를 전달받음
      itemType: String, // 적군 또는 캐릭터 이름
    },
    setup() {
    const { getSkillIcon, getPropertyColor, getTextColor } = useIconAndColor();

    return {
      getSkillIcon,
      getPropertyColor,
      getTextColor,
    };
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
  