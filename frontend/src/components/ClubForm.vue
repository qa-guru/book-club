<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useForm, Field, ErrorMessage } from 'vee-validate'
import * as yup from 'yup'
import { useAuthStore } from '@/stores/auth'

const props = defineProps({
  clubId: {
    type: Number,
    default: null,
  },
})

const emit = defineEmits(['submit'])
const router = useRouter()
const isLoading = ref(false)

const validationSchema = yup.object({
  bookTitle: yup.string().required('Название книги обязательно'),
  bookAuthors: yup.string().required('Автор(ы) книги обязательно'),
  publicationYear: yup.number().typeError('Ага, число').required('Год выпуска обязательно'),
  description: yup.string().required('Описание книги обязательно'),
  telegramChatLink: yup
    .string()
    .required('Ссылка на Telegram чат обязательна')
    .matches(/^https:\/\/t.me\//, 'Ссылка должна начинаться с https://t.me/'),
})

const { handleSubmit, setValues } = useForm({
  validationSchema,
})

onMounted(async () => {
  if (props.clubId) {
    isLoading.value = true
    try {
      const response = await axios.get(`/api/v1/clubs/${props.clubId}/`)
      const authStore = useAuthStore()
      if (authStore.user && Number(response.data.owner?.id) !== Number(authStore.user.id)) {
        router.push({ name: 'clubs' })
        return
      }
      setValues({
        bookTitle: response.data.bookTitle,
        bookAuthors: response.data.bookAuthors,
        publicationYear: response.data.publicationYear,
        description: response.data.description,
        telegramChatLink: response.data.telegramChatLink,
      })
    } catch (error) {
      console.error('Error fetching club:', error)
      router.push({ name: 'clubs' })
    } finally {
      isLoading.value = false
    }
  }
})

const onSubmit = handleSubmit(async (values) => {
  isLoading.value = true
  try {
    if (props.clubId) {
      await axios.put(`/api/v1/clubs/${props.clubId}/`, values)
    } else {
      await axios.post('/api/v1/clubs/', values)
    }
    emit('submit')
    router.push({ name: 'clubs' })
  } catch (error) {
    if (axios.isAxiosError(error) && error.response?.data) {
      console.error('Server validation errors:', error.response.data)
    }
    console.error('Error saving club:', error)
  } finally {
    isLoading.value = false
  }
})
</script>

<template>
  <div class="club-form">
    <form @submit="onSubmit">
      <div class="form-group">
        <label for="bookTitle">Название книги *</label>
        <Field
          id="bookTitle"
          name="bookTitle"
          type="text"
          placeholder="Компьютерные сети"
          :disabled="isLoading"
          class="form-input"
        />
        <ErrorMessage name="bookTitle" class="error" />
      </div>

      <div class="form-group">
        <label for="bookAuthors">Автор(ы) книги *</label>
        <Field
          id="bookAuthors"
          name="bookAuthors"
          type="text"
          placeholder="Дэвид Уэзеролл и Эндрю Таненбаум"
          :disabled="isLoading"
          class="form-input"
        />
        <ErrorMessage name="bookAuthors" class="error" />
      </div>

      <div class="form-group">
        <label for="publicationYear">Год выпуска *</label>
        <Field
          id="publicationYear"
          type="number"
          name="publicationYear"
          placeholder="2012"
          :disabled="isLoading"
          class="form-input"
        />
        <ErrorMessage name="publicationYear" class="error" />
      </div>

      <div class="form-group">
        <label for="description">Описание книги *</label>
        <Field
          id="description"
          name="description"
          as="textarea"
          rows="5"
          placeholder="Перед вами шестое издание самой авторитетной книги по современным сетевым технологиям, написанное признанным экспертом Эндрю Таненбаумом в соавторстве со специалистом компании Google Дэвидом Уэзероллом и профессором Чикагского университета Ником Фимстером. Первая версия этого классического труда появилась"
          :disabled="isLoading"
          class="form-textarea"
        />
        <ErrorMessage name="description" class="error" />
      </div>

      <div class="form-group">
        <label for="telegramChatLink">Ссылка на Telegram чат *</label>
        <Field
          id="telegramChatLink"
          name="telegramChatLink"
          placeholder="https://t.me/..."
          :disabled="isLoading"
          class="form-input"
        />
        <ErrorMessage name="telegramChatLink" class="error" />
      </div>

      <div class="form-actions">
        <button type="submit" :disabled="isLoading" class="submit-btn" :class="{ 'btn-loading': isLoading }">
          {{ isLoading ? 'Сохранение...' : clubId ? 'Сохранить изменения' : 'Создать клуб' }}
        </button>
        <button type="button" @click="router.push('/')" :disabled="isLoading" class="cancel-btn">
          Отмена
        </button>
      </div>
    </form>
  </div>
</template>

<style scoped>
.club-form {
  width: 100%;
  max-width: 540px;
  padding: var(--space-4);
  margin: 0 auto;
  box-sizing: border-box;
}

form {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  padding: var(--space-10);
  box-sizing: border-box;
  box-shadow: var(--shadow-md);
}

.form-group {
  margin-bottom: var(--space-6);
}

.form-group label {
  display: block;
  font-size: clamp(var(--text-base), 3vw, var(--text-lg));
  font-weight: var(--weight-medium);
  margin-bottom: var(--space-2);
  color: var(--color-text-inverse);
}

.form-input,
.form-textarea {
  width: 100%;
  background: var(--color-input-bg);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-input-border);
  padding: var(--space-4) var(--space-6);
  font-family: var(--font-body);
  font-size: clamp(var(--text-sm), 3vw, var(--text-base));
  color: var(--color-input-text);
  box-sizing: border-box;
  transition: border-color var(--duration-fast) var(--ease-out), box-shadow var(--duration-fast) var(--ease-out);
}

