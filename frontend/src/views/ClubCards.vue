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
  padding: 1rem 1rem;
  box-sizing: border-box;
}

.clubs-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  width: 100%;
  max-width: 1200px;
  margin: 2rem 0;
}

.club-card {
  background: var(--color-black);
  border-radius: 50px;
  padding: 2rem;
  color: var(--color-white);
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
}

.club-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}

.club-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.club-header h2 {
  font-size: clamp(1.25rem, 3vw, 1.5rem);
  font-weight: 500;
  margin: 0;
  flex: 1;
}

.year {
  background: var(--color-primary);
  border-radius: 20px;
  padding: 0.25rem 0.75rem;
  font-size: 0.875rem;
  margin-left: 1rem;
}

.authors {
  font-size: clamp(0.875rem, 2vw, 1rem);
  color: var(--color-text-secondary);
  margin-bottom: 1rem;
  font-style: italic;
}

.description {
  font-size: clamp(0.875rem, 2vw, 1rem);
  margin-bottom: 1.5rem;
  flex: 1;
}

.club-footer {
  display: flex;
  justify-content: center;
}

.join-btn,
.open-btn {
  width: 100%;
  height: 50px;
  border-radius: 30px;
  border: none;
  font-size: clamp(1rem, 2vw, 1.125rem);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.join-btn {
  background: var(--color-primary);
  color: var(--color-white);
}

.open-btn {
  background: var(--color-white);
  color: var(--color-black);
}

.join-btn:hover,
.open-btn:hover {
  opacity: 0.9;
  transform: translateY(-2px);
}

.error {
  color: var(--color-error);
}

.no-results {
  background: var(--color-black);
  color: var(--color-white);
  padding: 1rem;
  border-radius: 50px;
  text-align: center;
  margin-top: 1rem;
  font-size: clamp(1rem, 2vw, 1.125rem);
  max-width: 300px;
  margin-left: auto;
  margin-right: auto;
}

@media (max-width: 768px) {
  .no-results {
    padding: 1.5rem;
    border-radius: 30px;
  }
}

@media (max-width: 480px) {
  .no-results {
    padding: 1rem;
    border-radius: 20px;
  }
}

@media (max-width: 768px) {
  .clubs-list {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  }

  .club-card {
    padding: 1.5rem;
    border-radius: 30px;
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
    margin-left: 0;
    margin-top: 0.5rem;
  }
}
</style>
