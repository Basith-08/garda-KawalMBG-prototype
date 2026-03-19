<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import { getData, saveData, type Distribution } from '@/services/localStorage'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const toast = useToast()
const authStore = useAuthStore()
const draft = ref<any>(null)

onMounted(() => {
  const stored = localStorage.getItem('kawalmbg_draft_dist')
  if (stored) draft.value = JSON.parse(stored)
})

function confirm() {
  if (draft.value) {
    const data = getData()
    draft.value.schools.forEach((school: string) => {
      const dist: Distribution = {
        id: Date.now().toString() + Math.random().toString(36).substr(2, 5),
        vendorId: authStore.user?.id || '2',
        schoolName: school,
        porsi: draft.value.jumlahPorsi,
        status: 'medium',
        statusText: 'Pending Review',
        time: new Date().toLocaleDateString('id-ID', { day: 'numeric', month: 'short', year: 'numeric' }),
        riskScore: 78,
        menuName: draft.value.menuUtama.split(',')[0] || 'Menu Baru',
        menuUtama: draft.value.menuUtama,
        suhu: 32,
        durasi: 45,
        levelRisiko: 'MEDIUM',
        catatan: 'Data dikirim via aplikasi. Menunggu balasan & validasi sensor.'
      }
      data.distributions.unshift(dist)
    })
    saveData(data)
    localStorage.removeItem('kawalmbg_draft_dist')
  }

  toast.add({ severity: 'success', summary: 'Distribusi Dimulai', detail: 'Data berhasil diverifikasi dan direkam ke blockchain log', life: 4000 })
  router.push('/vendor/history')
}
</script>

<template>
  <div class="animate-fade-in">
    <button @click="router.back()" class="inline-flex items-center gap-2 text-navy-600 hover:text-navy-900 mb-6 text-sm font-medium">
      <i class="pi pi-chevron-left text-xs"></i> Kembali
    </button>

    <div class="flex flex-col md:flex-row gap-6 md:gap-8 max-w-4xl mx-auto">
      <!-- Gauge -->
      <div class="w-full md:flex-1 bg-white rounded-xl border border-navy-200 shadow-sm p-8 flex flex-col items-center justify-center">
        <div class="gauge-container mb-4">
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

      <!-- Breakdown -->
      <div class="w-full md:w-80 shrink-0">
        <div class="border border-navy-200 rounded-xl p-6 bg-navy-100 h-full">
          <h3 class="text-xl font-bold text-navy-900 mb-5">AI Analysis Breakdown</h3>
          <ul class="space-y-4">
            <li class="flex items-start gap-3">
              <span class="w-3 h-3 bg-navy-300 rounded-full mt-1.5 shrink-0"></span>
              <p class="text-sm text-navy-700">Suhu luar: 32°C <span class="text-brand-danger font-medium">(Risiko Sedang)</span></p>
            </li>
            <li class="flex items-start gap-3">
              <span class="w-3 h-3 bg-navy-300 rounded-full mt-1.5 shrink-0"></span>
              <p class="text-sm text-navy-700">Estimasi Tiba: 09:30 <span class="text-brand-success font-medium">(Tepat Waktu)</span></p>
            </li>
            <li class="flex items-start gap-3">
              <span class="w-3 h-3 bg-navy-300 rounded-full mt-1.5 shrink-0"></span>
              <p class="text-sm text-navy-700">Catatan: Menu santan sensitif suhu panas. Pastikan ventilasi kendaraan baik</p>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <div class="flex justify-center mt-8 md:mt-10">
      <button @click="confirm" class="w-full sm:w-auto px-12 py-4 bg-brand-success hover:opacity-90 text-white font-semibold rounded-xl transition-opacity shadow-md text-lg">
        Konfirmasi & Mulai Distribusi
      </button>
    </div>
  </div>
</template>
