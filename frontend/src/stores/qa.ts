import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/utils/api'
import type { ChatMessage, ChatSession } from '@/types/api'
import { useAuthStore } from './auth'

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
  const qaRequestTimeout = Number(import.meta.env.VITE_QA_TIMEOUT || 60000)

  const normalizeFeatures = (features?: QaFeatures) => ({
    knowledge_base: !!features?.knowledge_base,
    weather: !!features?.weather,
    voice: !!features?.voice
  })

  const getResponsePayload = <T = any>(response: any): T | undefined =>
    response?.data ?? response

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

      const sessionPayload = getResponsePayload<{ session?: QaSessionResponse }>(response)?.session
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
      const items = getResponsePayload<{ items?: QaSessionResponse[] }>(response)?.items || []
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
      const items = getResponsePayload<{ items?: QaMessageResponse[] }>(response)?.items || []
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

  // 发送消息（带流式显示效果）
  const sendMessage = async (content: string, options?: QaFeatures) => {
    if (!content.trim()) return { success: false, error: '内容不能为空' }

    const authStore = useAuthStore()
    const token = authStore.token

    console.log('===== sendMessage 开始 =====')
    console.log('Content:', content)
    console.log('Options:', options)
    console.log('Token:', token)
    console.log('CurrentSession:', currentSession.value)

    if (shouldCreateNewSession(options)) {
      console.log('需要创建新会话...')
      const created = await createSession(undefined, options)
      if (!created.success) {
        return created
      }
    }

    const targetSessionId = currentSession.value?.id
    if (!targetSessionId) {
      console.error('会话ID不存在')
      return { success: false, error: '会话创建失败' }
    }

    console.log('目标会话ID:', targetSessionId)

    isLoading.value = true
    isTyping.value = true

    // 添加用户消息
    const userMessage: ChatMessage = {
      id: Date.now(),
      role: 'user',
      content,
      session_id: targetSessionId,
      message_type: 'text',
      timestamp: new Date().toISOString()
    }
    messages.value.push(userMessage)
    console.log('已添加用户消息，当前消息数:', messages.value.length)

    // 创建一个空白的助手消息
    const assistantMessageId = Date.now() + 1
    const assistantMessage: ChatMessage = {
      id: assistantMessageId,
      role: 'assistant',
      content: '',
      session_id: targetSessionId,
      message_type: 'text',
      created_at: new Date().toISOString()
    }
    messages.value.push(assistantMessage)

    try {
      console.log('发送API请求...')

      const response = await api.post<any>('/qa/messages', {
        content,
        session_id: targetSessionId,
        message_type: 'text'
      }, {
        timeout: qaRequestTimeout
      })

      console.log('===== API 响应 =====')
      console.log('完整响应:', response)

      // 获取助手回复内容
      let assistantContent = ''

      const messagePayload = getResponsePayload<{ message?: QaMessageResponse }>(response)?.message

      if (messagePayload?.content) {
        assistantContent = messagePayload.content
        console.log('✓ 从 response.message.content 获取')
      } else if (messagePayload) {
        assistantContent = typeof messagePayload === 'string' ? messagePayload : JSON.stringify(messagePayload)
        console.log('✓ 从 response.message 获取')
      } else {
        console.error('无法提取消息内容')
        assistantContent = '抱歉，我无法理解您的请求。'
      }

      console.log('助手回复:', assistantContent.substring(0, 100))

      // 只更新当前请求对应的占位消息，避免并发错位
      const targetMessage = messages.value.find(msg => msg.id === assistantMessageId)
      if (targetMessage) {
        targetMessage.content = assistantContent
        console.log('✓ 已更新助手消息')
      }

      isTyping.value = false
      console.log('✓ 消息发送成功')
      return { success: true }
    } catch (error) {
      console.error('===== 发送消息失败 =====')
      console.error('错误类型:', (error as any).constructor.name)
      console.error('错误信息:', (error as any).message)
      console.error('完整错误:', error)

      // 移除空白的助手消息
      const targetIndex = messages.value.findIndex(msg => msg.id === assistantMessageId)
      if (targetIndex >= 0 && !messages.value[targetIndex].content) {
        messages.value.splice(targetIndex, 1)
        console.log('已移除空白助手消息')
      }

      isTyping.value = false
      return { success: false, error: '发送消息失败' }
    } finally {
      isLoading.value = false
      console.log('isLoading 已重置为 false')
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
