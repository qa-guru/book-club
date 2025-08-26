<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'
import type { Club } from '@/types/clubs'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const club = ref<Club | null>(null)

const fetchClub = async () => {
  const response = await axios.get(`/api/v1/clubs/${route.params.id}/`)
  club.value = response.data
}

const joinClub = async () => {
  await axios.post(`/api/v1/clubs/${route.params.id}/members/me/`)
  await fetchClub()
}

const leaveClub = async () => {
  await axios.delete(`/api/v1/clubs/${route.params.id}/members/me/`)
  router.push('/')
}

onMounted(() => {
  fetchClub()
})
</script>

<template>
  <div class="club-details">
    <div v-if="club" class="club-content">
      <div class="club-header">
        <h1>{{ club.bookTitle }}</h1>
        <span class="year">{{ club.publicationYear }}</span>
      </div>

      <p class="authors">Автор(ы): {{ club.bookAuthors }}</p>
      <p class="description">{{ club.description }}</p>

      <div class="club-actions">
        <a
          v-if="club.telegramChatLink"
          :href="club.telegramChatLink"
          target="_blank"
          class="telegram-btn"
        >
          Открыть Telegram чат
        </a>

        <template v-if="authStore.isAuthenticated">
          <button
            v-if="authStore.user?.id && !club.members.includes(authStore.user.id)"
            @click="joinClub"
            class="join-btn"
          >
            Присоединиться
          </button>

          <button
            v-if="
              authStore.user?.id &&
              club.members.includes(authStore.user.id) &&
              club.owner !== authStore.user.id
            "
            @click="leaveClub"
            class="leave-btn"
          >
            Покинуть клуб
          </button>

          <router-link
            v-if="club.owner === authStore.user?.id"
            :to="`/clubs/${club.id}/edit`"
            class="edit-btn"
          >
            Редактировать клуб
          </router-link>
        </template>
      </div>
    </div>
  </div>
</template>

<style scoped>
.club-details {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  padding: 1rem 1rem;
  box-sizing: border-box;
}

.loading,
.error {
  text-align: center;
  font-size: clamp(1rem, 3vw, 1.25rem);
  padding: 2rem;
  color: var(--color-white);
}

.error {
  color: var(--color-error);
}

.club-content {
  background: var(--color-black);
  border-radius: 50px;
  padding: 2.5rem;
  color: var(--color-white);
}

.club-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.club-header h1 {
  font-size: clamp(1.5rem, 4vw, 2rem);
  margin: 0;
  font-weight: 500;
  flex: 1;
  min-width: 60%;
}

.year {
  background: var(--color-primary);
  border-radius: 20px;
  padding: 0.5rem 1rem;
  font-size: clamp(0.875rem, 2vw, 1rem);
  margin-left: 1rem;
}

.authors {
  font-size: clamp(1rem, 2.5vw, 1.25rem);
  color: var(--color-text-secondary);
  margin-bottom: 1.5rem;
  font-style: italic;
}

.description {
  font-size: clamp(1rem, 2.5vw, 1.125rem);
  line-height: 1.6;
  margin-bottom: 2.5rem;
  white-space: pre-line;
}

.club-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 2rem;
}

.telegram-btn,
.join-btn,
.leave-btn,
.edit-btn {
  height: 50px;
  border-radius: 30px;
  border: none;
  font-size: clamp(1rem, 2vw, 1.125rem);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 0 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  flex: 1;
  min-width: 200px;
  max-width: 100%;
  box-sizing: border-box;
  white-space: nowrap;
}

.telegram-btn {
  background: #0088cc;
  color: white;
}

.join-btn {
  background: var(--color-primary);
  color: var(--color-white);
}

.leave-btn {
  background: var(--color-error);
  color: var(--color-white);
}

.edit-btn {
  background: var(--color-white);
  color: var(--color-black);
}

.telegram-btn:hover,
.join-btn:hover,
.leave-btn:hover,
.edit-btn:hover {
  opacity: 0.9;
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .club-content {
    padding: 1.5rem;
    border-radius: 30px;
  }

  .club-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .year {
    margin-left: 0;
    margin-top: 0.75rem;
  }

  .club-actions {
    flex-direction: column;
    align-items: stretch;
  }

  .telegram-btn,
  .join-btn,
  .leave-btn,
  .edit-btn {
    width: 100%;
    min-width: 100%;
    flex: none;
  }
}

@media (max-width: 480px) {
  .club-details {
    padding: 1rem;
  }

  .club-content {
    padding: 1.25rem;
  }

  .telegram-btn,
  .join-btn,
  .leave-btn,
  .edit-btn {
    height: 45px;
    padding: 0 1rem;
  }
}
</style>
