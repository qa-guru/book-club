<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const username = ref('')
const password = ref('')
const error = ref('')

async function handleSubmit() {
  try {
    await authStore.login(username.value, password.value)
    if (authStore.pendingClubJoin) {
      router.push({ name: 'club-details', params: { id: authStore.pendingClubJoin } })
      authStore.clearPendingClubJoin()
    } else {
      router.push('/')
    }
  } catch {
    error.value = 'Ты не пройдешь!'
  }
}
</script>

<template>
  <div class="login-page" data-testid="login-page">
    <div class="login-container" data-testid="login-container">
      <div class="login-form" data-testid="login-form">
        <form @submit.prevent="handleSubmit" data-testid="login-form-element">
          <div class="form-group" data-testid="username-form-group">
            <label for="username" data-testid="username-label">Логин*</label>
            <input
              v-model="username"
              type="text"
              id="username"
              required
              placeholder="segfault"
              data-testid="username-input"
            />
          </div>
          <div class="form-group" data-testid="password-form-group">
            <label for="password" data-testid="password-label">Надежный пароль*</label>
            <input
              v-model="password"
              type="password"
              id="password"
              required
              placeholder="1111"
              data-testid="password-input"
            />
          </div>
          <button type="submit" class="submit-btn" data-testid="submit-button">Войти</button>
          <p v-if="error" class="error" data-testid="error-message">{{ error }}</p>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  padding: 2rem 1rem;
  box-sizing: border-box;
}

.login-container {
  width: 100%;
  max-width: 540px;
  background: var(--color-black);
  border-radius: 50px;
  padding: 2.5rem;
  box-sizing: border-box;
  margin-top: 1rem;
}

.login-form {
  width: 100%;
  color: var(--color-white);
}

.login-form h2 {
  font-size: clamp(1.5rem, 4vw, 2rem);
  margin-bottom: 2rem;
  text-align: center;
  font-weight: 500;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  font-size: clamp(1rem, 3vw, 1.25rem);
  font-weight: 500;
  margin-bottom: 0.5rem;
}

.form-group input {
  width: 100%;
  height: 50px;
  background: var(--color-white);
  border-radius: 30px;
  border: none;
  padding: 0 1.5rem;
  font-size: clamp(0.875rem, 3vw, 1.125rem);
  color: var(--colore-input-text);
  font-style: italic;
  box-sizing: border-box;
}

.form-group input::placeholder {
  color: var(--colore-input-text);
  font-style: italic;
  opacity: 1;
}

.submit-btn {
  width: 100%;
  max-width: 257px;
  height: 50px;
  background: var(--color-primary);
  border-radius: 30px;
  border: none;
  color: var(--color-white);
  font-size: clamp(1rem, 3vw, 1.25rem);
  font-weight: 500;
  display: block;
  margin: 2rem auto 0;
  cursor: pointer;
  transition: all 0.3s ease;
}

.submit-btn:hover {
  opacity: 0.9;
  transform: translateY(-2px);
}

.error {
  color: var(--color-error);
  text-align: center;
  margin-top: 1rem;
  font-size: clamp(0.875rem, 2vw, 1rem);
}

@media (max-width: 480px) {
  .login-container {
    padding: 1.5rem;
    border-radius: 30px;
    width: calc(100vw - 1rem);
    max-height: calc(100vh - 1rem);
  }

  .submit-btn {
    max-width: 100%;
  }
}

@supports (-webkit-touch-callout: none) {
  .login-page {
    height: -webkit-fill-available;
  }
}
</style>
