<template>
  <div>
    <div
      class="flex flex-row gap-4 items-center my-4"
      v-for="(item, index) in value"
    >
      <textarea
        v-model="item.value"
        class="bg-gray-600 w-full flex-auto"
      ></textarea>
      <TrashIcon
        class="h-6 w-6 text-white flex-none"
        @click="deleteItem(index)"
      ></TrashIcon>
    </div>
    <div class="flex justify-center">
      <PlusCircleIcon
        class="h-6 w-6 text-white flex-none"
        @click="addItem"
      ></PlusCircleIcon>
    </div>
  </div>
</template>
<script setup>
import { TrashIcon, PlusCircleIcon } from "@heroicons/vue/24/solid";
import { computed, ref, watchEffect } from "vue";

const props = defineProps(["modelValue"]);
const emit = defineEmits(["update:modelValue"]);

const value = ref(
  props.modelValue.map((v) => {
    return { value: v };
  })
);
function addItem() {
  value.value.push({ value: "" });
}
function deleteItem(index) {
  value.value.splice(index, 1);
}
const arrayValue = computed(() => {
  return value.value.map((v) => v.value);
});
watchEffect(() => {
  emit("update:modelValue", arrayValue);
});
</script>
