<template>
  <button
    type="button"
    class="btn-primary w-full justify-center"
    @click="$emit('generate')"
  >
    <i class="fas fa-magic"></i>
    {{ label }}
  </button>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    label?: string
  }>(),
  {
    label: 'AI 生成行程'
  }
)

defineEmits<{
  generate: []
}>()
</script>
