<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const isEditing = ref(false)
const isLoading = ref(false)
const error = ref('')
const success = ref('')

// Форма для редактирования
const editForm = ref({
  username: '',
  firstName: '',
  lastName: '',
  email: '',
})

// Инициализация формы данными пользователя
onMounted(() => {
  if (authStore.user) {
    editForm.value = {
      username: authStore.user.username || '',
      firstName: authStore.user.firstName || '',
      lastName: authStore.user.lastName || '',
      email: authStore.user.email || '',
    }
  }
})

const handleLogout = async () => {
  await authStore.logout()
  router.push('/signin')
}

const startEditing = () => {
  isEditing.value = true
  error.value = ''
  success.value = ''
}

const cancelEditing = () => {
  isEditing.value = false
  error.value = ''
  success.value = ''

  if (authStore.user) {
    editForm.value = {
      username: authStore.user.username || '',
      firstName: authStore.user.firstName || '',
      lastName: authStore.user.lastName || '',
      email: authStore.user.email || '',
    }
  }
}

const updateProfile = async () => {
  isLoading.value = true
  error.value = ''
  success.value = ''

  try {
    // Подготавливаем данные для отправки (только измененные поля)
    const updatedData: Record<string, string> = {}

    if (editForm.value.username !== authStore.user?.username) {
      updatedData.username = editForm.value.username
    }
    if (editForm.value.firstName !== authStore.user?.firstName) {
      updatedData.first_name = editForm.value.firstName
    }
    if (editForm.value.lastName !== authStore.user?.lastName) {
      updatedData.last_name = editForm.value.lastName
    }
    if (editForm.value.email !== authStore.user?.email) {
      updatedData.email = editForm.value.email
    }

    // Если есть что обновлять
    if (Object.keys(updatedData).length > 0) {
      await authStore.updateUser(updatedData)
      success.value = 'Профиль успешно обновлен'
    } else {
      success.value = 'Нет изменений для сохранения'
    }

    isEditing.value = false
  } catch (err: unknown) {
    const apiError = err as {
      response?: {
        data?: {
          username?: string[]
          email?: string[]
        }
      }
    }
    const errors = apiError.response?.data

    if (errors?.username) {
      error.value = `Логин: ${errors.username.join(', ')}`
    } else if (errors?.email) {
      error.value = `Email: ${errors.email.join(', ')}`
    } else {
      error.value = 'Ошибка при обновлении профиля'
    }
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="page">
    <div v-if="authStore.user" class="profile-info">
      <!-- Режим просмотра -->
      <div v-if="!isEditing" class="profile-view">
        <div class="avatar-container">
          <div class="avatar">
            {{ authStore.user.username?.charAt(0).toUpperCase() || '?' }}
          </div>
        </div>

        <div class="info-grid">
          <div class="info-item">
            <span class="label">Логин:</span>
            <span class="value">{{ authStore.user.username }}</span>
          </div>

          <div v-if="authStore.user.firstName" class="info-item">
            <span class="label">Имя:</span>
            <span class="value">{{ authStore.user.firstName }}</span>
          </div>

          <div v-if="authStore.user.lastName" class="info-item">
            <span class="label">Фамилия:</span>
            <span class="value">{{ authStore.user.lastName }}</span>
          </div>

          <div v-if="authStore.user.email" class="info-item">
            <span class="label">Email:</span>
            <span class="value">{{ authStore.user.email }}</span>
          </div>
        </div>

        <div class="action-buttons">
          <button @click="startEditing" class="edit-btn">Редактировать</button>
          <button @click="handleLogout" class="logout-btn">Выйти</button>
        </div>
      </div>

      <!-- Режим редактирования -->
      <div v-else class="profile-edit">
        <h2 class="edit-title">Редактирование профиля</h2>

        <form @submit.prevent="updateProfile" class="edit-form">
          <div class="form-group">
            <label for="username">Логин*</label>
            <input
              v-model="editForm.username"
              type="text"
              id="username"
              required
              placeholder="Введите логин"
            />
          </div>

          <div class="form-group">
            <label for="firstName">Имя</label>
            <input
              v-model="editForm.firstName"
              type="text"
              id="firstName"
              placeholder="Введите имя"
            />
          </div>

          <div class="form-group">
            <label for="lastName">Фамилия</label>
            <input
              v-model="editForm.lastName"
              type="text"
              id="lastName"
              placeholder="Введите фамилию"
            />
          </div>

          <div class="form-group">
            <label for="email">Email</label>
            <input v-model="editForm.email" type="email" id="email" placeholder="Введите email" />
          </div>

          <div v-if="error" class="error">{{ error }}</div>
          <div v-if="success" class="success">{{ success }}</div>

          <div class="form-actions">
            <button type="submit" class="save-btn" :disabled="isLoading">
              {{ isLoading ? 'Сохранение...' : 'Сохранить' }}
            </button>
            <button type="button" class="cancel-btn" @click="cancelEditing" :disabled="isLoading">
              Отмена
            </button>
          </div>
        </form>
      </div>
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

/* Режим просмотра */
.profile-view {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.avatar-container {
  display: flex;
  justify-content: center;
}

.avatar {
  width: 100px;
  height: 100px;
  background: var(--color-primary);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  font-weight: 500;
  color: var(--color-white);
  text-transform: uppercase;
}

.info-grid {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.info-item .label {
  font-weight: 500;
  color: var(--color-primary);
  font-size: 1rem;
}

.info-item .value {
  font-size: 1rem;
  word-break: break-word;
  text-align: right;
}

.empty-state {
  width: 100%;
  text-align: center;
  color: rgba(255, 255, 255, 0.5);
  font-style: italic;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 1rem;
}

.edit-btn {
  width: 100%;
  height: 50px;
  background: var(--color-primary);
  border-radius: 30px;
  border: none;
  color: var(--color-white);
  font-size: clamp(1rem, 3vw, 1.25rem);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.edit-btn:hover {
  opacity: 0.9;
  transform: translateY(-2px);
}

.logout-btn {
  width: 100%;
  height: 50px;
  background: var(--color-error);
  border-radius: 30px;
  border: none;
  color: var(--color-white);
  font-size: clamp(1rem, 3vw, 1.25rem);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  opacity: 0.9;
  transform: translateY(-2px);
}

/* Режим редактирования */
.profile-edit {
  width: 100%;
}

.edit-title {
  font-size: clamp(1.25rem, 4vw, 1.5rem);
  margin-bottom: 2rem;
  text-align: center;
  font-weight: 500;
  color: var(--color-white);
}

.edit-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  margin-bottom: 0.5rem;
}

.form-group label {
  display: block;
  font-size: clamp(0.875rem, 3vw, 1rem);
  font-weight: 500;
  margin-bottom: 0.5rem;
  color: var(--color-white);
}

.form-group input {
  width: 100%;
  height: 50px;
  background: var(--color-white);
  border-radius: 30px;
  border: none;
  padding: 0 1.5rem;
  font-size: clamp(0.875rem, 3vw, 1rem);
  color: var(--color-input-text);
  font-style: italic;
  box-sizing: border-box;
}

.form-group input::placeholder {
  color: var(--color-input-text);
  font-style: italic;
  opacity: 1;
}

.form-actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 1rem;
}

.save-btn {
  width: 100%;
  height: 50px;
  background: var(--color-primary);
  border-radius: 30px;
  border: none;
  color: var(--color-white);
  font-size: clamp(1rem, 3vw, 1.25rem);
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
  width: 100%;
  height: 50px;
  background: transparent;
  border: 2px solid var(--color-primary);
  border-radius: 30px;
  color: var(--color-primary);
  font-size: clamp(1rem, 3vw, 1.25rem);
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

.error {
  color: var(--color-error);
  text-align: center;
  font-size: clamp(0.875rem, 2vw, 1rem);
  margin-top: 0.5rem;
}

.success {
  color: #4caf50;
  text-align: center;
  font-size: clamp(0.875rem, 2vw, 1rem);
  margin-top: 0.5rem;
}

@media (max-width: 768px) {
  .profile-info {
    padding: 1.5rem;
    border-radius: 30px;
  }

  .avatar {
    width: 80px;
    height: 80px;
    font-size: 2.5rem;
  }

  .info-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.25rem;
  }

  .info-item .value {
    text-align: left;
  }
}

@media (max-width: 480px) {
  .page {
    padding: 1rem;
  }

  .profile-info {
    padding: 1.25rem;
  }

  .avatar {
    width: 70px;
    height: 70px;
    font-size: 2rem;
  }

  .edit-btn,
  .logout-btn,
  .save-btn,
  .cancel-btn {
    height: 45px;
    font-size: 1rem;
  }
}

@supports (-webkit-touch-callout: none) {
  .page {
    min-height: -webkit-fill-available;
  }
}
</style>
