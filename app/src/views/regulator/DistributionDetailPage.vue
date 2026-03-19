<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getData } from '@/services/api'

const route = useRoute()
const router = useRouter()
const data = getData()
const dist = computed(() => data.distributions.find((d: any) => d.id === route.params.distId))
</script>

<template>
  <div class="animate-fade-in" v-if="dist">
    <button @click="router.back()" class="inline-flex items-center gap-2 text-navy-600 hover:text-navy-900 mb-6 text-sm font-medium">
      <i class="pi pi-chevron-left text-xs"></i> Kembali
    </button>

    <div class="flex flex-col md:flex-row justify-between items-start gap-4 md:gap-0 mb-6">
      <div>
        <span class="inline-block bg-navy-800 text-white text-xs font-semibold px-4 py-1.5 rounded-full mb-3">Detail Distribusi</span>
        <h1 class="text-2xl font-bold text-navy-900 mb-1">{{ dist.menuName }}</h1>
        <p class="text-sm text-navy-500">18 Maret 2026 - {{ dist.schoolName }}</p>
      </div>
      <div class="bg-green-100 px-5 py-3 rounded-xl flex items-center gap-3">
        <div class="w-10 h-10 bg-brand-success rounded-full flex items-center justify-center">
          <i class="pi pi-check text-white text-lg"></i>
        </div>
        <div>
          <p class="text-xs text-brand-success font-bold">Status Akhir</p>
          <p class="text-sm font-bold text-brand-success">Berhasil Terverifikasi</p>
        </div>
      </div>
    </div>

    <!-- AI Risk + Photos -->
    <div class="flex flex-col lg:flex-row gap-6 lg:gap-8 mb-8">
      <!-- AI Risk -->
      <div class="flex-1">
        <div class="bg-navy-800 text-white px-6 py-3 rounded-t-xl">
          <h3 class="text-lg font-bold">AI Risk Analysis</h3>
        </div>
        <div class="bg-white border border-navy-200 border-t-0 rounded-b-xl p-6">
          <div class="flex justify-between items-center mb-6">
            <span class="text-sm font-medium text-navy-600">Level Risiko</span>
            <span class="text-sm font-bold text-brand-success">{{ dist.levelRisiko }}</span>
          </div>
          <!-- Gauge -->
          <div class="flex flex-col items-center mb-4">
            <div class="gauge-container">
              <svg viewBox="0 0 280 160" class="gauge-svg">
                <path d="M 30 150 A 110 110 0 0 1 250 150" fill="none" stroke="#e2e8f0" stroke-width="20" stroke-linecap="round"/>
                <path d="M 30 150 A 110 110 0 0 1 140 40" fill="none" stroke="#94a3b8" stroke-width="20" stroke-linecap="round"/>
              </svg>
              <div class="absolute inset-0 flex items-center justify-center pt-8">
                <span class="text-2xl font-bold text-navy-900">Medium</span>
              </div>
            </div>
            <div class="flex justify-between w-64 mt-2">
              <span class="text-sm font-bold text-navy-900">LOW</span>
              <div class="w-6 h-6 rounded-full bg-navy-300"></div>
              <span class="text-sm font-bold text-navy-900">HIGH</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Photos -->
      <div class="flex-1">
        <h3 class="text-xl font-bold text-navy-900 mb-4">Bukti Visual Lapangan</h3>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <img src="https://images.unsplash.com/photo-1567521464027-f127ff144326?w=400&h=250&fit=crop" class="w-full h-40 object-cover rounded-xl" alt="foto produksi" />
            <p class="text-xs text-navy-500 mt-2 text-center">Foto Produksi (Vendor)</p>
          </div>
          <div>
            <img src="https://images.unsplash.com/photo-1588072432836-e10032774350?w=400&h=250&fit=crop" class="w-full h-40 object-cover rounded-xl" alt="foto penerimaan" />
            <p class="text-xs text-navy-500 mt-2 text-center">Foto Penerimaan (Sekolah)</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Environment Info -->
    <div class="bg-navy-800 text-white rounded-xl p-6 max-w-lg">
      <div class="flex gap-8 mb-4">
        <div>
          <div class="flex items-center gap-2 mb-1"><i class="pi pi-sun text-amber-300"></i></div>
          <p class="text-xs text-navy-400">Suhu Lingkungan</p>
          <p class="text-lg font-bold">{{ dist.suhu }}°C</p>
        </div>
        <div>
          <div class="flex items-center gap-2 mb-1"><i class="pi pi-truck text-brand-accent"></i></div>
          <p class="text-xs text-navy-400">Durasi Distribusi</p>
          <p class="text-lg font-bold">{{ dist.durasi }} Menit</p>
        </div>
      </div>
      <p class="text-sm text-navy-400 leading-relaxed">{{ dist.catatan }}</p>
    </div>
  </div>
</template>
