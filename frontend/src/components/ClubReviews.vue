<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useReviewsStore } from '@/stores/reviews'
import { useAuthStore } from '@/stores/auth'
import type { BookReview } from '@/types/clubs'
import type { User } from '@/types/users'

const props = defineProps<{
  clubId: number
  clubMembers: number[]
  clubOwner: number
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
  } catch (err) {
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
  } catch (err) {
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
  } catch (err) {
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
            {{ formatDate(review.createdAt) }}
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
  margin-top: 3rem;
  border-top: 2px solid rgba(255, 255, 255, 0.1);
  padding-top: 2rem;
}

.reviews-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.reviews-header h2 {
  font-size: clamp(1.25rem, 3vw, 1.5rem);
  margin: 0;
  color: var(--color-white);
}

.add-review-btn {
  background: var(--color-primary);
  color: var(--color-white);
  border: none;
  border-radius: 30px;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.add-review-btn:hover {
  opacity: 0.9;
  transform: translateY(-2px);
}

.review-form {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 30px;
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.review-form h3 {
  margin: 0 0 1.5rem 0;
  color: var(--color-white);
  font-size: 1.25rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: var(--color-white);
  font-weight: 500;
}

.rating-input {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.rating-input select {
  width: 150px;
  height: 45px;
  background: var(--color-white);
  border: none;
  border-radius: 30px;
  padding: 0 1.5rem;
  font-size: 1rem;
  color: var(--colore-input-text);
  cursor: pointer;
}

.stars-preview {
  color: gold;
  font-size: 1.25rem;
  letter-spacing: 2px;
}

.form-group input {
  width: 100%;
  height: 45px;
  background: var(--color-white);
  border: none;
  border-radius: 30px;
  padding: 0 1.5rem;
  font-size: 1rem;
  color: var(--colore-input-text);
  box-sizing: border-box;
}

.form-group textarea {
  width: 100%;
  background: var(--color-white);
  border: none;
  border-radius: 30px;
  padding: 1rem 1.5rem;
  font-size: 1rem;
  color: var(--colore-input-text);
  resize: vertical;
  box-sizing: border-box;
  font-family: inherit;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.save-btn {
  flex: 1;
  height: 45px;
  background: var(--color-primary);
  border: none;
  border-radius: 30px;
  color: var(--color-white);
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.save-btn:hover:not(:disabled) {
  opacity: 0.9;
  transform: translateY(-2px);
}

.save-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.cancel-btn {
  flex: 1;
  height: 45px;
  background: transparent;
  border: 2px solid var(--color-primary);
  border-radius: 30px;
  color: var(--color-primary);
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cancel-btn:hover:not(:disabled) {
  background: var(--color-primary);
  color: var(--color-white);
  transform: translateY(-2px);
}

.cancel-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Список отзывов */
.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.review-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 30px;
  padding: 1.5rem;
  transition: transform 0.3s ease;
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
  width: 40px;
  height: 40px;
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

.reviewer-name {
  font-weight: 500;
  color: var(--color-white);
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
  color: var(--color-white);
}

.review-content {
  margin-bottom: 1rem;
  line-height: 1.6;
  color: var(--color-white);
  white-space: pre-line;
}

.review-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.review-date {
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.875rem;
}

.review-actions {
  display: flex;
  gap: 0.5rem;
}

.edit-review-btn,
.delete-review-btn {
  padding: 0.4rem 1rem;
  border: none;
  border-radius: 20px;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.edit-review-btn {
  background: var(--color-white);
  color: var(--color-black);
}

.delete-review-btn {
  background: var(--color-error);
  color: var(--color-white);
}

.edit-review-btn:hover,
.delete-review-btn:hover {
  opacity: 0.9;
  transform: translateY(-2px);
}

.no-reviews {
  text-align: center;
  color: rgba(255, 255, 255, 0.5);
  font-style: italic;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 30px;
}

.loading {
  text-align: center;
  color: var(--color-white);
  padding: 2rem;
}

.error {
  color: var(--color-error);
  text-align: center;
  margin-bottom: 1rem;
}

.success {
  color: #4caf50;
  text-align: center;
  margin-bottom: 1rem;
}

@media (max-width: 768px) {
  .reviews-section {
    margin-top: 2rem;
    padding-top: 1.5rem;
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
    padding: 1rem;
  }

  .reviewer-avatar {
    width: 35px;
    height: 35px;
    font-size: 1rem;
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
