<template>
  <div
    class="container mx-auto bg-gray-600 rounded p-6 my-6 text-white relative border"
  >
    <div class="absolute top-0 right-0">{{ answer.id }}</div>
    <AnswerList :answer="answer" :answer-type="answerType"> </AnswerList>
    <AnswerTags :answer="answer"></AnswerTags>
  </div>
</template>
<script setup>
defineProps(["answer", "answerType"]);
</script>
