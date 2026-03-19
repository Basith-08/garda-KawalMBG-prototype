<script setup lang="ts">
import { ref } from 'vue'

const selectedReport = ref<number>(0)
const selectedFormat = ref<string>('PDF')

const reportTypes = [
  { title: 'Laporan Akuntabilitas Fiskal', desc: 'Audit fraud disbursement & anomali klaim vendor.' },
  { title: 'Laporan Akuntabilitas Fiskal', desc: 'Ringkasan insiden, risk score, & verifikasi guru.' },
]
</script>

<template>
  <div class="animate-fade-in">
    <div class="flex flex-col sm:flex-row justify-between items-start gap-4 sm:gap-0 mb-8">
      <div>
        <h1 class="text-3xl font-bold text-navy-900 mb-2">Generate Report & Audit</h1>
        <p class="text-navy-500">Ekspor data komprehensif untuk kebutuhan audit BPK/BGN.</p>
      </div>
      <button class="px-5 py-2.5 border border-navy-300 rounded-lg text-sm font-medium text-navy-700 hover:bg-navy-100 transition-colors">
        Tandai semua dibaca
      </button>
    </div>

    <h2 class="text-xl font-bold text-navy-900 mb-4">Jenis Laporan</h2>
    <div class="flex flex-col sm:flex-row gap-4 sm:gap-6 mb-8 sm:mb-10">
      <button
        v-for="(rt, i) in reportTypes" :key="i"
        @click="selectedReport = i"
        class="flex-1 p-6 border-2 rounded-xl text-left transition-all"
        :class="selectedReport === i ? 'border-brand-accent bg-blue-50' : 'border-navy-200 bg-white hover:border-navy-300'"
      >
        <h3 class="font-bold text-navy-900 mb-2">{{ rt.title }}</h3>
        <p class="text-sm text-navy-500">{{ rt.desc }}</p>
      </button>
    </div>

    <div class="flex flex-col sm:flex-row gap-6 sm:gap-16 mb-10">
      <div>
        <h2 class="text-xl font-bold text-navy-900 mb-4">Rentang Waktu</h2>
        <select class="px-5 py-3 border border-navy-200 rounded-lg text-sm bg-white min-w-[200px]">
          <option>Maret  - 2026</option>
          <option>Februari  - 2026</option>
          <option>Januari  - 2026</option>
        </select>
      </div>
      <div>
        <h2 class="text-xl font-bold text-navy-900 mb-4">Format File</h2>
        <div class="flex gap-3">
          <button
            @click="selectedFormat = 'PDF'"
            class="px-6 py-3 border-2 rounded-lg text-sm font-semibold transition-all"
            :class="selectedFormat === 'PDF' ? 'border-brand-accent bg-blue-50 text-brand-accent' : 'border-navy-200 text-navy-600'"
          >PDF</button>
          <button
            @click="selectedFormat = 'EXCEL'"
            class="px-6 py-3 border-2 rounded-lg text-sm font-semibold transition-all"
            :class="selectedFormat === 'EXCEL' ? 'border-brand-accent bg-blue-50 text-brand-accent' : 'border-navy-200 text-navy-600'"
          >EXCEL</button>
        </div>
      </div>
    </div>

    <button class="w-full sm:w-auto px-10 py-4 bg-brand-accent hover:bg-brand-accent-hover text-white font-semibold rounded-xl transition-colors shadow-md text-lg">
      Unduh Laporan Audit
    </button>
  </div>
</template>
