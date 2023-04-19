<template>
  <div class="container mx-auto bg-gray-600 rounded p-6 my-6 text-white">
    <label class="block" for="qtext">Question Text</label>
    <textarea
      id="qtext"
      class="bg-gray-600 w-full"
      v-model="state.question_text"
    ></textarea>

    <QuestionTypeInput v-model="state.question_type"></QuestionTypeInput>

    <TextList v-model="state.options"></TextList>
    <TextList
      v-if="state.question_type === 'MATCH'"
      v-model="state.extra_options"
    ></TextList>
    <button @click="createQuestion">click</button>
  </div>
</template>

<script setup>
import { reactive } from "vue";
const state = reactive({
  question_text: "",
  question_type: "ONE",
  options: [],
  extra_options: [],
});
function createQuestion() {
  $fetch("/question/", {
    method: "POST",
    baseURL: "http://127.0.0.1:8000",
    params: { user_id: "test_front" },
    body: {
      question_text: state.question_text,
      question_type: state.question_type,
      options: state.options,
      extra_options: state.extra_options,
    },
  }).then((res) => {
    navigateTo({ path: "/question/" + res.id });
  });
}
</script>