.form-input {
  min-height: 48px;
}

.form-textarea {
  min-height: 120px;
  resize: vertical;
}

.form-input::placeholder,
.form-textarea::placeholder {
  color: var(--color-input-placeholder);
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(var(--color-primary-rgb), 0.2);
}

.form-input:disabled,
.form-textarea:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.error {
  color: var(--color-error);
  font-size: var(--text-sm);
  margin-top: var(--space-2);
  display: block;
  font-weight: var(--weight-medium);
}

.form-actions {
  display: flex;
  justify-content: center;
  gap: var(--space-4);
  margin-top: var(--space-8);
}

.submit-btn,
.cancel-btn {
  min-height: 48px;
  border-radius: var(--radius-pill);
  border: none;
  font-family: var(--font-body);
  font-size: clamp(var(--text-base), 3vw, var(--text-lg));
  font-weight: var(--weight-medium);
  cursor: pointer;
  transition: background-color var(--duration-normal) var(--ease-out), transform var(--duration-fast) var(--ease-out);
  padding: 0 var(--space-8);
}

.submit-btn {
  background: var(--color-primary);
  color: var(--color-text-inverse);
}

.submit-btn:hover:not(:disabled) {
  background: var(--color-primary-hover);
  transform: translateY(-2px);
}

.submit-btn:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

.cancel-btn {
  background: var(--color-input-bg);
  color: var(--color-text);
}

.cancel-btn:hover:not(:disabled) {
  background: rgba(245, 240, 232, 0.9);
  transform: translateY(-2px);
}

.cancel-btn:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

.submit-btn:disabled,
.cancel-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

@media (max-width: 768px) {
  .club-form {
    padding: var(--space-4);
  }

  form {
    padding: var(--space-6);
    border-radius: var(--radius-md);
  }

  .form-actions {
    flex-direction: column;
    gap: var(--space-3);
  }

  .submit-btn,
  .cancel-btn {
    width: 100%;
  }
}

@media (max-width: 480px) {
  form {
    padding: var(--space-5);
  }

  .form-group {
    margin-bottom: var(--space-4);
  }

  .form-input {
    min-height: 44px;
    padding: 0 var(--space-4);
  }

  .form-textarea {
    min-height: 100px;
  }
}
</style>
