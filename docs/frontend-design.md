# WanderFlow - 前端架构设计文档（基于实际界面需求）

## 目录
1. [架构概述](#架构概述)
2. [技术选型](#技术选型)
3. [页面结构分析](#页面结构分析)
4. [前端架构设计](#前端架构设计)
5. [组件设计](#组件设计)
6. [状态管理](#状态管理)
7. [路由设计](#路由设计)
8. [API层设计](#api层设计)
9. [样式系统](#样式系统)
10. [构建和部署](#构建和部署)

---

## 架构概述

### 项目定位
基于现有demonstration的前端界面，设计一个现代化、模块化、可维护的前端架构。支持7个核心页面：首页、登录、注册、行程规划、AI助手、文案生成、账户设置。

### 设计原则
- **组件化**：页面拆分为可复用的组件
- **模块化**：功能模块独立，便于维护
- **响应式**：移动端优先，适配所有设备
- **类型安全**：TypeScript提供类型检查
- **性能优化**：懒加载、代码分割、缓存策略
- **可测试**：单元测试和集成测试支持

---

## 技术选型

### 核心框架
- **主框架**: Vue 3.4+ (Composition API)
- **类型系统**: TypeScript 5.0+
- **构建工具**: Vite 5.0+
- **包管理器**: pnpm / npm 9+

### UI框架与样式
- **CSS框架**: Tailwind CSS 3.4+
- **组件库**: Headless UI / Radix Vue (无样式组件)
- **图标库**: Font Awesome 6.4+
- **动画库**: Framer Motion (Vue版本) / GSAP
- **样式预处理**: PostCSS + Autoprefixer

### 状态管理
- **全局状态**: Pinia
- **本地状态**: Vue Composition API (ref/reactive)
- **持久化**: Pinia Plugin Persistedstate

### 网络请求
- **HTTP客户端**: Axios
- **WebSocket**: 原生WebSocket / Socket.io-client
- **实时通信**: Server-Sent Events (SSE)

### 开发工具
- **代码规范**: ESLint + Prettier
- **提交规范**: Husky + Commitlint
- **单元测试**: Vitest + Vue Test Utils
- **E2E测试**: Cypress / Playwright

---

## 页面结构分析

基于demonstration分析，前端包含以下页面和功能：

### 1. 首页 (index.html)
**功能**：
- 品牌展示和导航
- 主Banner和CTA
- 功能特性介绍
- 用户统计展示
- 登录/注册入口

**核心组件**：
- Navbar (导航栏)
- Hero (主Banner)
- Features (功能展示)
- CTA (行动号召)
- Footer (页脚)

### 2. 认证页面 (login.html, register.html)
**功能**：
- 用户登录/注册表单
- 表单验证
- 第三方登录
- 记住登录状态
- 密码找回

**核心组件**：
- AuthForm (认证表单)
- SocialLogin (第三方登录)
- PasswordInput (密码输入)
- Checkbox (复选框)

### 3. 行程规划页 (planner.html)
**功能**：
- 行程参数设置（目的地、天数、预算、风格）
- AI生成行程
- 行程列表展示
- 行程编辑
- 导出功能

**核心组件**：
- ItineraryForm (行程表单)
- ItineraryCard (行程卡片)
- StyleSelector (风格选择器)
- BudgetInput (预算输入)
- GenerateButton (生成按钮)

### 4. AI助手页 (qa.html)
**功能**：
- 聊天界面
- 消息列表
- 功能开关（知识库、天气、语音）
- 天气查询面板
- 语音控制面板
- 快捷问题

**核心组件**：
- ChatContainer (聊天容器)
- MessageList (消息列表)
- MessageBubble (消息气泡)
- InputBox (输入框)
- FeatureToggle (功能开关)
- WeatherPanel (天气面板)
- VoicePanel (语音面板)
- QuickQuestions (快捷问题)

### 5. 文案生成页 (copywriter.html)
**功能**：
- 图片上传
- 平台风格选择
- 关键词输入
- 情感基调控制
- 文案生成
- 结果预览

**核心组件**：
- ImageUploader (图片上传)
- PlatformSelector (平台选择器)
- KeywordInput (关键词输入)
- EmotionSlider (情感滑块)
- GenerateButton (生成按钮)
- ResultPreview (结果预览)

### 6. 设置页 (settings.html)
**功能**：
- 用户信息展示
- 头像上传
- 偏好设置（语言、货币、主题）
- 隐私与安全
- 会员信息

**核心组件**：
- UserProfile (用户资料)
- AvatarUpload (头像上传)
- PreferenceSettings (偏好设置)
- SecuritySettings (安全设置)
- SubscriptionInfo (订阅信息)

---

## 前端架构设计

### 目录结构

```
frontend/
├── public/                     # 静态资源
│   ├── favicon.ico
│   └── images/
│
├── src/
│   ├── main.ts                # 应用入口
│   ├── App.vue                # 根组件
│   ├── router/
│   │   └── index.ts           # 路由配置
│   │
│   ├── views/                 # 【页面组件】
│   │   ├── Home.vue
│   │   ├── Login.vue
│   │   ├── Register.vue
│   │   ├── Planner.vue
│   │   ├── QA.vue
│   │   ├── Copywriter.vue
│   │   └── Settings.vue
│   │
│   ├── components/            # 【公共组件】
│   │   ├── common/
│   │   │   ├── Navbar.vue
│   │   │   ├── Footer.vue
│   │   │   ├── Button.vue
│   │   │   └── Input.vue
│   │   │
│   │   ├── auth/
│   │   │   ├── AuthForm.vue
│   │   │   ├── SocialLogin.vue
│   │   │   └── PasswordInput.vue
│   │   │
│   │   ├── chat/
│   │   │   ├── ChatContainer.vue
│   │   │   ├── MessageList.vue
│   │   │   ├── MessageBubble.vue
│   │   │   └── InputBox.vue
│   │   │
│   │   ├── planner/
│   │   │   ├── ItineraryForm.vue
│   │   │   ├── ItineraryCard.vue
│   │   │   └── StyleSelector.vue
│   │   │
│   │   ├── copywriter/
│   │   │   ├── ImageUploader.vue
│   │   │   ├── PlatformSelector.vue
│   │   │   ├── KeywordInput.vue
│   │   │   ├── EmotionSlider.vue
│   │   │   └── ResultPreview.vue
│   │   │
│   │   └── settings/
│   │       ├── UserProfile.vue
│   │       ├── PreferenceSettings.vue
│   │       ├── SecuritySettings.vue
│   │       └── SubscriptionInfo.vue
│   │
│   ├── composables/           # 【组合式函数】
│   │   ├── useAuth.ts
│   │   ├── useApi.ts
│   │   ├── useChat.ts
│   │   ├── useWeather.ts
│   │   ├── useVoice.ts
│   │   └── useFileUpload.ts
│   │
│   ├── stores/                # 【Pinia状态管理】
│   │   ├── auth.ts
│   │   ├── user.ts
│   │   ├── chat.ts
│   │   ├── itinerary.ts
│   │   └── settings.ts
│   │
│   ├── utils/                 # 【工具函数】
│   │   ├── api.ts
│  .ts
│   │   ├── auth │   ├── validation.ts
│   │   ├── date.ts
│   │   └── constants.ts
│   │
│   ├── types/                 # 【TypeScript类型定义】
│   │   ├── user.ts
│   │   ├── itinerary.ts
│   │   ├── chat.ts
│   │   └── api.ts
│   │
│   ├── assets/                # 资源文件
│   │   ├── styles/
│   │   │   ├── main.css
│   │   │   └── variables.css
│   │   └── icons/
│   │
│   └── styles/                # 全局样式
│       ├── main.css
│       ├── tailwind.css
│       └── components.css
│
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
├── tailwind.config.js
└── README.md
```

### 架构分层

```
┌─────────────────────────────────────┐
│           页面层 (Views)              │
│         业务页面组件                  │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│         组件层 (Components)           │
│       可复用业务组件                  │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│      组合式函数层 (Composables)       │
│        逻辑复用                      │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│       状态管理层 (Stores)            │
│        Pinia状态管理                │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│        工具层 (Utils)                │
│      API、工具函数、常量              │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│        类型层 (Types)                │
│       TypeScript类型定义             │
└─────────────────────────────────────┘
```

---

## 组件设计

### 组件分类

#### 1. 页面组件 (Views)
- **职责**：页面整体布局和路由
- **特点**：不可复用，每个路由对应一个
- **内容**：包含业务组件的组合

#### 2. 业务组件 (Business Components)
- **职责**：特定业务逻辑的UI展示
- **特点**：可复用，与业务域相关
- **示例**：ChatContainer、ItineraryForm、ImageUploader

#### 3. 基础组件 (Base Components)
- **职责**：通用的UI基础元素
- **特点**：高度可复用，与业务无关
- **示例**：Button、Input、Modal、Dropdown

### 组件通信

#### Props & Emits
```typescript
// 子组件
<template>
  <button @click="handleClick">{{ title }}</button>
</template>

<script setup lang="ts">
interface Props {
  title: string
  type?: 'primary' | 'secondary'
}

const props = withDefaults(defineProps<Props>(), {
  type: 'primary'
})

const emit = defineEmits<{
  click: []
}>()

const handleClick = () => {
  emit('click')
}
</script>
```

#### Provide/Inject
```typescript
// 父组件
provide('theme', 'dark')

// 子组件
const theme = inject('theme')
```

#### Event Bus (mitt)
```typescript
// utils/eventBus.ts
import mitt from 'mitt'
export const eventBus = mitt()

// 使用
eventBus.emit('user-login', userData)
eventBus.on('user-login', (data) => { ... })
```

---

## 状态管理

### Pinia Store设计

#### 1. Auth Store (auth.ts)
```typescript
interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  loading: boolean
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: null,
    token: localStorage.getItem('token'),
    isAuthenticated: false,
    loading: false
  }),

  getters: {
    isLoggedIn: (state) => !!state.token,
    userName: (state) => state.user?.name || ''
  },

  actions: {
    async login(credentials: LoginCredentials) {
      // 登录逻辑
    },
    async logout() {
      // 登出逻辑
    }
  }
})
```

#### 2. Chat Store (chat.ts)
```typescript
interface ChatState {
  messages: ChatMessage[]
  isLoading: boolean
  knowledgeBaseEnabled: boolean
  weatherEnabled: boolean
  voiceEnabled: boolean
  currentSessionId: string | null
}

export const useChatStore = defineStore('chat', {
  state: (): ChatState => ({
    messages: [],
    isLoading: false,
    knowledgeBaseEnabled: false,
    weatherEnabled: false,
    voiceEnabled: false,
    currentSessionId: null
  }),

  actions: {
    async sendMessage(content: string) {
      // 发送消息逻辑
    },
    toggleFeature(feature: 'knowledgeBase' | 'weather' | 'voice') {
      // 切换功能开关
    }
  }
})
```

#### 3. Itinerary Store (itinerary.ts)
```typescript
interface ItineraryState {
  itineraries: Itinerary[]
  currentItinerary: Itinerary | null
  loading: boolean
}

export const useItineraryStore = defineStore('itinerary', {
  state: (): ItineraryState => ({
    itineraries: [],
    currentItinerary: null,
    loading: false
  }),

  actions: {
    async generateItinerary(params: ItineraryParams) {
      // 生成行程逻辑
    },
    async saveItinerary(itinerary: Itinerary) {
      // 保存行程逻辑
    }
  }
})
```

---

## 路由设计

### 路由配置 (router/index.ts)

```typescript
import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresGuest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue'),
    meta: { requiresGuest: true }
  },
  {
    path: '/planner',
    name: 'Planner',
    component: () => import('@/views/Planner.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/qa',
    name: 'QA',
    component: () => import('@/views/QA.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/copywriter',
    name: 'Copywriter',
    component: () => import('@/views/Copywriter.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('@/views/Settings.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next('/planner')
  } else {
    next()
  }
})

export default router
```

---

## API层设计

### API封装 (utils/api.ts)

```typescript
import axios, { AxiosInstance, AxiosRequestConfig } from 'axios'

class ApiClient {
  private client: AxiosInstance

  constructor() {
    this.client = axios.create({
      baseURL: import.meta.env.VITE_API_BASE_URL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json'
      }
    })

    this.setupInterceptors()
  }

  private setupInterceptors() {
    // 请求拦截器
    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('token')
        if (token) {
          config.headers.Authorization = `Bearer ${token}`
        }
        return config
      },
      (error) => Promise.reject(error)
    )

    // 响应拦截器
    this.client.interceptors.response.use(
      (response) => response.data,
      (error) => {
        if (error.response?.status === 401) {
          // token过期，跳转登录
          window.location.href = '/login'
        }
        return Promise.reject(error)
      }
    )
  }

  async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    return this.client.get(url, config)
  }

  async post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    return this.client.post(url, data, config)
  }

  async put<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    return this.client.put(url, data, config)
  }

  async delete<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    return this.client.delete(url, config)
  }
}

export const apiClient = new ApiClient()
```

### API模块

```typescript
// api/auth.ts
export const authApi = {
  login: (credentials: LoginCredentials) =>
    apiClient.post<{ user: User; token: string }>('/auth/login', credentials),

  register: (data: RegisterData) =>
    apiClient.post<{ user: User; token: string }>('/auth/register', data),

  logout: () => apiClient.post('/auth/logout'),

  getProfile: () => apiClient.get<User>('/auth/profile')
}

// api/chat.ts
export const chatApi = {
  sendMessage: (data: { content: string; sessionId?: string }) =>
    apiClient.post<ChatMessage>('/chat/message', data),

  getHistory: (sessionId: string) =>
    apiClient.get<ChatMessage[]>(`/chat/history/${sessionId}`),

  queryWeather: (city: string) =>
    apiClient.get<WeatherData>(`/weather/${city}`)
}
```

---

## 样式系统

### Tailwind CSS配置 (tailwind.config.js)

```javascript
module.exports = {
  content: ['./index.html', './src/**/*.{vue,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0fdfa',
          100: '#ccfbf1',
          500: '#14b8a6',
          600: '#0d9488',
          700: '#0f766e'
        }
      },
      fontFamily: {
        sans: ['Poppins', 'Nunito', 'sans-serif']
      },
      boxShadow: {
        'glass': '0 8px 32px 0 rgba(31, 38, 135, 0.37)'
      },
      backdropBlur: {
        xs: '2px'
      }
    }
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography')
  ]
}
```

### 自定义CSS (styles/main.css)

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* CSS变量 */
:root {
  --color-primary: #00D4AA;
  --color-secondary: #45B7D1;
  --gradient-main: linear-gradient(135deg, #00D4AA 0%, #45B7D1 100%);
}

/* 组件样式 */
@layer components {
  .btn-primary {
    @apply bg-gradient-to-r from-teal-400 to-blue-500 text-white font-semibold py-2 px-6 rounded-full hover:shadow-lg transition-all;
  }

  .glass-card {
    @apply bg-white/80 backdrop-blur-md border border-white/50 rounded-2xl shadow-glass;
  }

  .input-field {
    @apply w-full px-4 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-400 focus:border-transparent;
  }
}

/* 动画 */
@layer utilities {
  .fade-in-up {
    animation: fadeInUp 0.6s ease-out;
  }

  .float-anim {
    animation: float 6s ease-in-out infinite;
  }

  @keyframes fadeInUp {
    from {
      opacity: 0;
      transform: translateY(30px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  @keyframes float {
    0%, 100% {
      transform: translateY(0);
    }
    50% {
      transform: translateY(-20px);
    }
  }
}
```

---

## 构建和部署

### Vite配置 (vite.config.ts)

```typescript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')
    }
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  },
  build: {
    target: 'esnext',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['vue', 'vue-router', 'pinia'],
          ui: ['@headlessui/vue', '@heroicons/vue']
        }
      }
    }
  }
})
```

### 环境变量

```
# .env.development
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_APP_TITLE=WanderFlow
VITE_ENABLE_MOCK=true

# .env.production
VITE_API_BASE_URL=https://api.wanderflow.com
VITE_APP_TITLE=WanderFlow
VITE_ENABLE_MOCK=false
```

---

## 性能优化策略

### 1. 代码分割
- 路由懒加载
- 组件动态导入
- 第三方库分离

### 2. 资源优化
- 图片懒加载
- 资源压缩
- CDN加速

### 3. 缓存策略
- 浏览器缓存
- HTTP缓存头
- Service Worker离线缓存

### 4. 渲染优化
- Virtual Scrolling (长列表)
- 组件按需渲染
- 防抖节流

---

## 测试策略

### 单元测试
- 组件测试 (Vue Test Utils)
- 工具函数测试 (Vitest)
- Store测试

### E2E测试
- 用户流程测试 (Cypress)
- API集成测试
- 跨浏览器测试

---

## 总结

本架构设计基于实际前端界面需求，具有以下特点：

1. **清晰的分层**：Views → Components → Composables → Stores → Utils
2. **高度模块化**：功能模块独立，易于维护和扩展
3. **类型安全**：TypeScript全覆盖，减少运行时错误
4. **组件化设计**：可复用的组件库，提高开发效率
5. **现代化技术栈**：Vue 3 + Vite + Tailwind CSS + Pinia
6. **性能优化**：代码分割、懒加载、缓存策略
7. **开发体验**：热更新、TypeScript、ESLint/Prettier

该架构能够满足当前7个页面的所有功能需求，并为未来功能扩展提供了良好的基础。
