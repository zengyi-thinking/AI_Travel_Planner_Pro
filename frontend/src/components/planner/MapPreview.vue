<template>
  <div class="w-full h-64 bg-slate-200 rounded-2xl relative overflow-hidden shadow-inner group cursor-pointer">
    <img
      :src="imageUrl"
      class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
      alt="地图预览"
    >
    <div class="absolute inset-0 bg-black/10 flex items-center justify-center group-hover:bg-black/20 transition-colors">
      <button class="bg-white px-4 py-2 rounded-full shadow-lg font-bold text-slate-700 flex items-center gap-2 transform transition-transform group-hover:scale-105">
        <i class="fas fa-map"></i> 查看地图预览
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    imageUrl?: string
  }>(),
  {
    imageUrl:
      'https://images.unsplash.com/photo-1526481280693-3bfa7568e0f3?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80'
  }
)
</script>
