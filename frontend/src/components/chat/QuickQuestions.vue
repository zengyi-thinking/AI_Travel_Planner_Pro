<template>
  <div class="grid grid-cols-2 gap-3 text-sm">
    <button
      v-for="question in questions"
      :key="question"
      type="button"
      class="quick-question bg-white border border-slate-200 p-3 rounded-xl hover:border-teal-400 hover:text-teal-600 transition-colors text-left"
      @click="$emit('select', question)"
    >
      <slot name="icon" :question="question" />
      {{ question }}
    </button>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  questions: string[]
}>()

defineEmits<{
  select: [string]
}>()
</script>
