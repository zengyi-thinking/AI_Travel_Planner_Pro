<template>
  <div class="glass-card p-6 flex flex-col h-full bg-white/60 relative overflow-hidden">
    <div class="absolute top-0 right-0 p-4 opacity-10 pointer-events-none">
      <AppIcon name="quote-right" size="xl" class="text-9xl text-slate-800" />
    </div>

    <h3 class="text-lg font-bold text-slate-700 mb-4">生成结果预览</h3>

    <div class="flex-1 bg-white border border-slate-100 rounded-2xl p-6 shadow-inner overflow-y-auto">
      <div v-if="content" class="space-y-4">
        <div class="flex items-center gap-3 mb-4">
          <img src="https://i.pravatar.cc/100?img=12" class="w-10 h-10 rounded-full" alt="用户头像">
          <div>
            <div class="font-bold text-sm">{{ userName }}</div>
            <div class="text-xs text-slate-400">刚刚发布于 {{ location }}</div>
          </div>
        </div>

        <div class="text-slate-600 leading-relaxed whitespace-pre-line">
          {{ content }}
        </div>

        <div class="grid grid-cols-2 gap-2 mt-4">
          <div class="h-32 bg-slate-200 rounded-lg animate-pulse"></div>
          <div class="h-32 bg-slate-200 rounded-lg animate-pulse"></div>
        </div>
      </div>

      <div v-else class="text-center text-slate-400 py-16">
        <AppIcon name="magic" size="xl" class="mb-4" />
        <p>点击生成按钮开始创作</p>
      </div>
    </div>

    <div class="flex gap-3 mt-4">
      <AppButton block variant="secondary" icon="copy" iconPrefix="far" @click="handleCopy" :disabled="!content">
        {{ copyButtonText }}
      </AppButton>
      <AppButton block variant="secondary" icon="share-alt" @click="handleShare" :disabled="!content">
        分享
      </AppButton>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import AppButton from '@/components/common/AppButton.vue'
import AppIcon from '@/components/common/AppIcon.vue'

const props = withDefaults(
  defineProps<{
    content: string
    userName?: string
    location?: string
  }>(),
  {
    userName: 'Alex Chen',
    location: '冰岛'
  }
)

const copyButtonText = ref('复制')
const copyTimeout = ref<number | null>(null)

const handleCopy = async () => {
  if (!props.content) return

  try {
    await navigator.clipboard.writeText(props.content)
    copyButtonText.value = '已复制!'
    
    if (copyTimeout.value) {
      clearTimeout(copyTimeout.value)
    }
    
    copyTimeout.value = setTimeout(() => {
      copyButtonText.value = '复制'
    }, 2000) as unknown as number
  } catch (err) {
    console.error('Failed to copy:', err)
    // 降级方案
    const textArea = document.createElement('textarea')
    textArea.value = props.content
    document.body.appendChild(textArea)
    textArea.select()
    document.execCommand('copy')
    document.body.removeChild(textArea)
    copyButtonText.value = '已复制!'
    
    if (copyTimeout.value) {
      clearTimeout(copyTimeout.value)
    }
    
    copyTimeout.value = setTimeout(() => {
      copyButtonText.value = '复制'
    }, 2000) as unknown as number
  }
}

const handleShare = () => {
  if (!props.content) return
  
  if (navigator.share) {
    navigator.share({
      title: 'WanderFlow 文案',
      text: props.content
    }).catch(err => {
      console.error('Share failed:', err)
    })
  } else {
    // 降级：复制到剪贴板
    handleCopy()
  }
}
</script>
