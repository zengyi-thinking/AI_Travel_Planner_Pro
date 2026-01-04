<template>
  <header class="h-16 bg-white/80 backdrop-blur border-b border-slate-100 flex justify-between items-center px-8 z-10">
    <h2 class="text-xl font-bold text-slate-700">{{ title }}</h2>
    <div class="flex gap-3">
      <!-- 历史记录按钮 -->
      <AppButton
        variant="secondary"
        size="sm"
        @click="$emit('openHistory')"
      >
        <AppIcon name="clock" class="mr-1" />
        历史记录
      </AppButton>

      <!-- 通知按钮 -->
      <AppButton variant="secondary" size="sm" class="rounded-full w-10 h-10 !p-0">
        <AppIcon name="bell" />
      </AppButton>

      <!-- 导出按钮 -->
      <AppButton
        variant="primary"
        size="sm"
        :disabled="!itinerary"
        :loading="isExporting"
        @click="handleExportPDF"
      >
        导出行程
      </AppButton>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import AppButton from '@/components/common/AppButton.vue'
import AppIcon from '@/components/common/AppIcon.vue'
import type { Itinerary } from '@/types/api'

defineEmits<{
  openHistory: []
}>()

const props = withDefaults(
  defineProps<{
    title?: string
    itinerary?: Itinerary | null
  }>(),
  {
    title: '我的新旅程',
    itinerary: null
  }
)

const isExporting = ref(false)

const handleExportPDF = async () => {
  if (!props.itinerary) {
    return
  }

  try {
    isExporting.value = true

    // 调用后端API导出PDF
    const token = localStorage.getItem('token')
    const response = await fetch(
      `http://localhost:8000/api/v1/planner/itineraries/${props.itinerary.id}/export/pdf`,
      {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      }
    )

    if (!response.ok) {
      throw new Error('导出失败')
    }

    // 下载PDF文件
    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${props.itinerary.title}.pdf`
    document.body.appendChild(a)
    a.click()
    window.URL.revokeObjectURL(url)
    document.body.removeChild(a)

    isExporting.value = false
  } catch (error) {
    console.error('导出PDF失败:', error)
    isExporting.value = false
    alert('导出失败，请重试')
  }
}
</script>
