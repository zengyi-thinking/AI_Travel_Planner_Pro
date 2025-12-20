<template>
  <aside class="w-64 bg-white border-r border-slate-100 flex flex-col z-20 shadow-sm">
    <div class="p-6 flex items-center gap-2 text-teal-500">
      <i class="fas fa-paper-plane text-2xl"></i>
      <span class="font-bold text-xl text-slate-800">WanderFlow</span>
    </div>

    <nav class="flex-1 mt-4">
      <router-link to="/planner" class="nav-item active">
        <i class="fas fa-map w-6"></i> 规划行程
      </router-link>
      <router-link to="/qa" class="nav-item">
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
      <div class="flex items-center gap-3 p-2 hover:bg-slate-50 rounded-lg cursor-pointer transition-colors">
        <img src="https://i.pravatar.cc/100?img=12" class="w-10 h-10 rounded-full" alt="用户头像">
        <div>
          <div class="text-sm font-bold text-slate-700">Alex Chen</div>
          <div class="text-xs text-slate-400">Pro 用户</div>
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
// Planner sidebar navigation.
</script>
