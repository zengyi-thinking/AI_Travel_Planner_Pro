<template>
  <div id="app">
    <router-view />
    <ToastContainer />
  </div>
</template>

<script setup lang="ts">
import ToastContainer from \'@/components/common/ToastContainer.vue\'

// This is the root component
</script>

<style>
#app {
  font-family: 'Poppins', 'Nunito', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
