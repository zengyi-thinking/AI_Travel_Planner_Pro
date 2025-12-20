<template>
  <div class="space-y-4">
    <MessageBubble
      v-for="message in messages"
      :key="message.id"
      :role="message.role"
      :content="message.content"
    />
  </div>
</template>

<script setup lang="ts">
import MessageBubble from '@/components/chat/MessageBubble.vue'

interface ChatMessage {
  id: number
  role: 'user' | 'assistant'
  content: string
}

defineProps<{
  messages: ChatMessage[]
}>()
</script>
