<template>
  <div
    class="bg-gray-600 rounded p-2 my-2 first:pt-0 first:mt-0 last:mb-0 divide-y"
  >
    <AnswerOne
      v-if="answerType == 'ONE'"
      v-for="(isCorrect, text) in answer.answer"
      :is-correct="isCorrect"
      :text="text"
    ></AnswerOne>
    <AnswerMany
      v-if="answerType == 'MANY'"
      v-for="(isCorrect, text) in answer.answer"
      :is-correct="isCorrect"
      :text="text"
    ></AnswerMany>
    <AnswerOrder
      v-if="answerType == 'ORDER'"
      v-for="(isCorrect, text) in answer.answer"
      :is-correct="isCorrect"
      :text="text"
    ></AnswerOrder>
    <AnswerMatch
      v-if="answerType == 'MATCH'"
      v-for="(isCorrect, text) in answer.answer"
      :is-correct="isCorrect"
      :text="text"
    ></AnswerMatch>
  </div>
</template>
<script setup>
defineProps(["answer", "answerType"]);
</script>
