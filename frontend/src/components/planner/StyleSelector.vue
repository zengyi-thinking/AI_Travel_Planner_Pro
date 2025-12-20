<template>
  <div class="flex flex-wrap gap-2">
    <button
      v-for="option in options"
      :key="option.value"
      type="button"
      :class="modelValue === option.value ? activeClass : inactiveClass"
      class="px-3 py-1 rounded-full border text-sm transition-colors"
      @click="$emit('update:modelValue', option.value)"
    >
      <span class="mr-1">{{ option.icon }}</span>{{ option.label }}
    </button>
  </div>
</template>

<script setup lang="ts">
const options = [
  { value: 'leisure', label: '休闲放松', icon: '🌿' },
  { value: 'adventure', label: '特种兵打卡', icon: '⚡' },
  { value: 'foodie', label: '美食探索', icon: '🍜' }
]

withDefaults(
  defineProps<{
    modelValue: string
    activeClass?: string
    inactiveClass?: string
  }>(),
  {
    activeClass: 'bg-teal-50 border-teal-200 text-teal-700',
    inactiveClass: 'bg-white border-slate-200 text-slate-500 hover:border-teal-400 hover:text-teal-500'
  }
)

defineEmits<{
  'update:modelValue': [string]
}>()
</script>
