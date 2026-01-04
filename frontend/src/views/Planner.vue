<template>
  <div class="bg-[#F8FAFC] h-screen flex overflow-hidden">
    <AppSidebar active="planner">
      <template #footer>
        <div class="p-4 border-t border-slate-100">
          <div class="flex items-center gap-3 p-2 hover:bg-slate-50 rounded-lg cursor-pointer transition-colors">
            <img :src="user?.avatar || 'https://i.pravatar.cc/100?img=12'" class="w-10 h-10 rounded-full" alt="用户头像">
            <div>
              <div class="text-sm font-bold text-slate-700">{{ user?.name || '未登录' }}</div>
              <div class="text-xs text-slate-400">{{ user?.membership_level === 'pro' ? 'Pro 用户' : 'Free 用户' }}</div>
            </div>
          </div>
        </div>
      </template>
    </AppSidebar>

    <main class="flex-1 flex flex-col relative overflow-hidden">
      <PlannerHeader
        :itinerary="currentItinerary"
        :title="headerTitle"
        @open-history="handleOpenHistory"
      />

      <!-- 未登录提示 -->
      <div v-if="!isAuthenticated" class="flex-1 flex items-center justify-center">
        <div class="bg-white rounded-2xl p-8 shadow-xl max-w-md mx-4 text-center">
          <div class="w-20 h-20 bg-teal-100 rounded-full flex items-center justify-center mx-auto mb-6">
            <AppIcon name="lock" class="text-4xl text-teal-600" />
          </div>
          <h2 class="text-2xl font-bold text-slate-800 mb-4">需要登录</h2>
          <p class="text-slate-600 mb-6">请先登录后再使用AI行程规划功能</p>
          <div class="space-y-3">
            <AppButton block @click="handleQuickLogin" :loading="isLogging">
              快速登录（测试账号）
            </AppButton>
            <AppButton block variant="outline" @click="$router.push('/login')">
              前往登录页
            </AppButton>
          </div>
        </div>
      </div>

      <!-- 已登录内容 -->
      <div v-else class="flex-1 overflow-y-auto p-8 relative">
        <div class="absolute top-0 right-0 w-[600px] h-[600px] bg-teal-50 rounded-full filter blur-[100px] -z-10 pointer-events-none"></div>

        <!-- 历史模式：返回按钮 -->
        <div v-if="isHistoryMode" class="max-w-7xl mx-auto mb-4">
          <AppButton variant="secondary" size="sm" @click="handleBackToNew">
            <AppIcon name="arrow-left" class="mr-1" />
            返回创建新行程
          </AppButton>
        </div>

        <div class="grid gap-8 max-w-7xl mx-auto" :class="isHistoryMode ? 'lg:grid-cols-1' : 'lg:grid-cols-3'">
          <!-- 左侧栏：表单和灵感（仅新建模式显示） -->
          <div v-if="!isHistoryMode" class="lg:col-span-1 space-y-6">
            <ItineraryForm
              :destination="destination"
              :days="days"
              :budget="budget"
              :travelStyle="travelStyle"
              :disabled="isLoading"
              @update:destination="destination = $event"
              @update:days="days = $event"
              @update:budget="budget = $event"
              @update:travelStyle="travelStyle = $event"
              @generate="handleGenerate"
            />

            <InspirationCard class="fade-in-up" />
          </div>

          <!-- 右侧主区域：地图和行程卡片 -->
          <div :class="isHistoryMode ? 'w-full' : 'lg:col-span-2'" class="flex flex-col gap-6">
            <MapPreview />

            <!-- 成功提示 -->
            <div v-if="successMessage" class="success-toast">
              <AppIcon name="check-circle" class="text-green-500" />
              <span>{{ successMessage }}</span>
            </div>

            <!-- 错误提示 -->
            <div v-if="errorMessage" class="error-toast">
              <AppIcon name="exclamation-circle" class="text-red-500" />
              <span>{{ errorMessage }}</span>
            </div>

            <!-- 行程卡片 -->
            <ItineraryCard
              v-if="currentItinerary"
              :itinerary="currentItinerary"
              :is-generating-detail="isGeneratingDetail"
              @delete="handleDelete"
              @edit="handleEditDay"
              @generate-complete="handleGenerateComplete"
              @optimize-complete="handleOptimizeComplete"
              @update-itinerary="handleUpdateItinerary"
            />
            <EmptyStateCard v-else />
          </div>
        </div>
      </div>
    </main>
   
    <!-- 历史记录浮窗 -->
    <HistoryPanel
      :is-open="isHistoryPanelOpen"
      @close="handleCloseHistoryPanel"
      @select="handleSelectHistory"
    />
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import AppIcon from '@/components/common/AppIcon.vue'
import AppSidebar from '@/components/common/AppSidebar.vue'
import AppButton from '@/components/common/AppButton.vue'
import ItineraryForm from '@/components/planner/ItineraryForm.vue'
import ItineraryCard from '@/components/planner/ItineraryCard.vue'
import MapPreview from '@/components/planner/MapPreview.vue'
import PlannerHeader from '@/components/planner/PlannerHeader.vue'
import InspirationCard from '@/components/planner/InspirationCard.vue'
import EmptyStateCard from '@/components/planner/EmptyStateCard.vue'
import HistoryPanel from '@/components/planner/HistoryPanel.vue'
import { useItineraryStore } from '@/stores/itinerary'
import { useAuthStore } from '@/stores/auth'
import type { ItineraryCreateRequest } from '@/types/api'

