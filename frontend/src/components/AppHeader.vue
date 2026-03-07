<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { ref, computed } from 'vue'

const authStore = useAuthStore()
const isAuthenticated = computed(() => authStore.isAuthenticated)
const isMenuOpen = ref(false)

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

const closeMenu = () => {
  isMenuOpen.value = false
}
</script>

<template>
  <header class="header" data-testid="header">
    <div class="header-content">
      <router-link to="/" class="logo" data-testid="logo-link">Читальная</router-link>

      <button
        class="burger-menu"
        @click="toggleMenu"
        :class="{ active: isMenuOpen }"
        aria-label="Меню"
        data-testid="burger-menu"
      >
        <div class="burger-line burger-line-1" data-testid="burger-line-1"></div>
        <div class="burger-line burger-line-2" data-testid="burger-line-2"></div>
        <div class="burger-line burger-line-3" data-testid="burger-line-3"></div>
      </button>

      <div
        class="nav-overlay"
        :class="{ active: isMenuOpen }"
        @click="closeMenu"
        data-testid="nav-overlay"
      ></div>

      <nav class="nav" :class="{ active: isMenuOpen }" data-testid="main-nav">
        <router-link to="/" class="nav-link" @click="closeMenu" data-testid="clubs-link"
          >Клубы</router-link
        >
        <template v-if="isAuthenticated">
          <router-link
            to="/clubs/create"
            class="nav-link"
            @click="closeMenu"
            data-testid="create-club-link"
          >
            Создать клуб
          </router-link>
          <router-link to="/profile" class="nav-link" @click="closeMenu" data-testid="profile-link"
            >Профиль</router-link
          >
        </template>
        <template v-else>
          <router-link to="/signin" class="nav-link" @click="closeMenu" data-testid="signin-link"
            >Войти</router-link
          >
          <router-link to="/signup" class="nav-link" @click="closeMenu" data-testid="signup-link"
            >Регистрация</router-link
          >
        </template>
      </nav>
    </div>
  </header>
</template>

<style scoped>
.header {
  background-color: var(--color-surface);
  position: sticky;
  top: 0;
  z-index: 100;
  padding: var(--space-2) var(--space-4);
  box-shadow: var(--shadow-md);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1300px;
  margin: 0 auto;
  width: 100%;
  position: relative;
  min-height: 48px;
}

.logo {
  font-family: var(--font-heading);
  font-weight: var(--weight-semibold);
  font-size: clamp(var(--text-xl), 3vw, var(--text-2xl));
  color: var(--color-text-inverse);
  text-decoration: none;
  transition: color var(--duration-normal) var(--ease-out);
  z-index: 102;
}

.logo:hover {
  color: var(--color-primary);
}

.logo:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 4px;
  border-radius: var(--radius-sm);
}

.nav {
  display: flex;
  gap: var(--space-6);
}

.nav-link {
  position: relative;
  text-decoration: none;
  color: var(--color-text-inverse);
  font-weight: var(--weight-medium);
  font-size: clamp(var(--text-sm), 2vw, var(--text-base));
  white-space: nowrap;
  transition: color var(--duration-normal) var(--ease-out);
  padding: var(--space-2) 0;
}

.nav-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background-color: var(--color-primary);
  transition: width var(--duration-normal) var(--ease-out);
}

.nav-link:hover {
  color: var(--color-text-muted);
}

.nav-link:hover::after {
  width: 100%;
}

.nav-link:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 4px;
  border-radius: var(--radius-sm);
}

.burger-menu {
  display: none;
  cursor: pointer;
  width: 44px;
  height: 44px;
  position: relative;
  z-index: 102;
  background: transparent;
  border: none;
  padding: var(--space-2);
  border-radius: var(--radius-sm);
  transition: background var(--duration-fast) var(--ease-out);
}

.burger-menu:hover {
  background: rgba(245, 240, 232, 0.08);
}

.burger-menu:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

.burger-line {
  position: absolute;
  width: calc(100% - 16px);
  height: 2px;
  background-color: var(--color-text-inverse);
  left: 8px;
  transition: all var(--duration-normal) var(--ease-out);
}

.burger-line-1 {
  top: 14px;
  transform-origin: left center;
}

.burger-line-2 {
  top: 50%;
  transform: translateY(-50%);
  transform-origin: center;
}

.burger-line-3 {
  bottom: 14px;
  transform-origin: left center;
}

.nav-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(44, 42, 38, 0.5);
  opacity: 0;
  visibility: hidden;
  transition: opacity var(--duration-normal) var(--ease-out), visibility var(--duration-normal);
  z-index: 100;
}

.nav-overlay.active {
  opacity: 1;
  visibility: visible;
}

@media (max-width: 768px) {
  .nav {
    position: fixed;
    top: 0;
    right: -100%;
    width: min(75%, 280px);
    height: 100vh;
    background-color: var(--color-surface);
    flex-direction: column;
    align-items: flex-end;
    padding: 80px var(--space-4) var(--space-6);
    gap: var(--space-3);
    transition: right var(--duration-normal) var(--ease-out);
    z-index: 101;
    box-shadow: var(--shadow-lg);
  }

  .nav.active {
    right: 0;
  }

  .burger-menu {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .nav-link {
    font-size: var(--text-base);
    width: auto;
    padding: var(--space-3) var(--space-4);
    border-radius: var(--radius-sm);
    transition: background-color var(--duration-fast) var(--ease-out);
    text-align: right;
  }

  .nav-link:hover {
    background-color: rgba(245, 240, 232, 0.1);
  }

  .nav-link::after {
    display: none;
  }
}
</style>
