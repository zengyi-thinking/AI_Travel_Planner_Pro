<template>
  <header class="h-16 bg-white/80 backdrop-blur border-b border-slate-100 flex justify-between items-center px-8 z-10">
    <h2 class="text-xl font-bold text-slate-700">{{ title }}</h2>
    <div class="flex gap-4">
      <button class="w-10 h-10 rounded-full bg-slate-100 flex items-center justify-center text-slate-500 hover:bg-slate-200">
        <i class="fas fa-bell"></i>
      </button>
      <button class="btn-primary px-4 py-2 text-sm shadow-none">
        导出行程
      </button>
    </div>
  </header>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    title?: string
  }>(),
  {
    title: '我的新旅程'
  }
)
</script>
