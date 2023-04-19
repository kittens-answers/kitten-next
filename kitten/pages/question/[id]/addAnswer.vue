<template>
  <div
    class="container mx-auto bg-gray-600 rounded p-6 my-6 text-white relative"
  >
    <NuxtLink class="absolute top-0 right-0" :to="'/question/' + data.id">{{
      data.id
    }}</NuxtLink>
    <Question :question="data"></Question>
    <TextList v-if="showOptions" v-model="state.options"></TextList>
    <TextList v-if="showExtraOptions" v-model="state.extra_options"></TextList>

    <AddAnswerOne
      v-if="data.question_type === 'ONE'"
      :options="state.options"
      v-model="state.answer"
    ></AddAnswerOne>
    <AddAnswerMany
      v-if="data.question_type === 'MANY'"
      :options="state.options"
      v-model="state.answer"
    ></AddAnswerMany>
  </div>
</template>

<script setup>
import { computed } from "vue";
const route = useRoute();
const { data } = await useFetch("/question/" + route.params.id, {
  method: "GET",
  baseURL: "http://127.0.0.1:8000",
});
const state = reactive({
  options: data.value.options.options,
  extra_options: data.value.options.extra_options,
  answer: [],
});
const showOptions = computed(() => {
  return data.value.options.options.length === 0;
});
const showExtraOptions = computed(() => {
  return (
    data.value.options.extra_options.length === 0 &&
    data.value.question_type === "MATCH"
  );
});
</script>
