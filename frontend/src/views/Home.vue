<template>
  <div class="relative min-h-screen overflow-hidden">
    <div class="absolute inset-0 -z-10">
      <div class="absolute top-24 right-[-120px] h-96 w-96 rounded-full bg-teal-200/70 blur-[90px] animate-blob"></div>
      <div class="absolute bottom-10 left-[-120px] h-96 w-96 rounded-full bg-blue-200/70 blur-[90px] animate-blob animation-delay-2000"></div>
    </div>

    <Navbar />
    <Hero />
  </div>
</template>

<script setup lang="ts">
import Navbar from '@/components/common/Navbar.vue'
import Hero from '@/components/home/Hero.vue'
</script>
