<template>
  <div class="relative inline-flex items-center justify-center">
    <svg :width="size" :height="size" class="transform -rotate-90">
      <circle
        :cx="size / 2"
        :cy="size / 2"
        :r="radius"
        stroke="hsl(var(--muted))"
        :stroke-width="strokeWidth"
        fill="transparent"
        class="opacity-20"
      />
      <circle
        :cx="size / 2"
        :cy="size / 2"
        :r="radius"
        :stroke="color"
        :stroke-width="strokeWidth"
        fill="transparent"
        :stroke-dasharray="strokeDasharray"
        :stroke-dashoffset="strokeDashoffset"
        class="transition-all duration-500 ease-in-out"
        stroke-linecap="round"
      />
    </svg>
    <div class="absolute inset-0 flex items-center justify-center">
      <slot />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  value: {
    type: Number,
    default: 0
  },
  size: {
    type: Number,
    default: 120
  },
  strokeWidth: {
    type: Number,
    default: 8
  },
  color: {
    type: String,
    default: "hsl(var(--primary))"
  }
})

const radius = computed(() => (props.size - props.strokeWidth) / 2)
const circumference = computed(() => radius.value * 2 * Math.PI)
const strokeDasharray = computed(() => circumference.value)
const strokeDashoffset = computed(() => circumference.value - (props.value / 100) * circumference.value)
</script>