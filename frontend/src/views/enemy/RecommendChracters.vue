<template>
    <div>
      <h1>Character List</h1>
  
      <!-- Range 캐릭터 리스트 -->
      <div v-if="enemiesByRange.length">
        <h2>Characters by Range</h2>
        <ul>
          <CharacterItem
            v-for="character in enemiesByRange"
            :key="character.id"
            :character="character"
            @edit="goToEdit"
            :showEditButton="false"
          />
        </ul>
      </div>
      <div v-else>
        <p>No characters by range found.</p>
      </div>
  
      <!-- Property 캐릭터 리스트 -->
      <div v-if="enemiesByProperty.length">
        <h2>Characters by Property</h2>
        <ul>
          <CharacterItem
            v-for="character in enemiesByProperty"
            :key="character.id"
            :character="character"
            @edit="goToEdit"
            :showEditButton="false"
          />
        </ul>
      </div>
      <div v-else>
        <p>No characters by property found.</p>
      </div>
  
      <BackButton target="/enemy-list"/>
    </div>
  </template>
  
  <script>
  import CharacterItem from "@/components/character/CharacterItem.vue";
  import { fetchList } from "@/services/apiService.js";
  import BackButton from "@/components/common/BackButton.vue";
  import { useRouterActions } from "@/composables/useRouterActions";
  
  export default {
    props: ['id'],
    components: {
      CharacterItem,
      BackButton,
    },
    data() {
      return {
        enemiesByRange: [], // range 캐릭터 데이터 저장
        enemiesByProperty: [], // property 캐릭터 데이터 저장
      };
    },
    created() {
        console.log('Received ID:', this.id);
        this.fetchCharacters(); // 페이지 생성 시 API 호출
    },
    setup() {
      const { goBack, goToEdit, goAdd } = useRouterActions("character");
  
      return {
        goBack,
        goToEdit,
        goAdd,
      };
    },
    methods: {
      async fetchCharacters() {
        try {
          const response = await fetchList(`/api/recommend/${this.$route.params.id}`);
          // 응답에서 characters_by_range와 characters_by_property를 각각 분리하여 저장
          this.enemiesByRange = response.characters_by_range;
          this.enemiesByProperty = response.characters_by_properties;
        } catch (error) {
          console.error("Error fetching enemies:", error);
        }
      },
    },
  };
  </script>
  