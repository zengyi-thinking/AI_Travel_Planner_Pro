<template>
  <div class="map-preview-wrapper">
    <!-- 标题栏 -->
    <div class="map-header" v-if="showHeader && itinerary">
      <div class="header-left">
        <h3 class="map-title">🗺️ 行程地图预览</h3>
        <span class="map-subtitle" v-if="itinerary.destination">
          {{ itinerary.destination }} · {{ itinerary.days }}天行程
        </span>
      </div>
      <div class="header-right">
        <AppButton
          v-if="hasCoordinates"
          variant="ghost"
          size="sm"
          icon="expand"
          @click="toggleFullscreen"
        >
          全屏查看
        </AppButton>
      </div>
    </div>

    <!-- 地图容器 -->
    <div class="map-container-wrapper" :class="{ 'fullscreen': isFullscreen }">
      <InteractiveMap
        :height="mapHeight"
        :itinerary="itinerary"
      />

      <!-- 空状态提示 -->
      <div v-if="!itinerary || !itinerary.days_detail?.length" class="map-empty-state">
        <AppIcon name="map-marked-alt" size="4x" class="text-slate-300 mb-4" />
        <p class="text-slate-500 text-lg mb-2">暂无行程数据</p>
        <p class="text-slate-400 text-sm">生成行程后即可在地图上查看路线</p>
      </div>

      <!-- 无坐标提示 -->
      <div v-else-if="!hasCoordinates" class="map-no-coordinates">
        <AppIcon name="map-marker-alt" size="3x" class="text-amber-400 mb-3" />
        <p class="text-slate-600 mb-1">正在加载地图坐标...</p>
        <p class="text-slate-400 text-sm">AI 正在为您的行程添加地理位置信息</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import AppIcon from '@/components/common/AppIcon.vue'
import AppButton from '@/components/common/AppButton.vue'
import InteractiveMap from '@/components/planner/InteractiveMap.vue'
import { useItineraryStore } from '@/stores/itinerary'

interface Props {
  showHeader?: boolean
  mapHeight?: string
}

const props = withDefaults(defineProps<Props>(), {
  showHeader: true,
  mapHeight: '320px'
})

const itineraryStore = useItineraryStore()
const itinerary = computed(() => itineraryStore.currentItinerary)
const isFullscreen = ref(false)

// 添加调试日志
watch(itinerary, (newVal) => {
  console.log('📍 MapPreview: itinerary 数据变化', newVal)
  console.log('📍 days_detail:', newVal?.days_detail)
  console.log('📍 hasCoordinates:', hasCoordinates.value)
}, { deep: true })

/**
 * 检查行程是否包含坐标数据
 */
const hasCoordinates = computed(() => {
  if (!itinerary.value?.days_detail) {
    console.log('⚠️ MapPreview: 没有 days_detail')
    return false
  }

  const hasCoords = itinerary.value.days_detail.some(day =>
    day.activities?.some(activity => {
      const has = activity.coordinates && activity.coordinates.lat && activity.coordinates.lng
      if (!has) {
        console.log(`⚠️ 活动 ${activity.title} 缺少坐标`)
      }
      return has
    })
  )

  console.log(`📍 hasCoordinates: ${hasCoords}`)
  return hasCoords
})

/**
 * 切换全屏模式
 */
function toggleFullscreen() {
  isFullscreen.value = !isFullscreen.value
}
</script>

<style scoped>
.map-preview-wrapper {
  @apply w-full bg-white rounded-xl shadow-md overflow-hidden;
  border: 1px solid #e2e8f0;
}

.map-header {
  @apply flex items-center justify-between px-4 py-2 border-b border-slate-100;
  background: linear-gradient(to right, #f8fafc, #ffffff);
  min-height: 48px;
}

.header-left {
  @apply flex flex-col;
}

.map-title {
  @apply text-sm font-bold text-slate-800 mb-0;
  font-size: 14px;
}

.map-subtitle {
  @apply text-xs text-slate-500;
  font-size: 12px;
}

.header-right {
  @apply flex items-center gap-2;
}

.map-container-wrapper {
  @apply relative w-full;
  transition: all 0.3s ease;
  min-height: 320px;
}

.map-container-wrapper.fullscreen {
  @apply fixed inset-0 z-50 bg-white;
  border-radius: 0;
  min-height: 100vh;
}

.map-empty-state {
  @apply absolute inset-0 flex flex-col items-center justify-center bg-slate-50;
  min-height: 320px;
}

.map-no-coordinates {
  @apply absolute inset-0 flex flex-col items-center justify-center bg-amber-50;
  min-height: 320px;
}

/* 全屏模式下添加关闭按钮 */
.map-container-wrapper.fullscreen::after {
  content: '×';
  @apply absolute top-4 right-4 w-10 h-10 bg-white rounded-full shadow-lg flex items-center justify-center text-2xl text-slate-600 cursor-pointer hover:bg-slate-100;
  z-index: 100;
}
</style>
