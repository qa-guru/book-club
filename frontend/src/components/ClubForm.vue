<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useForm, Field, ErrorMessage } from 'vee-validate'
import * as yup from 'yup'

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
  description: yup.string().required('Опсисание книги обязательно'),
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
      // Обработка ошибок сервера
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
        <button type="submit" :disabled="isLoading" class="submit-btn">
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
  padding: 1rem 1rem;
  margin: 0 auto;
  box-sizing: border-box;
}

form {
  background: var(--color-black);
  border-radius: 50px;
  padding: 2.5rem;
  box-sizing: border-box;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  font-size: clamp(1rem, 3vw, 1.25rem);
  font-weight: 500;
  margin-bottom: 0.5rem;
  color: var(--color-white);
}

.form-input,
.form-textarea {
  width: 100%;
  background: var(--color-white);
  border-radius: 30px;
  border: none;
  padding: 1rem 1.5rem;
  font-size: clamp(0.875rem, 3vw, 1.125rem);
  color: var(--colore-input-text);
  box-sizing: border-box;
}

.form-input {
  height: 50px;
}

.form-textarea {
  min-height: 120px;
  resize: vertical;
}

.form-input::placeholder,
.form-textarea::placeholder {
  color: var(--colore-input-text);
  opacity: 1;
  font-style: italic;
}

.error {
  color: var(--color-error);
  font-size: 0.875rem;
  margin-top: 0.5rem;
  display: block;
}

.form-actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 2rem;
}

.submit-btn,
.cancel-btn {
  height: 50px;
  border-radius: 30px;
  border: none;
  font-size: clamp(1rem, 3vw, 1.25rem);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 0 2rem;
}

.submit-btn {
  background: var(--color-primary);
  color: var(--color-white);
}

.cancel-btn {
  background: var(--color-white);
  color: var(--color-black);
}

.submit-btn:hover,
.cancel-btn:hover {
  opacity: 0.9;
  transform: translateY(-2px);
}

.submit-btn:disabled,
.cancel-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

@media (max-width: 768px) {
  .club-form {
    padding: 1rem;
  }

  form {
    padding: 1.5rem;
    border-radius: 30px;
  }

  .form-actions {
    flex-direction: column;
    gap: 0.75rem;
  }

  .submit-btn,
  .cancel-btn {
    width: 100%;
  }
}

@media (max-width: 480px) {
  form {
    padding: 1.25rem;
  }

  .form-group {
    margin-bottom: 1rem;
  }

  .form-input {
    height: 45px;
    padding: 0 1rem;
  }

  .form-textarea {
    min-height: 100px;
  }
}
</style>
