<template>
  <Teleport to="body">
    <TransitionGroup
      name="toast"
      tag="div"
      class="toast-container fixed top-4 right-4 z-50 flex flex-col gap-2 pointer-events-none"
    >
      <div
        v-for="toast in toasts"
        :key="toast.id"
        :class="['toast', `toast-${toast.type}`, 'pointer-events-auto']"
        role="alert"
      >
        <!-- 图标 -->
        <div class="toast-icon">
          <AppIcon
            :name="getIconName(toast.type)"
            :class="getIconClass(toast.type)"
          />
        </div>

        <!-- 内容 -->
        <div class="toast-content flex-1">
          <div v-if="toast.title" class="toast-title">
            {{ toast.title }}
          </div>
          <div class="toast-message">
            {{ toast.message }}
          </div>

          <!-- 操作按钮 -->
          <div v-if="toast.actions && toast.actions.length > 0" class="toast-actions">
            <button
              v-for="(action, idx) in toast.actions"
              :key="idx"
              :class="[
                'toast-action-btn',
                action.primary ? 'toast-action-primary' : 'toast-action-secondary'
              ]"
              @click="handleAction(toast, action)"
            >
              {{ action.label }}
            </button>
          </div>
        </div>

        <!-- 关闭按钮 -->
        <button
          class="toast-close"
          @click="removeToast(toast.id)"
          aria-label="关闭"
        >
          <AppIcon name="times" />
        </button>

        <!-- 进度条 -->
        <div
          v-if="toast.duration && toast.duration > 0"
          class="toast-progress"
          :style="{ animationDuration: `${toast.duration}ms` }"
        />
      </div>
    </TransitionGroup>
  </Teleport>
</template>

<script setup lang="ts">
import { storeToRefs } from 'pinia'
import AppIcon from './AppIcon.vue'
import { useToastStore, type ToastType } from '@/stores/toast'

const toastStore = useToastStore()
const { toasts } = storeToRefs(toastStore)
const { removeToast } = toastStore

function getIconName(type: ToastType): string {
  const iconMap = {
    success: 'check-circle',
    error: 'exclamation-circle',
    warning: 'exclamation-triangle',
    info: 'info-circle'
  }
  return iconMap[type] || 'info-circle'
}

function getIconClass(type: ToastType): string {
  const classMap = {
    success: 'text-green-500',
    error: 'text-red-500',
    warning: 'text-orange-500',
    info: 'text-blue-500'
  }
  return classMap[type] || 'text-blue-500'
}

function handleAction(toast: any, action: any) {
  action.handler()
  removeToast(toast.id)
}
</script>

<style scoped>
.toast-container {
  max-width: 420px;
  width: 100%;
}

.toast {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  padding: 16px;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  min-width: 320px;
  position: relative;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.8);
}

.toast-icon {
  flex-shrink: 0;
  font-size: 24px;
  margin-top: 2px;
}

.toast-content {
  flex: 1;
  min-width: 0;
}

.toast-title {
  font-weight: 600;
  font-size: 15px;
  color: #1e293b;
  margin-bottom: 4px;
}

.toast-message {
  font-size: 14px;
  color: #64748b;
  line-height: 1.5;
}

.toast-actions {
  display: flex;
  gap: 8px;
  margin-top: 12px;
}

.toast-action-btn {
  padding: 6px 14px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.toast-action-primary {
  background: linear-gradient(135deg, #00d4aa 0%, #45b7d1 100%);
  color: white;
}

.toast-action-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 212, 170, 0.3);
}

.toast-action-secondary {
  background: #f1f5f9;
  color: #64748b;
}

.toast-action-secondary:hover {
  background: #e2e8f0;
}

.toast-close {
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  border-radius: 8px;
  border: none;
  background: transparent;
  color: #94a3b8;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  font-size: 16px;
}

.toast-close:hover {
  background: #f1f5f9;
  color: #64748b;
}

.toast-progress {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 3px;
  background: linear-gradient(90deg, #00d4aa, #45b7d1);
  animation: toast-progress linear forwards;
  transform-origin: left;
}

@keyframes toast-progress {
  from {
    transform: scaleX(1);
  }
  to {
    transform: scaleX(0);
  }
}

/* Toast 类型样式 */
.toast-success {
  border-left: 4px solid #10b981;
}

.toast-error {
  border-left: 4px solid #ef4444;
}

.toast-warning {
  border-left: 4px solid #f59e0b;
}

.toast-info {
  border-left: 4px solid #3b82f6;
}

/* 进入/离开动画 */
.toast-enter-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.toast-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 1, 1);
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(100%) scale(0.9);
}

.toast-move {
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* 深色模式支持 */
@media (prefers-color-scheme: dark) {
  .toast {
    background: rgba(30, 41, 59, 0.95);
    border-color: rgba(51, 65, 85, 0.8);
  }

  .toast-title {
    color: #f1f5f9;
  }

  .toast-message {
    color: #cbd5e1;
  }

  .toast-action-secondary {
    background: #334155;
    color: #cbd5e1;
  }

  .toast-action-secondary:hover {
    background: #475569;
  }

  .toast-close:hover {
    background: #334155;
    color: #cbd5e1;
  }
}
</style>
