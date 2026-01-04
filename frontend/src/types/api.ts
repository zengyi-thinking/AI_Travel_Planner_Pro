// API 鍝嶅簲绫诲瀷瀹氫箟
export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
}

// 鍒嗛〉鍝嶅簲绫诲瀷
export interface PaginatedResponse<T = any> {
  items: T[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

// API 璇锋眰鍙傛暟绫诲瀷
export interface ApiRequest {
  [key: string]: any
}

// 鐢ㄦ埛鐩稿叧绫诲瀷
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

// 琛岀▼瑙勫垝鐩稿叧绫诲瀷 (V2.0 - 鏀寔涓板瘜鐨勫疄鐢ㄤ俊鎭?
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

  // V2 鏂板瀛楁
  summary?: string
  highlights?: string[]
  best_season?: string
  weather?: string
  actual_cost?: number
  cost_breakdown?: CostBreakdown
  preparation?: PreparationInfo
  tips?: TravelTips
  cover_image?: string

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
  use_strict_json?: boolean
}

// 璐圭敤鏄庣粏
export interface CostBreakdown {
  transportation: number
  accommodation: number
  food: number
  tickets: number
  shopping: number
  other: number
}

// 琛屽墠鍑嗗
export interface PreparationInfo {
  documents: string[]
  essentials: string[]
  suggestions: string[]
  booking_reminders: string[]
}

// 瀹炵敤鎻愮ず
export interface TravelTips {
  transportation?: string
  accommodation?: string
  food?: string
  shopping?: string
  safety?: string
  other?: string[]
}

// 姣忔棩琛岀▼ (V2.0)
export interface DayPlan {
  day_number: number
  title: string
  date?: string
  summary?: string
  activities: Activity[]
  notes?: string
  total_cost?: number
  accommodation?: AccommodationInfo
}

// 娲诲姩淇℃伅 (V2.0 - 鐢ㄦ埛鍙嬪ソ璁捐)
export interface Activity {
  // 鍩烘湰淇℃伅
  title: string
  type: 'attraction' | 'meal' | 'transport' | 'accommodation' | 'shopping' | 'entertainment'
  time: string
  duration: string

  // 鏅偣/娲诲姩淇℃伅
  description: string
  highlights?: string[]
  address?: string
  ticket_price?: number
  need_booking?: boolean
  booking_info?: string

  // 椁愰ギ淇℃伅
  cuisine?: string
  average_cost: number
  recommended_dishes?: string[]
  wait_time?: string
  opening_hours?: string

  // 璐村＋淇℃伅
  best_time?: string
  tips?: string[]
  dress_code?: string

  // 浜ら€氫俊鎭?
  transportation?: TransportationInfo
  parking_info?: string

  // 鎶€鏈暟鎹紙鐢ㄤ簬鍦板浘锛?
  coordinates?: {
    lng: number
    lat: number
  }
}

// 浜ら€氫俊鎭?
export interface TransportationInfo {
  method: string
  from_location?: string
  to_location?: string
  duration: string
  cost: number
  tips?: string
}

// 浣忓淇℃伅
export interface AccommodationInfo {
  name: string
  address: string
  type: string
  facilities?: string[]
  rating?: number
  booking_status?: string
}

// QA 鑱婂ぉ鐩稿叧绫诲瀷
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

// 鏂囨鐢熸垚鐩稿叧绫诲瀷
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

// 璁よ瘉鐩稿叧绫诲瀷
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

