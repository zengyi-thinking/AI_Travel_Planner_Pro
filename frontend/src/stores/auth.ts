import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/utils/api'
import type { User, LoginRequest, RegisterRequest, LoginResponse, RegisterResponse } from '@/types/api'

export const useAuthStore = defineStore('auth', () => {
  // 状态
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)
  const isAuthenticated = ref(false)
  const isLoading = ref(false)

  // 从本地存储初始化
  const initFromStorage = () => {
    const storedToken = localStorage.getItem('token')
    const storedUser = localStorage.getItem('user')

    if (storedToken && storedUser) {
      token.value = storedToken
      user.value = JSON.parse(storedUser)
      isAuthenticated.value = true
    }
  }

  // 登录
  const login = async (credentials: LoginRequest) => {
    isLoading.value = true
    try {
      console.log('Login request:', credentials)
      const response = await api.post<any>('/auth/login', credentials)
      console.log('Login response:', response)

      // 直接从response中获取数据
      user.value = response.user
      token.value = response.access_token
      isAuthenticated.value = true

      localStorage.setItem('token', response.access_token)
      localStorage.setItem('user', JSON.stringify(response.user))

      return { success: true }
    } catch (error) {
      console.error('Login failed:', error)
      return { success: false, error: '登录失败，请检查邮箱和密码' }
    } finally {
      isLoading.value = false
    }
  }

  // 注册
  const register = async (data: RegisterRequest) => {
    isLoading.value = true
    try {
      console.log('Register request:', data)
      const response = await api.post<any>('/auth/register', data)
      console.log('Register response:', response)

      // 直接从response中获取数据
      user.value = response.user
      token.value = response.access_token
      isAuthenticated.value = true

      localStorage.setItem('token', response.access_token)
      localStorage.setItem('user', JSON.stringify(response.user))

      return { success: true }
    } catch (error) {
      console.error('Register failed:', error)
      return { success: false, error: '注册失败，请稍后重试' }
    } finally {
      isLoading.value = false
    }
  }

  // 登出
  const logout = async () => {
    try {
      await api.post('/auth/logout')
    } catch (error) {
      console.warn('Logout request failed:', error)
    }
    user.value = null
    token.value = null
    isAuthenticated.value = false

    // 清除本地存储
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  // 更新用户信息
  const updateProfile = async (data: Partial<User>) => {
    if (!user.value) return { success: false, error: '用户未登录' }

    try {
      const response = await api.put<User>('/auth/me', data)
      user.value = response
      localStorage.setItem('user', JSON.stringify(user.value))

      return { success: true }
    } catch (error) {
      console.error('Update profile failed:', error)
      return { success: false, error: '更新失败' }
    }
  }

  return {
    // 状态
    user,
    token,
    isAuthenticated,
    isLoading,

    // 方法
    initFromStorage,
    login,
    register,
    logout,
    updateProfile
  }
})
