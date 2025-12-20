<template>
  <section class="relative flex min-h-screen items-center pt-24">
    <div class="mx-auto grid w-full max-w-7xl items-center gap-12 px-6 md:grid-cols-2">
      <div class="fade-in-up">
        <div class="inline-block rounded-full border border-teal-100 bg-teal-50 px-4 py-1 text-sm font-semibold text-teal-600">
          ? AI 驱动的下一代旅行助手
        </div>
        <h1 class="mt-4 text-5xl font-bold leading-tight text-slate-800 md:text-7xl">
          让旅行 <br>
          <span class="bg-gradient-to-r from-teal-400 to-blue-500 bg-clip-text text-transparent">简单而纯粹</span>
        </h1>
        <p class="mt-6 max-w-lg text-lg leading-relaxed text-slate-500">
          告别繁琐的攻略查询。输入您的预算和偏好，WanderFlow 在几秒钟内为您生成包含景点、交通、美食的完美行程。
        </p>
        <div class="mt-8 flex flex-wrap gap-4">
          <router-link to="/planner" class="btn-primary text-lg px-8 py-4 shadow-xl hover:shadow-2xl">
            立即创建行程 <i class="fas fa-magic ml-2"></i>
          </router-link>
          <button class="flex items-center gap-2 rounded-full border-2 border-slate-200 px-8 py-4 font-bold text-slate-600 transition-all hover:border-teal-500 hover:text-teal-500">
            <i class="fas fa-play-circle text-xl"></i> 观看演示
          </button>
        </div>

        <div class="mt-10 flex items-center gap-4">
          <div class="flex -space-x-4">
            <img class="h-10 w-10 rounded-full border-2 border-white" src="https://i.pravatar.cc/100?img=1" alt="用户头像">
            <img class="h-10 w-10 rounded-full border-2 border-white" src="https://i.pravatar.cc/100?img=2" alt="用户头像">
            <img class="h-10 w-10 rounded-full border-2 border-white" src="https://i.pravatar.cc/100?img=3" alt="用户头像">
            <div class="flex h-10 w-10 items-center justify-center rounded-full border-2 border-white bg-slate-100 text-xs font-bold text-slate-500">
              +2k
            </div>
          </div>
          <div class="text-sm text-slate-500">
            <span class="font-bold text-slate-800">2,000+</span> 旅行者正在使用
          </div>
        </div>
      </div>

      <div class="relative fade-in-up md:pl-6" style="animation-delay: 0.2s;">
        <div class="relative z-10 transition-transform duration-500 hover:-translate-y-2">
          <img
            src="https://images.unsplash.com/photo-1500835556837-99ac94a94552?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80"
            alt="Travel"
            class="h-[500px] w-full rounded-[2rem] border-4 border-white object-cover shadow-2xl"
          >

          <div class="float-anim absolute -bottom-6 -left-6 flex items-center gap-3 rounded-2xl bg-white p-4 shadow-xl">
            <div class="flex h-10 w-10 items-center justify-center rounded-full bg-teal-100 text-teal-600">
              <i class="fas fa-map-marker-alt"></i>
            </div>
            <div>
              <div class="text-sm font-bold text-slate-800">已抵达 巴黎</div>
              <div class="text-xs text-slate-500">距离目的地 2km</div>
            </div>
          </div>

          <div class="absolute -right-6 top-10 rounded-2xl bg-white/90 p-4 shadow-xl backdrop-blur">
            <div class="flex items-center gap-2">
              <span class="text-yellow-500"><i class="fas fa-star"></i></span>
              <span class="font-bold text-slate-800">4.9</span>
              <span class="text-xs text-slate-400">(行程评分)</span>
            </div>
          </div>
        </div>

        <div class="absolute left-1/2 top-1/2 h-[120%] w-[120%] -translate-x-1/2 -translate-y-1/2 rounded-full border border-slate-200/70 opacity-50"></div>
        <div class="absolute left-1/2 top-1/2 h-[140%] w-[140%] -translate-x-1/2 -translate-y-1/2 rounded-full border border-dashed border-slate-200/70 opacity-30 animate-spin-slow"></div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
// Hero section for the landing page.
</script>

<style scoped>
.animate-spin-slow {
  animation: spin 20s linear infinite;
}

@keyframes spin {
  from {
    transform: translate(-50%, -50%) rotate(0deg);
  }
  to {
    transform: translate(-50%, -50%) rotate(360deg);
  }
}
</style>
