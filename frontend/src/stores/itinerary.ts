import { defineStore } from 'pinia'
import { ref } from 'vue'
import api, { longRunningApi } from '@/utils/api'
import type { Itinerary, ItineraryCreateRequest, DayPlan } from '@/types/api'

export const useItineraryStore = defineStore('itinerary', () => {
  const itineraries = ref<Itinerary[]>([])
  const currentItinerary = ref<Itinerary | null>(null)
  const isLoading = ref(false)
  const generatedPlans = ref<Record<number, DayPlan[]>>({})

  const fetchItineraries = async (page = 1, size = 10) => {
    isLoading.value = true
    try {
      const response = await api.get<Itinerary[]>('/api/v1/planner/itineraries', {
        params: { page, size }
      })
      itineraries.value = response
      return { success: true, data: response }
    } catch (error) {
      console.error('Failed to fetch itineraries:', error)
      return { success: false, error: '获取行程失败' }
    } finally {
      isLoading.value = false
    }
  }

  const createItinerary = async (data: ItineraryCreateRequest, options?: { useStrictJson?: boolean }) => {
    isLoading.value = true
    try {
      const response = await api.post<Itinerary>('/api/v1/planner/generate', {
        ...data,
        ...options
      })
      itineraries.value.unshift(response)
      currentItinerary.value = response
      return { success: true, data: response }
    } catch (error) {
      console.error('Failed to create itinerary:', error)
      return { success: false, error: '创建行程失败' }
    } finally {
      isLoading.value = false
    }
  }

  const updateItinerary = async (id: number, data: Partial<ItineraryCreateRequest>) => {
    try {
      const response = await api.put<Itinerary>(`/api/v1/planner/itineraries/${id}`, data)
      const index = itineraries.value.findIndex(item => item.id === id)
      if (index !== -1) {
        itineraries.value[index] = response
      }
      if (currentItinerary.value?.id === id) {
        currentItinerary.value = response
      }
      return { success: true, data: response }
    } catch (error) {
      console.error('Failed to update itinerary:', error)
      return { success: false, error: '更新行程失败' }
    }
  }

  const deleteItinerary = async (id: number) => {
    try {
      await api.delete(`/api/v1/planner/itineraries/${id}`)
      itineraries.value = itineraries.value.filter(item => item.id !== id)
      if (currentItinerary.value?.id === id) {
        currentItinerary.value = null
      }
      return { success: true }
    } catch (error) {
      console.error('Failed to delete itinerary:', error)
      return { success: false, error: '删除行程失败' }
    }
  }

  const generateDetailedItinerary = async (itineraryId: number, useStrictJson: boolean = true) => {
    isLoading.value = true
    try {
      // 使用longRunningApi以支持更长的超时时间（AI生成可能需要30-60秒）
      const response = await longRunningApi.post<Itinerary>(
        `/api/v1/planner/itineraries/${itineraryId}/generate-detail`,
        { use_strict_json: useStrictJson }
      )

      // 🔍 调试：检查返回数据是否包含坐标
      console.log('📍 [API] 详细行程生成完成')
      console.log('📍 [API] 行程ID:', response.id)
      console.log('📍 [API] days_detail数量:', response.days_detail?.length || 0)

      if (response.days_detail) {
        response.days_detail.forEach((day, dayIndex) => {
          console.log(`📍 [API] 第${dayIndex + 1}天: ${day.title}, 活动数: ${day.activities?.length || 0}`)

          if (day.activities) {
            day.activities.forEach((activity, actIndex) => {
              const hasCoords = activity.coordinates && activity.coordinates.lat && activity.coordinates.lng
              console.log(`  ${actIndex + 1}. ${activity.title}: ${hasCoords ? '✅有坐标' : '❌无坐标'}`)
              if (hasCoords) {
                console.log(`     坐标: (${activity.coordinates.lat}, ${activity.coordinates.lng})`)
              }
            })
          }
        })
      }

      if (currentItinerary.value?.id === itineraryId) {
        currentItinerary.value = response
      }
      return { success: true, data: response }
    } catch (error) {
      console.error('Failed to generate detailed itinerary:', error)
      return { success: false, error: '生成详细行程失败' }
    } finally {
      isLoading.value = false
    }
  }

  const optimizeItinerary = async (itineraryId: number, feedback: { feedback: string; affected_days?: number[] }) => {
    isLoading.value = true
    try {
      // 使用longRunningApi以支持更长的超时时间（AI优化可能需要30-60秒）
      const response = await longRunningApi.post<Itinerary>(
        `/api/v1/planner/itineraries/${itineraryId}/optimize`,
        {
          feedback: feedback.feedback,
          affected_days: feedback.affected_days || [],
          use_strict_json: true
        }
      )
      if (currentItinerary.value?.id === itineraryId) {
        currentItinerary.value = response
      }
      return { success: true, data: response }
    } catch (error) {
      console.error('Failed to optimize itinerary:', error)
      return { success: false, error: '优化行程失败' }
    } finally {
      isLoading.value = false
    }
  }

  const getGeneratedPlans = (itineraryId: number) => {
    return generatedPlans.value[itineraryId] || []
  }

  return {
    itineraries,
    currentItinerary,
    isLoading,
    generatedPlans,
    fetchItineraries,
    createItinerary,
    updateItinerary,
    deleteItinerary,
    generateDetailedItinerary,
    optimizeItinerary,
    getGeneratedPlans
  }
})
