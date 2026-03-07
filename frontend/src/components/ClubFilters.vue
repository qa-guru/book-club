<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useClubsStore } from '@/stores/clubs'

const router = useRouter()
const authStore = useAuthStore()
const clubsStore = useClubsStore()

const searchQuery = ref('')
const activeFilter = ref<'all' | 'member' | 'owner'>('all')
const isFiltersExpanded = ref(false)

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    clubsStore.searchClubs(searchQuery.value.trim())
  } else {
    clubsStore.fetchClubs()
  }
}

const applyFilter = (filter: 'all' | 'member' | 'owner') => {
  if (!authStore.isAuthenticated && filter !== 'all') {
    router.push('/signin')
    return
  }

  activeFilter.value = filter
  if (filter === 'all') {
    clubsStore.fetchClubs()
  } else {
    clubsStore.filterByMembership(filter)
  }

  if (window.innerWidth < 768) {
    isFiltersExpanded.value = false
  }
}
</script>

<template>
  <div class="combined-container">
    <div class="search-filters-wrapper">
      <div class="search-container">
        <div class="search-input-wrapper">
          <input
            v-model="searchQuery"
            @keyup.enter="handleSearch"
            type="text"
            placeholder="Поиск книжных клубов..."
            class="search-input"
          />
          <button @click="handleSearch" class="search-button">Найти</button>
        </div>
      </div>

      <div class="filters-container" :class="{ expanded: isFiltersExpanded }">
        <div class="filter-options">
          <button
            @click="applyFilter('all')"
            :class="{ active: activeFilter === 'all' }"
            class="filter-option"
          >
            Все клубы
          </button>
          <button
            @click="applyFilter('owner')"
            :class="{ active: activeFilter === 'owner' }"
            class="filter-option"
          >
            Мои клубы
          </button>
          <button
            @click="applyFilter('member')"
            :class="{ active: activeFilter === 'member' }"
            class="filter-option"
          >
            Участвую
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.combined-container {
  width: 100%;
  display: flex;
  justify-content: center;
  box-sizing: border-box;
}

.search-filters-wrapper {
  width: 100%;
  max-width: 600px;
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  box-sizing: border-box;
  box-shadow: var(--shadow-sm);
}

.search-container {
  margin-bottom: var(--space-4);
}

.search-input-wrapper {
  display: flex;
  gap: var(--space-3);
}

.search-input {
  flex: 1;
  min-height: 48px;
  background: var(--color-input-bg);
  border-radius: var(--radius-pill);
  border: 1px solid var(--color-input-border);
  padding: 0 var(--space-6);
  font-family: var(--font-body);
  font-size: var(--text-base);
  color: var(--color-input-text);
  box-sizing: border-box;
  min-width: 0;
  transition: border-color var(--duration-fast) var(--ease-out), box-shadow var(--duration-fast) var(--ease-out);
}

.search-input::placeholder {
  color: var(--color-input-placeholder);
}

.search-input:hover {
  border-color: rgba(44, 42, 38, 0.25);
}

.search-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(var(--color-primary-rgb), 0.2);
}

.search-button {
  min-height: 48px;
  padding: 0 var(--space-6);
  background: var(--color-primary);
  border-radius: var(--radius-pill);
  border: none;
  color: var(--color-text-inverse);
  font-family: var(--font-body);
  font-size: var(--text-base);
  font-weight: var(--weight-medium);
  cursor: pointer;
  white-space: nowrap;
  transition: background-color var(--duration-normal) var(--ease-out), transform var(--duration-fast) var(--ease-out);
}

.search-button:hover {
  background: var(--color-primary-hover);
  transform: translateY(-1px);
}

.search-button:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

.filter-options {
  display: flex;
  gap: var(--space-2);
  justify-content: center;
  flex-wrap: wrap;
}

.filter-option {
  min-height: 40px;
  padding: 0 var(--space-5);
  background: var(--color-input-bg);
  border-radius: var(--radius-pill);
  border: 1px solid transparent;
  color: var(--color-text);
  font-family: var(--font-body);
  font-size: var(--text-sm);
  font-weight: var(--weight-medium);
  cursor: pointer;
  transition: background-color var(--duration-fast) var(--ease-out), color var(--duration-fast) var(--ease-out);
}

.filter-option:hover {
  background: rgba(245, 240, 232, 0.9);
}

.filter-option:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

.filter-option.active {
  background: var(--color-primary);
  color: var(--color-text-inverse);
}

@media (max-width: 768px) {
  .search-filters-wrapper {
    border-radius: var(--radius-md);
    padding: var(--space-5);
  }

  .search-button {
    padding: 0 var(--space-4);
  }

  .filter-option {
    flex: 1;
    min-width: 100px;
    padding: 0 var(--space-3);
  }
}

@media (max-width: 480px) {
  .search-filters-wrapper {
    border-radius: var(--radius-md);
    padding: var(--space-4);
  }

  .search-input {
    min-height: 44px;
    padding: 0 var(--space-4);
  }

  .search-button {
    min-height: 44px;
    padding: 0 var(--space-4);
  }

  .filter-option {
    min-height: 36px;
    font-size: var(--text-xs);
  }
}
</style>
