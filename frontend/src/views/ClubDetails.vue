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
  padding: var(--space-4);
  box-sizing: border-box;
}

.loading {
  text-align: center;
  font-size: var(--text-lg);
  padding: var(--space-8);
  color: var(--color-text-muted);
  background: var(--color-surface);
  border-radius: var(--radius-lg);
}

.error {
  text-align: center;
  font-size: var(--text-lg);
  padding: var(--space-8);
  color: var(--color-error);
  font-weight: var(--weight-medium);
  background: var(--color-surface);
  border-radius: var(--radius-lg);
}

.club-content {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  padding: var(--space-10);
  color: var(--color-text-inverse);
  box-shadow: var(--shadow-md);
}

.club-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--space-6);
  flex-wrap: wrap;
  gap: var(--space-3);
}

.club-header h1 {
  font-family: var(--font-heading);
  font-size: clamp(var(--text-2xl), 4vw, var(--text-3xl));
  margin: 0;
  font-weight: var(--weight-medium);
  flex: 1;
  min-width: 60%;
  line-height: var(--leading-tight);
}

.year {
  background: var(--color-primary);
  color: var(--color-text-inverse);
  border-radius: var(--radius-md);
  padding: var(--space-2) var(--space-4);
  font-size: clamp(var(--text-sm), 2vw, var(--text-base));
  font-weight: var(--weight-medium);
  flex-shrink: 0;
}

.authors {
  font-size: clamp(var(--text-base), 2.5vw, var(--text-lg));
  color: var(--color-text-muted);
  margin-bottom: var(--space-6);
  font-style: italic;
}

.description {
  font-size: clamp(var(--text-base), 2.5vw, var(--text-lg));
  line-height: var(--leading-relaxed);
  margin-bottom: var(--space-10);
  white-space: pre-line;
}

.club-stats {
  display: flex;
  gap: var(--space-8);
  margin: var(--space-8) 0;
  padding: var(--space-6) 0;
  border-top: 1px solid rgba(245, 240, 232, 0.12);
  border-bottom: 1px solid rgba(245, 240, 232, 0.12);
}

.stat-item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.stat-label {
  color: var(--color-text-muted);
  font-size: var(--text-base);
}

.stat-value {
  font-size: var(--text-lg);
  font-weight: var(--weight-medium);
  color: var(--color-primary);
}

.club-actions {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-4);
  margin-top: var(--space-8);
}

.telegram-btn,
.join-btn,
.leave-btn,
.edit-btn {
  min-height: 48px;
  border-radius: var(--radius-pill);
  border: none;
  font-family: var(--font-body);
  font-size: clamp(var(--text-base), 2vw, var(--text-lg));
  font-weight: var(--weight-medium);
  cursor: pointer;
  transition: background-color var(--duration-normal) var(--ease-out), transform var(--duration-fast) var(--ease-out);
  padding: 0 var(--space-6);
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
  color: var(--color-text-inverse);
}

.telegram-btn:hover {
  background: #0077b5;
  transform: translateY(-2px);
}

.join-btn {
  background: var(--color-primary);
  color: var(--color-text-inverse);
}

.join-btn:hover {
  background: var(--color-primary-hover);
  transform: translateY(-2px);
}

.leave-btn {
  background: var(--color-error);
  color: var(--color-text-inverse);
}

.leave-btn:hover {
  background: var(--color-error-hover);
  transform: translateY(-2px);
}

.edit-btn {
  background: var(--color-input-bg);
  color: var(--color-text);
}

.edit-btn:hover {
  background: rgba(245, 240, 232, 0.95);
  transform: translateY(-2px);
}

.telegram-btn:focus-visible,
.join-btn:focus-visible,
.leave-btn:focus-visible,
.edit-btn:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

@media (max-width: 768px) {
  .club-content {
    padding: var(--space-6);
    border-radius: var(--radius-md);
  }

  .club-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .year {
    margin-top: var(--space-3);
  }

  .club-stats {
    flex-direction: column;
    gap: var(--space-4);
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
    padding: var(--space-4);
  }

  .club-content {
    padding: var(--space-5);
  }

  .telegram-btn,
  .join-btn,
  .leave-btn,
  .edit-btn {
    min-height: 44px;
    padding: 0 var(--space-4);
  }
}
</style>
