import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface LoadingState {
  id: string
  message?: string
  type?: 'default' | 'blur' | 'transparent'
}

export const useLoadingStore = defineStore('loading', () => {
  const loadingStates = ref<Map<string, LoadingState>>(new Map())
  const globalLoading = ref(false)
  const globalLoadingMessage = ref('加载中...')

  /**
   * 显示指定 key 的 loading 状态
   */
  const showLoading = (key: string, message?: string, type?: LoadingState['type']) => {
    loadingStates.value.set(key, {
      id: key,
      message,
      type
    })
  }

  /**
   * 隐藏指定 key 的 loading 状态
   */
  const hideLoading = (key: string) => {
    loadingStates.value.delete(key)
  }

  /**
   * 检查指定 key 是否在加载中
   */
  const isLoading = (key?: string): boolean => {
    if (key) {
      return loadingStates.value.has(key)
    }
    return loadingStates.value.size > 0
  }

  /**
   * 获取指定 key 的加载状态
   */
  const getLoadingState = (key: string): LoadingState | undefined => {
    return loadingStates.value.get(key)
  }

  /**
   * 显示全局 loading
   */
  const showGlobalLoading = (message = '加载中...') => {
    globalLoading.value = true
    globalLoadingMessage.value = message
    document.body.style.overflow = 'hidden'
  }

  /**
   * 隐藏全局 loading
   */
  const hideGlobalLoading = () => {
    globalLoading.value = false
    document.body.style.overflow = ''
  }

  /**
   * 清空所有 loading 状态
   */
  const clearAll = () => {
    loadingStates.value.clear()
    globalLoading.value = false
    document.body.style.overflow = ''
  }

  return {
    loadingStates,
    globalLoading,
    globalLoadingMessage,
    showLoading,
    hideLoading,
    isLoading,
    getLoadingState,
    showGlobalLoading,
    hideGlobalLoading,
    clearAll
  }
})
