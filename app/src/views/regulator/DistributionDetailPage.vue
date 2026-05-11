<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getData } from '@/services/api'
import { assessDistribution } from '@/services/distributionAssessment'

const route = useRoute()
const router = useRouter()
const data = getData()
const dist = computed(() => data.distributions.find((d: any) => d.id === route.params.distId))
const assessment = computed(() => (dist.value ? dist.value.assessment ?? assessDistribution(dist.value) : null))
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
        <p class="text-sm text-navy-500">{{ dist.time }} - {{ dist.schoolName }}</p>
      </div>
      <div class="px-5 py-3 rounded-xl flex items-center gap-3" :class="assessment?.riskStatus === 'HIGH' ? 'bg-red-100' : assessment?.riskStatus === 'MEDIUM' ? 'bg-amber-100' : 'bg-green-100'">
        <div class="w-10 h-10 rounded-full flex items-center justify-center" :class="assessment?.riskStatus === 'HIGH' ? 'bg-red-600' : assessment?.riskStatus === 'MEDIUM' ? 'bg-amber-500' : 'bg-brand-success'">
          <i :class="assessment?.riskStatus === 'HIGH' ? 'pi pi-exclamation-triangle' : assessment?.riskStatus === 'MEDIUM' ? 'pi pi-eye' : 'pi pi-check'" class="text-white text-lg"></i>
        </div>
        <div>
          <p class="text-xs font-bold" :class="assessment?.riskStatus === 'HIGH' ? 'text-red-700' : assessment?.riskStatus === 'MEDIUM' ? 'text-amber-700' : 'text-brand-success'">Risk Status</p>
          <p class="text-sm font-bold" :class="assessment?.riskStatus === 'HIGH' ? 'text-red-700' : assessment?.riskStatus === 'MEDIUM' ? 'text-amber-700' : 'text-brand-success'">{{ assessment?.riskStatus || dist.levelRisiko }}</p>
        </div>
      </div>
    </div>

    <!-- AI Risk + Photos -->
    <div class="flex flex-col lg:flex-row gap-6 lg:gap-8 mb-8">
      <!-- AI Risk -->
      <div class="flex-1">
        <div class="bg-navy-800 text-white px-6 py-3 rounded-t-xl">
          <h3 class="text-lg font-bold">Operational Risk Assessment</h3>
        </div>
        <div v-if="assessment" class="bg-white border border-navy-200 border-t-0 rounded-b-xl p-6 space-y-6">
          <div class="flex flex-wrap items-start justify-between gap-4">
            <div>
              <p class="text-sm font-medium text-navy-600 mb-1">Final Risk Score</p>
              <p class="text-3xl font-bold text-navy-900">{{ assessment.finalRiskScore }}/100</p>
            </div>
            <div class="px-4 py-2 rounded-full text-sm font-bold" :class="assessment.riskStatus === 'HIGH' ? 'bg-red-100 text-red-700' : assessment.riskStatus === 'MEDIUM' ? 'bg-amber-100 text-amber-700' : 'bg-emerald-100 text-emerald-700'">
              {{ assessment.riskStatus }}
            </div>
          </div>
          <div>
            <h4 class="text-sm font-bold text-navy-900 mb-2">Operational Summary</h4>
            <p class="text-sm text-navy-600 leading-relaxed">{{ assessment.operationalSummary }}</p>
          </div>
          <div>
            <h4 class="text-sm font-bold text-navy-900 mb-2">Exposure Analysis</h4>
            <ul class="space-y-2 text-sm text-navy-600">
              <li v-for="item in assessment.exposureAnalysis" :key="item">• {{ item }}</li>
            </ul>
          </div>
          <div>
            <h4 class="text-sm font-bold text-navy-900 mb-2">SOP Violation Detection</h4>
            <ul class="space-y-2 text-sm text-navy-600">
              <li v-for="item in assessment.sopViolations" :key="item">• {{ item }}</li>
            </ul>
          </div>
          <div>
            <h4 class="text-sm font-bold text-navy-900 mb-2">Risk Factors</h4>
            <ul class="space-y-2 text-sm text-navy-600">
              <li v-for="item in assessment.riskFactors" :key="item">• {{ item }}</li>
            </ul>
          </div>
          <div>
            <h4 class="text-sm font-bold text-navy-900 mb-2">Recommended Action</h4>
            <p class="text-sm text-navy-600 leading-relaxed">{{ assessment.recommendedAction }}</p>
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
          <p class="text-xs text-navy-400">Ambient Temperature</p>
          <p class="text-lg font-bold">{{ dist.suhu }}°C</p>
        </div>
        <div>
          <div class="flex items-center gap-2 mb-1"><i class="pi pi-truck text-brand-accent"></i></div>
          <p class="text-xs text-navy-400">Distribution Duration</p>
          <p class="text-lg font-bold">{{ dist.durasi }} Menit</p>
        </div>
      </div>
      <p class="text-sm text-navy-400 leading-relaxed">{{ dist.catatan }}</p>
    </div>
  </div>
</template>
