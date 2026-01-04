<template>
  <Teleport to="body">
    <!-- 全局 Loading 遮罩 -->
    <Transition name="loading-fade">
      <div
        v-if="globalLoading"
        class="loading-overlay"
      >
        <div class="loading-content">
          <div class="loading-spinner">
            <div class="spinner-ring"></div>
            <div class="spinner-ring"></div>
            <div class="spinner-ring"></div>
          </div>
          <p v-if="globalLoadingMessage" class="loading-message">
            {{ globalLoadingMessage }}
          </p>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { useLoadingStore } from '@/stores/loading'

const loadingStore = useLoadingStore()
const { globalLoading, globalLoadingMessage } = storeToRefs(loadingStore)
</script>

<style scoped>
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.loading-content {
  text-align: center;
}

.loading-spinner {
  position: relative;
  width: 80px;
  height: 80px;
  margin: 0 auto 20px;
}

.spinner-ring {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 3px solid transparent;
  animation: spin 1.5s cubic-bezier(0.68, -0.55, 0.265, 1.55) infinite;
}

.spinner-ring:nth-child(1) {
  border-top-color: #00d4aa;
  animation-delay: 0s;
}

.spinner-ring:nth-child(2) {
  border-top-color: #45b7d1;
  animation-delay: -0.15s;
  width: 80%;
  height: 80%;
  top: 10%;
  left: 10%;
}

.spinner-ring:nth-child(3) {
  border-top-color: #a78bfa;
  animation-delay: -0.3s;
  width: 60%;
  height: 60%;
  top: 20%;
  left: 20%;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.loading-message {
  font-size: 16px;
  color: #475569;
  font-weight: 500;
  margin: 0;
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

/* 淡入淡出动画 */
.loading-fade-enter-active,
.loading-fade-leave-active {
  transition: opacity 0.3s ease;
}

.loading-fade-enter-from,
.loading-fade-leave-to {
  opacity: 0;
}

/* 深色模式支持 */
@media (prefers-color-scheme: dark) {
  .loading-overlay {
    background: rgba(15, 23, 42, 0.9);
  }

  .loading-message {
    color: #e2e8f0;
  }
}
</style>
