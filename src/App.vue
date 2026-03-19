<script setup lang="ts">
import { onMounted } from 'vue'
import { seedData } from '@/services/localStorage'

onMounted(() => {
  seedData()
})
</script>

<template>
  <router-view />
</template>
