<script setup lang="ts">
import { ref } from 'vue'
import { getData, type Alert, type Distribution } from '@/services/api'
import * as XLSX from 'xlsx'
import jsPDF from 'jspdf'
import autoTable from 'jspdf-autotable'

const selectedReport = ref<number>(0)
const selectedFormat = ref<string>('PDF')

const reportTypes = [
  { title: 'Laporan Akuntabilitas Fiskal', desc: 'Audit fraud disbursement & anomali klaim vendor.' },
  { title: 'Laporan Performa Vendor', desc: 'Ringkasan insiden, risk score, & verifikasi guru.' },
]

function exportReport() {
  const data = getData()
  let rows: any[] = []
  let head: string[] = []

  if (selectedReport.value === 0) {
    // Akuntabilitas Fiskal (Alerts / Fraud)
    head = ['Tanggal', 'Tingkat', 'Vendor', 'Deskripsi Insiden', 'Status Pengecekan']
    rows = data.alerts.map((a: Alert) => ({
      Tanggal: a.time,
      Tingkat: a.type,
      Vendor: a.vendorName,
      Deskripsi: a.description,
      Status: a.statusTag
    }))
  } else {
    // Performa Vendor (Distributions)
    head = ['Tanggal', 'Sekolah', 'Porsi', 'Risk Score', 'Level Risiko', 'Catatan AI']
    rows = data.distributions.map((d: Distribution) => ({
      Tanggal: d.time,
      Sekolah: d.schoolName,
      Porsi: d.porsi,
      Risk: d.riskScore,
      Level: d.levelRisiko,
      Catatan: d.catatan
    }))
  }

  const title = reportTypes[selectedReport.value].title

  if (selectedFormat.value === 'EXCEL') {
    const ws = XLSX.utils.json_to_sheet(rows)
    const wb = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(wb, ws, 'Laporan')
    XLSX.writeFile(wb, `${title.replace(/\s+/g, '_')}.xlsx`)
  } else {
    const doc = new jsPDF('landscape')
    doc.setFontSize(16)
    doc.text(title, 14, 15)
    doc.setFontSize(10)
    doc.text('Di-generate pada: ' + new Date().toLocaleString('id-ID'), 14, 22)
    
    const body = rows.map(r => Object.values(r) as any[])
    autoTable(doc, {
      startY: 28,
      head: [head],
      body: body,
      theme: 'grid',
      styles: { fontSize: 8 },
      headStyles: { fillColor: [30, 41, 59] } // navy-900
    })
    
    doc.save(`${title.replace(/\s+/g, '_')}.pdf`)
  }
}
</script>

<template>
  <div class="animate-fade-in">
    <div class="flex flex-col sm:flex-row justify-between items-start gap-4 sm:gap-0 mb-8">
      <div>
        <h1 class="text-3xl font-bold text-navy-900 mb-2">Generate Report & Audit</h1>
        <p class="text-navy-500">Ekspor data komprehensif untuk kebutuhan audit BPK/BGN.</p>
      </div>
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
          <option>Maret - 2026</option>
          <option>Februari - 2026</option>
          <option>Januari - 2026</option>
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

    <button @click="exportReport" class="w-full sm:w-auto px-10 py-4 bg-brand-accent hover:bg-brand-accent-hover text-white font-semibold rounded-xl transition-colors shadow-md text-lg">
      Unduh Laporan Audit
    </button>
  </div>
</template>
