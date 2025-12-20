<template>
  <div v-if="visible" class="mb-4 glass-card p-4 rounded-xl">
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-3">
        <div
          class="w-3 h-3 rounded-full animate-pulse"
          :class="isRecording ? 'bg-green-500' : 'bg-red-500'"
        ></div>
        <span class="text-sm text-slate-600">{{ statusText }}</span>
      </div>
      <div class="flex gap-2 items-center">
        <button
          v-if="!isRecording"
          type="button"
          class="bg-red-500 hover:bg-red-600 text-white rounded-full w-12 h-12 flex items-center justify-center transition-colors"
          @click="$emit('record')"
        >
          <i class="fas fa-microphone"></i>
        </button>
        <button
          v-else
          type="button"
          class="bg-slate-500 hover:bg-slate-600 text-white rounded-full w-12 h-12 flex items-center justify-center transition-colors"
          @click="$emit('stop')"
        >
          <i class="fas fa-stop"></i>
        </button>
        <button
          v-if="hasPlayback"
          type="button"
          class="bg-green-500 hover:bg-green-600 text-white rounded-full w-12 h-12 flex items-center justify-center transition-colors"
          @click="$emit('play')"
        >
          <i class="fas fa-play"></i>
        </button>
        <button type="button" class="text-slate-400 hover:text-slate-600" @click="$emit('close')">
          <i class="fas fa-times"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  visible: boolean
  isRecording: boolean
  statusText: string
  hasPlayback: boolean
}>()

defineEmits<{
  record: []
  stop: []
  play: []
  close: []
}>()
</script>
