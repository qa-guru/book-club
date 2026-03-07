<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useReviewsStore } from '@/stores/reviews'
import { useAuthStore } from '@/stores/auth'
import type { BookReview } from '@/types/clubs'

const props = defineProps<{
  clubId: number
  clubMembers: number[]
  clubOwner?: number
}>()

const reviewsStore = useReviewsStore()
const authStore = useAuthStore()

const isCreating = ref(false)
const isEditing = ref(false)
const editingReviewId = ref<number | null>(null)
const isLoading = ref(false)
const error = ref('')
const success = ref('')

const reviewForm = ref({
  review: '',
  assessment: 5,
  readPages: 0,
})

const userReview = ref<BookReview | null>(null)

const clubReviews = computed(() => {
  return reviewsStore.getClubReviews(props.clubId)
})

const canReview = computed(() => {
  if (!authStore.isAuthenticated || !authStore.user) return false
  return props.clubMembers.includes(authStore.user.id) && !userReview.value
})

const canEditReview = (review: BookReview) => {
  return authStore.user?.id === review.user.id
}

const loadReviews = async () => {
  await reviewsStore.fetchClubReviews(props.clubId)

  if (authStore.user) {
    userReview.value = clubReviews.value.find((r) => r.user.id === authStore.user?.id) || null
  }
}

const startCreate = () => {
  isCreating.value = true
  isEditing.value = false
  editingReviewId.value = null
  reviewForm.value = {
    review: '',
    assessment: 5,
    readPages: 0,
  }
  error.value = ''
  success.value = ''
}

const startEdit = (review: BookReview) => {
  isEditing.value = true
  isCreating.value = false
  editingReviewId.value = review.id
  reviewForm.value = {
    review: review.review,
    assessment: review.assessment,
    readPages: review.readPages ?? 0,
  }
  error.value = ''
  success.value = ''
}

const cancelForm = () => {
  isCreating.value = false
  isEditing.value = false
  editingReviewId.value = null
  error.value = ''
  success.value = ''
}

const createReview = async () => {
  if (!reviewForm.value.review.trim()) {
    error.value = 'Пожалуйста, напишите отзыв'
    return
  }

  if (reviewForm.value.readPages < 0) {
    error.value = 'Количество прочитанных страниц не может быть отрицательным'
    return
  }

  isLoading.value = true
  error.value = ''
  success.value = ''

  try {
    const newReview = await reviewsStore.createReview(props.clubId, {
      review: reviewForm.value.review,
      assessment: reviewForm.value.assessment,
      readPages: reviewForm.value.readPages,
    })

    userReview.value = newReview
    success.value = 'Отзыв успешно создан'
    isCreating.value = false
  } catch {
    error.value = 'Ошибка при создании отзыва'
  } finally {
    isLoading.value = false
  }
}

const updateReview = async () => {
  if (!editingReviewId.value) return

  if (!reviewForm.value.review.trim()) {
    error.value = 'Пожалуйста, напишите отзыв'
    return
  }

  isLoading.value = true
  error.value = ''
  success.value = ''

  try {
    const updatedReview = await reviewsStore.updateReview(editingReviewId.value, {
      review: reviewForm.value.review,
      assessment: reviewForm.value.assessment,
      readPages: reviewForm.value.readPages,
    })

    if (userReview.value?.id === editingReviewId.value) {
      userReview.value = updatedReview
    }

    success.value = 'Отзыв успешно обновлен'
    isEditing.value = false
    editingReviewId.value = null
  } catch {
    error.value = 'Ошибка при обновлении отзыва'
  } finally {
    isLoading.value = false
  }
}

const deleteReview = async (reviewId: number) => {
  if (!confirm('Вы уверены, что хотите удалить этот отзыв?')) return

  try {
    await reviewsStore.deleteReview(reviewId, props.clubId)

    if (userReview.value?.id === reviewId) {
      userReview.value = null
    }

    success.value = 'Отзыв успешно удален'
  } catch {
    error.value = 'Ошибка при удалении отзыва'
  }
}

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

onMounted(() => {
  loadReviews()
})
</script>

