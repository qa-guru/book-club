import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/signin',
      name: 'signin',
      component: () => import('@/views/SignIn.vue'),
      meta: { title: 'Вход' },
    },
    {
      path: '/signup',
      name: 'signup',
      component: () => import('@/views/SignUp.vue'),
      meta: { title: 'Регистрация' },
    },
    {
      path: '/clubs/create',
      name: 'create-club',
      component: () => import('@/views/CreateClub.vue'),
      meta: {
        requiresAuth: true,
        title: 'Создание клуба',
      },
    },
    {
      path: '/clubs/:id/edit',
      name: 'edit-club',
      component: () => import('@/views/EditClub.vue'),
      meta: {
        requiresAuth: true,
        title: 'Редактирование клуба',
      },
    },
    {
      path: '/clubs/:id',
      name: 'club-details',
      component: () => import('@/views/ClubDetails.vue'),
      meta: {
        requiresAuth: false,
        title: 'Детали клуба',
      },
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('@/views/UserProfile.vue'),
      meta: {
        requiresAuth: true,
        title: 'Профиль',
      },
    },
    {
      path: '/',
      name: 'clubs',
      component: () => import('@/views/ClubCards.vue'),
      meta: { title: 'Клубы' },
    },
  ],
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'signin' })
    return
  }

  if (to.name === 'edit-club' && to.params.id) {
    const response = await axios.get(`/api/v1/clubs/${to.params.id}/`)

    if (String(response.data.owner.id) !== String(authStore.user?.id)) {
      next({ name: 'clubs' })
      return
    }
  }

  next()
})

export default router
