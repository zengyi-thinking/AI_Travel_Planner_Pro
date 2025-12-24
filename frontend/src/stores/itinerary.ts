import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/utils/api'
import type { Itinerary, ItineraryCreateRequest, DayPlan } from '@/types/api'

export const useItineraryStore = defineStore('itinerary', () => {
  // 状态
  const itineraries = ref<Itinerary[]>([])
  const currentItinerary = ref<Itinerary | null>(null)
  const isLoading = ref(false)
  const generatedPlans = ref<Record<number, DayPlan[]>>({})

  // 获取所有行程
  const fetchItineraries = async (page = 1, size = 10) => {
    isLoading.value = true
    try {
      const response = await api.get<Itinerary[]>('/planner/itineraries', {
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

  // 创建行程
  const createItinerary = async (data: ItineraryCreateRequest) => {
    isLoading.value = true
    try {
      const response = await api.post<Itinerary>('/planner/generate', data)
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

  // 更新行程
  const updateItinerary = async (id: number, data: Partial<ItineraryCreateRequest>) => {
    try {
      const response = await api.put<Itinerary>(`/planner/itineraries/${id}`, data)
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

  // 删除行程
  const deleteItinerary = async (id: number) => {
    try {
      await api.delete(`/planner/itineraries/${id}`)

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

  // AI 生成行程
  const generateItineraryPlan = async (itineraryId: number, preferences: any) => {
    isLoading.value = true
    try {
      const response = await api.post<DayPlan[]>(`/planner/itineraries/${itineraryId}/generate`, preferences)
      generatedPlans.value[itineraryId] = response
      return { success: true, data: response }
    } catch (error) {
      console.error('Failed to generate itinerary:', error)
      return { success: false, error: 'AI生成行程失败' }
    } finally {
      isLoading.value = false
    }
  }

  // 获取生成的行程计划
  const getGeneratedPlans = (itineraryId: number) => {
    return generatedPlans.value[itineraryId] || []
  }

  return {
    // 状态
    itineraries,
    currentItinerary,
    isLoading,
    generatedPlans,

    // 方法
    fetchItineraries,
    createItinerary,
    updateItinerary,
    deleteItinerary,
    generateItineraryPlan,
    getGeneratedPlans
  }
})
