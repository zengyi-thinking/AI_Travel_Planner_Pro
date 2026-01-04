<template>
  <div>
    <label class="block text-sm font-bold text-slate-500 mb-2">1. 上传照片 (AI 将识别内容)</label>

    <!-- 上传区域 -->
    <div
      v-if="uploadedImages.length === 0"
      class="border-2 border-dashed border-slate-300 rounded-2xl h-32 flex flex-col items-center justify-center text-slate-400 hover:border-teal-400 hover:bg-teal-50/50 transition-colors cursor-pointer group relative"
      @click="triggerFileInput"
      @drop="handleDrop"
      @dragover.prevent="handleDragOver"
      @dragleave.prevent="handleDragLeave"
      :class="{ 'border-teal-400 bg-teal-50/50': isDragging }">
      <input
        ref="fileInput"
        type="file"
        class="hidden"
        accept="image/jpeg,image/png,image/gif,image/webp"
        @change="handleFileSelect"
      >
      <AppIcon name="cloud-upload-alt" size="xl" class="mb-2 group-hover:scale-110 transition-transform" />
      <span class="text-sm">点击或拖拽上传照片</span>
      <span v-if="isUploading" class="text-xs text-teal-600 mt-1">上传中...</span>
    </div>

    <!-- 图片预览列表 -->
    <div v-else class="space-y-2">
      <div
        v-for="(image, index) in uploadedImages"
        :key="index"
        class="relative group border border-slate-200 rounded-xl overflow-hidden bg-slate-50">
        <img :src="image" class="w-full h-32 object-cover" alt="上传的图片">
        <div class="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-2">
          <button
            @click="removeImage(index)"
            class="p-2 bg-red-500 text-white rounded-full hover:bg-red-600 transition-colors">
            <AppIcon name="trash" size="sm" />
          </button>
        </div>
      </div>

      <!-- 继续添加按钮 -->
      <button
        @click="triggerFileInput"
        class="w-full border-2 border-dashed border-slate-300 rounded-xl py-3 text-slate-400 hover:border-teal-400 hover:text-teal-500 transition-colors">
        + 添加更多图片
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import AppIcon from '@/components/common/AppIcon.vue'
import { useCopywritingStore } from '@/stores/copywriting'

const copywritingStore = useCopywritingStore()
const { uploadedImages } = copywritingStore

const fileInput = ref<HTMLInputElement | null>(null)
const isDragging = ref(false)
const isUploading = ref(false)

const triggerFileInput = () => {
  fileInput.value?.click()
}

const handleFileSelect = async (event: Event) => {
  const target = event.target as HTMLInputElement
  const files = target.files
  if (files && files.length > 0) {
    await uploadFiles(Array.from(files))
  }
  // 重置 input 以允许重复选择同一文件
  target.value = ''
}

const handleDragOver = () => {
  isDragging.value = true
}

const handleDragLeave = () => {
  isDragging.value = false
}

const handleDrop = async (event: DragEvent) => {
  isDragging.value = false
  const files = event.dataTransfer?.files
  if (files && files.length > 0) {
    await uploadFiles(Array.from(files))
  }
}

const uploadFiles = async (files: File[]) => {
  // 过滤图片文件
  const imageFiles = files.filter(file => file.type.startsWith('image/'))
  
  if (imageFiles.length === 0) {
    alert('请选择图片文件')
    return
  }

  isUploading.value = true

  try {
    await copywritingStore.uploadImages(imageFiles)
  } catch (error) {
    console.error('Upload failed:', error)
    alert('图片上传失败，请重试')
  } finally {
    isUploading.value = false
  }
}

const removeImage = (index: number) => {
  copywritingStore.removeImage(index)
}
</script>