const router = useRouter()
const destination = ref('')
const days = ref(3)
const budget = ref(5000)
const travelStyle = ref('leisure')
const successMessage = ref('')
const errorMessage = ref('')
const isGeneratingDetail = ref(false)
const isLogging = ref(false)

// 历史模式状态
const isHistoryMode = ref(false)
const isHistoryPanelOpen = ref(false)

const authStore = useAuthStore()
const itineraryStore = useItineraryStore()

// 初始化认证状态
const { user, isAuthenticated } = storeToRefs(authStore)
const { currentItinerary, isLoading } = storeToRefs(itineraryStore)

// 计算标题（根据模式显示）
const headerTitle = computed(() => {
  if (isHistoryMode.value && currentItinerary.value) {
    return currentItinerary.value.title
  }
  return '我的新旅程'
})

// 组件挂载时检查登录状态
onMounted(() => {
  authStore.initFromStorage()
})

// 清除消息
const clearMessages = () => {
  successMessage.value = ''
  errorMessage.value = ''
}

// 显示成功消息
const showSuccess = (message: string) => {
  clearMessages()
  successMessage.value = message
  setTimeout(() => {
    successMessage.value = ''
  }, 5000)
}

// 显示错误消息
const showError = (message: string) => {
  clearMessages()
  errorMessage.value = message
  setTimeout(() => {
    errorMessage.value = ''
  }, 5000)
}

// 快速登录（测试账号）
const handleQuickLogin = async () => {
  isLogging.value = true
  try {
    const result = await authStore.login({
      email: 'test@wanderflow.com',
      password: 'test123456'
    })

    if (result.success) {
      showSuccess('登录成功！现在可以开始规划行程了')
    } else {
      showError(result.error || '登录失败')
    }
  } finally {
    isLogging.value = false
  }
}

// 创建行程并自动生成详细行程
const handleGenerate = async () => {
  // 再次检查登录状态
  if (!isAuthenticated.value) {
    showError('请先登录后再创建行程')
    return
  }

  clearMessages()

  const requestData: ItineraryCreateRequest = {
    title: `${destination.value} ${days.value}日游`,
    destination: destination.value,
    days: days.value,
    budget: budget.value,
    travel_style: travelStyle.value as 'leisure' | 'adventure' | 'foodie',
    use_strict_json: true
  }

  console.log('开始生成行程:', requestData)

  // 1. 创建基础行程
  const result = await itineraryStore.createItinerary(requestData)

  if (!result.success) {
    showError(result.error || '创建行程失败，请重试')
    return
  }

  showSuccess('行程创建成功！AI正在生成详细行程...')

  // 2. 自动生成详细行程
  if (result.data?.id) {
    isGeneratingDetail.value = true
    const detailResult = await itineraryStore.generateDetailedItinerary(
      result.data.id,
      true  // 使用严格JSON格式
    )
    isGeneratingDetail.value = false

    if (detailResult.success) {
      showSuccess('完整行程已生成！请查看详细信息')
    } else {
      showError('详细行程生成失败，您可以稍后手动点击"AI生成详细行程"按钮')
    }
  }
}

// 删除行程
const handleDelete = async (id: number) => {
  if (confirm('确定要删除这个行程吗？')) {
    const result = await itineraryStore.deleteItinerary(id)
    if (result.success) {
      showSuccess('行程已删除')
    } else {
      showError(result.error || '删除失败')
    }
  }
}

// 编辑某一天的行程
const handleEditDay = (dayNumber: number) => {
  console.log('编辑第', dayNumber, '天')
  // TODO: 实现编辑功能
}

// AI生成完成回调
const handleGenerateComplete = (success: boolean) => {
  if (success) {
    showSuccess('完整行程已生成！请查看详细信息')
  } else {
    showError('详细行程生成失败，请重试')
  }
}

// AI优化完成回调
const handleOptimizeComplete = (success: boolean) => {
  if (success) {
    showSuccess('行程优化成功！请查看更新后的内容')
  } else {
    showError('优化失败，请重试')
  }
}

// 处理行程更新
const handleUpdateItinerary = (updatedItinerary: any) => {
  // 更新store中的行程
  itineraryStore.currentItinerary = updatedItinerary
  showSuccess('行程已保存')
}

// 打开历史记录面板
const handleOpenHistory = () => {
  isHistoryPanelOpen.value = true
}

// 关闭历史记录面板
const handleCloseHistoryPanel = () => {
  isHistoryPanelOpen.value = false
}

// 选择历史行程
const handleSelectHistory = async (itinerary: any) => {
  isHistoryMode.value = true
  console.log('切换到历史行程:', itinerary)
}

// 返回新建模式
const handleBackToNew = () => {
  isHistoryMode.value = false
  itineraryStore.currentItinerary = null
  console.log('返回新建模式')
}

// 监听当前行程变化
watch(currentItinerary, (newItinerary) => {
  if (newItinerary) {
    console.log('当前行程已更新:', newItinerary)
  }
}, { deep: true })
</script>

<style scoped>
.success-toast {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.25rem;
  background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
  border: 1px solid rgba(22, 163, 74, 0.3);
  border-radius: 0.75rem;
  color: #166534;
  font-size: 0.9375rem;
  font-weight: 500;
  animation: slideIn 0.3s ease-out;
}

.error-toast {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.25rem;
  background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
  border: 1px solid rgba(220, 38, 38, 0.3);
  border-radius: 0.75rem;
  color: #991b1b;
  font-size: 0.9375rem;
  font-weight: 500;
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
