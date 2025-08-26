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
  background-color: var(--color-black);
  position: sticky;
  top: 0;
  z-index: 100;
  padding: 0.5rem 1rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1300px;
  margin: 0 auto;
  width: 100%;
  position: relative;
  height: 40px;
}

.logo {
  font-weight: 700;
  font-size: clamp(1.25rem, 3vw, 1.5rem);
  color: var(--color-white);
  text-decoration: none;
  transition: opacity 0.3s;
  z-index: 102;
}

.logo:hover {
  opacity: 0.8;
}

.nav {
  display: flex;
  gap: clamp(0.75rem, 2vw, 1.5rem);
}

.nav-link {
  position: relative;
  text-decoration: none;
  color: var(--color-white);
  font-weight: 500;
  font-size: clamp(0.875rem, 2vw, 1rem);
  white-space: nowrap;
  transition: all 0.3s ease;
  padding: 0.25rem 0;
}

.nav-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background-color: var(--color-white);
  transition: width 0.3s ease;
}

.nav-link:hover::after {
  width: 100%;
}

.burger-menu {
  display: none;
  cursor: pointer;
  width: 28px;
  height: 28px;
  position: relative;
  z-index: 102;
  background: transparent;
  border: none;
  padding: 0;
}

.burger-line {
  position: absolute;
  width: 100%;
  height: 2px;
  background-color: var(--color-white);
  left: 0;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.burger-line-1 {
  top: 6px;
  transform-origin: left center;
}

.burger-line-2 {
  top: 50%;
  transform: translateY(-50%);
  transform-origin: center;
}

.burger-line-3 {
  bottom: 6px;
  transform-origin: left center;
}

.nav-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
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
    background-color: var(--color-black);
    flex-direction: column;
    align-items: flex-end;
    padding: 80px 1rem 1.5rem;
    gap: 0.75rem;
    transition: right 0.3s ease;
    z-index: 101;
    box-shadow: -5px 0 15px rgba(0, 0, 0, 0.2);
  }

  .nav.active {
    right: 0;
  }

  .burger-menu {
    display: block;
  }

  .nav-link {
    font-size: 1rem;
    width: auto;
    padding: 0.35rem 0.5rem;
    border-radius: 4px;
    transition: background-color 0.2s;
    text-align: right;
  }

  .nav-link:hover {
    background-color: rgba(255, 255, 255, 0.1);
  }

  .nav-link::after {
    display: none;
  }
}
</style>
