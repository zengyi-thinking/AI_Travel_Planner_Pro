import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/utils/api'
import type { CopywritingRequest, CopywritingResult } from '@/types/api'

interface CopywriterContentResponse {
  id: number
  content_type: string
  platform?: string
  output_content: string
  input_data?: {
    keywords?: string[]
    images?: string[]
  }
  rating?: number | null
  created_at: string
}

export const useCopywritingStore = defineStore('copywriting', () => {
  // 状态
  const results = ref<CopywritingResult[]>([])
  const isGenerating = ref(false)
  const currentResult = ref<CopywritingResult | null>(null)
  const selectedPlatform = ref<'xiaohongshu' | 'wechat' | 'weibo'>('xiaohongshu')
  const keywords = ref<string>('')
  const emotionLevel = ref(50)
  const uploadedImages = ref<string[]>([])

  // 生成文案
  const generateCopywriting = async (request: CopywritingRequest) => {
    isGenerating.value = true
    try {
      const response = await api.post<CopywriterContentResponse>('/api/v1/copywriter/generate', request)
      const result: CopywritingResult = {
        id: response.id,
        content: response.output_content,
        platform: response.platform || request.platform,
        keywords: response.input_data?.keywords || request.keywords,
        images: request.images || [],
        created_at: response.created_at,
        rating: response.rating ?? null
      }

      results.value.unshift(result)
      currentResult.value = result

      return { success: true, data: result }
    } catch (error) {
      console.error('Failed to generate copywriting:', error)
      return { success: false, error: '生成文案失败' }
    } finally {
      isGenerating.value = false
    }
  }

  // 重新生成
  const regenerate = async () => {
    const request: CopywritingRequest = {
      platform: selectedPlatform.value,
      keywords: keywords.value.split(',').map(k => k.trim()).filter(Boolean),
      emotion_level: emotionLevel.value,
      images: uploadedImages.value
    }

    return await generateCopywriting(request)
  }

  // 上传图片
  const uploadImages = async (files: File[]) => {
    try {
      const urls: string[] = []
      for (const file of files) {
        const formData = new FormData()
        formData.append('image', file)
        const response = await api.post<{ image_url: string }>('/api/v1/copywriter/upload-image', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
        urls.push(response.image_url)
      }
      uploadedImages.value.push(...urls)

      return { success: true, data: urls }
    } catch (error) {
      console.error('Failed to upload images:', error)
      return { success: false, error: '图片上传失败' }
    }
  }

  // 删除图片
  const removeImage = (index: number) => {
    uploadedImages.value.splice(index, 1)
  }

  // 获取历史生成记录
  const fetchResults = async () => {
    try {
      const response = await api.get<CopywriterContentResponse[]>('/api/v1/copywriter/contents', {
        params: { page: 1, size: 20 }
      })
      results.value = response.map(item => ({
        id: item.id,
        content: item.output_content,
        platform: item.platform || 'xiaohongshu',
        keywords: item.input_data?.keywords || [],
        images: item.input_data?.images || [],
        created_at: item.created_at,
        rating: item.rating ?? null
      }))
      return { success: true, data: results.value }
    } catch (error) {
      console.error('Failed to fetch results:', error)
      return { success: false, error: '获取历史记录失败' }
    }
  }

  // 删除结果
  const deleteResult = async (id: number) => {
    try {
      console.warn('Delete API not implemented; removing locally.')
      results.value = results.value.filter(r => r.id !== id)

      if (currentResult.value?.id === id) {
        currentResult.value = null
      }

      return { success: true }
    } catch (error) {
      console.error('Failed to delete result:', error)
      return { success: false, error: '删除失败' }
    }
  }

  return {
    // 状态
    results,
    isGenerating,
    currentResult,
    selectedPlatform,
    keywords,
    emotionLevel,
    uploadedImages,

    // 方法
    generateCopywriting,
    regenerate,
    uploadImages,
    removeImage,
    fetchResults,
    deleteResult
  }
})
