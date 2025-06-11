import { createRouter, createWebHistory } from 'vue-router';
import LoginView from './LoginView.vue';
import DashboardView from './DashboardView.vue';
import UserProfile from './UserProfile.vue';
import RegisterView from './RegisterView.vue';

const routes = [
  { path: '/', component: LoginView },
  { path: '/dashboard', component: DashboardView },
  { path: '/customer_profile', component: UserProfile},
  { path: '/register', component: RegisterView},
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
