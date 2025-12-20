<template>
  <div class="glass-card p-6">
    <h3 class="text-lg font-bold text-slate-800 mb-4 flex items-center gap-2">
      <span class="w-1 h-6 bg-teal-400 rounded-full"></span> 旅程设定
    </h3>

    <form class="space-y-4">
      <div>
        <label class="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">目的地</label>
        <div class="input-icon-wrapper">
          <i class="fas fa-map-marker-alt"></i>
          <input
            :value="destination"
            type="text"
            class="input-field"
            placeholder="例如：京都, 日本"
            @input="$emit('update:destination', ($event.target as HTMLInputElement).value)"
          >
        </div>
      </div>

      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">天数</label>
          <input
            :value="days"
            type="number"
            class="input-field px-4 !pl-4"
            placeholder="5"
            min="1"
            @input="$emit('update:days', Number(($event.target as HTMLInputElement).value))"
          >
        </div>
        <div>
          <label class="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">预算</label>
          <input
            :value="budget"
            type="number"
            class="input-field px-4 !pl-4"
            placeholder="￥ 5000"
            min="0"
            @input="$emit('update:budget', Number(($event.target as HTMLInputElement).value))"
          >
        </div>
      </div>

      <div>
        <label class="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">旅行风格</label>
        <StyleSelector v-model="styleValue" />
      </div>

      <GenerateButton @generate="$emit('generate')" />
    </form>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import StyleSelector from '@/components/planner/StyleSelector.vue'
import GenerateButton from '@/components/planner/GenerateButton.vue'

const props = defineProps<{
  destination: string
  days: number
  budget: number
  travelStyle: string
}>()

const emit = defineEmits<{
  'update:destination': [string]
  'update:days': [number]
  'update:budget': [number]
  'update:travelStyle': [string]
  generate: []
}>()

const styleValue = computed({
  get: () => props.travelStyle,
  set: (value: string) => emit('update:travelStyle', value)
})
</script>
