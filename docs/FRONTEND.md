# 前端开发指南

## 目录

- [技术栈](#技术栈)
- [项目结构](#项目结构)
- [核心概念](#核心概念)
- [状态管理](#状态管理)
- [路由管理](#路由管理)
- [组件开发](#组件开发)
- [样式指南](#样式指南)
- [开发规范](#开发规范)
- [测试指南](#测试指南)
- [常见问题](#常见问题)

## 技术栈

- **框架**: Vue 3.4+ (Composition API)
- **语言**: TypeScript 5.0+
- **构建工具**: Vite 5.0+
- **样式**: Tailwind CSS 3.4+
- **状态管理**: Pinia
- **路由**: Vue Router 4
- **HTTP 客户端**: Axios
- **开发工具**: ESLint + Prettier

## 项目结构

```
frontend/
├── public/                    # 静态资源
│   └── vite.svg
│
├── src/                       # 源代码
│   ├── assets/                # 资源文件
│   │   └── logo.svg
│   │
│   ├── components/            # 公共组件
│   │   ├── common/            # 通用组件
│   │   ├── auth/              # 认证组件
│   │   ├── chat/              # 聊天组件
│   │   ├── planner/           # 行程规划组件
│   │   ├── copywriter/        # 文案生成组件
│   │   └── settings/          # 设置组件
│   │
│   ├── composables/           # 组合式函数
│   │   ├── useApi.ts          # API 请求
│   │   ├── useLocalStorage.ts # 本地存储
│   │   └── useTheme.ts        # 主题切换
│   │
│   ├── router/                # 路由配置
│   │   └── index.ts
│   │
│   ├── stores/                # Pinia 状态管理
│   │   ├── auth.ts            # 认证状态
│   │   ├── itinerary.ts       # 行程管理
│   │   ├── qa.ts              # 问答管理
│   │   └── copywriting.ts     # 文案管理
│   │
│   ├── types/                 # 类型定义
│   │   └── api.ts             # API 类型
│   │
│   ├── utils/                 # 工具函数
│   │   ├── common.ts          # 通用工具
│   │   ├── date.ts            # 日期工具
│   │   └── validation.ts      # 验证工具
│   │
│   ├── views/                 # 页面组件
│   │   ├── Home.vue           # 首页
│   │   ├── Login.vue          # 登录页
│   │   ├── Register.vue       # 注册页
│   │   ├── Planner.vue        # 行程规划页
│   │   ├── QA.vue             # AI 助手页
│   │   ├── Copywriter.vue     # 文案生成页
│   │   └── Settings.vue       # 设置页
│   │
│   ├── App.vue                # 根组件
│   └── main.ts                # 应用入口
│
├── index.html                 # HTML 入口
├── package.json               # 依赖配置
├── vite.config.ts             # Vite 配置
├── tsconfig.json              # TypeScript 配置
├── tailwind.config.js         # Tailwind 配置
└── postcss.config.js          # PostCSS 配置
```

## 核心概念

### Composition API

Vue 3 的 Composition API 提供了更灵活的组件逻辑组织方式：

```vue
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

// 响应式数据
const count = ref(0)
const doubleCount = computed(() => count.value * 2)

// 方法
const increment = () => {
  count.value++
}

// 生命周期
onMounted(() => {
  console.log('Component mounted')
})
</script>
```

### Props 和 Emits

```vue
<!-- 子组件 -->
<script setup lang="ts">
interface Props {
  title: string
  size?: 'small' | 'medium' | 'large'
}

const props = defineProps<Props>()

const emit = defineEmits<{
  update: [value: string]
  click: []
}>()

const handleClick = () => {
  emit('click')
}
</script>

<!-- 父组件 -->
<ChildComponent
  title="Hello"
  size="medium"
  @update="handleUpdate"
  @click="handleClick"
/>
```

### 插槽 (Slots)

```vue
<!-- BaseButton.vue -->
<template>
  <button class="btn">
    <slot>默认文本</slot>
  </button>
</template>

<!-- 使用 -->
<BaseButton>自定义按钮文本</BaseButton>
<BaseButton />
```

## 状态管理

### Pinia Store

使用 Pinia 进行状态管理：

```typescript
// stores/counter.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useCounterStore = defineStore('counter', () => {
  // 状态
  const count = ref(0)

  // 计算属性
  const doubleCount = computed(() => count.value * 2)

  // 方法
  const increment = () => {
    count.value++
  }

  const reset = () => {
    count.value = 0
  }

  return {
    count,
    doubleCount,
    increment,
    reset
  }
})
```

```vue
<!-- 在组件中使用 -->
<script setup lang="ts">
import { useCounterStore } from '@/stores/counter'

const counterStore = useCounterStore()
</script>

<template>
  <div>
    <p>Count: {{ counterStore.count }}</p>
    <p>Double: {{ counterStore.doubleCount }}</p>
    <button @click="counterStore.increment">Increment</button>
  </div>
</template>
```

### Store 模块

#### 认证 Store (stores/auth.ts)

```typescript
import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { User } from '@/types/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)
  const isAuthenticated = ref(false)

  const login = async (email: string, password: string) => {
    // 登录逻辑
  }

  const logout = () => {
    user.value = null
    token.value = null
    isAuthenticated.value = false
  }

  return {
    user,
    token,
    isAuthenticated,
    login,
    logout
  }
})
```

#### 行程 Store (stores/itinerary.ts)

```typescript
import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Itinerary } from '@/types/api'

export const useItineraryStore = defineStore('itinerary', () => {
  const itineraries = ref<Itinerary[]>([])
  const currentItinerary = ref<Itinerary | null>(null)

  const fetchItineraries = async () => {
    // 获取行程列表
  }

  const createItinerary = async (data: any) => {
    // 创建行程
  }

  return {
    itineraries,
    currentItinerary,
    fetchItineraries,
    createItinerary
  }
})
```

## 路由管理

### 路由配置 (router/index.ts)

```typescript
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/Home.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/Login.vue'),
      meta: { requiresGuest: true }
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/Register.vue'),
      meta: { requiresGuest: true }
    },
    {
      path: '/planner',
      name: 'planner',
      component: () => import('@/views/Planner.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/qa',
      name: 'qa',
      component: () => import('@/views/QA.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/copywriter',
      name: 'copywriter',
      component: () => import('@/views/Copywriter.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/settings',
      name: 'settings',
      component: () => import('@/views/Settings.vue'),
      meta: { requiresAuth: true }
    }
  ]
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

### 导航守卫

```typescript
// 全局前置守卫
router.beforeEach(async (to, from, next) => {
  // 加载用户信息
  const authStore = useAuthStore()
  if (!authStore.user && authStore.token) {
    await authStore.fetchUser()
  }
  next()
})

// 全局后置钩子
router.afterEach((to, from) => {
  // 页面访问统计
  console.log(`Navigated from ${from.name} to ${to.name}`)
})
```

## 组件开发

### 组件设计原则

1. **单一职责**: 每个组件只负责一个功能
2. **可复用性**: 设计通用的公共组件
3. **可维护性**: 代码结构清晰，易于理解
4. **可测试性**: 组件逻辑独立，易于单元测试

### 组件示例

#### 通用按钮组件

```vue
<!-- components/common/BaseButton.vue -->
<template>
  <button
    :class="[
      'px-4 py-2 rounded-lg font-medium transition-colors',
      {
        'bg-teal-500 text-white hover:bg-teal-600': variant === 'primary',
        'bg-slate-200 text-slate-700 hover:bg-slate-300': variant === 'secondary',
        'bg-red-500 text-white hover:bg-red-600': variant === 'danger',
        'opacity-50 cursor-not-allowed': disabled
      }
    ]"
    :disabled="disabled"
    @click="handleClick"
  >
    <slot />
  </button>
</template>

<script setup lang="ts">
interface Props {
  variant?: 'primary' | 'secondary' | 'danger'
  disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  disabled: false
})

const emit = defineEmits<{
  click: []
}>()

const handleClick = () => {
  if (!props.disabled) {
    emit('click')
  }
}
</script>
```

#### 加载状态组件

```vue
<!-- components/common/LoadingSpinner.vue -->
<template>
  <div class="flex justify-center items-center">
    <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-teal-500"></div>
  </div>
</template>

<script setup lang="ts">
// 无需脚本逻辑
</script>
```

#### 卡片组件

```vue
<!-- components/common/Card.vue -->
<template>
  <div class="bg-white rounded-lg shadow-md p-6">
    <div v-if="$slots.header" class="border-b border-slate-200 pb-4 mb-4">
      <slot name="header" />
    </div>
    <div class="mb-4">
      <slot />
    </div>
    <div v-if="$slots.footer" class="border-t border-slate-200 pt-4 mt-4">
      <slot name="footer" />
    </div>
  </div>
</template>

<script setup lang="ts">
// 无需脚本逻辑
</script>
```

### 表单组件

```vue
<!-- components/common/BaseInput.vue -->
<template>
  <div class="space-y-2">
    <label v-if="label" :for="inputId" class="block text-sm font-medium text-slate-700">
      {{ label }}
    </label>
    <input
      :id="inputId"
      v-model="inputValue"
      :type="type"
      :placeholder="placeholder"
      :disabled="disabled"
      :class="[
        'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-400',
        {
          'border-slate-300': !error,
          'border-red-500': error,
          'bg-slate-100 cursor-not-allowed': disabled
        }
      ]"
      @input="handleInput"
      @blur="handleBlur"
    />
    <p v-if="error" class="text-sm text-red-600">{{ error }}</p>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

interface Props {
  label?: string
  modelValue: string | number
  type?: string
  placeholder?: string
  disabled?: boolean
  error?: string
}

const props = withDefaults(defineProps<Props>(), {
  type: 'text',
  placeholder: '',
  disabled: false
})

const emit = defineEmits<{
  'update:modelValue': [value: string | number]
  blur: []
}>()

const inputId = computed(() => `input-${Math.random().toString(36).substr(2, 9)}`)
const inputValue = ref(props.modelValue)

const handleInput = (event: Event) => {
  const target = event.target as HTMLInputElement
  emit('update:modelValue', target.value)
}

const handleBlur = () => {
  emit('blur')
}
</script>
```

## 样式指南

### Tailwind CSS 类名约定

1. **一致的顺序**: 按照属性重要性排序
2. **语义化命名**: 使用有意义的类名
3. **响应式设计**: 移动端优先

```vue
<template>
  <div class="p-4 md:p-6 lg:p-8">
    <h1 class="text-2xl font-bold text-slate-800 mb-4">
      标题
    </h1>
    <p class="text-slate-600 leading-relaxed">
      内容
    </p>
  </div>
</template>
```

### 自定义样式

在 `tailwind.config.js` 中扩展主题：

```javascript
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0fdfa',
          500: '#14b8a6',
          900: '#134e4a'
        }
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif']
      }
    }
  }
}
```

### CSS 变量

```css
:root {
  --color-primary: #14b8a6;
  --color-primary-dark: #0f766e;
}

.btn-primary {
  background-color: var(--color-primary);
}

.btn-primary:hover {
  background-color: var(--color-primary-dark);
}
```

## 开发规范

### 代码风格

1. **使用 TypeScript 严格模式**
2. **组件命名**: PascalCase (`UserProfile.vue`)
3. **文件名**: PascalCase (`UserProfile.ts`)
4. **变量/函数**: camelCase (`getUserInfo`)
5. **常量**: UPPER_CASE (`API_BASE_URL`)

### 目录约定

```
components/
├── common/          # 通用组件
│   ├── BaseButton.vue
│   ├── BaseInput.vue
│   └── LoadingSpinner.vue
├── auth/            # 认证相关
│   ├── LoginForm.vue
│   └── RegisterForm.vue
└── ...
```

### Props 定义

```typescript
// ✅ 推荐
interface Props {
  title: string
  size?: 'small' | 'medium' | 'large'
  disabled?: boolean
}

defineProps<Props>()

// ❌ 不推荐
defineProps({
  title: String,
  size: {
    type: String,
    default: 'medium'
  }
})
```

### Emits 定义

```typescript
// ✅ 推荐
const emit = defineEmits<{
  update: [value: string]
  click: []
  change: [event: Event]
}>()

// ❌ 不推荐
const emit = defineEmits(['update', 'click'])
```

### 注释规范

```vue
<script setup lang="ts">
/**
 * 用户资料组件
 * 用于展示和编辑用户信息
 *
 * @author Alex Chen
 * @version 1.0.0
 */

// 响应式数据
const user = ref<User | null>(null)

// 方法：获取用户信息
const fetchUser = async () => {
  // 实现
}
</script>
```

## 开发工具

### ESLint 配置

```javascript
// .eslintrc.js
module.exports = {
  extends: [
    'eslint:recommended',
    '@vue/typescript/recommended',
    'plugin:vue/vue3-essential'
  ],
  rules: {
    'vue/multi-word-component-names': 'off',
    '@typescript-eslint/no-unused-vars': 'error'
  }
}
```

### Prettier 配置

```javascript
// .prettierrc
{
  "semi": false,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "none",
  "printWidth": 100
}
```

### 脚本命令

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vue-tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext .vue,.js,.ts --fix",
    "format": "prettier --write src/"
  }
}
```

## 性能优化

### 1. 组件懒加载

```typescript
const Home = () => import('@/views/Home.vue')
const About = () => import('@/views/About.vue')
```

### 2. 响应式优化

```typescript
// 使用 readonly 防止意外修改
const readonlyData = readonly(expensiveComputation())

// 使用 shallowRef 减少深层响应
const shallowData = shallowRef(largeObject)

// 使用 markRaw 标记非响应式对象
const nonReactiveData = markRaw(externalLibrary)
```

### 3. 虚拟滚动

```vue
<template>
  <VirtualList
    :items="largeList"
    :item-height="50"
    :container-height="400"
  >
    <template #default="{ item }">
      <div class="p-4">{{ item.title }}</div>
    </template>
  </VirtualList>
</template>
```

### 4. 缓存策略

```typescript
// 使用 computed 缓存
const expensiveValue = computed(() => {
  return expensiveOperation()
})

// 使用缓存装饰器
const cachedFetch = useMemoize(fetchData)
```

## 测试指南

### 单元测试

使用 Vitest 进行单元测试：

```typescript
// tests/components/BaseButton.test.ts
import { mount } from '@vue/test-utils'
import BaseButton from '@/components/common/BaseButton.vue'

describe('BaseButton', () => {
  it('renders button text', () => {
    const wrapper = mount(BaseButton, {
      slots: {
        default: 'Click me'
      }
    })
    expect(wrapper.text()).toBe('Click me')
  })

  it('emits click event when clicked', async () => {
    const wrapper = mount(BaseButton)
    await wrapper.trigger('click')
    expect(wrapper.emitted('click')).toHaveLength(1)
  })
})
```

### 组件测试

```typescript
// tests/views/Login.test.ts
import { describe, it, expect } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { mount } from '@vue/test-utils'
import Login from '@/views/Login.vue'

describe('Login', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('submits login form', async () => {
    const wrapper = mount(Login)
    await wrapper.find('input[type="email"]').setValue('test@example.com')
    await wrapper.find('input[type="password"]').setValue('password')
    await wrapper.find('form').trigger('submit.prevent')
    expect(wrapper.emitted('login')).toBeTruthy()
  })
})
```

## 常见问题

### Q: 如何处理异步请求？

A: 使用 `async/await` 和错误处理：

```typescript
const fetchData = async () => {
  try {
    loading.value = true
    const data = await api.get('/data')
    data.value = data
  } catch (error) {
    console.error('Failed to fetch data:', error)
  } finally {
    loading.value = false
  }
}
```

### Q: 如何实现组件通信？

A: 使用 Props/Emits 或 Provide/Inject：

```typescript
// 父组件
const message = ref('Hello from parent')

// 子组件
const { parent } = getCurrentInstance()
const parentMessage = computed(() => parent?.props.message)
```

### Q: 如何优化大型列表渲染？

A: 使用虚拟滚动或分页：

```vue
<template>
  <div v-if="visibleItems.length">
    <div v-for="item in visibleItems" :key="item.id">
      {{ item.title }}
    </div>
  </div>
</template>

<script setup lang="ts">
const visibleItems = computed(() => {
  return items.value.slice(0, visibleCount.value)
})
</script>
```

### Q: 如何实现主题切换？

A: 使用 CSS 变量和组合式函数：

```typescript
// composables/useTheme.ts
export function useTheme() {
  const theme = ref<'light' | 'dark'>('light')

  const toggleTheme = () => {
    theme.value = theme.value === 'light' ? 'dark' : 'light'
    document.documentElement.classList.toggle('dark', theme.value === 'dark')
  }

  return { theme, toggleTheme }
}
```

## 最佳实践

1. **组件拆分**: 保持组件小而专注
2. **状态提升**: 合理管理组件状态
3. **性能优化**: 使用缓存和懒加载
4. **错误处理**: 完善的错误边界
5. **可访问性**: 遵循 a11y 指南
6. **国际化**: 预留多语言支持
7. **测试覆盖**: 编写全面的测试用例
8. **文档更新**: 及时更新代码文档

---

更多详细信息请参考 [主 README](../README.md)
