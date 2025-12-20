<template>
  <div class="h-screen flex bg-[#F8FAFC]">
    <!-- Sidebar -->
    <aside class="w-64 bg-white border-r border-slate-100 flex flex-col shadow-sm flex-shrink-0">
      <div class="p-6 flex items-center gap-2 text-teal-500">
        <i class="fas fa-paper-plane text-2xl"></i>
        <span class="font-bold text-xl text-slate-800">WanderFlow</span>
      </div>
      <nav class="flex-1 mt-4">
        <router-link to="/planner" class="nav-item">
          <i class="fas fa-map w-6"></i> 规划行程
        </router-link>
        <router-link to="/qa" class="nav-item active">
          <i class="fas fa-comment-dots w-6"></i> AI 助手
        </router-link>
        <router-link to="/copywriter" class="nav-item">
          <i class="fas fa-pen-nib w-6"></i> 文案生成
        </router-link>
        <router-link to="/settings" class="nav-item">
          <i class="fas fa-cog w-6"></i> 账户设置
        </router-link>
      </nav>
      <div class="p-4 border-t border-slate-100">
        <div class="bg-teal-50 rounded-xl p-4">
          <h4 class="text-sm font-bold text-teal-800 mb-1">对话模式</h4>
          <div class="space-y-2 text-xs">
            <div class="flex items-center gap-2 text-slate-600">
              <i class="fas fa-circle text-[8px] text-green-500"></i>
              <span>智能对话</span>
            </div>
            <div class="flex items-center gap-2 text-slate-600">
              <i class="fas fa-circle text-[8px] text-blue-500"></i>
              <span>知识库问答</span>
            </div>
            <div class="flex items-center gap-2 text-slate-600">
              <i class="fas fa-circle text-[8px] text-yellow-500"></i>
              <span>天气查询</span>
            </div>
            <div class="flex items-center gap-2 text-slate-600">
              <i class="fas fa-circle text-[8px] text-purple-500"></i>
              <span>语音对话</span>
            </div>
          </div>
        </div>
      </div>
    </aside>

    <ChatContainer>
      <template #header>
        <div class="flex items-center justify-between w-full">
          <div class="flex items-center gap-3">
            <div class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
            <h2 class="text-lg font-bold text-slate-700">WanderBot 智能向导</h2>
            <span class="text-xs bg-green-100 text-green-600 px-2 py-1 rounded-full">在线</span>
          </div>
          <div class="flex items-center gap-3">
            <FeatureToggle
              :label="`知识库: ${knowledgeEnabled ? 'ON' : 'OFF'}`"
              icon="fas fa-database"
              :active="knowledgeEnabled"
              active-class="bg-blue-200 text-blue-700"
              inactive-class="bg-blue-100 text-blue-600"
              @toggle="toggleFeature('knowledge')"
            />
            <FeatureToggle
              :label="`天气: ${weatherEnabled ? 'ON' : 'OFF'}`"
              icon="fas fa-cloud-sun"
              :active="weatherEnabled"
              active-class="bg-yellow-200 text-yellow-700"
              inactive-class="bg-yellow-100 text-yellow-600"
              @toggle="toggleFeature('weather')"
            />
            <FeatureToggle
              :label="`语音: ${voiceEnabled ? 'ON' : 'OFF'}`"
              icon="fas fa-microphone"
              :active="voiceEnabled"
              active-class="bg-purple-200 text-purple-700"
              inactive-class="bg-purple-100 text-purple-600"
              @toggle="toggleFeature('voice')"
            />
          </div>
        </div>
      </template>

      <template #body>
        <div class="max-w-4xl mx-auto space-y-6">
          <div class="flex justify-center fade-in-up">
            <div class="glass-card p-6 max-w-2xl text-center">
              <div class="w-16 h-16 bg-gradient-to-br from-teal-400 to-blue-500 rounded-full flex items-center justify-center mx-auto mb-4 text-white text-2xl shadow-lg float-anim">
                <i class="fas fa-robot"></i>
              </div>
              <h3 class="text-xl font-bold text-slate-800 mb-2">嗨，我是您的全能旅行助理！</h3>
              <p class="text-slate-500 text-sm mb-6">您可以向我咨询天气、签证政策、行程规划或任何旅行问题。</p>
              <QuickQuestions :questions="quickQuestions" @select="handleQuickQuestion">
                <template #icon="{ question }">
                  <i :class="quickQuestionIcon(question)" class="mr-2"></i>
                </template>
              </QuickQuestions>
            </div>
          </div>

          <MessageList :messages="messages" />
        </div>
      </template>

      <template #footer>
        <div class="max-w-4xl mx-auto">
          <WeatherPanel
            :visible="weatherEnabled"
            :city="weatherCity"
            :loading="weatherLoading"
            :results="weatherResults"
            @update:city="weatherCity = $event"
            @query="queryWeather"
            @close="weatherEnabled = false"
          />
          <VoicePanel
            :visible="voiceEnabled"
            :is-recording="voiceRecording"
            :status-text="voiceStatusText"
            :has-playback="voiceHasPlayback"
            @record="startRecording"
            @stop="stopRecording"
            @play="playRecording"
            @close="voiceEnabled = false"
          />
          <InputBox
            v-model="inputMessage"
            placeholder="输入您的问题..."
            @send="sendMessage"
          />
          <div class="flex justify-center mt-3">
            <div class="flex gap-2 text-xs text-slate-400">
              <span><i class="fas fa-keyboard mr-1"></i>Enter 发送</span>
              <span>|</span>
              <span><i class="fas fa-magic mr-1"></i>点击快捷问题</span>
            </div>
          </div>
        </div>
      </template>
    </ChatContainer>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import ChatContainer from '@/components/chat/ChatContainer.vue'
