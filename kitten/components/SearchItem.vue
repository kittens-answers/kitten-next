<template>
  <div
    class="container mx-auto bg-gray-600 rounded p-6 my-6 text-white relative"
  >
    <NuxtLink class="absolute top-0 right-0" :to="'/question/' + data.id">{{
      data.id
    }}</NuxtLink>
    <Question :question="data"></Question>
    <Answers
      v-for="answer in data['answers']"
      :answer="answer"
      :answer-type="data.question_type"
    ></Answers>
    <NuxtLink :to="'/question/' + data.id + '/addAnswer'">
      <PlusCircleIcon class="h-6 w-6 text-white"></PlusCircleIcon
    ></NuxtLink>
  </div>
</template>
<script setup>
import { PlusCircleIcon } from "@heroicons/vue/24/solid";
defineProps(["data"]);
</script>
