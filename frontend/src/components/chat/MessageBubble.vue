<template>
  <div class="flex gap-4" :class="role === 'user' ? 'flex-row-reverse' : ''">
    <div
      v-if="role === 'assistant'"
      class="w-10 h-10 bg-gradient-to-br from-teal-400 to-blue-500 rounded-full flex items-center justify-center text-white shadow-sm"
    >
      <i class="fas fa-robot"></i>
    </div>
    <img
      v-else
      src="https://i.pravatar.cc/100?img=12"
      alt="用户头像"
      class="w-10 h-10 rounded-full border-2 border-white shadow-sm"
    >
    <div class="max-w-xl">
      <div
        :class="role === 'user' ? 'bg-white rounded-2xl rounded-tr-none' : 'bg-teal-50 border border-teal-100 rounded-2xl rounded-tl-none'"
        class="p-4 text-slate-700 shadow-sm"
      >
        {{ content }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  role: 'user' | 'assistant'
  content: string
}

defineProps<Props>()
</script>
