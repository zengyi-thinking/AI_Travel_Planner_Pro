// API 响应类型定义
export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
}

// 分页响应类型
export interface PaginatedResponse<T = any> {
  items: T[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

// API 请求参数类型
export interface ApiRequest {
  [key: string]: any
}

// 用户相关类型
export interface User {
  id: number
  email: string
  name: string
  avatar?: string
  membership_level: 'free' | 'pro'
  created_at: string
  updated_at: string
}

export interface LoginRequest {
  email: string
  password: string
}

export interface RegisterRequest {
  email: string
  password: string
  name: string
}

// 行程规划相关类型
export interface Itinerary {
  id: number
  user_id: number
  title: string
  destination: string
  departure?: string | null
  days: number
  budget: number | null
  travel_style: 'leisure' | 'adventure' | 'foodie'
  status: 'draft' | 'active' | 'completed' | 'archived'
  ai_generated?: boolean
  days_detail?: DayPlan[]
  created_at: string
  updated_at: string
}

export interface ItineraryCreateRequest {
  title: string
  destination: string
  departure?: string | null
  days: number
  budget?: number | null
  travel_style: 'leisure' | 'adventure' | 'foodie'
}

export interface DayPlan {
  day: number
  activities: Activity[]
  accommodation?: string
  meals: string[]
}

export interface Activity {
  time: string
  title: string
  description: string
  location: string
  duration: string
  cost?: number
  tips?: string[]
}

// QA 聊天相关类型
export interface ChatMessage {
  id: number
  role: 'user' | 'assistant'
  content: string
  session_id: number
  message_type?: 'text' | 'voice'
  created_at?: string
  timestamp?: string
  metadata?: Record<string, any>
}

export interface ChatSession {
  id: number
  user_id: number
  title: string
  features?: {
    knowledge_base?: boolean
    weather?: boolean
    voice?: boolean
  }
  created_at: string
  updated_at: string
}

export interface QaRequest {
  question: string
  session_id?: string
  context?: Record<string, any>
}

// 文案生成相关类型
export interface CopywritingRequest {
  platform: 'xiaohongshu' | 'wechat' | 'weibo'
  keywords: string[]
  emotion_level: number
  images?: string[]
  custom_style?: string
}

export interface CopywritingResult {
  id: number
  content: string
  platform: string
  keywords: string[]
  created_at: string
  rating?: number | null
}

// 认证相关类型
export interface AuthToken {
  access_token: string
  token_type: string
  expires_in: number
}

export interface AuthResponse {
  access_token: string
  token_type: string
  expires_in: number
  user: User
}

export interface LoginResponse extends AuthResponse {}
export interface RegisterResponse extends AuthResponse {}
