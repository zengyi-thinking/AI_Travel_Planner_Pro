<template>
  <AppButton 
    block 
    :icon="isGenerating ? 'circle-notch' : 'magic'" 
    :iconSpin="isGenerating"
    size="lg" 
    @click="$emit('generate')"
    :disabled="isGenerating"
  >
    {{ label }}
  </AppButton>
</template>

<script setup lang="ts">
import AppButton from '@/components/common/AppButton.vue'

withDefaults(
  defineProps<{
    label?: string
    isGenerating?: boolean
  }>(),
  {
    label: '一键生成文案',
    isGenerating: false
  }
)

defineEmits<{
  generate: []
}>()
</script>
