import { useToastStore, type Toast } from '@/stores/toast'

/**
 * Toast 通知 Composable
 * 提供便捷的方法来显示各种类型的通知消息
 */
export function useToast() {
  const toastStore = useToastStore()

  return {
    /**
     * 显示成功提示
     */
    success: (message: string, options?: Partial<Omit<Toast, 'id' | 'type' | 'message'>>) => {
      return toastStore.success(message, options)
    },

    /**
     * 显示错误提示
     */
    error: (message: string, options?: Partial<Omit<Toast, 'id' | 'type' | 'message'>>) => {
      return toastStore.error(message, options)
    },

    /**
     * 显示警告提示
     */
    warning: (message: string, options?: Partial<Omit<Toast, 'id' | 'type' | 'message'>>) => {
      return toastStore.warning(message, options)
    },

    /**
     * 显示信息提示
     */
    info: (message: string, options?: Partial<Omit<Toast, 'id' | 'type' | 'message'>>) => {
      return toastStore.info(message, options)
    },

    /**
     * 添加自定义 toast
     */
    addToast: (toast: Omit<Toast, 'id'>) => {
      return toastStore.addToast(toast)
    },

    /**
     * 移除指定的 toast
     */
    removeToast: (id: number) => {
      toastStore.removeToast(id)
    },

    /**
     * 清空所有 toast
     */
    clearAll: () => {
      toastStore.clearAll()
    }
  }
}
