<template>
  <div class="blob-background">
    <div v-for="(blob, index) in blobs" :key="index" class="blob" :style="blob.style"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const blobs = ref<Array<{ style: string }>>([])

const generateBlobs = () => {
  const count = 12
  const newBlobs = []

  for (let i = 0; i < count; i++) {
    const size = Math.random() * 100 + 50
    const opacity = 0.8
    const left = Math.random() * 100
    const top = Math.random() * 100

    newBlobs.push({
      style: `
        width: ${size}px;
        height: ${size}px;
        left: ${left}%;
        top: ${top}%;
        opacity: ${opacity};
        animation-duration: ${Math.random() * 20 + 10}s;
        animation-delay: ${Math.random() * 5}s;
      `,
    })
  }

  blobs.value = newBlobs
}

onMounted(() => {
  generateBlobs()
})
</script>

<style scoped>
.blob-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  overflow: hidden;
  pointer-events: none;
}

.blob {
  position: absolute;
  background: radial-gradient(ellipse at center, var(--color-blob) 0%, var(--color-blob-alt) 100%);
  border-radius: 50%;
  animation: float ease-in-out infinite;
}

@keyframes float {
  0%,
  100% {
    transform: translate(0, 0) scale(1);
    border-radius: 50% 50% 60% 40%;
  }
  25% {
    transform: translate(-20%, -10%) scale(1.1);
    border-radius: 60% 40% 50% 50%;
  }
  50% {
    transform: translate(10%, 10%) scale(0.9);
    border-radius: 40% 60% 40% 60%;
  }
  75% {
    transform: translate(-10%, 20%) scale(1.05);
    border-radius: 50% 50% 40% 60%;
  }
}
</style>
