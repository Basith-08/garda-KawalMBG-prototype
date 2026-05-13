<script setup lang="ts">
import { computed } from 'vue'
import type { Distribution, DistributionReceipt, ReceiptArrivalStatus, ReceiptIssueType } from '@/types/domain'

const props = defineProps<{
  distribution: Distribution
  receipt?: DistributionReceipt | null
  receiptUrl?: string
}>()

const receiptStatus = computed<ReceiptArrivalStatus>(() => props.receipt?.arrivalStatus ?? props.distribution.arrivalStatus ?? 'not_confirmed')
const receiptIssueType = computed<ReceiptIssueType | null>(() => props.receipt?.receiptIssueType ?? props.distribution.receiptIssueType ?? null)
const receiptEvidenceUploaded = computed(() => props.receipt?.receiptEvidenceUploaded ?? props.distribution.receiptEvidenceUploaded ?? false)
const receiptNote = computed(() => props.receipt?.receiptNote ?? props.distribution.receiptNote ?? null)
const receiptVerifiedAt = computed(() => props.receipt?.receiptVerifiedAt ?? props.distribution.receiptVerifiedAt ?? null)

function formatReceiptStatus(status: ReceiptArrivalStatus) {
  return {
    received_ok: 'Diterima baik',
    received_with_issue: 'Diterima dengan masalah',
    not_received: 'Belum diterima',
    not_confirmed: 'Belum dikonfirmasi',
  }[status]
}

function formatIssueType(issueType: ReceiptIssueType | null) {
  if (!issueType) return 'Tidak ada'
  return {
    packaging_damaged: 'Kemasan rusak',
    portion_shortage: 'Jumlah kurang',
    unsafe_smell_or_quality: 'Bau / mutu tidak layak',
    menu_mismatch: 'Menu tidak sesuai',
    late_arrival: 'Datang terlambat',
    not_received: 'Belum diterima',
    other: 'Lainnya',
  }[issueType]
}

function formatVerifiedAt(value?: string | null) {
  if (!value) return 'Belum ada'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value
  return new Intl.DateTimeFormat('id-ID', {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(date)
}

function receiptTone(status: ReceiptArrivalStatus) {
  if (status === 'received_ok') return 'bg-emerald-100 text-emerald-700 border-emerald-200'
  if (status === 'received_with_issue') return 'bg-amber-100 text-amber-700 border-amber-200'
  if (status === 'not_received') return 'bg-red-100 text-red-700 border-red-200'
  return 'bg-navy-100 text-navy-600 border-navy-200'
}
</script>

<template>
  <section class="rounded-2xl border border-navy-200 bg-white p-6 space-y-6">
    <div class="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
      <div>
        <h3 class="text-lg font-bold text-navy-900">Receipt & Evidence Verification</h3>
        <p class="text-sm text-navy-500 mt-1">Ringkasan receipt sekolah, kategori masalah, jejak evidence, dan timeline operasional.</p>
      </div>
      <a
        v-if="receiptUrl"
        :href="receiptUrl"
        target="_blank"
        rel="noreferrer"
        class="inline-flex items-center justify-center rounded-xl border border-navy-200 bg-white px-4 py-2 text-sm font-semibold text-navy-700 hover:bg-navy-100 transition-colors"
      >
        Buka Receipt Publik
      </a>
    </div>

    <div class="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
      <article class="rounded-2xl border p-4" :class="receiptTone(receiptStatus)">
        <p class="text-xs font-semibold uppercase tracking-[0.18em]">Receipt Sekolah</p>
        <p class="mt-3 text-sm font-bold">{{ formatReceiptStatus(receiptStatus) }}</p>
      </article>
      <article class="rounded-2xl border border-navy-100 bg-navy-50 p-4">
        <p class="text-xs font-semibold uppercase tracking-[0.18em] text-navy-500">Kategori Masalah</p>
        <p class="mt-3 text-sm font-bold text-navy-900">{{ formatIssueType(receiptIssueType) }}</p>
      </article>
      <article class="rounded-2xl border border-navy-100 bg-navy-50 p-4">
        <p class="text-xs font-semibold uppercase tracking-[0.18em] text-navy-500">Evidence Receipt</p>
        <p class="mt-3 text-sm font-bold" :class="receiptEvidenceUploaded ? 'text-emerald-700' : 'text-navy-900'">
          {{ receiptEvidenceUploaded ? 'Terlampir' : 'Belum ada' }}
        </p>
      </article>
      <article class="rounded-2xl border border-navy-100 bg-navy-50 p-4">
        <p class="text-xs font-semibold uppercase tracking-[0.18em] text-navy-500">Verified At</p>
        <p class="mt-3 text-sm font-bold text-navy-900">{{ formatVerifiedAt(receiptVerifiedAt) }}</p>
      </article>
    </div>

    <div v-if="receiptNote" class="rounded-2xl border border-navy-100 bg-navy-50 px-4 py-4">
      <p class="text-xs font-semibold uppercase tracking-[0.18em] text-navy-500 mb-2">Catatan Receipt</p>
      <p class="text-sm leading-relaxed text-navy-700">{{ receiptNote }}</p>
    </div>

    <div class="grid grid-cols-2 gap-4 md:grid-cols-5 text-sm">
      <div>
        <p class="text-xs text-navy-500 mb-1">Cooked</p>
        <p class="font-bold text-navy-900">{{ distribution.cookedAt || '-' }}</p>
      </div>
      <div>
        <p class="text-xs text-navy-500 mb-1">Packaged</p>
        <p class="font-bold text-navy-900">{{ distribution.packagedAt || '-' }}</p>
      </div>
      <div>
        <p class="text-xs text-navy-500 mb-1">Pickup</p>
        <p class="font-bold text-navy-900">{{ distribution.pickupAt || '-' }}</p>
      </div>
      <div>
        <p class="text-xs text-navy-500 mb-1">Delivered</p>
        <p class="font-bold text-navy-900">{{ distribution.deliveredAt || '-' }}</p>
      </div>
      <div>
        <p class="text-xs text-navy-500 mb-1">Evidence Vendor</p>
        <p class="font-bold" :class="distribution.evidenceUploaded ? 'text-emerald-700' : 'text-amber-700'">
          {{ distribution.evidenceUploaded ? 'Lengkap' : 'Perlu dilengkapi' }}
        </p>
      </div>
    </div>

    <div class="grid grid-cols-2 gap-3 md:grid-cols-5 text-xs">
      <span class="rounded-lg px-3 py-2" :class="distribution.qcPhotoUploaded ? 'bg-emerald-100 text-emerald-700' : 'bg-navy-100 text-navy-500'">QC</span>
      <span class="rounded-lg px-3 py-2" :class="distribution.productionPhotoUploaded ? 'bg-emerald-100 text-emerald-700' : 'bg-navy-100 text-navy-500'">Produksi</span>
      <span class="rounded-lg px-3 py-2" :class="distribution.packagingPhotoUploaded ? 'bg-emerald-100 text-emerald-700' : 'bg-navy-100 text-navy-500'">Kemasan</span>
      <span class="rounded-lg px-3 py-2" :class="distribution.vehiclePhotoUploaded ? 'bg-emerald-100 text-emerald-700' : 'bg-navy-100 text-navy-500'">Kendaraan</span>
      <span class="rounded-lg px-3 py-2" :class="distribution.evidenceUploaded ? 'bg-emerald-100 text-emerald-700' : 'bg-amber-100 text-amber-700'">Evidence</span>
    </div>
  </section>
</template>
