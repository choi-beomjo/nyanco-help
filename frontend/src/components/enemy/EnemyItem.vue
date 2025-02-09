<template>
  <li class="enemy-item">
    <div class="enemy-info">
      <strong>ID:</strong> <span>{{ enemy.id }}</span>
      <strong>Name:</strong> <span>{{ enemy.name }}</span>
      <strong>ATK:</strong> <span>{{ enemy.atk }}</span>
      <strong>HP:</strong> <span>{{ enemy.hp }}</span>
      <strong>Range:</strong> <span>{{ enemy.range }}</span>
      <strong>Skills:</strong> 
      <div class="skill-list">
        <span v-for="skill in enemy.skills" :key="skill.id" class="skill-tag">
          <span v-html="getSkillIcon(skill.name)"></span> 
          {{ skill.name }}
        </span>
      </div>
      <strong>Properties:</strong>
      <div class="property-list">
        <span
          v-for="property in enemy.properties"
          :key="property.id"
          :class="['property-tag', getPropertyClass(property.name)]"
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
export default {
  props: {
    enemy: {
      type: Object,
      required: true,
    },
  },
  methods: {
    getPropertyClass(property) {
      const propertyColors = {
        red: "property-red",
        white: "property-white",
        metal: "property-metal",
        angel: "property-yellow",
        zombie: "property-purple",
        black: "property-black",
        devil: "property-navy",
        fly: "property-green",
        alien: "property-sky"
      };
      return propertyColors[property.toLowerCase()] || "property-default";
    },
    getSkillIcon(skill) {
      const skillIcons = {
        "멈추기": `<i class="fas fa-clock"></i>`, // 🕰️ 시계
        "멈추기 무효": `
            <i class="fas fa-clock"></i>
            <i class="fas fa-ban margin-left: 5px"></i>
        `, // 🕰️+🚫 (시계+금지)
        "엄청 강하다": `<i class="fas fa-hand-rock"></i>`, // ✊ 권투 글러브
        "방어력 증가": `<i class="fas fa-shield-alt"></i>`, // 🛡️ 방패
        "파동": `<i class="fas fa-wave-square"></i>`, // 🌊 파동
        "독 데미지": `<i class="fas fa-skull-crossbones"></i>`, // ☠️ 독
        "날려버린다": `<i class="fas fa-wind"></i>`, // 💨 바람
        "공격력 업":`
            <i class="fas fa-hammer"></i>
            <i class="fas fa-arrow-up margin-left: 5px"></i>
        `,
        "느리게 한다":`
          <i class="fas fa-running"></i>
          <i class="fas fa-arrow-down margin-left: 5px"></i>
        `,
      };
      return skillIcons[skill] ||  `<i class="fas fa-question-circle"></i>`; // ❓ 기본 아이콘
    },
  },
};
</script>
