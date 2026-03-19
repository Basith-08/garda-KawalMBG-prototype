<script setup lang="ts">
import { onMounted } from 'vue'
import { seedData } from '@/services/localStorage'
import Toast from 'primevue/toast'

onMounted(() => {
  seedData()
})
</script>

<template>
  <Toast />
  <router-view />
</template>
