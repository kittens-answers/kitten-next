<template>
  <div class="container mx-auto bg-gray-600 p-6 gap-4 grid grid-cols-1">
    <input class="w-full bg-gray-600" v-model="q" />
    <button @click="search">Найти</button>
    <SearchItem v-for="data in items" :data="data"></SearchItem>
  </div>
</template>
<script setup>
import { ref } from "vue";
const q = ref("");
const items = ref([]);
function search() {
  $fetch("/search/", {
    method: "POST",
    baseURL: "http://127.0.0.1:8000",
    params: { q: q.value },
  }).then((res) => {
    items.value = res;
  });
}
</script>
