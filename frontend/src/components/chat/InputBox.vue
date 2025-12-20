<template>
  <div class="relative">
    <input
      :value="modelValue"
      type="text"
      class="w-full bg-slate-50 border-2 border-slate-200 rounded-full py-4 pl-6 pr-24 focus:outline-none focus:border-teal-400 focus:bg-white transition-all shadow-inner"
      :placeholder="placeholder"
      @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
      @keydown.enter.prevent="$emit('send')"
    >
    <button
      type="button"
      class="absolute right-2 top-2 w-10 h-10 bg-teal-500 hover:bg-teal-600 text-white rounded-full flex items-center justify-center transition-colors shadow-md"
      @click="$emit('send')"
    >
      <i class="fas fa-paper-plane"></i>
    </button>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  modelValue: string
  placeholder?: string
}>()

defineEmits<{
  'update:modelValue': [string]
  send: []
}>()
</script>
