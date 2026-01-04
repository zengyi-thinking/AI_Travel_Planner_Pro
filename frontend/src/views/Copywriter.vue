<template>
  <div class="bg-[#F8FAFC] h-screen flex overflow-hidden">
    <AppSidebar active="copywriter" />

    <main class="flex-1 flex flex-col h-full relative">
      <div class="absolute inset-0 bg-gradient-to-br from-teal-50/50 to-blue-50/50 -z-10"></div>
      <CopywriterHeader />

      <div class="flex-1 overflow-hidden p-6">
        <div class="max-w-6xl mx-auto h-full grid lg:grid-cols-2 gap-6">
          <CopywriterForm
            :platform="selectedPlatform"
            :keywords="keywords"
            :emotion="emotionLevel"
            :isGenerating="isGenerating"
            @update:platform="selectedPlatform = $event"
            @update:keywords="keywords = $event"
            @update:emotion="emotionLevel = $event"
            @generate="generateContent"
          />

          <ResultPreview 
            :content="generatedContent" 
            :images="generatedImages"
            class="fade-in-up" 
          />
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { storeToRefs } from 'pinia'
import AppSidebar from '@/components/common/AppSidebar.vue'
import CopywriterHeader from '@/components/copywriter/CopywriterHeader.vue'
import CopywriterForm from '@/components/copywriter/CopywriterForm.vue'
import ResultPreview from '@/components/copywriter/ResultPreview.vue'
import { useCopywritingStore } from '@/stores/copywriting'

const copywritingStore = useCopywritingStore()
const { selectedPlatform, keywords, emotionLevel, currentResult, uploadedImages, isGenerating } = storeToRefs(copywritingStore)
const generatedContent = computed(() => currentResult.value?.content || '')
const generatedImages = computed(() => currentResult.value?.images || [])

const generateContent = async () => {
  await copywritingStore.generateCopywriting({
    platform: selectedPlatform.value,
    keywords: keywords.value.split(',').map((word) => word.trim()).filter(Boolean),
    emotion_level: emotionLevel.value,
    images: uploadedImages.value
  })
}
</script>
