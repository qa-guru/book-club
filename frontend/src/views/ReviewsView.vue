<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useReviewsStore } from '@/stores/reviews'
import { useRouter } from 'vue-router'

const reviewsStore = useReviewsStore()
const router = useRouter()

const currentPage = ref(1)
const pageSize = ref(10)

const totalPages = computed(() => {
  return Math.ceil(reviewsStore.pagination.count / pageSize.value)
})

const formatDate = (dateString?: string) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  })
}

const getStars = (assessment: number) => {
  return '★'.repeat(assessment) + '☆'.repeat(5 - assessment)
}

const goToPage = (page: number) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    reviewsStore.fetchReviews(page, pageSize.value)
  }
}

const goToClub = (clubId: number) => {
  router.push(`/clubs/${clubId}`)
}

onMounted(() => {
  reviewsStore.fetchReviews(currentPage.value, pageSize.value)
})
</script>

<template>
  <div class="reviews-page">
    <h1>Все отзывы</h1>

    <div v-if="reviewsStore.isLoading" class="loading">Загрузка отзывов...</div>

    <div v-else-if="reviewsStore.error" class="error">
      {{ reviewsStore.error }}
    </div>

    <div v-else-if="reviewsStore.reviews.length === 0" class="no-reviews">
      <p>Пока нет отзывов</p>
    </div>

    <div v-else class="reviews-list">
      <div
        v-for="review in reviewsStore.reviews"
        :key="review.id"
        class="review-card"
        @click="goToClub(review.club)"
      >
        <div class="review-header">
          <div class="reviewer-info">
            <span class="reviewer-avatar">
              {{ review.username?.[0] || '?' }}
            </span>
            <div class="reviewer-details">
              <span class="reviewer-name">{{ review.username || 'Пользователь' }}</span>
              <span class="club-id">Клуб #{{ review.club }}</span>
            </div>
          </div>
          <div class="review-rating">
            <span class="stars">{{ getStars(review.assessment) }}</span>
            <span class="read-pages">{{ review.readPages }} стр.</span>
          </div>
        </div>

        <div class="review-content">
          <p>{{ review.review }}</p>
        </div>

        <div class="review-footer">
          <span class="review-date">
            {{ formatDate(review.createdAt) }}
          </span>
        </div>
      </div>
    </div>

    <div v-if="reviewsStore.pagination.count > pageSize" class="pagination">
      <button
        @click="goToPage(currentPage - 1)"
        :disabled="!reviewsStore.pagination.previous"
        class="pagination-btn"
      >
        ← Назад
      </button>

      <span class="page-info"> Страница {{ currentPage }} из {{ totalPages }} </span>

      <button
        @click="goToPage(currentPage + 1)"
        :disabled="!reviewsStore.pagination.next"
        class="pagination-btn"
      >
        Вперед →
      </button>
    </div>
  </div>
</template>

<style scoped>
.reviews-page {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  padding: 1rem 1rem;
  box-sizing: border-box;
  color: var(--color-white);
}

.reviews-page h1 {
  font-size: clamp(1.5rem, 4vw, 2rem);
  margin-bottom: 2rem;
  text-align: center;
}

.loading,
.error,
.no-reviews {
  text-align: center;
  padding: 3rem;
  background: var(--color-black);
  border-radius: 50px;
}

.error {
  color: var(--color-error);
}

.no-reviews {
  color: rgba(255, 255, 255, 0.5);
  font-style: italic;
}

.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.review-card {
  background: var(--color-black);
  border-radius: 30px;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.review-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(255, 107, 0, 0.3);
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.reviewer-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.reviewer-avatar {
  width: 45px;
  height: 45px;
  background: var(--color-primary);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  font-weight: 500;
  color: var(--color-white);
  text-transform: uppercase;
}

.reviewer-details {
  display: flex;
  flex-direction: column;
}

.reviewer-name {
  font-weight: 500;
  font-size: 1rem;
}

.club-id {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.5);
}

.review-rating {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.stars {
  color: gold;
  font-size: 1.25rem;
  letter-spacing: 2px;
}

.read-pages {
  background: var(--color-primary);
  border-radius: 20px;
  padding: 0.25rem 0.75rem;
  font-size: 0.875rem;
}

.review-content {
  margin-bottom: 1rem;
  line-height: 1.6;
  white-space: pre-line;
}

.review-footer {
  display: flex;
  justify-content: flex-end;
}

.review-date {
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.875rem;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
}

.pagination-btn {
  background: var(--color-primary);
  color: var(--color-white);
  border: none;
  border-radius: 30px;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.pagination-btn:hover:not(:disabled) {
  opacity: 0.9;
  transform: translateY(-2px);
}

.pagination-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.page-info {
  font-size: 1rem;
  color: var(--color-white);
}

@media (max-width: 768px) {
  .review-card {
    padding: 1.25rem;
  }

  .review-header {
    flex-direction: column;
  }

  .review-rating {
    width: 100%;
    justify-content: space-between;
  }

  .pagination {
    flex-direction: column;
  }

  .pagination-btn {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .review-card {
    padding: 1rem;
  }

  .reviewer-avatar {
    width: 40px;
    height: 40px;
    font-size: 1rem;
  }
}
</style>
