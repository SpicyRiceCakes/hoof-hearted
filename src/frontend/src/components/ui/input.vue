<template>
  <input
    :class="cn(
      'flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50',
      $attrs.class
    )"
    v-bind="$attrs"
    :value="modelValue"
    @input="handleInput"
  />
</template>

<script setup>
import { cn } from '@/lib/utils'

defineProps({
  modelValue: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue'])

const handleInput = (event) => {
  emit('update:modelValue', event.target.value)
}
</script>