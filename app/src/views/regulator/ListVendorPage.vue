<script setup lang="ts">
import { ref, computed } from 'vue'
import { getData, type Vendor } from '@/services/api'

const data = getData()
const vendors = ref<Vendor[]>(data.vendors)
const searchQuery = ref('')
const page = ref(1)

const filtered = computed(() => {
  if (!searchQuery.value) return vendors.value
  return vendors.value.filter(v => v.name.toLowerCase().includes(searchQuery.value.toLowerCase()))
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
      <input v-model="searchQuery" type="text" placeholder="Masukan nama vendor" class="w-full sm:flex-1 px-5 py-3.5 border border-navy-300 rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-brand-accent" />
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
            <th class="text-left px-6 py-4 text-sm font-semibold text-navy-700">Vendor</th>
            <th class="text-left px-6 py-4 text-sm font-semibold text-navy-700">Status</th>
            <th class="text-left px-6 py-4 text-sm font-semibold text-navy-700">Trust Score</th>
            <th class="px-6 py-4"></th>
            <th class="px-6 py-4"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="v in filtered" :key="v.id" class="odd:bg-navy-50 hover:bg-navy-100 transition-colors">
            <td class="px-6 py-4 text-sm text-navy-700">{{ v.name }}</td>
            <td class="px-6 py-4">
              <div class="flex items-center gap-2">
                <span class="w-3 h-3 rounded-full" :class="statusColor(v.status)"></span>
                <span class="text-sm text-navy-700">{{ v.statusText }}</span>
              </div>
            </td>
            <td class="px-6 py-4 text-sm font-semibold text-navy-900">{{ v.trustScore }}</td>
            <td class="px-6 py-4">
              <span class="text-xs flex items-center gap-1" :class="v.trendDir === 'up' ? 'text-brand-success' : 'text-brand-danger'">
                <i :class="v.trendDir === 'up' ? 'pi pi-arrow-up-right' : 'pi pi-arrow-down-right'" class="text-[10px]"></i>
                {{ v.trend }}% Dari bulan lalu
              </span>
            </td>
            <td class="px-6 py-4">
              <router-link :to="`/regulator/vendors/${v.id}`" class="text-navy-500 hover:text-navy-900"><i class="pi pi-eye text-lg"></i></router-link>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="filtered.length === 0" class="p-10 text-center text-navy-500 bg-white border-b border-navy-100">
        <i class="pi pi-inbox text-4xl mb-3 text-navy-300"></i>
        <p>Tidak ada vendor yang sesuai dengan pencarian.</p>
      </div>
      <div class="flex justify-end items-center gap-2 px-6 py-4 border-t border-navy-100">
        <button class="w-8 h-8 rounded border border-navy-200 flex items-center justify-center text-navy-500 hover:bg-navy-100"><i class="pi pi-chevron-left text-xs"></i></button>
        <button class="w-8 h-8 rounded flex items-center justify-center text-sm font-semibold" :class="page === 1 ? 'bg-brand-accent text-white' : 'border border-navy-200 text-navy-600'" @click="page = 1">1</button>
        <button class="w-8 h-8 rounded flex items-center justify-center text-sm font-semibold" :class="page === 2 ? 'bg-brand-accent text-white' : 'border border-navy-200 text-navy-600'" @click="page = 2">2</button>
        <button class="w-8 h-8 rounded border border-navy-200 flex items-center justify-center text-navy-500 hover:bg-navy-100"><i class="pi pi-chevron-right text-xs"></i></button>
      </div>
    </div>
  </div>
</template>
