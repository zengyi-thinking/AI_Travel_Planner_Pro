<template>
  <nav class="fixed top-0 z-50 w-full px-6 py-6">
    <div class="glass-card mx-auto flex max-w-7xl items-center justify-between px-6 py-3">
      <div class="flex items-center gap-2 text-teal-600">
        <i class="fas fa-paper-plane text-2xl"></i>
        <span class="text-xl font-bold text-slate-800">WanderFlow</span>
      </div>
      <div class="hidden gap-8 text-slate-600 font-medium md:flex">
        <a href="#" class="hover:text-teal-500 transition-colors">功能</a>
        <a href="#" class="hover:text-teal-500 transition-colors">目的地</a>
        <a href="#" class="hover:text-teal-500 transition-colors">关于我们</a>
      </div>
      <div class="flex gap-3">
        <router-link to="/login" class="px-5 py-2 text-slate-600 font-medium hover:text-teal-600">
          登录
        </router-link>
        <router-link to="/register" class="btn-primary py-2 px-6 text-sm">
          开始规划
        </router-link>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
// Shared top navigation bar for marketing pages.
</script>
