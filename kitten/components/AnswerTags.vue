<template>
  <div>
    <p>
      Как верный этот ответ отметили {{ isCorrect.percentTrue }}%({{
        isCorrect.countsTrue
      }}) людей. Как не верный {{ isCorrect.percentFalse }}%({{
        isCorrect.countsFalse
      }}).
    </p>

    <div class="flex flex-row">
      <div
        class="bg-green-600 h-4"
        :style="{ width: isCorrect.percentTrue + '%' }"
      ></div>
      <div
        class="bg-red-600 h-4"
        :style="{ width: isCorrect.percentFalse + '%' }"
      ></div>
    </div>
  </div>
</template>
<script setup>
import { computed } from "vue";
const props = defineProps(["answer"]);
const isCorrect = computed(() => {
  return {
    countsTrue: props.answer.tags_stat.IS_CORRECT?.True?.counts
      ? props.answer.tags_stat.IS_CORRECT?.True?.counts
      : 0,
    percentTrue: props.answer.tags_stat.IS_CORRECT?.True?.percent
      ? props.answer.tags_stat.IS_CORRECT?.True?.percent
      : 0,
    countsFalse: props.answer.tags_stat.IS_CORRECT?.False?.counts
      ? props.answer.tags_stat.IS_CORRECT?.False?.counts
      : 0,
    percentFalse: props.answer.tags_stat.IS_CORRECT?.False?.percent
      ? props.answer.tags_stat.IS_CORRECT?.False?.percent
      : 0,
  };
});
</script>
