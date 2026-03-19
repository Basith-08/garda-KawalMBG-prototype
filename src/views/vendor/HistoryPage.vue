<script setup lang="ts">
import { ref, computed } from 'vue'
import { getData, type Distribution } from '@/services/localStorage'

const data = getData()
const distributions = ref<Distribution[]>(data.distributions)
const searchQuery = ref('')

const filtered = computed(() => {
  if (!searchQuery.value) return distributions.value
  return distributions.value.filter(d => d.schoolName.toLowerCase().includes(searchQuery.value.toLowerCase()))
})

function statusColor(s: string) {
  if (s === 'safe') return 'bg-status-safe'
  if (s === 'medium') return 'bg-status-medium'
  return 'bg-status-high-risk'
}
</script>

<template>
  <div class="animate-fade-in">
    <div class="flex flex-col sm:flex-row items-center gap-3 mb-4">
      <input v-model="searchQuery" type="text" placeholder="Masukan nama sekolah" class="w-full sm:flex-1 px-5 py-3.5 border border-navy-300 rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-brand-accent" />
      <div class="flex gap-3 w-full sm:w-auto justify-end">
        <button class="w-12 h-12 rounded-full border border-navy-300 flex items-center justify-center hover:bg-navy-100 shrink-0"><i class="pi pi-search text-navy-600"></i></button>
        <button class="w-12 h-12 rounded-full bg-navy-900 text-white flex items-center justify-center hover:bg-navy-800 shrink-0"><i class="pi pi-filter"></i></button>
      </div>
    </div>
    <div class="mb-4 flex items-center gap-2">
      <span class="text-sm text-navy-600">Filter aktif:</span>
      <span class="bg-navy-200 text-navy-600 text-xs px-3 py-1 rounded-full flex items-center gap-1">Semua <button class="ml-1">×</button></span>
    </div>

    <div class="bg-white rounded-xl shadow-sm border border-navy-200 overflow-x-auto">
      <table class="w-full min-w-[800px]">
        <thead>
          <tr class="border-b-2 border-navy-200">
            <th class="text-left px-6 py-4 text-sm font-semibold text-navy-700">Sekolah</th>
            <th class="text-left px-6 py-4 text-sm font-semibold text-navy-700">Porsi</th>
            <th class="text-left px-6 py-4 text-sm font-semibold text-navy-700">Status</th>
            <th class="text-left px-6 py-4 text-sm font-semibold text-navy-700">Time</th>
            <th class="text-left px-6 py-4 text-sm font-semibold text-navy-700">Risk Score</th>
            <th class="px-6 py-4"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="d in filtered" :key="d.id" class="odd:bg-navy-50 hover:bg-navy-100 transition-colors">
            <td class="px-6 py-4 text-sm text-navy-700">{{ d.schoolName }}</td>
            <td class="px-6 py-4 text-sm text-navy-700">{{ d.porsi }}</td>
            <td class="px-6 py-4">
              <div class="flex items-center gap-2">
                <span class="w-3 h-3 rounded-full" :class="statusColor(d.status)"></span>
                <span class="text-sm">{{ d.statusText }}</span>
              </div>
            </td>
            <td class="px-6 py-4 text-sm text-navy-700">{{ d.time }}</td>
            <td class="px-6 py-4 text-sm font-semibold text-navy-900">{{ d.riskScore }}</td>
            <td class="px-6 py-4">
              <router-link :to="`/vendor/history/${d.id}`" class="text-navy-500 hover:text-navy-900">
                <i class="pi pi-eye text-lg"></i>
              </router-link>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
