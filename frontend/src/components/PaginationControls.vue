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
  gap: var(--space-6);
  margin-top: var(--space-8);
  padding: var(--space-6);
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
  box-shadow: var(--shadow-sm);
}

.pagination-buttons {
  display: flex;
  gap: var(--space-3);
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
}

.pagination-button {
  padding: var(--space-3) var(--space-5);
  border: none;
  background-color: var(--color-input-bg);
  border-radius: var(--radius-pill);
  cursor: pointer;
  transition: background-color var(--duration-normal) var(--ease-out), transform var(--duration-fast) var(--ease-out), box-shadow var(--duration-fast);
  font-family: var(--font-body);
  font-weight: var(--weight-medium);
  color: var(--color-text);
  min-width: 44px;
  min-height: 44px;
  text-align: center;
  box-shadow: var(--shadow-sm);
}

.pagination-button:hover:not(:disabled):not(.active) {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  background-color: rgba(245, 240, 232, 0.95);
}

.pagination-button:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

.pagination-button.active {
  background-color: var(--color-primary);
  color: var(--color-text-inverse);
  box-shadow: 0 4px 12px rgba(var(--color-primary-rgb), 0.35);
  transform: scale(1.02);
  cursor: default;
}

.pagination-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
}

.ellipsis {
  padding: var(--space-3) var(--space-2);
  display: inline-block;
  color: var(--color-text-inverse);
  font-size: var(--text-lg);
}

.page-size-selector {
  position: relative;
  display: flex;
  align-items: center;
  gap: var(--space-4);
  color: var(--color-text-inverse);
  width: 100%;
  max-width: 300px;
}

.page-size-selector label {
  font-weight: var(--weight-medium);
  font-size: var(--text-base);
  white-space: nowrap;
}

.custom-select {
  position: relative;
  width: 100%;
}

.select-header {
  padding: var(--space-3) var(--space-5);
  border-radius: var(--radius-pill);
  background-color: var(--color-input-bg);
  color: var(--color-text);
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: box-shadow var(--duration-fast) var(--ease-out), transform var(--duration-fast) var(--ease-out);
  box-shadow: var(--shadow-sm);
  font-family: var(--font-body);
}

.select-header:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
}

.select-header:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

.select-header:after {
  content: '';
  display: inline-block;
  width: 12px;
  height: 12px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: center;
  transition: transform var(--duration-fast) var(--ease-out);
}

.select-options {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: var(--color-input-bg);
  border-radius: var(--radius-md);
  margin-top: var(--space-2);
  overflow: hidden;
  box-shadow: var(--shadow-lg);
  z-index: 100;
  max-height: 0;
  opacity: 0;
  visibility: hidden;
  transition: max-height var(--duration-normal) var(--ease-out), opacity var(--duration-normal), visibility var(--duration-normal);
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
  padding: var(--space-3) var(--space-5);
  cursor: pointer;
  transition: background-color var(--duration-fast) var(--ease-out), color var(--duration-fast);
  color: var(--color-text);
  display: flex;
  align-items: center;
  font-family: var(--font-body);
}

.select-option:hover:not(.not-selectable) {
  background-color: var(--color-primary);
  color: var(--color-text-inverse);
}

.select-option.selected {
  background-color: var(--color-primary-soft);
  cursor: default;
}

.select-option.not-selectable {
  cursor: default;
  pointer-events: none;
}

.select-option.not-selectable:hover {
  background-color: transparent;
  color: var(--color-text);
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
  animation: none;
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
    padding: var(--space-5);
    border-radius: var(--radius-md);
  }

  .pagination-buttons {
    gap: var(--space-2);
  }

  .pagination-button {
    padding: var(--space-2) var(--space-4);
    min-width: 40px;
  }

  .page-size-selector {
    flex-direction: column;
    align-items: stretch;
    gap: var(--space-3);
  }

  .page-size-selector label {
    text-align: center;
  }

  .select-header {
    padding: var(--space-2) var(--space-4);
  }

  .select-option {
    padding: var(--space-2) var(--space-4);
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
