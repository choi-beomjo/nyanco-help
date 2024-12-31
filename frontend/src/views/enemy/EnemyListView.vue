<template>
  <div>
    <h1>Enemy List</h1>
    <div v-if="enemies.length">
      <ul>
        <EnemyItem
          v-for="enemy in enemies"
          :key="enemy.id"
          :enemy="enemy"
          @edit="goToEdit"
        />
      </ul>
    </div>
    <div v-else>
      <p>No enemies found.</p>
    </div>
    <BackButton />
    <button @click="goAdd">Add Enemy</button>
  </div>
</template>
  
  <script>
  import EnemyItem from "@/components/enemy/EnemyItem.vue";
  import { fetchList } from "@/services/apiService.js";
  import BackButton from "@/components/common/BackButton.vue";
  import { useRouterActions } from "@/composables/useRouterActions";

  export default {
    components:{
      EnemyItem,
      BackButton,
    },
    data() {
      return {
        enemies: [], // 적 데이터 저장
      };
    },
    created() {
      this.fetchEnemies(); // 페이지 생성 시 API 호출
    },
    setup() {
    const { goBack, goToEdit, goAdd } = useRouterActions("enemy");

    return {
      goBack,
      goToEdit,
      goAdd,
    };
  },
    methods: {
      async fetchEnemies() {
        try {
          this.enemies = await fetchList("/api/enemy/list");
        } catch (error) {
          console.error("Error fetching enemies:", error);
        }
      },
    },
  };
  </script>
  