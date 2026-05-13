<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { fetchDistributionReceipt, submitDistributionReceipt } from '@/services/receipts'
import type { DistributionReceipt, ReceiptArrivalStatus, ReceiptIssueType } from '@/types/domain'

const route = useRoute()
const receipt = ref<DistributionReceipt | null>(null)
const selectedStatus = ref<ReceiptArrivalStatus>('received_ok')
const selectedIssueType = ref<ReceiptIssueType | null>(null)
const evidenceUploaded = ref(false)
const note = ref('')
const loading = ref(true)
const submitting = ref(false)
const submitted = ref(false)
const error = ref('')

const issueTypeOptions: Array<{ value: ReceiptIssueType; label: string }> = [
  { value: 'packaging_damaged', label: 'Kemasan rusak' },
  { value: 'portion_shortage', label: 'Jumlah kurang' },
  { value: 'unsafe_smell_or_quality', label: 'Bau / mutu tidak layak' },
  { value: 'menu_mismatch', label: 'Menu tidak sesuai' },
  { value: 'late_arrival', label: 'Datang terlambat' },
  { value: 'other', label: 'Lainnya' },
]

async function loadReceipt() {
  loading.value = true
  error.value = ''
  try {
    receipt.value = await fetchDistributionReceipt(String(route.params.id))
    selectedStatus.value = receipt.value.arrivalStatus ?? 'received_ok'
    selectedIssueType.value = receipt.value.receiptIssueType ?? null
    evidenceUploaded.value = receipt.value.receiptEvidenceUploaded ?? false
    note.value = receipt.value.receiptNote ?? ''
  } catch (err: any) {
    error.value = err?.response?.data?.detail || 'Distribusi tidak ditemukan'
  } finally {
    loading.value = false
  }
}

async function submitReceipt() {
  submitting.value = true
  error.value = ''
  try {
    const issueType =
      selectedStatus.value === 'received_with_issue'
        ? selectedIssueType.value
        : selectedStatus.value === 'not_received'
          ? 'not_received'
          : null

    receipt.value = await submitDistributionReceipt(String(route.params.id), {
      arrivalStatus: selectedStatus.value,
      issueType,
      evidenceUploaded: selectedStatus.value === 'received_with_issue' ? evidenceUploaded.value : false,
      note: note.value.trim() || undefined,
    })
    submitted.value = true
  } catch (err: any) {
    error.value = err?.response?.data?.detail || 'Konfirmasi gagal dikirim'
  } finally {
    submitting.value = false
  }
}

function setSelectedStatus(status: ReceiptArrivalStatus) {
  selectedStatus.value = status
  submitted.value = false
  if (status === 'received_ok') {
    selectedIssueType.value = null
    evidenceUploaded.value = false
  }
  if (status === 'not_received') {
    selectedIssueType.value = 'not_received'
    evidenceUploaded.value = false
  }
}

onMounted(loadReceipt)
</script>

