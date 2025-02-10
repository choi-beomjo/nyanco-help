<template>
  <li class="character-item">
    <div class="character-info">
      <strong>ID</strong> <span>{{ character.id }}</span>
      <strong>Name</strong> <span>{{ character.name }}</span>
      <strong>ATK</strong> <span>{{ character.atk }}</span>
      <strong>HP</strong> <span>{{ character.hp }}</span>
      <strong>Range</strong> <span>{{ character.range }}</span>
      <strong>Grade</strong> <span>{{ character.grade }}</span>

      <strong>Skills</strong>
      <div class="skill-list">
        <span v-for="skill in character.skills" :key="skill.id" class="skill-tag">
          <span v-html="getSkillIcon(skill.name)"></span> 
          {{ skill.name }}
        </span>
      </div>

      <strong>Properties</strong>
      <div class="property-list">
        <span
          v-for="property in character.properties"
          :key="property.id"
          :style="{ backgroundColor: getPropertyColor(property.name), color: getTextColor(property.name) }"
          class="property-tag"
        >
          {{ property.name }}
        </span>
      </div>
    </div>

    <div class="character-actions">
      <button v-if="showEditButton" @click="$emit('edit', character.id)">Edit</button>
    </div>
  </li>
</template>

<script>
import "@/assets/css/CharacterItem.css";
import "@fortawesome/fontawesome-free/css/all.css"; // Font Awesome Import
import { useIconAndColor } from "@/composables/useIconAndColor";

export default {
  props: {
    character: {
      type: Object,
      required: true,
    },
    showEditButton: {
      type: Boolean,
      default: true,
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
};
</script>
