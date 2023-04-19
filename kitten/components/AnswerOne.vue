<template>
    <div class="flex flex-row gap-4 items-center">
        <div class="flex-none">
            <CheckIcon class="h-6 w-6 text-white" v-if="isCorrect == 'True'"></CheckIcon>
            <XMarkIcon class="h-6 w-6 text-white" v-else></XMarkIcon>
        </div>
        <div class="flex-auto">{{ text }}</div>
    </div>
</template>
<script setup>
import { XMarkIcon, CheckIcon } from '@heroicons/vue/24/solid'

defineProps(["isCorrect", "text"])

</script>