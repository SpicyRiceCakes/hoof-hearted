<template>
  <div :class="cn('backdrop-blur-sm bg-background/80 border-border/50 rounded-lg border bg-card text-card-foreground shadow-sm', $attrs.class)">
    <div class="flex flex-row items-center justify-between space-y-0 pb-2 p-6">
      <div class="text-sm font-medium flex items-center gap-2">
        <component :is="icon" class="h-4 w-4" />
        {{ title }}
      </div>
    </div>
    <div class="p-6 pt-0">
      <slot />
    </div>
  </div>
</template>

<script setup>
import { cn } from '@/lib/utils'

defineProps({
  title: {
    type: String,
    required: true
  },
  icon: {
    type: Object,
    required: true
  }
})
</script>