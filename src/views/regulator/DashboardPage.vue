<script setup lang="ts">
import { computed } from 'vue'
import { getData } from '@/services/localStorage'

const data = getData()
const highRiskCount = computed(() => data.vendors.filter((v: any) => v.status === 'high-risk').length)
const topVendors = computed(() =>
  [...data.vendors].sort((a: any, b: any) => b.trustScore - a.trustScore).slice(0, 5)
)
</script>

<template>
  <div class="animate-fade-in">
    <!-- Stat Cards -->
    <div class="grid grid-cols-4 gap-5 mb-8">
      <div class="bg-white rounded-xl p-5 border border-navy-200 shadow-sm">
        <div class="flex justify-between items-start">
          <div>
            <p class="text-sm text-navy-500 mb-1">Total Vendor</p>
            <p class="text-3xl font-bold text-navy-900">{{ data.vendors.length }}</p>
          </div>
          <div class="w-10 h-10 bg-purple-100 rounded-full flex items-center justify-center">
            <i class="pi pi-users text-purple-500"></i>
          </div>
        </div>
        <p class="text-xs text-brand-success mt-3 flex items-center gap-1">
          <i class="pi pi-arrow-up text-[10px]"></i> +1 Up from past week
        </p>
      </div>
      <div class="bg-white rounded-xl p-5 border border-navy-200 shadow-sm">
        <div class="flex justify-between items-start">
          <div>
            <p class="text-sm text-navy-500 mb-1">Distribusi Hari Ini</p>
            <p class="text-3xl font-bold text-navy-900">31,890</p>
          </div>
          <div class="w-10 h-10 bg-amber-100 rounded-full flex items-center justify-center">
            <i class="pi pi-box text-amber-500"></i>
          </div>
        </div>
        <p class="text-xs text-brand-success mt-3 flex items-center gap-1">
          <i class="pi pi-arrow-up text-[10px]"></i> 88% Tepat waktu
        </p>
      </div>
      <div class="bg-white rounded-xl p-5 border border-navy-200 shadow-sm">
        <div class="flex justify-between items-start">
          <div>
            <p class="text-sm text-navy-500 mb-1">High Risk</p>
            <p class="text-3xl font-bold text-navy-900">{{ highRiskCount }}</p>
          </div>
          <div class="w-10 h-10 bg-red-100 rounded-full flex items-center justify-center">
            <i class="pi pi-info-circle text-red-500"></i>
          </div>
        </div>
        <p class="text-xs text-brand-danger mt-3 flex items-center gap-1">
          <i class="pi pi-arrow-down text-[10px]"></i> 4.3% Dari bulan lalu
        </p>
      </div>
      <div class="bg-white rounded-xl p-5 border border-navy-200 shadow-sm">
        <div class="flex justify-between items-start">
          <div>
            <p class="text-sm text-navy-500 mb-1">Fraud Prevented</p>
            <p class="text-3xl font-bold text-navy-900">Rp 1.2M</p>
          </div>
          <div class="w-10 h-10 bg-yellow-100 rounded-full flex items-center justify-center">
            <i class="pi pi-info-circle text-yellow-500"></i>
          </div>
        </div>
        <p class="text-xs text-brand-danger mt-3">Estimation</p>
      </div>
    </div>

    <!-- Map & Top Vendor -->
    <div class="flex gap-6">
      <div class="flex-1">
        <div class="flex items-center gap-3 mb-4">
          <i class="pi pi-map text-xl text-navy-900"></i>
          <h2 class="text-2xl font-bold text-navy-900">Peta Risiko Distribusi</h2>
          <select class="ml-auto px-4 py-2 border border-navy-200 rounded-lg text-sm bg-white">
            <option>Tangerang</option>
            <option>Jakarta</option>
            <option>Bogor</option>
          </select>
        </div>
        <div class="bg-navy-200 rounded-xl h-80 flex items-center justify-center relative">
          <div class="absolute top-4 left-4 bg-white rounded-lg p-3 shadow-sm">
            <div class="flex items-center gap-2 mb-2"><span class="w-3 h-3 rounded-full bg-brand-success"></span><span class="text-sm">Safe</span></div>
            <div class="flex items-center gap-2"><span class="w-3 h-3 rounded-full bg-brand-danger"></span><span class="text-sm">High Risk</span></div>
          </div>
          <p class="text-navy-500 text-sm">Map Placeholder</p>
        </div>
      </div>
      <div class="w-72 shrink-0">
        <div class="bg-navy-900 text-white rounded-t-xl px-6 py-4">
          <h3 class="text-lg font-bold">Top Vendor</h3>
        </div>
        <div class="bg-white rounded-b-xl border border-navy-200 border-t-0 px-6 py-4 space-y-3">
          <p v-for="(v, i) in topVendors" :key="v.id" class="text-sm text-navy-700" :class="i < topVendors.length - 1 ? 'border-b border-navy-100 pb-2' : ''">
            #{{ i + 1 }}. {{ v.name }} ({{ v.trustScore }})
          </p>
        </div>
        <router-link to="/regulator/vendors" class="block mt-3 w-full py-3 bg-brand-accent text-white text-center rounded-xl font-semibold hover:bg-brand-accent-hover transition-colors">
          Lihat Semua
        </router-link>
      </div>
    </div>
  </div>
</template>
