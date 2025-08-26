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
  background: var(--color-black);
  border-radius: 50px;
  padding: 1.5rem;
  box-sizing: border-box;
}

.search-container {
  margin-bottom: 1rem;
}

.search-input-wrapper {
  display: flex;
  gap: 0.5rem;
}

.search-input {
  flex: 1;
  height: 50px;
  background: var(--color-white);
  border-radius: 30px;
  border: none;
  padding: 0 1.5rem;
  font-size: 1rem;
  color: var(--colore-input-text);
  font-style: italic;
  box-sizing: border-box;
  min-width: 0;
}

.search-button {
  height: 50px;
  padding: 0 1.5rem;
  background: var(--color-primary);
  border-radius: 30px;
  border: none;
  color: var(--color-white);
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  white-space: nowrap;
}

.filter-options {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
}

.filter-option {
  height: 40px;
  padding: 0 1.25rem;
  background: var(--color-white);
  border-radius: 30px;
  border: none;
  color: var(--color-black);
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
}

.filter-option.active {
  background: var(--color-primary);
  color: var(--color-white);
}

@media (max-width: 768px) {
  .search-filters-wrapper {
    border-radius: 30px;
    padding: 1.25rem;
  }

  .search-input-wrapper {
    flex-direction: row;
  }

  .search-button {
    padding: 0 1rem;
  }

  .filter-options {
    flex-wrap: wrap;
  }

  .filter-option {
    flex: 1;
    min-width: 100px;
    padding: 0 0.5rem;
    font-size: 0.85rem;
  }
}

@media (max-width: 480px) {
  .search-filters-wrapper {
    border-radius: 25px;
    padding: 1rem;
  }

  .search-input {
    height: 45px;
    font-size: 0.9rem;
    padding: 0 1rem;
  }

  .search-button {
    height: 45px;
    font-size: 0.9rem;
    padding: 0 0.8rem;
  }

  .filter-option {
    height: 36px;
    font-size: 0.8rem;
  }
}
</style>
