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
    await authStore.register(username.value, password.value)
    await authStore.login(username.value, password.value)
    if (authStore.pendingClubJoin) {
      router.push({ name: 'club-details', params: { id: authStore.pendingClubJoin } })
      authStore.clearPendingClubJoin()
    } else {
      router.push('/')
    }
  } catch {
    error.value = 'Ошибка при регистрации'
  }
}
</script>

<template>
  <div class="login-page" data-testid="signup-page">
    <div class="login-container" data-testid="signup-container">
      <div class="login-form" data-testid="signup-form">
        <form @submit.prevent="handleSubmit" data-testid="signup-form-element">
          <div class="form-group" data-testid="username-form-group">
            <label for="username" data-testid="username-label">Логин*</label>
            <input
              v-model="username"
              type="text"
              id="username"
              required
              placeholder="username"
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
              placeholder="password"
              data-testid="password-input"
            />
          </div>
          <button type="submit" class="submit-btn" data-testid="signup-button">
            Зарегистрироваться
          </button>
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
  padding: var(--space-8) var(--space-4);
  box-sizing: border-box;
}

.login-container {
  width: 100%;
  max-width: 480px;
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  padding: var(--space-10);
  box-sizing: border-box;
  margin-top: var(--space-4);
  box-shadow: var(--shadow-md);
}

.login-form {
  width: 100%;
  color: var(--color-text-inverse);
}

.login-form h2 {
  font-family: var(--font-heading);
  font-size: clamp(var(--text-2xl), 4vw, var(--text-3xl));
  margin-bottom: var(--space-8);
  text-align: center;
  font-weight: var(--weight-medium);
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

.submit-btn {
  width: 100%;
  max-width: 260px;
  min-height: 48px;
  background: var(--color-primary);
  border-radius: var(--radius-pill);
  border: none;
  color: var(--color-text-inverse);
  font-family: var(--font-body);
  font-size: clamp(var(--text-base), 3vw, var(--text-lg));
  font-weight: var(--weight-medium);
  display: block;
  margin: var(--space-8) auto 0;
  cursor: pointer;
  transition: background-color var(--duration-normal) var(--ease-out), transform var(--duration-fast) var(--ease-out);
}

.submit-btn:hover {
  background: var(--color-primary-hover);
  transform: translateY(-2px);
}

.submit-btn:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

.error {
  color: var(--color-error);
  text-align: center;
  margin-top: var(--space-4);
  font-size: var(--text-sm);
  font-weight: var(--weight-medium);
}

@media (max-width: 480px) {
  .login-container {
    padding: var(--space-6);
    border-radius: var(--radius-md);
    width: calc(100vw - var(--space-4));
  }

  .submit-btn {
    max-width: 100%;
  }
}

@supports (-webkit-touch-callout: none) {
  .login-page {
    min-height: -webkit-fill-available;
  }
}
</style>
