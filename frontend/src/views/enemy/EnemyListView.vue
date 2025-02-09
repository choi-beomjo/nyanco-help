<template>
  <div class="enemy-list-container">
    <h1>Enemy List</h1>
    <div v-if="enemies.length">
      <ul class="enemy-list">
        <EnemyItem
          v-for="enemy in enemies"
          :key="enemy.id"
          :enemy="enemy"
          @edit="goToEdit"
          @recommend="recommendEnemy(enemy.id)"
        />
      </ul>
    </div>
    <div v-else>
      <p class="no-enemies">No enemies found.</p>
    </div>
    <BackButton />
    <button @click="goAdd">Add Enemy</button>
    <button @click="goSearch">Search Enemy</button>
  </div>
</template>
  
  <script>
  import "@/assets/css/EnemyList.css";
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
      goSearch(){
        this.$router.push("/enemy/search");
      },
      recommendEnemy(id){
        this.$router.push(`/recommend/${id}`)
      }
    },
  };
  </script>
  