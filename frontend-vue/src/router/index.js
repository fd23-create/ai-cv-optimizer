import { createRouter, createWebHistory } from 'vue-router'
import { useAuth } from '@clerk/clerk-vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: () => import('@/views/Home.vue')
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: () => import('@/views/Dashboard.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/result/:id',
      name: 'Result',
      component: () => import('@/views/Result.vue'),
      meta: { requiresAuth: true }
    }
  ]
})

router.beforeEach((to, from, next) => {
  const { isSignedIn } = useAuth()
  
  if (to.meta.requiresAuth && !isSignedIn.value) {
    next('/')
  } else {
    next()
  }
})

export default router
