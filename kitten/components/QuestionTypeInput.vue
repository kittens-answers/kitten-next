<script setup>
import { computed } from "vue";

const props = defineProps(["modelValue"]);
const emit = defineEmits(["update:modelValue"]);
const converter = convertQType;

const value = computed({
  get() {
    return props.modelValue;
  },
  set(value) {
    emit("update:modelValue", value);
  },
});
</script>

<template>
  <div>
    <input type="radio" id="one" value="ONE" v-model="value" />
    <label for="one">{{ converter("ONE") }}</label>
  </div>
  <div>
    <input type="radio" id="many" value="MANY" v-model="value" />
    <label for="many">{{ converter("MANY") }}</label>
  </div>
  <input type="radio" id="order" value="ORDER" v-model="value" />
  <label for="order">{{ converter("ORDER") }}</label>
  <div>
    <input type="radio" id="match" value="MATCH" v-model="value" />
    <label for="match">{{ converter("MATCH") }}</label>
  </div>
</template>
