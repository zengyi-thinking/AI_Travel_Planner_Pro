<template>
  <div v-if="visible" class="mb-4 glass-card p-4 rounded-xl">
    <div class="flex items-center gap-4">
      <div class="flex-1">
        <input
          :value="city"
          type="text"
          class="w-full bg-slate-50 border border-slate-200 rounded-lg px-4 py-2 focus:outline-none focus:border-teal-400"
          placeholder="输入城市名，如：北京、上海"
          @input="$emit('update:city', ($event.target as HTMLInputElement).value)"
        >
      </div>
      <button
        type="button"
        class="btn-primary px-6 py-2 text-sm"
        @click="$emit('query')"
      >
        <i class="fas fa-cloud-sun mr-1"></i>查询天气
      </button>
      <button type="button" class="text-slate-400 hover:text-slate-600" @click="$emit('close')">
        <i class="fas fa-times"></i>
      </button>
    </div>

    <div v-if="loading" class="mt-4 text-center text-slate-500 text-sm">查询中...</div>

    <div v-else-if="results.length" class="mt-4">
      <div class="grid grid-cols-3 gap-4 text-sm">
        <div v-for="item in results" :key="item.date" class="bg-white p-4 rounded-xl border border-slate-200">
          <div class="text-center">
            <div class="text-sm font-semibold text-slate-600">{{ item.date }}</div>
            <div class="text-3xl my-2">{{ item.icon }}</div>
            <div class="text-xs text-slate-500">{{ item.desc }}</div>
            <div class="mt-3 flex justify-between text-sm">
              <span class="text-red-500 font-semibold">{{ item.high }}°</span>
              <span class="text-slate-400">/</span>
              <span class="text-blue-500 font-semibold">{{ item.low }}°</span>
            </div>
            <div class="mt-2 text-xs text-slate-500">
              <div>湿度: {{ item.humidity }}%</div>
              <div>风: {{ item.wind }}级</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface WeatherItem {
  date: string
  icon: string
  desc: string
  high: number
  low: number
  humidity: number
  wind: number
}

defineProps<{
  visible: boolean
  city: string
  loading: boolean
  results: WeatherItem[]
}>()

defineEmits<{
  'update:city': [string]
  query: []
  close: []
}>()
</script>
