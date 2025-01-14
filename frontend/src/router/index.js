import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../components/HomeView.vue';
import PostList from '../components/PostList.vue';
import LoginForm from "@/views/auth/LoginForm.vue";
import enemyRoutes from './enemyRoutes';
import propertyRoutes from './propertyRoutes';
import skillRoutes from './skillRoutes';
import characterRoutes from './characterRoutes';

const routes = [
  { path: '/', name: 'HomeView', component: HomeView },
  { path: '/posts', name: 'PostList', component: PostList, meta: { requiresAuth: true } },
  {
    path: "/login",
    name: "Login",
    component: LoginForm,
  },
  ...enemyRoutes,
  ...propertyRoutes,
  ...skillRoutes,
  ...characterRoutes,
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
