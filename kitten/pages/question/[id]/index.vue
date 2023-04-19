<template>
    <SearchItem :data="data"></SearchItem>
</template>
<script setup>
const route = useRoute()
const { data } = await useFetch("/question/" + route.params.id, { method: "GET", baseURL: "http://127.0.0.1:8000" })
</script>