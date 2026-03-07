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
            {{ formatDate(review.created) }}
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
  padding: var(--space-4);
  box-sizing: border-box;
  color: var(--color-text-inverse);
}

.reviews-page h1 {
  font-family: var(--font-heading);
  font-size: clamp(var(--text-2xl), 4vw, var(--text-3xl));
  margin-bottom: var(--space-8);
  text-align: center;
  color: var(--color-text);
}

.loading,
.error,
.no-reviews {
  text-align: center;
  padding: var(--space-12);
  background: var(--color-surface);
  border-radius: var(--radius-lg);
}

.error {
  color: var(--color-error);
  font-weight: var(--weight-medium);
}

.no-reviews {
  color: var(--color-text-muted);
  font-style: italic;
}

.reviews-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.review-card {
  background: var(--color-surface);
  border-radius: var(--radius-md);
  padding: var(--space-6);
  cursor: pointer;
  transition: transform var(--duration-normal) var(--ease-out), box-shadow var(--duration-normal) var(--ease-out);
}

.review-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--space-4);
  flex-wrap: wrap;
  gap: var(--space-4);
}

.reviewer-info {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.reviewer-avatar {
  width: 48px;
  height: 48px;
  background: var(--color-primary);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--text-lg);
  font-weight: var(--weight-medium);
  color: var(--color-text-inverse);
  text-transform: uppercase;
}

.reviewer-details {
  display: flex;
  flex-direction: column;
}

.reviewer-name {
  font-weight: var(--weight-medium);
  font-size: var(--text-base);
}

.club-id {
  font-size: var(--text-sm);
  color: var(--color-text-muted);
}

.review-rating {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.stars {
  color: var(--color-primary);
  font-size: var(--text-lg);
  letter-spacing: 2px;
}

.read-pages {
  background: var(--color-primary);
  border-radius: var(--radius-md);
  padding: var(--space-2) var(--space-3);
  font-size: var(--text-sm);
  color: var(--color-text-inverse);
}

.review-content {
  margin-bottom: var(--space-4);
  line-height: var(--leading-relaxed);
  white-space: pre-line;
}

.review-footer {
  display: flex;
  justify-content: flex-end;
}

.review-date {
  color: var(--color-text-muted);
  font-size: var(--text-sm);
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: var(--space-4);
  margin-top: var(--space-8);
}

.pagination-btn {
  background: var(--color-primary);
  color: var(--color-text-inverse);
  border: none;
  border-radius: var(--radius-pill);
  padding: var(--space-3) var(--space-6);
  font-family: var(--font-body);
  font-size: var(--text-base);
  font-weight: var(--weight-medium);
  cursor: pointer;
  transition: background-color var(--duration-normal) var(--ease-out), transform var(--duration-fast) var(--ease-out);
}

.pagination-btn:hover:not(:disabled) {
  background: var(--color-primary-hover);
  transform: translateY(-2px);
}

.pagination-btn:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

.pagination-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.page-info {
  font-size: var(--text-base);
  color: var(--color-text);
}

@media (max-width: 768px) {
  .review-card {
    padding: var(--space-5);
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
    padding: var(--space-4);
  }

  .reviewer-avatar {
    width: 40px;
    height: 40px;
    font-size: var(--text-base);
  }
}
</style>
