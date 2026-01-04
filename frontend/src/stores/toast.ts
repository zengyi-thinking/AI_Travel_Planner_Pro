import { defineStore } from 'pinia'
import { ref } from 'vue'

export type ToastType = 'success' | 'error' | 'warning' | 'info'

export interface Toast {
  id: number
  type: ToastType
  message: string
  duration?: number
  title?: string
  actions?: Array<{
    label: string
    handler: () => void
    primary?: boolean
  }>
}

export const useToastStore = defineStore('toast', () => {
  const toasts = ref<Toast[]>([])
  let toastIdCounter = 0

  /**
   * 添加一个新的 toast 通知
   */
  const addToast = (toast: Omit<Toast, 'id'>) => {
    const id = ++toastIdCounter
    const newToast: Toast = {
      id,
      duration: 5000,
      ...toast
    }

    toasts.value.push(newToast)

    // 自动移除 toast
    if (newToast.duration && newToast.duration > 0) {
      setTimeout(() => {
        removeToast(id)
      }, newToast.duration)
    }

    return id
  }

  /**
   * 移除指定的 toast 通知
   */
  const removeToast = (id: number) => {
    const index = toasts.value.findIndex(t => t.id === id)
    if (index > -1) {
      toasts.value.splice(index, 1)
    }
  }

  /**
   * 清空所有 toast 通知
   */
  const clearAll = () => {
    toasts.value = []
  }

  /**
   * 便捷方法：成功提示
   */
  const success = (message: string, options?: Partial<Omit<Toast, 'id' | 'type' | 'message'>>) => {
    return addToast({ type: 'success', message, ...options })
  }

  /**
   * 便捷方法：错误提示
   */
  const error = (message: string, options?: Partial<Omit<Toast, 'id' | 'type' | 'message'>>) => {
    return addToast({ type: 'error', message, duration: 8000, ...options })
  }

  /**
   * 便捷方法：警告提示
   */
  const warning = (message: string, options?: Partial<Omit<Toast, 'id' | 'type' | 'message'>>) => {
    return addToast({ type: 'warning', message, ...options })
  }

  /**
   * 便捷方法：信息提示
   */
  const info = (message: string, options?: Partial<Omit<Toast, 'id' | 'type' | 'message'>>) => {
    return addToast({ type: 'info', message, ...options })
  }

  return {
    toasts,
    addToast,
    removeToast,
    clearAll,
    success,
    error,
    warning,
    info
  }
})