<template>
  <main class="min-h-[calc(100vh-80px)] bg-navy-100 px-4 py-8 md:py-12">
    <section class="max-w-2xl mx-auto bg-white border border-navy-200 rounded-xl p-6 md:p-8 shadow-sm">
      <div v-if="loading" class="text-sm text-navy-600">Memuat data distribusi...</div>
      <div v-else-if="error" class="text-sm font-semibold text-red-700">{{ error }}</div>
      <div v-else-if="receipt" class="space-y-6">
        <div>
          <p class="text-sm font-bold text-brand-accent mb-2">Digital Receipt Sekolah</p>
          <h1 class="text-2xl md:text-3xl font-bold text-navy-900">{{ receipt.schoolName }}</h1>
          <p class="text-sm text-navy-600 mt-2">{{ receipt.menuUtama }} · {{ receipt.porsi }} porsi · {{ receipt.time }}</p>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <button
            type="button"
            @click="setSelectedStatus('received_ok')"
            class="px-4 py-3 rounded-lg border text-sm font-bold transition-colors"
            :class="selectedStatus === 'received_ok' ? 'bg-emerald-600 text-white border-emerald-600' : 'bg-white text-navy-700 border-navy-200 hover:bg-navy-100'"
          >
            Diterima baik
          </button>
          <button
            type="button"
            @click="setSelectedStatus('received_with_issue')"
            class="px-4 py-3 rounded-lg border text-sm font-bold transition-colors"
            :class="selectedStatus === 'received_with_issue' ? 'bg-amber-500 text-white border-amber-500' : 'bg-white text-navy-700 border-navy-200 hover:bg-navy-100'"
          >
            Ada masalah
          </button>
          <button
            type="button"
            @click="setSelectedStatus('not_received')"
            class="px-4 py-3 rounded-lg border text-sm font-bold transition-colors"
            :class="selectedStatus === 'not_received' ? 'bg-red-600 text-white border-red-600' : 'bg-white text-navy-700 border-navy-200 hover:bg-navy-100'"
          >
            Belum diterima
          </button>
        </div>

        <div v-if="selectedStatus === 'received_with_issue'" class="space-y-4">
          <div>
            <p class="text-sm font-bold text-navy-800 mb-3">Kategori masalah</p>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <button
                v-for="option in issueTypeOptions"
                :key="option.value"
                type="button"
                @click="selectedIssueType = option.value"
                class="rounded-lg border px-4 py-3 text-left text-sm font-semibold transition-colors"
                :class="selectedIssueType === option.value ? 'border-amber-500 bg-amber-50 text-amber-700' : 'border-navy-200 bg-white text-navy-700 hover:bg-navy-100'"
              >
                {{ option.label }}
              </button>
            </div>
          </div>

          <label class="flex items-start gap-3 rounded-lg border border-navy-200 px-4 py-3">
            <input v-model="evidenceUploaded" type="checkbox" class="mt-1 h-4 w-4 rounded border-navy-300 text-brand-accent focus:ring-brand-accent" />
            <span class="text-sm text-navy-700">
              Bukti foto receipt sudah dilampirkan.
              <span class="block text-xs text-navy-500 mt-1">Wajib untuk status masalah agar dashboard regulator punya jejak evidence receipt yang terstruktur.</span>
            </span>
          </label>
        </div>

        <label class="block">
          <span class="block text-sm font-bold text-navy-800 mb-2">Catatan</span>
          <textarea
            v-model="note"
            rows="4"
            class="w-full px-4 py-3 border border-navy-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-brand-accent"
            placeholder="Opsional untuk kondisi normal. Wajib diisi bila ada masalah."
          />
        </label>

        <div class="flex flex-col sm:flex-row sm:items-center gap-3">
          <button
            type="button"
            :disabled="submitting || (selectedStatus === 'received_with_issue' && (!selectedIssueType || !evidenceUploaded)) || (selectedStatus === 'not_received' && !note.trim())"
            @click="submitReceipt"
            class="px-6 py-3 bg-brand-accent hover:bg-brand-accent-hover disabled:bg-navy-300 disabled:cursor-not-allowed text-white font-semibold rounded-lg transition-colors"
          >
            {{ submitting ? 'Mengirim...' : 'Kirim Konfirmasi' }}
          </button>
          <p v-if="submitted" class="text-sm font-semibold text-emerald-700">Konfirmasi tersimpan dan dashboard regulator diperbarui.</p>
        </div>

        <div class="border-t border-navy-200 pt-5">
          <p class="text-sm font-bold text-navy-900 mb-2">Risk Status Setelah Konfirmasi</p>
          <div class="flex items-center justify-between gap-4">
            <p class="text-sm text-navy-600">{{ receipt.assessment.operationalSummary }}</p>
            <span class="px-3 py-1 rounded-full text-xs font-bold shrink-0" :class="receipt.assessment.riskStatus === 'HIGH' ? 'bg-red-100 text-red-700' : receipt.assessment.riskStatus === 'MEDIUM' ? 'bg-amber-100 text-amber-700' : 'bg-emerald-100 text-emerald-700'">
              {{ receipt.assessment.riskStatus }}
            </span>
          </div>
          <p v-if="receipt.receiptVerifiedAt" class="mt-3 text-xs text-navy-500">Verified at {{ new Intl.DateTimeFormat('id-ID', { dateStyle: 'medium', timeStyle: 'short' }).format(new Date(receipt.receiptVerifiedAt)) }}</p>
        </div>
      </div>
    </section>
  </main>
</template>
