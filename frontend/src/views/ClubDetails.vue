<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useClubsStore } from '@/stores/clubs'
import ClubReviews from '@/components/ClubReviews.vue'
import type { Club } from '@/types/clubs'

const route = useRoute()
const router = useRouter()

const authStore = useAuthStore()
const clubsStore = useClubsStore()

const club = ref<Club | null>(null)
const isLoading = ref(false)
const error = ref('')

const fetchClub = async () => {
  isLoading.value = true
  error.value = ''
  try {
    club.value = await clubsStore.fetchClub(Number(route.params.id))
  } catch {
    error.value = 'Не удалось загрузить информацию о клубе'
  } finally {
    isLoading.value = false
  }
}

const joinClub = async () => {
  try {
    await clubsStore.joinClub(Number(route.params.id))
    await fetchClub()
  } catch {
    error.value = 'Не удалось присоединиться к клубу'
  }
}

const leaveClub = async () => {
  if (!confirm('Вы уверены, что хотите покинуть клуб?')) return

  try {
    await clubsStore.leaveClub(Number(route.params.id))
    router.push('/')
  } catch {
    error.value = 'Не удалось покинуть клуб'
  }
}

const isMember = computed(() => {
  return authStore.user?.id && club.value?.members.includes(authStore.user.id)
})

const isOwner = computed(() => {
  return authStore.user?.id === club.value?.owner?.id
})

onMounted(() => {
  fetchClub()
})
</script>

<template>
  <div class="club-details">
    <div v-if="isLoading" class="loading">Загрузка...</div>
    <div v-else-if="error" class="error">{{ error }}</div>

    <div v-else-if="club" class="club-content">
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
          <button v-if="!isMember && !isOwner" @click="joinClub" class="join-btn">
            Присоединиться
          </button>

          <button v-if="isMember && !isOwner" @click="leaveClub" class="leave-btn">
            Покинуть клуб
          </button>

          <router-link v-if="isOwner" :to="`/clubs/${club.id}/edit`" class="edit-btn">
            Редактировать клуб
          </router-link>
        </template>
      </div>

      <div class="club-stats">
        <div class="stat-item">
          <span class="stat-label">Участников:</span>
          <span class="stat-value">{{ club.members.length }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">Отзывов:</span>
          <span class="stat-value">{{ club.reviews?.length || 0 }}</span>
        </div>
      </div>

      <ClubReviews :club-id="club.id" :club-members="club.members" :club-owner="club.owner?.id" />
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

.club-stats {
  display: flex;
  gap: 2rem;
  margin: 2rem 0;
  padding: 1.5rem 0;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.stat-label {
  color: rgba(255, 255, 255, 0.6);
  font-size: 1rem;
}

.stat-value {
  font-size: 1.25rem;
  font-weight: 500;
  color: var(--color-primary);
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

  .club-stats {
    flex-direction: column;
    gap: 1rem;
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
