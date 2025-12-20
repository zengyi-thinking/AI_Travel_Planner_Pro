<template>
  <div class="bg-[#F8FAFC] h-screen flex overflow-hidden">
    <PlannerSidebar />

    <main class="flex-1 flex flex-col relative overflow-hidden">
      <PlannerHeader />

      <div class="flex-1 overflow-y-auto p-8 relative">
        <div class="absolute top-0 right-0 w-[600px] h-[600px] bg-teal-50 rounded-full filter blur-[100px] -z-10 pointer-events-none"></div>

        <div class="grid lg:grid-cols-3 gap-8 max-w-7xl mx-auto">
          <div class="lg:col-span-1 space-y-6">
            <ItineraryForm
              :destination="destination"
              :days="days"
              :budget="budget"
              :travel-style="travelStyle"
              @update:destination="destination = $event"
              @update:days="days = $event"
              @update:budget="budget = $event"
              @update:travelStyle="travelStyle = $event"
              @generate="generateItinerary"
            />

            <InspirationCard class="fade-in-up" />
          </div>

          <div class="lg:col-span-2 flex flex-col gap-6">
            <MapPreview />

            <ItineraryCard v-if="generatedItinerary" :itinerary="generatedItinerary" />
            <EmptyStateCard v-else />
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import ItineraryForm from '@/components/planner/ItineraryForm.vue'
import ItineraryCard from '@/components/planner/ItineraryCard.vue'
import PlannerSidebar from '@/components/planner/PlannerSidebar.vue'
import MapPreview from '@/components/planner/MapPreview.vue'
import PlannerHeader from '@/components/planner/PlannerHeader.vue'
import InspirationCard from '@/components/planner/InspirationCard.vue'
import EmptyStateCard from '@/components/planner/EmptyStateCard.vue'

const destination = ref('')
const days = ref(3)
const budget = ref(5000)
const travelStyle = ref('leisure')
const generatedItinerary = ref<null | {
  title: string
  summary: string
  destination: string
  days: number
  budget: number
  styleLabel: string
}>(null)

const styleLabelMap: Record<string, string> = {
  leisure: '休闲放松',
  adventure: '特种兵打卡',
  foodie: '美食探索'
}

const generateItinerary = () => {
  generatedItinerary.value = {
    title: `${destination.value} ${days.value}日游`,
    summary: '行程已生成，点击右上角导出或继续调整参数优化线路。',
    destination: destination.value,
    days: days.value,
    budget: budget.value,
    styleLabel: styleLabelMap[travelStyle.value] || travelStyle.value
  }
}
</script>
