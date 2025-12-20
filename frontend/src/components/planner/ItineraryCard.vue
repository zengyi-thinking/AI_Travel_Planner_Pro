<template>
  <div class="glass-card flex-1 p-8 flex flex-col items-center justify-center text-center">
    <div class="w-20 h-20 bg-slate-50 rounded-full flex items-center justify-center mb-4">
      <i :class="icon" class="text-3xl text-slate-300"></i>
    </div>
    <h3 class="text-lg font-bold text-slate-700">{{ itinerary.title }}</h3>
    <p class="text-slate-400 max-w-xs mt-2">{{ itinerary.summary }}</p>
    <div class="mt-6 grid grid-cols-2 gap-3 text-sm text-slate-600">
      <div class="bg-white/80 rounded-xl px-4 py-3 border border-slate-100">
        目的地：{{ itinerary.destination }}
      </div>
      <div class="bg-white/80 rounded-xl px-4 py-3 border border-slate-100">
        天数：{{ itinerary.days }} 天
      </div>
      <div class="bg-white/80 rounded-xl px-4 py-3 border border-slate-100">
        预算：￥{{ itinerary.budget }}
      </div>
      <div class="bg-white/80 rounded-xl px-4 py-3 border border-slate-100">
        风格：{{ itinerary.styleLabel }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface ItinerarySummary {
  title: string
  summary: string
  destination: string
  days: number
  budget: number
  styleLabel: string
}

withDefaults(
  defineProps<{
    itinerary: ItinerarySummary
    icon?: string
  }>(),
  {
    icon: 'fas fa-clipboard-list'
  }
)
</script>
