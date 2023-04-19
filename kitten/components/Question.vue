<template>
  <p class="text-xl text-justify">
    {{ question.text }}
  </p>
  <p class="text-base text-justify text-slate-400">
    {{ converter(question.question_type) }}
  </p>
  <div class="divide-y">
    <p v-for="option in question.options.options">{{ option }}</p>
  </div>
  <div class="divide-y">
    <p v-for="option in question.options.extra_options">{{ option }}</p>
  </div>
</template>
<script setup>
defineProps(["question"]);
const converter = convertQType;
</script>
