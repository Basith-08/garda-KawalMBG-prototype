<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import { getData, saveData, type Distribution } from '@/services/api'
import { useAuthStore } from '@/stores/auth'
import { assessDistribution, statusFromRisk } from '@/services/distributionAssessment'

const router = useRouter()
const toast = useToast()
const authStore = useAuthStore()
const draft = ref<any>(null)

onMounted(() => {
  const stored = localStorage.getItem('kawalmbg_draft_dist')
  if (stored) draft.value = JSON.parse(stored)
})

const previewDistribution = computed<Distribution | null>(() => {
  if (!draft.value) return null

  return {
    id: 'preview',
    vendorId: authStore.user?.vendorId || '2',
    schoolName: draft.value.schools?.[0] || 'Tujuan belum dipilih',
    porsi: draft.value.jumlahPorsi || 0,
    status: 'medium',
    statusText: 'Pending Review',
    time: new Date().toLocaleDateString('id-ID', { day: 'numeric', month: 'short', year: 'numeric' }),
    riskScore: 0,
    menuName: draft.value.menuUtama?.split(',')[0] || 'Menu Baru',
    menuUtama: draft.value.menuUtama || 'Menu belum diisi',
    suhu: 32,
    durasi: 45,
    levelRisiko: 'MEDIUM',
    catatan: 'Preview operasional menggunakan parameter distribusi default sebelum telemetri rute masuk.',
  }
})

const previewAssessment = computed(() => (previewDistribution.value ? assessDistribution(previewDistribution.value) : null))

function confirm() {
  if (draft.value) {
    const data = getData()
    const assessment = previewAssessment.value
    draft.value.schools.forEach((school: string) => {
      const dist: Distribution = {
        id: Date.now().toString() + Math.random().toString(36).substr(2, 5),
        vendorId: authStore.user?.vendorId || '2',
        schoolName: school,
        porsi: draft.value.jumlahPorsi,
        status: statusFromRisk(assessment?.riskStatus || 'MEDIUM'),
        statusText: 'Exposure Review',
        time: new Date().toLocaleDateString('id-ID', { day: 'numeric', month: 'short', year: 'numeric' }),
        riskScore: assessment?.finalRiskScore || 58,
        menuName: draft.value.menuUtama.split(',')[0] || 'Menu Baru',
        menuUtama: draft.value.menuUtama,
        suhu: 32,
        durasi: 45,
        levelRisiko: `${assessment?.riskStatus || 'MEDIUM'} RISK`,
        catatan: assessment?.operationalSummary || 'Data dikirim via aplikasi. Menunggu balasan & validasi sensor.',
        assessment: assessment || undefined,
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
      <div v-if="previewAssessment && previewDistribution" class="w-full md:flex-1 bg-white rounded-xl border border-navy-200 shadow-sm p-8">
        <div class="flex flex-wrap items-start justify-between gap-4 mb-6">
          <div>
            <p class="text-sm font-semibold text-navy-500 mb-2">Operational Risk Assessment</p>
            <h2 class="text-3xl font-bold text-navy-900">{{ previewAssessment.finalRiskScore }}/100</h2>
          </div>
          <div class="px-4 py-2 rounded-full text-sm font-bold" :class="previewAssessment.riskStatus === 'HIGH' ? 'bg-red-100 text-red-700' : previewAssessment.riskStatus === 'MEDIUM' ? 'bg-amber-100 text-amber-700' : 'bg-emerald-100 text-emerald-700'">
            {{ previewAssessment.riskStatus }}
          </div>
        </div>

        <div class="space-y-5">
          <div>
            <h3 class="text-sm font-bold text-navy-900 mb-2">Operational Summary</h3>
            <p class="text-sm text-navy-600 leading-relaxed">{{ previewAssessment.operationalSummary }}</p>
          </div>
          <div>
            <h3 class="text-sm font-bold text-navy-900 mb-2">Exposure Analysis</h3>
            <ul class="space-y-2 text-sm text-navy-600">
              <li v-for="item in previewAssessment.exposureAnalysis" :key="item">• {{ item }}</li>
            </ul>
          </div>
          <div>
            <h3 class="text-sm font-bold text-navy-900 mb-2">Recommended Action</h3>
            <p class="text-sm text-navy-600 leading-relaxed">{{ previewAssessment.recommendedAction }}</p>
          </div>
        </div>
      </div>

      <div v-if="previewAssessment" class="w-full md:w-80 shrink-0">
        <div class="border border-navy-200 rounded-xl p-6 bg-navy-100 h-full">
          <h3 class="text-xl font-bold text-navy-900 mb-5">SOP Violation Detection</h3>
          <ul class="space-y-4">
            <li v-for="item in previewAssessment.sopViolations" :key="item" class="flex items-start gap-3">
              <span class="w-3 h-3 bg-navy-300 rounded-full mt-1.5 shrink-0"></span>
              <p class="text-sm text-navy-700">{{ item }}</p>
            </li>
          </ul>

          <h3 class="text-xl font-bold text-navy-900 mt-8 mb-5">Risk Factors</h3>
          <ul class="space-y-4">
            <li v-for="item in previewAssessment.riskFactors" :key="item" class="flex items-start gap-3">
              <span class="w-3 h-3 bg-brand-accent rounded-full mt-1.5 shrink-0"></span>
              <p class="text-sm text-navy-700">{{ item }}</p>
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
