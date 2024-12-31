import EnemyListView from "@/views/enemy/EnemyListView.vue";
import EnemyEdit from '@/views/enemy/EnemyEdit.vue';
import AddEnemy from '@/views/enemy/AddEnemy.vue';


export default [
  { path: "/enemy-list", name: "EnemyList", component: EnemyListView },
  { path: "/enemy/edit/:id", component: EnemyEdit, props: true },
  { path: "/enemy/add", component: AddEnemy},
];
