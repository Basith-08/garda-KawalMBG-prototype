<script setup lang="ts">
import { getData, type Alert } from '@/services/localStorage'
import { ref } from 'vue'

const data = getData()
const alerts = ref<Alert[]>(data.alerts)
</script>

<template>
  <div class="animate-fade-in">
    <div class="flex justify-between items-start mb-8">
      <div>
        <h1 class="text-3xl font-bold text-navy-900 mb-2">Predictive Alerts</h1>
        <p class="text-navy-500">Notifikasi proaktif dari AI Risk Engine dan status verifikasi lapangan.</p>
      </div>
      <button class="px-5 py-2.5 border border-navy-300 rounded-lg text-sm font-medium text-navy-700 hover:bg-navy-100 transition-colors">
        Tandai semua dibaca
      </button>
    </div>

    <div class="space-y-5">
      <div v-for="alert in alerts" :key="alert.id" class="bg-white rounded-xl border border-navy-200 shadow-sm overflow-hidden flex">
        <div class="w-1.5 shrink-0" :class="alert.type === 'CRITICAL' ? 'bg-brand-danger' : 'bg-brand-warning'"></div>
        <div class="flex-1 px-6 py-5">
          <div class="flex items-start gap-4">
            <div class="w-12 h-12 rounded-full flex items-center justify-center shrink-0" :class="alert.type === 'CRITICAL' ? 'bg-red-100' : 'bg-amber-100'">
              <i class="pi pi-shield text-lg" :class="alert.type === 'CRITICAL' ? 'text-brand-danger' : 'text-brand-warning'"></i>
            </div>
            <div class="flex-1">
              <div class="flex items-center justify-between mb-1">
                <p class="text-xs text-navy-500">
                  <span class="font-bold" :class="alert.type === 'CRITICAL' ? 'text-brand-danger' : 'text-brand-warning'">{{ alert.type }}</span>
                  <span class="mx-1">•</span>{{ alert.time }}
                </p>
                <span class="text-xs px-3 py-1 rounded-full border border-navy-200 text-navy-600">{{ alert.statusTag }}</span>
              </div>
              <h3 class="text-lg font-bold text-navy-900 mb-1">{{ alert.vendorName }}</h3>
              <p class="text-sm text-navy-600 mb-3">{{ alert.description }}</p>
              <button class="px-5 py-2 bg-navy-900 text-white text-sm font-medium rounded-lg hover:bg-navy-800 transition-colors">
                Cek Detail
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
