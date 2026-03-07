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
  padding: var(--space-4);
  box-sizing: border-box;
  color: var(--color-text-inverse);
}

.profile-info {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  padding: var(--space-10);
  box-sizing: border-box;
  box-shadow: var(--shadow-md);
}

/* Режим просмотра */
.profile-view {
  display: flex;
  flex-direction: column;
  gap: var(--space-8);
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
  font-family: var(--font-heading);
  font-size: 3rem;
  font-weight: var(--weight-medium);
  color: var(--color-text-inverse);
  text-transform: uppercase;
}

.info-grid {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-2) 0;
  border-bottom: 1px solid rgba(245, 240, 232, 0.12);
}

.info-item .label {
  font-weight: var(--weight-medium);
  color: var(--color-primary);
  font-size: var(--text-base);
}

.info-item .value {
  font-size: var(--text-base);
  word-break: break-word;
  text-align: right;
}

.empty-state {
  width: 100%;
  text-align: center;
  color: var(--color-text-muted);
  font-style: italic;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  margin-top: var(--space-4);
}

.edit-btn {
  width: 100%;
  min-height: 48px;
  background: var(--color-primary);
  border-radius: var(--radius-pill);
  border: none;
  color: var(--color-text-inverse);
  font-family: var(--font-body);
  font-size: clamp(var(--text-base), 3vw, var(--text-lg));
  font-weight: var(--weight-medium);
  cursor: pointer;
  transition: background-color var(--duration-normal) var(--ease-out), transform var(--duration-fast) var(--ease-out);
}

.edit-btn:hover {
  background: var(--color-primary-hover);
  transform: translateY(-2px);
}

.edit-btn:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

.logout-btn {
  width: 100%;
  min-height: 48px;
  background: var(--color-error);
  border-radius: var(--radius-pill);
  border: none;
  color: var(--color-text-inverse);
  font-family: var(--font-body);
  font-size: clamp(var(--text-base), 3vw, var(--text-lg));
  font-weight: var(--weight-medium);
  cursor: pointer;
  transition: background-color var(--duration-normal) var(--ease-out), transform var(--duration-fast) var(--ease-out);
}

.logout-btn:hover {
  background: var(--color-error-hover);
  transform: translateY(-2px);
}

.logout-btn:focus-visible {
  outline: 2px solid var(--color-error);
  outline-offset: 2px;
}

/* Режим редактирования */
.profile-edit {
  width: 100%;
}

.edit-title {
  font-family: var(--font-heading);
  font-size: clamp(var(--text-xl), 4vw, var(--text-2xl));
  margin-bottom: var(--space-8);
  text-align: center;
  font-weight: var(--weight-medium);
  color: var(--color-text-inverse);
}

.edit-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

.form-group {
  margin-bottom: var(--space-2);
}

.form-group label {
  display: block;
  font-size: clamp(var(--text-sm), 3vw, var(--text-base));
  font-weight: var(--weight-medium);
  margin-bottom: var(--space-2);
  color: var(--color-text-inverse);
}

.form-group input {
  width: 100%;
  min-height: 48px;
  background: var(--color-input-bg);
  border-radius: var(--radius-pill);
  border: 1px solid var(--color-input-border);
  padding: 0 var(--space-6);
  font-family: var(--font-body);
  font-size: clamp(var(--text-sm), 3vw, var(--text-base));
  color: var(--color-input-text);
  box-sizing: border-box;
  transition: border-color var(--duration-fast) var(--ease-out), box-shadow var(--duration-fast) var(--ease-out);
}

.form-group input::placeholder {
  color: var(--color-input-placeholder);
}

.form-group input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(var(--color-primary-rgb), 0.2);
}

.form-actions {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  margin-top: var(--space-4);
}

.save-btn {
  width: 100%;
  min-height: 48px;
  background: var(--color-primary);
  border-radius: var(--radius-pill);
  border: none;
  color: var(--color-text-inverse);
  font-family: var(--font-body);
  font-size: clamp(var(--text-base), 3vw, var(--text-lg));
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
  width: 100%;
  min-height: 48px;
  background: transparent;
  border: 2px solid var(--color-primary);
  border-radius: var(--radius-pill);
  color: var(--color-primary);
  font-family: var(--font-body);
  font-size: clamp(var(--text-base), 3vw, var(--text-lg));
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

.error {
  color: var(--color-error);
  text-align: center;
  font-size: var(--text-sm);
  margin-top: var(--space-2);
  font-weight: var(--weight-medium);
}

.success {
  color: var(--color-success);
  text-align: center;
  font-size: var(--text-sm);
  margin-top: var(--space-2);
}

@media (max-width: 768px) {
  .profile-info {
    padding: var(--space-6);
    border-radius: var(--radius-md);
  }

  .avatar {
    width: 80px;
    height: 80px;
    font-size: 2.5rem;
  }

  .info-item {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--space-1);
  }

  .info-item .value {
    text-align: left;
  }
}

@media (max-width: 480px) {
  .page {
    padding: var(--space-4);
  }

  .profile-info {
    padding: var(--space-5);
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
    min-height: 44px;
    font-size: var(--text-base);
  }
}

@supports (-webkit-touch-callout: none) {
  .page {
    min-height: -webkit-fill-available;
  }
}
</style>
