<script setup lang="ts">
import { getData } from '@/services/api'

const data = getData()
const distributions = data.distributions

function statusColor(s: string) {
  if (s === 'safe') return 'bg-status-safe'
  if (s === 'medium') return 'bg-status-medium'
  return 'bg-status-high-risk'
}
</script>

<template>
  <div class="animate-fade-in">
    <!-- Stat Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 md:gap-5 mb-8">
      <div class="bg-white rounded-xl p-5 border border-navy-200 shadow-sm">
        <div class="flex justify-between items-start">
          <div>
            <p class="text-sm text-navy-500 mb-1">Total corporation</p>
            <p class="text-3xl font-bold text-navy-900">5</p>
          </div>
          <div class="w-10 h-10 bg-purple-100 rounded-full flex items-center justify-center">
            <i class="pi pi-users text-purple-500"></i>
          </div>
        </div>
        <p class="text-xs text-brand-success mt-3 flex items-center gap-1">
          <i class="pi pi-arrow-up text-[10px]"></i> +1 Dari bulan lalu
        </p>
      </div>
      <div class="bg-white rounded-xl p-5 border border-navy-200 shadow-sm">
        <div class="flex justify-between items-start">
          <div>
            <p class="text-sm text-navy-500 mb-1">Today's Distribution</p>
            <p class="text-3xl font-bold text-navy-900">1.350</p>
          </div>
          <div class="w-10 h-10 bg-amber-100 rounded-full flex items-center justify-center">
            <i class="pi pi-box text-amber-500"></i>
          </div>
        </div>
        <p class="text-xs text-brand-success mt-3 flex items-center gap-1">
          <i class="pi pi-arrow-up text-[10px]"></i> 1.3% Dari kemarin
        </p>
      </div>
      <div class="bg-white rounded-xl p-5 border border-navy-200 shadow-sm">
        <div class="flex justify-between items-start">
          <div>
            <div class="flex items-center gap-2">
              <p class="text-sm text-navy-500 mb-1">Trust Score</p>
              <span class="bg-brand-success text-white text-[10px] font-bold px-2 py-0.5 rounded-full">Top 15%</span>
            </div>
            <p class="text-3xl font-bold text-navy-900">88/100</p>
          </div>
          <div class="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
            <i class="pi pi-chart-line text-brand-success"></i>
          </div>
        </div>
        <p class="text-xs text-brand-danger mt-3 flex items-center gap-1">
          <i class="pi pi-arrow-down text-[10px]"></i> 4.3% Dari bulan lalu
        </p>
      </div>
    </div>

    <!-- Recent History -->
    <h2 class="text-2xl font-bold text-navy-900 mb-4">Recent History</h2>
    <div class="bg-white rounded-xl shadow-sm border border-navy-200 overflow-x-auto">
      <table class="w-full min-w-[700px]">
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
              <router-link :to="`/vendor/dashboard/history/${d.id}`" class="text-navy-500 hover:text-navy-900">
                <i class="pi pi-eye text-lg"></i>
              </router-link>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
