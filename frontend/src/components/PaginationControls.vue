<script setup lang="ts">
import { computed, ref } from 'vue'
import { useClubsStore } from '@/stores/clubs'

const clubsStore = useClubsStore()

const currentPage = computed(() => clubsStore.pagination.currentPage)
const totalPages = computed(() => clubsStore.totalPages)
const pageSize = computed({
  get: () => clubsStore.pagination.pageSize,
  set: (value) => clubsStore.changePageSize(Number(value)),
})

const pageSizes = [5, 10, 15, 20, 25]
const isSelectOpen = ref(false)
const selectedSize = ref(pageSize.value)

const goToPage = (page: number) => {
  if (page >= 1 && page <= totalPages.value) {
    clubsStore.goToPage(page)
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    clubsStore.nextPage()
  }
}

const prevPage = () => {
  if (currentPage.value > 1) {
    clubsStore.prevPage()
  }
}

const toggleSelect = () => {
  isSelectOpen.value = !isSelectOpen.value
}

const selectOption = (size: number) => {
  if (size !== selectedSize.value) {
    pageSize.value = size
    selectedSize.value = size
  }
  isSelectOpen.value = false
}
</script>

<template>
  <div class="pagination-controls">
    <div class="pagination-buttons">
      <button @click="prevPage" :disabled="currentPage === 1" class="pagination-button">
        Назад
      </button>

      <template v-for="page in totalPages" :key="page">
        <button
          v-if="Math.abs(page - currentPage) <= 2 || page === 1 || page === totalPages"
          @click="goToPage(page)"
          :class="{ active: page === currentPage }"
          class="pagination-button"
          :disabled="page === currentPage"
        >
          {{ page }}
        </button>
        <span
          v-else-if="
            (page === 2 && currentPage - 2 > 2) ||
            (page === totalPages - 1 && currentPage + 2 < totalPages - 1)
          "
          class="ellipsis"
        >
          ...
        </span>
      </template>

      <button @click="nextPage" :disabled="currentPage === totalPages" class="pagination-button">
        Вперед
      </button>
    </div>

    <div class="page-size-selector">
      <label>Клубов на странице:</label>
      <div class="custom-select" :class="{ open: isSelectOpen }">
        <div class="select-header" @click="toggleSelect">
          {{ selectedSize }}
        </div>
        <div class="select-options">
          <div
            v-for="size in pageSizes"
            :key="size"
            class="select-option"
            :class="{
              selected: size === selectedSize,
              'not-selectable': size === selectedSize,
            }"
            @click="selectOption(size)"
          >
            {{ size }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.pagination-controls {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
  margin-top: 2rem;
  padding: 1.5rem;
  background: var(--color-black);
  border-radius: 50px;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

.pagination-buttons {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
}

.pagination-button {
  padding: 0.75rem 1.25rem;
  border: none;
  background-color: var(--color-white);
  border-radius: 30px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  font-weight: 500;
  color: var(--color-black);
  min-width: 44px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.pagination-button:hover:not(:disabled):not(.active) {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
  background-color: #f0f0f0;
}

.pagination-button.active {
  background-color: var(--color-primary);
  color: white;
  box-shadow: 0 4px 12px rgba(var(--color-primary-rgb), 0.3);
  transform: scale(1.05);
  cursor: default;
}

.pagination-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
}

.ellipsis {
  padding: 0.75rem 0.5rem;
  display: inline-block;
  color: var(--color-white);
  font-size: 1.2rem;
}

.page-size-selector {
  position: relative;
  display: flex;
  align-items: center;
  gap: 1rem;
  color: var(--color-white);
  width: 100%;
  max-width: 300px;
}

.page-size-selector label {
  font-weight: 500;
  font-size: 1rem;
  white-space: nowrap;
}

.custom-select {
  position: relative;
  width: 100%;
}

.select-header {
  padding: 0.75rem 1.25rem;
  border-radius: 30px;
  background-color: var(--color-white);
  color: var(--color-black);
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  font-style: italic;
}

.select-header:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
  transform: translateY(-1px);
}

.select-header:after {
  content: '';
  display: inline-block;
  width: 12px;
  height: 12px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: center;
  transition: transform 0.2s ease;
}

.select-options {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: var(--color-white);
  border-radius: 15px;
  margin-top: 5px;
  overflow: hidden;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  z-index: 100;
  max-height: 0;
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
}

.custom-select.open .select-options {
  max-height: 300px;
  opacity: 1;
  visibility: visible;
}

.custom-select.open .select-header:after {
  transform: rotate(180deg);
}

.select-option {
  padding: 0.75rem 1.25rem;
  cursor: pointer;
  transition: all 0.2s ease;
  color: var(--color-black);
  display: flex;
  align-items: center;
}

.select-option:hover:not(.not-selectable) {
  background-color: var(--color-primary);
  color: white;
}

.select-option.selected {
  background-color: rgba(var(--color-primary-rgb), 0.2);
  cursor: default;
}

.select-option.not-selectable {
  cursor: default;
  pointer-events: none;
}

.select-option.not-selectable:hover {
  background-color: transparent;
  color: var(--color-black);
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
  100% {
    transform: scale(1);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.pagination-button.active {
  animation: pulse 1.5s infinite;
}

.select-option {
  animation: fadeIn 0.3s ease forwards;
}

.select-option:nth-child(1) {
  animation-delay: 0.05s;
}
.select-option:nth-child(2) {
  animation-delay: 0.1s;
}
.select-option:nth-child(3) {
  animation-delay: 0.15s;
}
.select-option:nth-child(4) {
  animation-delay: 0.2s;
}
.select-option:nth-child(5) {
  animation-delay: 0.25s;
}

@media (max-width: 600px) {
  .pagination-controls {
    padding: 1.25rem;
    border-radius: 30px;
  }

  .pagination-buttons {
    gap: 0.5rem;
  }

  .pagination-button {
    padding: 0.6rem 1rem;
    min-width: 36px;
  }

  .page-size-selector {
    flex-direction: column;
    align-items: stretch;
    gap: 0.75rem;
  }

  .page-size-selector label {
    text-align: center;
  }

  .select-header {
    padding: 0.65rem 1.15rem;
  }

  .select-option {
    padding: 0.65rem 1.15rem;
  }
}

@media (hover: none) {
  .select-header:active {
    transform: scale(0.98);
  }

  .select-option:active:not(.not-selectable) {
    background-color: var(--color-primary);
    color: white;
  }
}
</style>
