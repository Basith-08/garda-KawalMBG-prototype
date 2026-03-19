<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { getData } from '@/services/api'

const route = useRoute()
const data = getData()
const school = computed(() => data.schools.find((s: any) => s.id === route.params.id))
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 md:px-8 py-6 md:py-8 animate-fade-in" v-if="school">
    <!-- School Info -->
    <div class="flex flex-col md:flex-row gap-6 md:gap-8 mb-8 md:mb-12">
      <div class="w-full md:w-72 h-48 bg-navy-200 rounded-xl shrink-0"></div>
      <div class="flex-1 py-2">
        <h1 class="text-3xl font-bold text-navy-900 mb-2">{{ school.name }}</h1>
        <p class="text-navy-700 mb-1"><span class="font-bold">NPSN:</span> {{ school.npsn }}</p>
        <p class="text-navy-700 mb-3"><span class="font-bold">Alamat:</span> {{ school.address }}</p>
        <p class="text-navy-600 mb-2 font-bold">Diedukasi & Dilayani Oleh:</p>
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-full bg-navy-200 flex items-center justify-center">
            <i class="pi pi-trophy text-navy-600"></i>
          </div>
          <span class="text-xl font-bold text-navy-900">{{ school.vendorName }}</span>
        </div>
      </div>
      <!-- Trust Score Card -->
      <div class="w-full md:w-64 shrink-0">
        <div class="bg-green-50 border border-green-200 rounded-xl p-6 text-center">
          <p class="text-brand-success font-bold text-sm mb-2 tracking-wider">PUBLIC TRUST SCORE</p>
          <p class="text-6xl font-bold text-brand-success mb-2">{{ school.trustScore }}</p>
          <div class="flex items-center justify-center gap-1 text-brand-success">
            <i class="pi pi-check-circle"></i>
            <span class="text-sm font-medium">Sangat Baik</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Menu Hari Ini & Nutrition -->
    <div class="flex flex-col lg:flex-row gap-6 lg:gap-8">
      <div class="flex-1 w-full">
        <div class="flex items-center gap-2 mb-2">
          <i class="pi pi-list text-xl text-navy-900"></i>
          <h2 class="text-2xl font-bold text-navy-900">Menu Hari Ini</h2>
        </div>
        <p class="text-sm text-navy-500 mb-4">Sesuai standar porsi "Isi Piringku"</p>
        <div class="w-full h-56 bg-navy-200 rounded-xl flex items-center justify-center">
          <img src="https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=500&h=300&fit=crop" class="w-full h-full object-cover rounded-xl" alt="menu" />
        </div>
      </div>
      <div class="flex-1 flex flex-col items-center justify-center">
        <h3 class="text-2xl font-bold text-navy-900 mb-6">Analisis Gizi</h3>
        <!-- Donut Chart Placeholder -->
        <div class="donut-container mb-4">
          <svg viewBox="0 0 200 200" class="w-full h-full">
            <circle cx="100" cy="100" r="80" fill="none" stroke="#e2e8f0" stroke-width="20"/>
            <circle cx="100" cy="100" r="80" fill="none" stroke="#93c5fd" stroke-width="20" stroke-dasharray="400" stroke-dashoffset="100" transform="rotate(-90 100 100)"/>
          </svg>
          <div class="donut-center">
            <div class="text-3xl font-bold text-navy-900">660</div>
            <div class="text-sm text-navy-500 font-semibold">KCAL</div>
          </div>
        </div>
      </div>
      <div class="w-full lg:w-72 shrink-0 space-y-5 pt-4 lg:pt-8">
        <div>
          <div class="flex justify-between text-sm mb-1"><span class="text-navy-700">Karbohidrat</span><span class="font-semibold">85g</span></div>
          <div class="h-2 bg-navy-200 rounded-full overflow-hidden"><div class="h-full bg-amber-400 rounded-full" style="width:65%"></div></div>
        </div>
        <div>
          <div class="flex justify-between text-sm mb-1"><span class="text-navy-700">Protein</span><span class="font-semibold">32g</span></div>
          <div class="h-2 bg-navy-200 rounded-full overflow-hidden"><div class="h-full bg-blue-500 rounded-full" style="width:50%"></div></div>
        </div>
        <div>
          <div class="flex justify-between text-sm mb-1"><span class="text-navy-700">Lemak Baik</span><span class="font-semibold">15g</span></div>
          <div class="h-2 bg-navy-200 rounded-full overflow-hidden"><div class="h-full bg-red-500 rounded-full" style="width:25%"></div></div>
        </div>
        <div>
          <div class="flex justify-between text-sm mb-1"><span class="text-navy-700">Serat</span><span class="font-semibold">12g</span></div>
          <div class="h-2 bg-navy-200 rounded-full overflow-hidden"><div class="h-full bg-teal-500 rounded-full" style="width:40%"></div></div>
        </div>
      </div>
    </div>
  </div>
</template>
