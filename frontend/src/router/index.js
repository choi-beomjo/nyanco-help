import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../components/HomeView.vue';
import PostList from '../components/PostList.vue';
import LoginForm from "@/views/auth/LoginForm.vue";
import EnemyListView from "@/views/enemy/EnemyListView.vue"
import EnemyEdit from '@/views/enemy/EnemyEdit.vue';
import SkillListView from "@/views/skill/SkillListView.vue"


const routes = [
  { path: '/', name: 'HomeView', component: HomeView },
  { path: '/posts', name: 'PostList', component: PostList, meta: { requiresAuth: true } },
  {
    path: "/login",
    name: "Login",
    component: LoginForm,
  },
  { path: "/enemy-list", name: "EnemyList", component: EnemyListView },
  { path: "/enemy/edit/:id", component: EnemyEdit, props: true },
  { path: "/skill-list", name: "SkillList", component: SkillListView }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem("token");

  if (to.meta.requiresAuth && !isAuthenticated) {
    next("/login");  // 로그인 필요 시 리다이렉트
  } else {
    next();  // 접근 허용
  }
});

export default router;
