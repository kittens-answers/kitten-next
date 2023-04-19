<template>
  <div class="sticky top-0 w-full container mx-auto bg-gray-800">
    <div class="flex justify-center gap-4">
      <NuxtLink to="/"
        ><HomeIcon class="h-6 w-6 text-white"></HomeIcon
      ></NuxtLink>
      <NuxtLink to="/search"
        ><MagnifyingGlassIcon class="h-6 w-6 text-white"></MagnifyingGlassIcon
      ></NuxtLink>
      <NuxtLink to="/question/new"
        ><DocumentPlusIcon class="h-6 w-6 text-white"></DocumentPlusIcon
      ></NuxtLink>
    </div>
  </div>
</template>
<script setup>
import {
  HomeIcon,
  DocumentPlusIcon,
  MagnifyingGlassIcon,
} from "@heroicons/vue/24/solid";
</script>
