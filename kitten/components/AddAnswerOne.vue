<template>
  <div v-for="(option, index) in options">
    <div class="flex flex-row gap-4">
      <input
        type="radio"
        :id="'var' + index"
        :value="option"
        v-model="checked"
      />
      <div>{{ option }}</div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from "vue";
const props = defineProps(["options", "modelValue"]);
const emit = defineEmits(["update:modelValue"]);
const checked = ref("");
watch(checked, () => {
  emit("update:modelValue", answer.value);
});
const answer = computed(() => {
  return props.options.map((v) => {
    return [v, convertBool(v === checked.value)];
  });
});
</script>
