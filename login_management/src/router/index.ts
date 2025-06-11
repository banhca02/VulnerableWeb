import { createRouter, createWebHistory } from 'vue-router';
import LoginView from '../components/LoginView.vue';
import DashboardView from '../components/DashboardView.vue';
import UserProfile from '../components/UserProfile.vue';
import RegisterView from '../components/RegisterView.vue';

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
