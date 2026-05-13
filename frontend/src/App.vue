<script setup lang="ts">
import { onMounted } from 'vue'
import { seedData } from '@/services/api'
import { useAuthStore } from '@/stores/auth'
import Toast from 'primevue/toast'

const authStore = useAuthStore()

onMounted(async () => {
  await authStore.restoreSession()
  await seedData(true)
})
</script>

<template>
  <Toast />
  <router-view />
</template>
