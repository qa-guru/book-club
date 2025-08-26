<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const handleLogout = () => {
  authStore.logout()
  router.push('/signin')
}
</script>

<template>
  <div class="page">
    <div v-if="authStore.user" class="profile-info">
      <p><strong>Логин пользователя:</strong> {{ authStore.user.username }}</p>
      <button @click="handleLogout" class="logout-btn">Выйти</button>
    </div>
  </div>
</template>

<style scoped>
.page {
  width: 100%;
  max-width: 540px;
  margin: 0 auto;
  padding: 1rem 1rem;
  box-sizing: border-box;
  color: var(--color-white);
}

.profile-info {
  background: var(--color-black);
  border-radius: 50px;
  padding: 2.5rem;
  box-sizing: border-box;
}

.profile-info p {
  font-size: clamp(1rem, 3vw, 1.25rem);
  margin-bottom: 1.5rem;
  line-height: 1.5;
  text-align: center;
}

.profile-info strong {
  font-weight: 500;
  color: var(--color-primary);
}

.logout-btn {
  width: 100%;
  max-width: 257px;
  height: 50px;
  background: var(--color-error);
  border-radius: 30px;
  border: none;
  color: var(--color-white);
  font-size: clamp(1rem, 3vw, 1.25rem);
  font-weight: 500;
  display: block;
  margin: 2rem auto 0;
  cursor: pointer;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  opacity: 0.9;
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .profile-info {
    padding: 1.5rem;
    border-radius: 30px;
  }

  .logout-btn {
    max-width: 100%;
  }
}

@media (max-width: 480px) {
  .page {
    padding: 1rem;
  }

  .profile-info {
    padding: 1.25rem;
  }

  .logout-btn {
    height: 45px;
  }
}
</style>