import FeatureToggle from '@/components/chat/FeatureToggle.vue'
import MessageList from '@/components/chat/MessageList.vue'
import InputBox from '@/components/chat/InputBox.vue'
import QuickQuestions from '@/components/chat/QuickQuestions.vue'
import WeatherPanel from '@/components/chat/WeatherPanel.vue'
import VoicePanel from '@/components/chat/VoicePanel.vue'

interface ChatMessage {
  id: number
  role: 'user' | 'assistant'
  content: string
}

interface WeatherItem {
  date: string
  icon: string
  desc: string
  high: number
  low: number
  humidity: number
  wind: number
}

const messages = ref<ChatMessage[]>([
  {
    id: 1,
    role: 'assistant',
    content: '您好！我是WanderBot，您的AI旅行助理。我可以帮您查询天气、推荐景点、制定行程等。'
  }
])

const inputMessage = ref('')
const knowledgeEnabled = ref(false)
const weatherEnabled = ref(false)
const voiceEnabled = ref(false)

const weatherCity = ref('')
const weatherLoading = ref(false)
const weatherResults = ref<WeatherItem[]>([])

const voiceRecording = ref(false)
const voiceStatusText = ref('点击开始录音')
const voiceHasPlayback = ref(false)

const quickQuestions = [
  '查询北京未来3天的天气',
  '帮我制定一个3天上海旅行计划',
  '泰国签证办理需要哪些材料？',
  '播放刚才的回复'
]

const quickQuestionIcon = (question: string) => {
  if (question.includes('天气')) return 'fas fa-cloud-sun text-yellow-500'
  if (question.includes('行程')) return 'fas fa-map-marked-alt text-green-500'
  if (question.includes('签证')) return 'fas fa-passport text-blue-500'
  return 'fas fa-volume-up text-purple-500'
}

const toggleFeature = (feature: 'knowledge' | 'weather' | 'voice') => {
  if (feature === 'knowledge') knowledgeEnabled.value = !knowledgeEnabled.value
  if (feature === 'weather') weatherEnabled.value = !weatherEnabled.value
  if (feature === 'voice') voiceEnabled.value = !voiceEnabled.value
}

const sendMessage = () => {
  if (!inputMessage.value.trim()) return

  messages.value.push({
    id: messages.value.length + 1,
    role: 'user',
    content: inputMessage.value
  })

  const userMessage = inputMessage.value
  inputMessage.value = ''

  setTimeout(() => {
    messages.value.push({
      id: messages.value.length + 1,
      role: 'assistant',
      content: `我理解您的问题是："${userMessage}"。我会为您提供详细的旅行建议。`
    })
  }, 800)
}

const handleQuickQuestion = (question: string) => {
  inputMessage.value = question
  sendMessage()
}

const queryWeather = () => {
  if (!weatherCity.value.trim()) return
  weatherLoading.value = true
  weatherResults.value = []

  setTimeout(() => {
    const now = new Date()
    weatherResults.value = Array.from({ length: 3 }).map((_, index) => {
      const date = new Date(now)
      date.setDate(now.getDate() + index)
      return {
        date: date.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' }),
        icon: ['☀️', '⛅', '🌧️'][index % 3],
        desc: ['阳光明媚', '多云转晴', '小雨'][index % 3],
        high: 22 + index,
        low: 12 + index,
        humidity: 50 + index * 5,
        wind: 2 + index
      }
    })
    weatherLoading.value = false
  }, 900)
}

const startRecording = () => {
  voiceRecording.value = true
  voiceStatusText.value = '正在录音...'
}

const stopRecording = () => {
  voiceRecording.value = false
  voiceStatusText.value = '录音已停止'
  voiceHasPlayback.value = true
}

const playRecording = () => {
  voiceStatusText.value = '播放中...'
  setTimeout(() => {
    voiceStatusText.value = '点击开始录音'
  }, 1000)
}
</script>