<template>
  <div class="reviews-section">
    <div class="reviews-header">
      <h2>Отзывы участников</h2>

      <button
        v-if="canReview && !isCreating && !isEditing && !userReview"
        @click="startCreate"
        class="add-review-btn"
      >
        Написать отзыв
      </button>
    </div>

    <div v-if="isCreating || isEditing" class="review-form">
      <h3>{{ isCreating ? 'Новый отзыв' : 'Редактирование отзыва' }}</h3>

      <form @submit.prevent="isCreating ? createReview() : updateReview()">
        <div class="form-group">
          <label for="assessment">Оценка</label>
          <!-- <div class="rating-input">
            <select v-model="reviewForm.assessment" id="assessment">
              <option v-for="n in 5" :key="n" :value="n">
                {{ n }} звезд{{ n === 1 ? 'а' : n < 5 ? 'ы' : '' }}
              </option>
            </select>
            <span class="stars-preview">{{ getStars(reviewForm.assessment) }}</span>
          </div> -->
          <div class="rating-input">
    <input
      v-model.number="reviewForm.assessment"
      type="number"
      id="assessment"
      min="1"
      max="5"
      placeholder="Оценка от 1 до 5"
    />
  </div>
        </div>

        <div class="form-group">
          <label for="readPages">Прочитано страниц</label>
          <input
            v-model.number="reviewForm.readPages"
            type="number"
            id="readPages"
            min="0"
            placeholder="Сколько страниц прочитали"
          />
        </div>

        <div class="form-group">
          <label for="review">Ваш отзыв</label>
          <textarea
            v-model="reviewForm.review"
            id="review"
            rows="5"
            placeholder="Поделитесь своими впечатлениями о книге..."
            required
          ></textarea>
        </div>

        <div v-if="error" class="error">{{ error }}</div>
        <div v-if="success" class="success">{{ success }}</div>

        <div class="form-actions">
          <button type="submit" class="save-btn" :disabled="isLoading">
            {{ isLoading ? 'Сохранение...' : isCreating ? 'Опубликовать' : 'Сохранить' }}
          </button>
          <button type="button" class="cancel-btn" @click="cancelForm" :disabled="isLoading">
            Отмена
          </button>
        </div>
      </form>
    </div>

    <div v-if="clubReviews.length > 0" class="reviews-list">
      <div
        v-for="review in clubReviews"
        :key="review.id"
        class="review-card"
        :class="{ 'user-review': review.user.id === authStore.user?.id }"
      >
        <div class="review-header">
          <div class="reviewer-info">
            <span class="reviewer-avatar">
              {{ review.user.username?.[0] || '?' }}
            </span>
            <span class="reviewer-name">
              {{ review.user.username || 'Пользователь' }}
            </span>
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

          <div v-if="canEditReview(review) && !isEditing && !isCreating" class="review-actions">
            <button @click="startEdit(review)" class="edit-review-btn">Редактировать</button>
            <button @click="deleteReview(review.id)" class="delete-review-btn">Удалить</button>
          </div>
        </div>
      </div>
    </div>

    <div v-else-if="!isCreating && !isLoading" class="no-reviews">
      <p>Пока нет отзывов. Будьте первым, кто поделится впечатлениями!</p>
    </div>

    <div v-if="reviewsStore.isLoading && !isLoading" class="loading">Загрузка отзывов...</div>
  </div>
</template>

<style scoped>
.reviews-section {
  margin-top: var(--space-12);
  border-top: 2px solid rgba(245, 240, 232, 0.12);
  padding-top: var(--space-8);
}

.reviews-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-8);
  flex-wrap: wrap;
  gap: var(--space-4);
}

.reviews-header h2 {
  font-family: var(--font-heading);
  font-size: clamp(var(--text-xl), 3vw, var(--text-2xl));
  margin: 0;
  color: var(--color-text-inverse);
}

.add-review-btn {
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
  white-space: nowrap;
}

.add-review-btn:hover {
  background: var(--color-primary-hover);
  transform: translateY(-2px);
}

.add-review-btn:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

.review-form {
  background: rgba(245, 240, 232, 0.06);
  border-radius: var(--radius-md);
  padding: var(--space-6);
  margin-bottom: var(--space-8);
}

.review-form h3 {
  margin: 0 0 var(--space-6) 0;
  color: var(--color-text-inverse);
  font-family: var(--font-heading);
  font-size: var(--text-xl);
}

.form-group {
  margin-bottom: var(--space-6);
}

.form-group label {
  display: block;
  margin-bottom: var(--space-2);
  color: var(--color-text-inverse);
  font-weight: var(--weight-medium);
}

