import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '../components/LandingPage.vue'
import RegisterForm from '../components/RegisterForm.vue'
import LoginForm from '../components/LoginForm.vue'
import Home from '../views/Home.vue'
import EditProfile from '../components/EditProfile.vue'

const routes = [
  { path: '/', name: 'Landing', component: LandingPage },
  { path: '/register', name: 'Register', component: RegisterForm },
  { path: '/login', name: 'Login', component: LoginForm },
  { path: '/home', name: 'Home', component: Home },
  { path: '/edit-profile', name: 'EditProfile', component: EditProfile },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
