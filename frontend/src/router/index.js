import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import MapView from '../views/MapView.vue'

const routes = [
  { path: '/', component: HomeView },
  { path: '/login', component: LoginView },
  { path: '/map', component: MapView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Navigation guard to check for username and password in sessionStorage
router.beforeEach((to, from, next) => {
  const username = sessionStorage.getItem('username')
  const password = sessionStorage.getItem('password')

  if (!username || !password) {
    if (to.path !== '/login') {
      return next('/login')
    }
  }
  next()
})

export default router