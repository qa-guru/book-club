<script setup lang="ts">
import AppHeader from '@/components/AppHeader.vue'
import BlobsBackground from '@/components/BlobsBackground.vue'
</script>

<template>
  <div class="app-layout">
    <BlobsBackground />
    <AppHeader />
    <main>
      <router-view />
    </main>
  </div>
</template>

<style>
@import '@/assets/main.css';

.app-layout {
  position: relative;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

main {
  position: relative;
  z-index: 1;
  flex: 1;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  padding: 1rem;
  box-sizing: border-box;
}
</style>
