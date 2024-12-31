<template>
  <div>
    <h1>Character List</h1>
    <div v-if="enemies.length">
      <ul>
        <CharacterItem
          v-for="character in enemies"
          :key="character.id"
          :character="character"
          @edit="goToEdit"
        />
      </ul>
    </div>
    <div v-else>
      <p>No enemies found.</p>
    </div>
    <BackButton />
    <button @click="goAdd">Add Character</button>
  </div>
</template>
  
  <script>
  // import axios from "@/services/axios.js"; // Axios로 API 호출
  import CharacterItem from "@/components/character/CharacterItem.vue";
  import { fetchList } from "@/services/apiService.js";
  import BackButton from "@/components/common/BackButton.vue";
  import { useRouterActions } from "@/composables/useRouterActions";

  export default {
    components:{
      CharacterItem,
      BackButton,
    },
    data() {
      return {
        enemies: [], // 적 데이터 저장
      };
    },
    created() {
      this.fetchCharacters(); // 페이지 생성 시 API 호출
    },
    setup() {
    const { goBack, goToEdit, goAdd } = useRouterActions("character"); // "skill" 대신 "enemy" 등 다른 값 사용 가능.

    return {
      goBack,
      goToEdit,
      goAdd,
    };
  },
    methods: {
      async fetchCharacters() {
        try {
          this.enemies = await fetchList("/api/character/list");
        } catch (error) {
          console.error("Error fetching enemies:", error);
        }
      },

    },
  };
  </script>
  