<template>
    <div class="flex flex-row gap-4 items-center">
        <div class="flex-none">
            <CheckCircleIcon class="h-6 w-6 text-white" v-if="isCorrect == 'True'"></CheckCircleIcon>
            <XCircleIcon class="h-6 w-6 text-white" v-else></XCircleIcon>
        </div>
        <div class="flex-auto">{{ text }}</div>
    </div>
</template>
<script setup>
import { XCircleIcon, CheckCircleIcon } from '@heroicons/vue/24/solid'

defineProps(["isCorrect", "text"])

</script>