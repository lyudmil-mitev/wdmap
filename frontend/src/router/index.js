import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import DetailView from '../views/DetailView.vue'

const routes = [
  { path: '/', component: HomeView },
  { path: '/login', component: LoginView },
  { path: '/property/:id', name: "PropertyDetails", component: DetailView },
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