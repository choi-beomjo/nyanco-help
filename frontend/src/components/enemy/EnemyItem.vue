<template>
  <li class="enemy-item">
    <div class="enemy-info">
      <strong>ID</strong> <span>{{ enemy.id }}</span>
      <strong>Name</strong> <span>{{ enemy.name }}</span>
      <strong>ATK</strong> <span>{{ enemy.atk }}</span>
      <strong>HP</strong> <span>{{ enemy.hp }}</span>
      <strong>Range</strong> <span>{{ enemy.range }}</span>
      <strong>Skills</strong> 
      <div class="skill-list">
        <span v-for="skill in enemy.skills" :key="skill.id" class="skill-tag">
          <span v-html="getSkillIcon(skill.name)"></span> 
          {{ skill.name }}
        </span>
      </div>
      <strong>Properties</strong>
      <div class="property-list">
        <span
    v-for="property in enemy.properties"
    :key="property.id"
    :style="{ backgroundColor: getPropertyColor(property.name), color: getTextColor(property.name) }"
    class="property-tag"
  >
          {{ property.name }}
        </span>
      </div>
    </div>
    <div class="enemy-actions">
      <button @click="$emit('edit', enemy.id)">Edit</button>
      <button @click="$emit('recommend', enemy)">Recommend</button>
    </div>
  </li>
</template>

<script>
import "@/assets/css/EnemyItem.css";
import "@fortawesome/fontawesome-free/css/all.css"; // Font Awesome Import
import { useIconAndColor } from "@/composables/useIconAndColor";
export default {
  props: {
    enemy: {
      type: Object,
      required: true,
    },
  },
  setup() {
    const { getSkillIcon, getPropertyColor, getTextColor } = useIconAndColor();

    return {
      getSkillIcon,
      getPropertyColor,
      getTextColor,
    };
  },
  methods: {
  },
};
</script>
