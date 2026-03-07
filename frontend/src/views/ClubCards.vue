<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useClubsStore } from '@/stores/clubs'
import { useAuthStore } from '@/stores/auth'
import ClubFilters from '@/components/ClubFilters.vue'
import PaginationControls from '@/components/PaginationControls.vue'
import type { Club } from '@/types/clubs'

const clubsStore = useClubsStore()
const authStore = useAuthStore()
const router = useRouter()

onMounted(async () => {
  await clubsStore.fetchClubs()

  if (authStore.isAuthenticated && authStore.pendingClubJoin) {
    const clubId = authStore.pendingClubJoin
    try {
      await clubsStore.joinClub(clubId)
      router.push(`/clubs/${clubId}`)
    } catch (err) {
      console.error('Ошибка при присоединении:', err)
    } finally {
      authStore.clearPendingClubJoin()
    }
  }
})

const isMember = (club: Club) => {
  return authStore.user && club.members.includes(authStore.user.id)
}

const joinClub = async (clubId: number) => {
  if (!authStore.isAuthenticated) {
    authStore.setPendingClubJoin(clubId)
    router.push('/signin')
    return
  }

  try {
    await clubsStore.joinClub(clubId)
    router.push(`/clubs/${clubId}`)
  } catch (err) {
    console.error('Ошибка при присоединении:', err)
  }
}

const openClubPage = (clubId: number) => {
  router.push(`/clubs/${clubId}`)
}

const truncateText = (text: string, maxLength: number = 150) => {
  if (!text) return ''
  if (text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}
</script>

<template>
  <div class="clubs-page">
    <ClubFilters />

    <div v-if="clubsStore.error" class="error">{{ clubsStore.error }}</div>
    <div v-else-if="clubsStore.clubs.length === 0" class="no-results">Клубы не найдены</div>

    <div v-else class="clubs-list">
      <div v-for="club in clubsStore.clubs" :key="club.id" class="club-card">
        <div class="club-header">
          <h2>{{ club.bookTitle }}</h2>
          <span class="year">{{ club.publicationYear }}</span>
        </div>

        <p class="authors">{{ club.bookAuthors }}</p>

        <p class="description">{{ truncateText(club.description) }}</p>

        <div class="club-footer">
          <button
            v-if="!isMember(club)"
            @click="joinClub(club.id)"
            class="join-btn"
            :class="{ 'btn-loading': clubsStore.isLoading }"
            :disabled="clubsStore.isLoading"
          >
            {{ clubsStore.isLoading ? 'Присоединение...' : 'Присоединиться' }}
          </button>

          <button
            v-if="authStore.isAuthenticated && isMember(club)"
            @click="openClubPage(club.id)"
            class="open-btn"
          >
            Открыть страницу
          </button>
        </div>
      </div>
    </div>
    <PaginationControls v-if="clubsStore.clubs.length > 0" />
  </div>
</template>

<style scoped>
.clubs-page {
  width: 100%;
  padding: var(--space-4);
  box-sizing: border-box;
}

.clubs-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--space-6);
  width: 100%;
  max-width: 1200px;
  margin: var(--space-8) 0;
}

.club-card {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  padding: var(--space-8);
  color: var(--color-text-inverse);
  display: flex;
  flex-direction: column;
  transition: transform var(--duration-normal) var(--ease-out), box-shadow var(--duration-normal) var(--ease-out);
}

.club-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.club-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--space-4);
  gap: var(--space-3);
}

.club-header h2 {
  font-family: var(--font-heading);
  font-size: clamp(var(--text-xl), 3vw, var(--text-2xl));
  font-weight: var(--weight-medium);
  margin: 0;
  flex: 1;
  line-height: var(--leading-tight);
}

.year {
  background: var(--color-primary);
  color: var(--color-text-inverse);
  border-radius: var(--radius-md);
  padding: var(--space-2) var(--space-3);
  font-size: var(--text-sm);
  font-weight: var(--weight-medium);
  flex-shrink: 0;
}

.authors {
  font-size: clamp(var(--text-sm), 2vw, var(--text-base));
  color: var(--color-text-muted);
  margin-bottom: var(--space-4);
  font-style: italic;
}

.description {
  font-size: clamp(var(--text-sm), 2vw, var(--text-base));
  line-height: var(--leading-relaxed);
  margin-bottom: var(--space-6);
  flex: 1;
  color: var(--color-text-muted);
}

.club-footer {
  display: flex;
  justify-content: center;
  margin-top: auto;
}

.join-btn,
.open-btn {
  width: 100%;
  min-height: 48px;
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-pill);
  border: none;
  font-family: var(--font-body);
  font-size: clamp(var(--text-base), 2vw, var(--text-lg));
  font-weight: var(--weight-medium);
  cursor: pointer;
  transition: background-color var(--duration-normal) var(--ease-out), transform var(--duration-fast) var(--ease-out);
}

.join-btn {
  background: var(--color-primary);
  color: var(--color-text-inverse);
}

.join-btn:hover:not(:disabled) {
  background: var(--color-primary-hover);
  transform: translateY(-2px);
}

.join-btn:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

.join-btn:disabled {
  cursor: not-allowed;
  opacity: 0.85;
}

.open-btn {
  background: var(--color-input-bg);
  color: var(--color-text);
}

.open-btn:hover {
  background: rgba(245, 240, 232, 0.95);
  transform: translateY(-2px);
}

.open-btn:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

.error {
  color: var(--color-error);
  font-weight: var(--weight-medium);
  padding: var(--space-4);
  text-align: center;
}

.no-results {
  background: var(--color-surface);
  color: var(--color-text-inverse);
  padding: var(--space-6);
  border-radius: var(--radius-lg);
  text-align: center;
  margin-top: var(--space-6);
  font-size: clamp(var(--text-base), 2vw, var(--text-lg));
  max-width: 360px;
  margin-left: auto;
  margin-right: auto;
}

@media (max-width: 768px) {
  .clubs-list {
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    margin-top: var(--space-6);
  }

  .club-card {
    padding: var(--space-6);
    border-radius: var(--radius-md);
  }

  .no-results {
    padding: var(--space-6);
  }
}

@media (max-width: 480px) {
  .clubs-list {
    grid-template-columns: 1fr;
  }

  .club-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .year {
    margin-top: var(--space-2);
  }

  .no-results {
    padding: var(--space-4);
  }
}
</style>
