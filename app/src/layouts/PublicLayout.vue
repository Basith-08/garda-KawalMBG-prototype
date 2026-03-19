<script setup lang="ts">
import { useRoute } from 'vue-router'

const route = useRoute()
</script>

<template>
  <div class="min-h-screen flex flex-col">
    <!-- Top Bar -->
    <header class="bg-navy-900 text-white px-4 md:px-6 py-4 flex items-center justify-between sticky top-0 z-50 shadow-md">
      <router-link to="/" class="text-lg md:text-xl font-bold tracking-tight hover:opacity-90 transition-opacity">KawalMBG</router-link>
      <nav class="flex items-center gap-4 md:gap-6">
        <router-link
          to="/vendor-score"
          class="text-sm font-medium transition-colors"
          :class="route.path.startsWith('/vendor-score') ? 'text-brand-accent' : 'text-navy-300 hover:text-white'"
        >
          Vendor Score
        </router-link>
        <router-link
          to="/education"
          class="text-sm font-medium transition-colors"
          :class="route.path === '/education' ? 'text-brand-accent' : 'text-navy-300 hover:text-white'"
        >
          Education &amp; FAQ
        </router-link>
      </nav>
    </header>

    <!-- Content -->
    <main class="flex-1 bg-navy-50">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>
