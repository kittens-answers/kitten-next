<template>
    <div class="flex flex-row gap-4 items-center">
        <div class="basis-1/2">{{ isCorrect }}</div>
        <div class="basis-1/2">{{ text }}</div>
    </div>
</template>
<script setup>
defineProps(["isCorrect", "text"])
</script>