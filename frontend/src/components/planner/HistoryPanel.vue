<template>
  <Teleport to="body">
    <!-- 遮罩层 -->
    <Transition name="fade">
      <div
        v-if="isOpen"
        class="fixed inset-0 bg-black/50 backdrop-blur-sm z-[9998]"
        @click="handleClose"
      ></div>
    </Transition>

    <!-- 浮窗 -->
    <Transition name="slide">
      <div
        v-if="isOpen"
        class="fixed top-0 right-0 h-full w-[480px] bg-white shadow-2xl z-[9999] flex flex-col"
      >
      <!-- 头部 -->
      <div class="px-6 py-4 border-b border-slate-100 flex items-center justify-between bg-gradient-to-r from-teal-50 to-white">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-teal-500 rounded-full flex items-center justify-center">
            <AppIcon name="clock" class="text-white text-lg" />
          </div>
          <div>
            <h2 class="text-lg font-bold text-slate-800">历史行程</h2>
            <p class="text-xs text-slate-500">{{ itineraries.length }} 条记录</p>
          </div>
        </div>
        <button
          @click="handleClose"
          class="w-8 h-8 rounded-full hover:bg-slate-100 flex items-center justify-center transition-colors"
        >
          <AppIcon name="x" class="text-slate-400" />
        </button>
      </div>

      <!-- 列表区域 -->
      <div class="flex-1 overflow-y-auto p-4 space-y-3">
        <!-- 加载状态 -->
        <div v-if="isLoading" class="flex items-center justify-center py-12">
          <div class="flex flex-col items-center gap-3">
            <div class="w-10 h-10 border-3 border-teal-500 border-t-transparent rounded-full animate-spin"></div>
            <p class="text-sm text-slate-500">加载中...</p>
          </div>
        </div>

        <!-- 空状态 -->
        <div v-else-if="itineraries.length === 0" class="flex flex-col items-center justify-center py-12">
          <div class="w-20 h-20 bg-slate-100 rounded-full flex items-center justify-center mb-4">
            <AppIcon name="folder-open" class="text-3xl text-slate-300" />
          </div>
          <p class="text-slate-500 font-medium">暂无历史行程</p>
          <p class="text-sm text-slate-400 mt-1">创建您的第一个行程吧</p>
        </div>

        <!-- 行程列表 -->
        <div
          v-for="itinerary in itineraries"
          :key="itinerary.id"
          @click="handleSelectItinerary(itinerary)"
          class="group bg-white border border-slate-200 rounded-xl p-4 cursor-pointer hover:border-teal-300 hover:shadow-md transition-all duration-200"
        >
          <div class="flex items-start gap-3">
            <!-- 图标 -->
            <div class="w-12 h-12 bg-gradient-to-br from-teal-400 to-teal-500 rounded-lg flex items-center justify-center flex-shrink-0">
              <AppIcon name="map" class="text-white text-xl" />
            </div>

            <!-- 内容 -->
            <div class="flex-1 min-w-0">
              <h3 class="font-bold text-slate-800 truncate group-hover:text-teal-600 transition-colors">
                {{ itinerary.title }}
              </h3>
              <div class="flex items-center gap-2 mt-1 text-xs text-slate-500">
                <span class="flex items-center gap-1">
                  <AppIcon name="map-pin" class="w-3 h-3" />
                  {{ itinerary.destination }}
                </span>
                <span>•</span>
                <span class="flex items-center gap-1">
                  <AppIcon name="calendar" class="w-3 h-3" />
                  {{ itinerary.days }} 天
                </span>
              </div>
              <div class="flex items-center gap-2 mt-2 text-xs text-slate-400">
                <AppIcon name="clock" class="w-3 h-3" />
                <span>{{ formatDate(itinerary.created_at) }}</span>
              </div>
            </div>

            <!-- 箭头 -->
            <div class="flex-shrink-0">
              <AppIcon name="chevron-right" class="text-slate-300 group-hover:text-teal-500 transition-colors" />
            </div>
          </div>
        </div>
      </div>

      <!-- 底部提示 -->
      <div class="px-6 py-3 border-t border-slate-100 bg-slate-50">
        <p class="text-xs text-slate-400 text-center">
          点击任意行程查看详情
        </p>
      </div>
    </div>
  </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import AppIcon from '@/components/common/AppIcon.vue'
import { useItineraryStore } from '@/stores/itinerary'
import type { Itinerary } from '@/types/api'

const props = defineProps<{
  isOpen: boolean
}>()

const emit = defineEmits<{
  close: []
  select: [itinerary: Itinerary]
}>()

const itineraryStore = useItineraryStore()
const itineraries = ref<Itinerary[]>([])
const isLoading = ref(false)

// 监听面板打开状态，加载历史行程
watch(() => props.isOpen, async (newValue) => {
  if (newValue) {
    await loadItineraries()
  }
})

// 加载历史行程
const loadItineraries = async () => {
  isLoading.value = true
  try {
    const result = await itineraryStore.loadHistoryItineraries(1, 50)
    if (result.success && result.data) {
      itineraries.value = result.data
    }
  } finally {
    isLoading.value = false
  }
}

// 选择行程
const handleSelectItinerary = async (itinerary: Itinerary) => {
  // 加载行程详情
  const result = await itineraryStore.getItineraryById(itinerary.id)
  if (result.success && result.data) {
    emit('select', result.data)
    handleClose()
  }
}

// 关闭面板
const handleClose = () => {
  emit('close')
}

// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))

  if (days === 0) {
    return '今天'
  } else if (days === 1) {
    return '昨天'
  } else if (days < 7) {
    return `${days} 天前`
  } else if (days < 30) {
    const weeks = Math.floor(days / 7)
    return `${weeks} 周前`
  } else if (days < 365) {
    const months = Math.floor(days / 30)
    return `${months} 个月前`
  } else {
    return date.toLocaleDateString('zh-CN', { year: 'numeric', month: 'numeric', day: 'numeric' })
  }
}
</script>

<style scoped>
/* 遮罩层动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 浮窗动画 */
.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(100%);
}

/* 滚动条样式 */
.flex-1.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.flex-1.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 3px;
}

.flex-1.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.flex-1.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>
