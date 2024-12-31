<template>
    <h1>Edit Character</h1>
    <form @submit.prevent="onSubmit">
      <!-- Attack Input -->
    <div>
      <label for="name">Name:</label>
      <input type="string" id="name" v-model="character.name" />
    
    </div>
    
    <!-- Attack Input -->
      <div>
        <label for="atk">Attack:</label>
        <input
          type="number"
          id="atk"
          v-model="character.atk"
        />
      </div>
  
      <!-- Health Input -->
      <div>
        <label for="hp">Health:</label>
        <input
          type="number"
          id="hp"
          v-model="character.hp"
        />
      </div>
  
      <!-- Range Input -->
      <div>
        <label for="range">Range:</label>
        <input
          type="number"
          id="range"
          v-model="character.range"
        />
      </div>

      <div>
        <h2>Skills</h2>
        <div v-for="skill in skills" :key="skill.id">
          <label :for="'skill-' + skill.id">
            <input
              type="checkbox"
              :id="'skill-' + skill.id"
              :value="skill.id"
              v-model="character.skills"
            />
            {{ skill.name }}
          </label>
        </div>
      </div>

      <div>
        <h2>Properties</h2>
        <div v-for="property in properties" :key="property.id">
          <label :for="'property-' + property.id">
            <input
              type="checkbox"
              :id="'property-' + property.id"
              :value="property.id"
              v-model="character.properties"
            />
            {{ property.name }}
          </label>
        </div>
      </div>
  
    <button type="submit">Save</button>
    </form>
</template>
  
  <script>
  import axios from "@/services/axios";
  //import CharacterInputField from "@/components/character/CharacterInputField.vue";
  import { fetchList } from "@/services/apiService.js";
  //import CharacterForm from "@/components/character/CharacterForm.vue";
  
  export default {
    data() {
      return {
        character: {
          atk: 0,
          hp: 0,
          range: 0,
          skills: [],
          properties: [],
        },
        skills: [],
        properties: [],
      };
    },
    async created() {
      const characterId = this.$route.params.id;
      try {
        const response = await axios.get(`/api/character/${characterId}`);
        this.character = response.data;

        this.skills = await fetchList("/api/skill/list");
        this.properties = await fetchList("/api/property/list");

        this.character.skills = this.character.skills.map(skill => skill.id);
      this.character.properties = this.character.properties.map(property => property.id);
      } catch (error) {
        console.error("Error fetching character:", error);
      }
    },
    methods: {
      async updateCharacter() {
        const characterId = this.$route.params.id;
        try {
          await axios.put(`/api/character/${characterId}`, this.character);
          alert("Character updated successfully!");
          this.$router.push("/character-list");
        } catch (error) {
          console.error("Error updating character:", error);
          alert("Failed to update character.");
        }
      },
      onSubmit() {
        console.info("Character INfo ",this.character);
        this.$emit("submit", this.character); // 부모 컴포넌트에 수정된 character 전달
        this.updateCharacter();
      },
    },
  };
  </script>
  