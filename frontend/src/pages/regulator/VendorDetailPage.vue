<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { getData } from '@/services/api'

const route = useRoute()
const data = getData()
const vendor = computed(() => data.vendors.find((v: any) => v.id === route.params.id))
const distributions = computed(() => data.distributions.filter((d: any) => d.vendorId === route.params.id))
const trustRows = computed(() => {
  const breakdown = vendor.value?.trustBreakdown
  if (!breakdown) return []
  return [
    ['Ketepatan waktu', breakdown.timeliness],
    ['Bukti QC', breakdown.evidence],
    ['Receipt sekolah', breakdown.schoolReceipt],
    ['Konsistensi porsi', breakdown.portionConsistency],
    ['Histori alert', breakdown.history],
  ]
})

function statusColor(s: string) {
  if (s === 'safe') return 'bg-status-safe'
  if (s === 'medium') return 'bg-status-medium'
  return 'bg-status-high-risk'
}
</script>

<template>
  <div class="animate-fade-in" v-if="vendor">
    <router-link to="/regulator/vendors" class="inline-flex items-center gap-2 text-navy-600 hover:text-navy-900 mb-6 text-sm font-medium">
      <i class="pi pi-chevron-left text-xs"></i> Kembali
    </router-link>

    <!-- Vendor Info -->
    <div class="flex flex-col md:flex-row gap-6 md:gap-8 mb-8 md:mb-10">
      <div class="w-full md:w-52 h-48 md:h-44 bg-navy-200 rounded-xl shrink-0"></div>
      <div class="flex-1 py-2">
        <h1 class="text-3xl font-bold text-navy-900 mb-2">{{ vendor.name }}</h1>
        <p class="text-navy-600 mb-1"><span class="font-bold">Bergabung sejak</span> {{ vendor.joinDate }}</p>
        <p class="text-navy-600"><span class="font-bold">Alamat</span> {{ vendor.address }}</p>
      </div>
      <div class="w-full md:w-72 shrink-0 bg-white border border-navy-200 rounded-xl p-5">
        <div class="flex items-center justify-between gap-3 mb-4">
          <div>
            <p class="text-xs font-bold text-navy-500 mb-1">Vendor Trust Score</p>
            <p class="text-3xl font-bold text-navy-900">{{ vendor.trustScore }}</p>
          </div>
          <span class="w-3 h-3 rounded-full" :class="statusColor(vendor.status)"></span>
        </div>
        <div class="space-y-3">
          <div v-for="[label, value] in trustRows" :key="label">
            <div class="flex justify-between text-xs text-navy-600 mb-1">
              <span>{{ label }}</span>
              <span class="font-bold">{{ value }}</span>
            </div>
            <div class="h-2 rounded-full bg-navy-100 overflow-hidden">
              <div class="h-full bg-brand-accent" :style="{ width: `${value}%` }"></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Log Distribusi -->
    <h2 class="text-2xl font-bold text-navy-900 mb-4">Log Distribusi Terakhir</h2>
    <div class="bg-white rounded-xl shadow-sm border border-navy-200 overflow-x-auto mb-8 md:mb-10">
      <table class="w-full min-w-[800px]">
        <thead>
          <tr class="border-b-2 border-navy-200">
            <th class="text-left px-6 py-4 text-sm font-semibold text-navy-700">Sekolah</th>
            <th class="text-left px-6 py-4 text-sm font-semibold text-navy-700">Porsi</th>
            <th class="text-left px-6 py-4 text-sm font-semibold text-navy-700">Status</th>
            <th class="text-left px-6 py-4 text-sm font-semibold text-navy-700">Time</th>
            <th class="text-left px-6 py-4 text-sm font-semibold text-navy-700">Operational Risk Score</th>
            <th class="px-6 py-4"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="d in distributions" :key="d.id" class="odd:bg-navy-50 hover:bg-navy-100 transition-colors">
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
              <router-link :to="`/regulator/vendors/${vendor.id}/distribution/${d.id}`" class="text-navy-500 hover:text-navy-900">
                <i class="pi pi-eye text-lg"></i>
              </router-link>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Schools -->
    <h2 class="text-2xl font-bold text-navy-900 mb-4">Sekolah Yang Dilayani</h2>
    <div class="flex flex-wrap gap-3">
      <span v-for="s in vendor.schools" :key="s" class="inline-flex items-center gap-2 px-5 py-2.5 bg-navy-200 rounded-full text-sm font-medium text-navy-700">
        <i class="pi pi-check-circle text-navy-500"></i> {{ s }}
      </span>
    </div>
  </div>
</template>
