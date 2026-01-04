<template>
  <div class="glass-card p-6 flex flex-col h-full overflow-y-auto fade-in-up">
    <div class="space-y-6">
      <ImageUploader />
      <PlatformSelector v-model="platformValue" />
      <KeywordInput v-model="keywordsValue" />
      <EmotionSlider v-model="emotionValue" />
      <GenerateButton @generate="$emit('generate')" :isGenerating="isGenerating" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import ImageUploader from '@/components/copywriter/ImageUploader.vue'
import PlatformSelector from '@/components/copywriter/PlatformSelector.vue'
import KeywordInput from '@/components/copywriter/KeywordInput.vue'
import EmotionSlider from '@/components/copywriter/EmotionSlider.vue'
import GenerateButton from '@/components/copywriter/GenerateButton.vue'

const props = defineProps<{
  platform: 'xiaohongshu' | 'wechat' | 'weibo'
  keywords: string
  emotion: number
  isGenerating?: boolean
}>()

const emit = defineEmits<{
  'update:platform': ['xiaohongshu' | 'wechat' | 'weibo']
  'update:keywords': [string]
  'update:emotion': [number]
  generate: []
}>()

const platformValue = computed({
  get: () => props.platform,
  set: (value) => emit('update:platform', value)
})

const keywordsValue = computed({
  get: () => props.keywords,
  set: (value) => emit('update:keywords', value)
})

const emotionValue = computed({
  get: () => props.emotion,
  set: (value) => emit('update:emotion', value)
})
</script>