.rating-input {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.rating-input select {
  width: 150px;
  min-height: 44px;
  background: var(--color-input-bg);
  border: 1px solid var(--color-input-border);
  border-radius: var(--radius-md);
  padding: 0 var(--space-6);
  font-family: var(--font-body);
  font-size: var(--text-base);
  color: var(--color-input-text);
  cursor: pointer;
}

.stars-preview {
  color: var(--color-primary);
  font-size: var(--text-lg);
  letter-spacing: 2px;
}

.form-group input {
  width: 100%;
  min-height: 44px;
  background: var(--color-input-bg);
  border: 1px solid var(--color-input-border);
  border-radius: var(--radius-md);
  padding: 0 var(--space-6);
  font-family: var(--font-body);
  font-size: var(--text-base);
  color: var(--color-input-text);
  box-sizing: border-box;
  transition: border-color var(--duration-fast) var(--ease-out);
}

.form-group input:focus {
  outline: none;
  border-color: var(--color-primary);
}

.form-group textarea {
  width: 100%;
  background: var(--color-input-bg);
  border: 1px solid var(--color-input-border);
  border-radius: var(--radius-md);
  padding: var(--space-4) var(--space-6);
  font-family: var(--font-body);
  font-size: var(--text-base);
  color: var(--color-input-text);
  resize: vertical;
  box-sizing: border-box;
  transition: border-color var(--duration-fast) var(--ease-out);
}

.form-group textarea:focus {
  outline: none;
  border-color: var(--color-primary);
}

.form-actions {
  display: flex;
  gap: var(--space-4);
  margin-top: var(--space-4);
}

.save-btn {
  flex: 1;
  min-height: 44px;
  background: var(--color-primary);
  border: none;
  border-radius: var(--radius-pill);
  color: var(--color-text-inverse);
  font-family: var(--font-body);
  font-size: var(--text-base);
  font-weight: var(--weight-medium);
  cursor: pointer;
  transition: background-color var(--duration-normal) var(--ease-out), transform var(--duration-fast) var(--ease-out);
}

.save-btn:hover:not(:disabled) {
  background: var(--color-primary-hover);
  transform: translateY(-2px);
}

.save-btn:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

.save-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.cancel-btn {
  flex: 1;
  min-height: 44px;
  background: transparent;
  border: 2px solid var(--color-primary);
  border-radius: var(--radius-pill);
  color: var(--color-primary);
  font-family: var(--font-body);
  font-size: var(--text-base);
  font-weight: var(--weight-medium);
  cursor: pointer;
  transition: background-color var(--duration-normal) var(--ease-out), color var(--duration-normal), transform var(--duration-fast) var(--ease-out);
}

.cancel-btn:hover:not(:disabled) {
  background: var(--color-primary);
  color: var(--color-text-inverse);
  transform: translateY(-2px);
}

.cancel-btn:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

.cancel-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Список отзывов */
.reviews-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.review-card {
  background: rgba(245, 240, 232, 0.06);
  border-radius: var(--radius-md);
  padding: var(--space-6);
  transition: transform var(--duration-normal) var(--ease-out);
}

.review-card:hover {
  transform: translateY(-2px);
}

.review-card.user-review {
  border: 2px solid var(--color-primary);
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
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
  width: 40px;
  height: 40px;
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

.reviewer-name {
  font-weight: var(--weight-medium);
  color: var(--color-text-inverse);
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
  color: var(--color-text-inverse);
  white-space: pre-line;
}

.review-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: var(--space-4);
}

.review-date {
  color: var(--color-text-muted);
  font-size: var(--text-sm);
}

.review-actions {
  display: flex;
  gap: var(--space-2);
}

.edit-review-btn,
.delete-review-btn {
  padding: var(--space-2) var(--space-4);
  border: none;
  border-radius: var(--radius-md);
  font-family: var(--font-body);
  font-size: var(--text-sm);
  font-weight: var(--weight-medium);
  cursor: pointer;
  transition: background-color var(--duration-fast) var(--ease-out), transform var(--duration-fast) var(--ease-out);
}

.edit-review-btn {
  background: var(--color-input-bg);
  color: var(--color-text);
}

.edit-review-btn:hover {
  background: rgba(245, 240, 232, 0.9);
  transform: translateY(-1px);
}

.edit-review-btn:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

.delete-review-btn {
  background: var(--color-error);
  color: var(--color-text-inverse);
}

.delete-review-btn:hover {
  background: var(--color-error-hover);
  transform: translateY(-1px);
}

.delete-review-btn:focus-visible {
  outline: 2px solid var(--color-error);
  outline-offset: 2px;
}

.no-reviews {
  text-align: center;
  color: var(--color-text-muted);
  font-style: italic;
  padding: var(--space-8);
  background: rgba(245, 240, 232, 0.06);
  border-radius: var(--radius-md);
}

.loading {
  text-align: center;
  color: var(--color-text-muted);
  padding: var(--space-8);
}

.error {
  color: var(--color-error);
  text-align: center;
  margin-bottom: var(--space-4);
  font-weight: var(--weight-medium);
}

.success {
  color: var(--color-success);
  text-align: center;
  margin-bottom: var(--space-4);
}

@media (max-width: 768px) {
  .reviews-section {
    margin-top: var(--space-8);
    padding-top: var(--space-6);
  }

  .review-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .review-rating {
    width: 100%;
    justify-content: space-between;
  }

  .form-actions {
    flex-direction: column;
  }

  .rating-input {
    flex-direction: column;
    align-items: flex-start;
  }

  .rating-input select {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .review-card {
    padding: var(--space-4);
  }

  .reviewer-avatar {
    width: 36px;
    height: 36px;
    font-size: var(--text-base);
  }

  .review-footer {
    flex-direction: column;
    align-items: flex-start;
  }

  .review-actions {
    width: 100%;
  }

  .edit-review-btn,
  .delete-review-btn {
    flex: 1;
    text-align: center;
  }
}
</style>
