<template>
  <div class="map-test-page">
    <div class="header">
      <h1>🗺️ 地图功能测试页面</h1>
      <p>使用预设数据测试地图标记和路线显示</p>
    </div>

    <div class="content">
      <!-- 测试地图 -->
      <InteractiveMap
        :height="'500px'"
        :itinerary="testItinerary"
      />

      <!-- 测试数据说明 -->
      <div class="info-panel">
        <h3>📊 测试数据说明</h3>
        <div class="day-list">
          <div v-for="day in testItinerary.days_detail" :key="day.day_number" class="day-item">
            <h4>
              <span
                class="color-dot"
                :style="{ backgroundColor: getDayRouteColor(day.day_number) }"
              ></span>
              第{{ day.day_number }}天: {{ day.title }}
            </h4>
            <ul>
              <li v-for="activity in day.activities" :key="activity.title">
                <strong>{{ activity.title }}</strong>
                <span class="coords" v-if="activity.coordinates">
                  ({{ activity.coordinates.lat.toFixed(4) }}, {{ activity.coordinates.lng.toFixed(4) }})
                </span>
                <span v-else class="no-coords">⚠️ 无坐标</span>
              </li>
            </ul>
          </div>
        </div>
      </div>

      <!-- 调试按钮 -->
      <div class="debug-panel">
        <button @click="refreshMap">🔄 刷新地图</button>
        <button @click="openConsole">💻 打开控制台</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import InteractiveMap from '@/components/planner/InteractiveMap.vue'

// 带完整坐标的测试数据
const testItinerary = ref({
  title: '北京3日文化深度游',
  destination: '北京',
  days: 3,
  days_detail: [
    {
      day_number: 1,
      title: '故宫周边深度游',
      activities: [
        {
          time: '09:00',
          title: '故宫博物院',
          type: 'attraction',
          description: '中国明清两代的皇家宫殿',
          location: '北京市东城区景山前街4号',
          duration: '3小时',
          average_cost: 60,
          coordinates: {
            lng: 116.40198150528495,
            lat: 39.927388327577795
          }
        },
        {
          time: '12:30',
          title: '全聚德烤鸭店',
          type: 'meal',
          description: '百年老字号，品尝正宗北京烤鸭',
          location: '北京市东城区前门大街30号',
          duration: '1.5小时',
          average_cost: 200,
          coordinates: {
            lng: 116.397029,
            lat: 39.900123
          }
        },
        {
          time: '15:00',
          title: '天安门广场',
          type: 'attraction',
          description: '世界上最大的城市广场之一',
          location: '北京市东城区',
          duration: '1小时',
          average_cost: 0,
          coordinates: {
            lng: 116.4224009776628,
            lat: 39.93482727239599
          }
        },
        {
          time: '19:00',
          title: '北京饭店',
          type: 'accommodation',
          description: '四星级商务酒店',
          location: '北京市东城区东长安街33号',
          duration: '晚上',
          average_cost: 600,
          coordinates: {
            lng: 116.410123,
            lat: 39.915456
          }
        }
      ]
    },
    {
      day_number: 2,
      title: '长城一日游',
      activities: [
        {
          time: '08:00',
          title: '八达岭长城',
          type: 'attraction',
          description: '明长城的精华路段',
          location: '北京市延庆区八达岭',
          duration: '4小时',
          average_cost: 40,
          coordinates: {
            lng: 116.016863,
            lat: 40.358431
          }
        },
        {
          time: '13:00',
          title: '长城脚下农家菜',
          type: 'meal',
          description: '品尝当地特色菜',
          location: '北京市延庆区八达岭镇',
          duration: '1小时',
          average_cost: 80,
          coordinates: {
            lng: 116.018542,
            lat: 40.359123
          }
        }
      ]
    },
    {
      day_number: 3,
      title: '颐和园漫步',
      activities: [
        {
          time: '09:00',
          title: '颐和园',
          type: 'attraction',
          description: '中国古典园林之首',
          location: '北京市海淀区新建宫门路',
          duration: '3小时',
          average_cost: 30,
          coordinates: {
            lng: 116.28438433097374,
            lat: 40.008141350407804
          }
        },
        {
          time: '12:30',
          title: '颐和园附近餐厅',
          type: 'meal',
          description: '享用午餐',
          location: '北京市海淀区',
          duration: '1小时',
          average_cost: 100,
          coordinates: {
            lng: 116.283123,
            lat: 40.009234
          }
        }
      ]
    }
  ]
})

function getDayRouteColor(dayNumber: number): string {
  const dayColors = [
    '#ef4444', // 第1天 - 红色
    '#3b82f6', // 第2天 - 蓝色
    '#10b981', // 第3天 - 绿色
    '#f59e0b', // 第4天 - 橙色
    '#8b5cf6', // 第5天 - 紫色
    '#ec4899', // 第6天 - 粉色
    '#06b6d4', // 第7天 - 青色
  ]
  return dayColors[(dayNumber - 1) % dayColors.length]
}

function refreshMap() {
  location.reload()
}

function openConsole() {
  alert('请按 F12 打开浏览器控制台查看详细日志')
}
</script>

<style scoped>
.map-test-page {
  @apply min-h-screen bg-slate-50 p-8;
}

.header {
  @apply text-center mb-8;
}

.header h1 {
  @apply text-3xl font-bold text-slate-800 mb-2;
}

.header p {
  @apply text-slate-600;
}

.content {
  @apply max-w-7xl mx-auto grid lg:grid-cols-3 gap-8;
}

.info-panel {
  @apply bg-white rounded-xl shadow-lg p-6 lg:col-span-1;
}

.info-panel h3 {
  @apply text-lg font-bold text-slate-800 mb-4;
}

.day-list {
  @apply space-y-4;
}

.day-item h4 {
  @apply flex items-center gap-2 mb-2;
}

.color-dot {
  @apply w-4 h-4 rounded-full;
}

.day-item ul {
  @apply list-none pl-4 space-y-1;
}

.day-item li {
  @apply text-sm py-1;
}

.coords {
  @apply text-xs text-slate-500 ml-2;
}

.no-coords {
  @apply text-xs text-amber-600 ml-2;
}

.debug-panel {
  @apply bg-white rounded-xl shadow-lg p-6 lg:col-span-3 flex gap-4;
}

.debug-panel button {
  @apply px-6 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition-colors;
}
</style>
