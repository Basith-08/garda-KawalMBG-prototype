<script setup lang="ts">
import { ref, computed } from 'vue'
import { getData, type School } from '@/services/localStorage'

const data = getData()
const schools = ref<School[]>(data.schools)
const searchQuery = ref('')

const filteredSchools = computed(() => {
  if (!searchQuery.value) return schools.value
  return schools.value.filter(s => s.name.toLowerCase().includes(searchQuery.value.toLowerCase()))
})

function statusColor(status: string) {
  if (status === 'safe') return 'bg-status-safe'
  if (status === 'medium') return 'bg-status-medium'
  return 'bg-status-high-risk'
}
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 md:px-8 py-6 md:py-8 animate-fade-in">
    <div class="flex flex-col lg:flex-row gap-6 lg:gap-8">
      <!-- Left: Search & Table -->
      <div class="flex-1 min-w-0">
        <div class="flex flex-col sm:flex-row items-center gap-3 mb-4 w-full">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Masukkan nama sekolah (contoh: SDN 01 Menteng)..."
            class="w-full sm:w-auto sm:flex-1 px-4 py-3 border border-navy-300 rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-brand-accent"
          />
          <div class="flex items-center gap-3 w-full sm:w-auto shrink-0 justify-end">
            <button class="w-12 h-12 rounded-full border border-navy-300 flex items-center justify-center hover:bg-navy-100 transition-colors">
              <i class="pi pi-search text-navy-600"></i>
            </button>
            <button class="w-12 h-12 rounded-full bg-navy-900 text-white flex items-center justify-center hover:bg-navy-800 transition-colors">
              <i class="pi pi-filter"></i>
            </button>
          </div>
        </div>

        <div class="mb-4 flex items-center gap-2">
          <span class="text-sm text-navy-600">Filter aktif:</span>
          <span class="bg-navy-200 text-navy-600 text-xs px-3 py-1 rounded-full flex items-center gap-1">
            Semua <button class="ml-1 hover:text-navy-900">×</button>
          </span>
        </div>

        <div class="bg-white rounded-xl shadow-sm border border-navy-200 overflow-x-auto">
          <table class="w-full min-w-[700px]">
            <thead>
              <tr class="border-b-2 border-navy-200">
                <th class="text-left px-6 py-4 text-sm font-semibold text-navy-700">Sekolah</th>
                <th class="text-left px-6 py-4 text-sm font-semibold text-navy-700">Vendor</th>
                <th class="text-left px-6 py-4 text-sm font-semibold text-navy-700">Trust Score</th>
                <th class="text-left px-6 py-4 text-sm font-semibold text-navy-700">Status</th>
                <th class="px-6 py-4"></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="school in filteredSchools" :key="school.id" class="odd:bg-navy-50 hover:bg-navy-100 transition-colors">
                <td class="px-6 py-4 text-sm text-navy-700">{{ school.name }}</td>
                <td class="px-6 py-4 text-sm text-navy-700">{{ school.vendorName }}</td>
                <td class="px-6 py-4 text-sm font-semibold text-navy-900">{{ school.trustScore }}</td>
                <td class="px-6 py-4">
                  <div class="flex items-center gap-2">
                    <span class="w-3 h-3 rounded-full" :class="statusColor(school.status)"></span>
                    <span class="text-sm text-navy-700">{{ school.statusText }}</span>
                  </div>
                </td>
                <td class="px-6 py-4">
                  <router-link :to="`/vendor-score/${school.id}`" class="text-navy-500 hover:text-navy-900 transition-colors">
                    <i class="pi pi-eye text-lg"></i>
                  </router-link>
                </td>
              </tr>
            </tbody>
          </table>
          <div v-if="filteredSchools.length === 0" class="p-10 text-center text-navy-500 bg-white">
            <i class="pi pi-inbox text-4xl mb-3 text-navy-300"></i>
            <p>Tidak ada sekolah yang sesuai dengan pencarian.</p>
          </div>
        </div>
      </div>

      <!-- Right: Legend -->
      <div class="w-full lg:w-80 shrink-0">
        <div class="bg-white rounded-xl shadow-sm border border-navy-200 p-6 sticky top-24">
          <h3 class="text-xl font-bold text-navy-900 mb-4">Keterangan:</h3>
          <ul class="space-y-4">
            <li>
              <span class="font-bold text-navy-900">Excellent (90-100)</span>
              <p class="text-sm text-navy-500 mt-0.5">Vendor sangat patuh dan kualitas terjaga.</p>
            </li>
            <li>
              <span class="font-bold text-navy-900">Good (70-89)</span>
              <p class="text-sm text-navy-500 mt-0.5">Kinerja stabil, terdapat kendala minor logistik.</p>
            </li>
            <li>
              <span class="font-bold text-navy-900">Warning (50-69)</span>
              <p class="text-sm text-navy-500 mt-0.5">Perlu pengawasan rutin dari komite sekolah.</p>
            </li>
            <li>
              <span class="font-bold text-navy-900">High Risk (&lt;50)</span>
              <p class="text-sm text-navy-500 mt-0.5">Rekomendasi peninjauan ulang kontrak.</p>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>
