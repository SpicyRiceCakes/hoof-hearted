<template>
  <div 
    ref="progressRef"
    :class="cn('relative h-4 w-full overflow-hidden rounded-full bg-secondary', $attrs.class)"
  >
    <div
      :class="cn('h-full w-full flex-1 bg-primary transition-all', indicatorClass)"
      :style="{ transform: `translateX(-${100 - (value || 0)}%)` }"
    />
  </div>
</template>

<script setup>
import { cn } from '@/lib/utils'

defineProps({
  value: {
    type: Number,
    default: 0
  },
  indicatorClass: {
    type: String,
    default: ''
  }
})
</script>