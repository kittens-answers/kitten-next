<template>
    <div class="flex flex-row gap-4 items-center">
        <div class="flex-none">
            {{ isCorrect }}
        </div>
        <div class="flex-auto">{{ text }}</div>
    </div>
</template>
<script setup>
defineProps(["isCorrect", "text"])
</script>