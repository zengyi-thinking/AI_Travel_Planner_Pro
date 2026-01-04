import { useLoadingStore, type LoadingState } from '@/stores/loading'

/**
 * Loading 状态管理 Composable
 * 提供便捷的方法来管理加载状态
 */
export function useLoading() {
  const loadingStore = useLoadingStore()

  return {
    /**
     * 显示指定 key 的 loading 状态
     */
    show: (key: string, message?: string, type?: LoadingState['type']) => {
      loadingStore.showLoading(key, message, type)
    },

    /**
     * 隐藏指定 key 的 loading 状态
     */
    hide: (key: string) => {
      loadingStore.hideLoading(key)
    },

    /**
     * 检查指定 key 是否在加载中
     */
    isLoading: (key?: string): boolean => {
      return loadingStore.isLoading(key)
    },

    /**
     * 获取指定 key 的加载状态
     */
    getLoadingState: (key: string): LoadingState | undefined => {
      return loadingStore.getLoadingState(key)
    },

    /**
     * 显示全局 loading
     */
    showGlobal: (message = '加载中...') => {
      loadingStore.showGlobalLoading(message)
    },

    /**
     * 隐藏全局 loading
     */
    hideGlobal: () => {
      loadingStore.hideGlobalLoading()
    },

    /**
     * 清空所有 loading 状态
     */
    clearAll: () => {
      loadingStore.clearAll()
    },

    /**
     * 包装异步函数，自动显示/隐藏 loading
     */
    async wrap<T>(
      key: string,
      fn: () => Promise<T>,
      message?: string
    ): Promise<T> {
      loadingStore.showLoading(key, message)
      try {
        return await fn()
      } finally {
        loadingStore.hideLoading(key)
      }
    },

    /**
     * 包装异步函数，使用全局 loading
     */
    async wrapGlobal<T>(
      fn: () => Promise<T>,
      message = '加载中...'
    ): Promise<T> {
      loadingStore.showGlobalLoading(message)
      try {
        return await fn()
      } finally {
        loadingStore.hideGlobalLoading()
      }
    }
  }
}
