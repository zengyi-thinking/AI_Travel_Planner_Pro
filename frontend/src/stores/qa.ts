import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/utils/api'
import type { ChatMessage, ChatSession } from '@/types/api'

interface QaResponse<T = any> {
  success: boolean
  code: number
  message: string
  data?: T
}

interface QaSessionResponse {
  id: number
  title: string
  features?: {
    knowledge_base?: boolean
    weather?: boolean
    voice?: boolean
  }
  created_at: string
}

interface QaMessageResponse {
  id: number
  session_id: number
  role: 'user' | 'assistant'
  content: string
  message_type: 'text' | 'voice'
  created_at: string
}

interface QaFeatures {
  knowledge_base?: boolean
  weather?: boolean
  voice?: boolean
}

export const useQaStore = defineStore('qa', () => {
  // 状态
  const sessions = ref<ChatSession[]>([])
  const currentSession = ref<ChatSession | null>(null)
  const messages = ref<ChatMessage[]>([])
  const isLoading = ref(false)
  const isTyping = ref(false)

  const normalizeFeatures = (features?: QaFeatures) => ({
    knowledge_base: !!features?.knowledge_base,
    weather: !!features?.weather,
    voice: !!features?.voice
  })

  const shouldCreateNewSession = (features?: QaFeatures) => {
    if (!currentSession.value) return true
    if (!features) return false
    const current = normalizeFeatures(currentSession.value.features)
    const next = normalizeFeatures(features)
    return (
      current.knowledge_base !== next.knowledge_base ||
      current.weather !== next.weather ||
      current.voice !== next.voice
    )
  }

  // 创建新会话
  const createSession = async (title?: string, features?: QaFeatures) => {
    try {
      const payload = {
        title: title || '新对话',
        features: features ? normalizeFeatures(features) : undefined
      }
      const response = await api.post<any>('/qa/sessions', payload)
      console.log('Create session response:', response)

      const sessionPayload = response.data?.session
      if (!sessionPayload) {
        return { success: false, error: '创建对话失败' }
      }

      const newSession: ChatSession = {
        id: sessionPayload.id,
        user_id: 0,
        title: sessionPayload.title,
        features: sessionPayload.features,
        created_at: sessionPayload.created_at,
        updated_at: sessionPayload.created_at
      }

      sessions.value.unshift(newSession)
      currentSession.value = newSession
      messages.value = []

      return { success: true, data: newSession }
    } catch (error) {
      console.error('Failed to create session:', error)
      return { success: false, error: '创建对话失败' }
    }
  }

  // 获取所有会话
  const fetchSessions = async (page = 1, size = 20) => {
    try {
      const response = await api.get<any>('/qa/sessions', {
        params: { page, size }
      })
      const items = response.data?.items || []
      sessions.value = items.map((session: any) => ({
        id: session.id,
        user_id: 0,
        title: session.title,
        features: session.features,
        created_at: session.created_at,
        updated_at: session.created_at
      }))
      return { success: true, data: sessions.value }
    } catch (error) {
      console.error('Failed to fetch sessions:', error)
      return { success: false, error: '获取对话列表失败' }
    }
  }

  // 切换会话
  const switchSession = async (sessionId: number) => {
    try {
      const response = await api.get<any>(`/qa/sessions/${sessionId}/messages`, {
        params: { page: 1, size: 50 }
      })
      const items = response.data?.items || []
      const session = sessions.value.find(s => s.id === sessionId)
      if (session) {
        currentSession.value = session
      }
      messages.value = items.map((msg: any) => ({
        id: msg.id,
        role: msg.role,
        content: msg.content,
        session_id: msg.session_id,
        message_type: msg.message_type,
        created_at: msg.created_at
      }))

      return { success: true }
    } catch (error) {
      console.error('Failed to switch session:', error)
      return { success: false, error: '切换对话失败' }
    }
  }

  // 发送消息
  const sendMessage = async (content: string, options?: QaFeatures) => {
    if (!content.trim()) return { success: false, error: '内容不能为空' }

    if (shouldCreateNewSession(options)) {
      const created = await createSession(undefined, options)
      if (!created.success) {
        return created
      }
    }

    const targetSessionId = currentSession.value?.id
    if (!targetSessionId) {
      return { success: false, error: '会话创建失败' }
    }

    isLoading.value = true
    isTyping.value = true

    const userMessage: ChatMessage = {
      id: Date.now(),
      role: 'user',
      content,
      session_id: targetSessionId,
      message_type: 'text',
      timestamp: new Date().toISOString()
    }
    messages.value.push(userMessage)

    try {
      const response = await api.post<any>('/qa/messages', {
        content,
        session_id: targetSessionId,
        message_type: 'text'
      })
      console.log('Send message response:', response)

      const messagePayload = response.data?.message
      if (messagePayload) {
        messages.value.push({
          id: messagePayload.id,
          role: messagePayload.role,
          content: messagePayload.content,
          session_id: messagePayload.session_id,
          message_type: messagePayload.message_type,
          created_at: messagePayload.created_at
        })
      }

      return { success: true }
    } catch (error) {
      console.error('Failed to send message:', error)
      return { success: false, error: '发送消息失败' }
    } finally {
      isTyping.value = false
      isLoading.value = false
    }
  }

  // 删除会话
  const deleteSession = async (sessionId: number) => {
    try {
      console.warn('Delete API not implemented; removing locally.')
      sessions.value = sessions.value.filter(s => s.id !== sessionId)

      if (currentSession.value?.id === sessionId) {
        currentSession.value = null
        messages.value = []
      }

      return { success: true }
    } catch (error) {
      console.error('Failed to delete session:', error)
      return { success: false, error: '删除对话失败' }
    }
  }

  // 清空当前对话
  const clearCurrentSession = () => {
    messages.value = []
  }

  return {
    // 状态
    sessions,
    currentSession,
    messages,
    isLoading,
    isTyping,

    // 方法
    createSession,
    fetchSessions,
    switchSession,
    sendMessage,
    deleteSession,
    clearCurrentSession
  }
})
