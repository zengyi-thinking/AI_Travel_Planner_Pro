<template>
  <button
    type="button"
    :class="active ? activeClass : inactiveClass"
    class="text-xs px-3 py-1 rounded-full transition-colors"
    @click="$emit('toggle')"
  >
    <i :class="icon" class="mr-1"></i>{{ label }}
  </button>
</template>

<script setup lang="ts">
interface Props {
  label: string
  icon: string
  active: boolean
  activeClass: string
  inactiveClass: string
}

defineProps<Props>()
defineEmits<{
  toggle: []
}>()
</script>
