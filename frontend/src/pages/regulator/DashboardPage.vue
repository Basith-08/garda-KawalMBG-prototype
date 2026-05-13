<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { fetchRegulatorOverview, type RegulatorOverview } from '@/services/regulator'

const overview = ref<RegulatorOverview | null>(null)
const loading = ref(true)
const error = ref('')

const metricTiles = computed(() => {
  if (!overview.value) return []
  const metrics = overview.value.platformMetrics
  return [
    {
      label: 'Vendor Terpantau',
      value: metrics.vendors,
      detail: `${metrics.schools} sekolah dalam cakupan pengawasan`,
      tone: 'text-navy-900',
      iconBg: 'bg-sky-100',
      icon: 'pi pi-users text-sky-700',
    },
    {
      label: 'Distribusi Tercatat',
      value: metrics.distributions,
      detail: `${metrics.onTimeRate}% masih dalam target durasi`,
      tone: 'text-navy-900',
      iconBg: 'bg-emerald-100',
      icon: 'pi pi-box text-emerald-700',
    },
    {
      label: 'Distribusi High Risk',
      value: metrics.highRiskDistributions,
      detail: `${metrics.receiptIssues} receipt issue perlu tindak lanjut`,
      tone: 'text-red-700',
      iconBg: 'bg-red-100',
      icon: 'pi pi-exclamation-triangle text-red-700',
    },
    {
      label: 'Alert Aktif',
      value: metrics.activeAlerts,
      detail: `${metrics.delayedDistributions} distribusi melewati target`,
      tone: 'text-amber-700',
      iconBg: 'bg-amber-100',
      icon: 'pi pi-bell text-amber-700',
    },
  ]
})

const watchlist = computed(() => {
  if (!overview.value) return []
  const metrics = overview.value.platformMetrics
  return [
    {
      label: 'Receipt bermasalah',
      value: metrics.receiptIssues,
      note: 'Kasus sekolah menerima distribusi dengan issue atau tidak menerima.',
    },
    {
      label: 'Distribusi terlambat',
      value: metrics.delayedDistributions,
      note: 'Durasi lebih dari 45 menit dari ambang operasi saat ini.',
    },
    {
      label: 'On-time rate',
      value: `${metrics.onTimeRate}%`,
      note: 'Rasio snapshot berdasarkan semua distribusi yang tersimpan.',
    },
  ]
})

function trustStatusClass(status: string) {
  if (status === 'high-risk') return 'bg-red-100 text-red-700'
  if (status === 'medium') return 'bg-amber-100 text-amber-700'
  return 'bg-emerald-100 text-emerald-700'
}

async function loadOverview() {
  loading.value = true
  error.value = ''
  try {
    overview.value = await fetchRegulatorOverview()
  } catch (err: any) {
    const detail = err?.response?.data?.detail
    error.value = typeof detail === 'string' ? detail : 'Gagal memuat snapshot regulator.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  void loadOverview()
})
</script>

<template>
  <div class="animate-fade-in space-y-8">
    <section class="flex flex-col lg:flex-row lg:items-end lg:justify-between gap-4">
      <div class="max-w-3xl">
        <p class="text-xs font-semibold uppercase tracking-[0.22em] text-sky-700 mb-3">Regulator Overview</p>
        <h1 class="text-3xl md:text-4xl font-bold text-navy-900 leading-tight">Permukaan kerja untuk memantau vendor, distribusi berisiko, dan receipt sekolah tanpa placeholder palsu.</h1>
        <p class="text-sm text-navy-500 mt-3">Snapshot ini memakai data backend aktual: vendor teratas berdasarkan trust score, distribusi high risk terbaru, serta metrik receipt dan keterlambatan.</p>
      </div>
      <button
        @click="loadOverview"
        class="px-5 py-3 rounded-xl border border-navy-200 bg-white text-sm font-semibold text-navy-700 hover:bg-navy-100 transition-colors self-start lg:self-auto"
      >
        Muat Ulang Snapshot
      </button>
    </section>

    <div v-if="error" class="rounded-2xl border border-red-200 bg-red-50 px-5 py-4 text-sm text-red-700">
      {{ error }}
    </div>

    <div v-if="loading && !overview" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
      <div v-for="item in 4" :key="item" class="h-32 rounded-2xl border border-navy-200 bg-white animate-pulse"></div>
    </div>

    <template v-if="overview">
      <section class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
        <article
          v-for="tile in metricTiles"
          :key="tile.label"
          class="rounded-2xl border border-navy-200 bg-white px-5 py-5 shadow-sm"
        >
          <div class="flex items-start justify-between gap-4">
            <div>
              <p class="text-xs uppercase tracking-[0.18em] text-navy-500 mb-3">{{ tile.label }}</p>
              <p class="text-3xl font-bold" :class="tile.tone">{{ tile.value }}</p>
            </div>
            <div class="w-11 h-11 rounded-full flex items-center justify-center" :class="tile.iconBg">
              <i :class="tile.icon"></i>
            </div>
          </div>
          <p class="text-sm text-navy-500 mt-4 leading-relaxed">{{ tile.detail }}</p>
        </article>
      </section>

      <section class="grid grid-cols-1 xl:grid-cols-[1.15fr,0.85fr] gap-6">
        <article class="rounded-3xl border border-navy-200 bg-white overflow-hidden">
          <div class="px-6 py-5 border-b border-navy-100">
            <h2 class="text-xl font-bold text-navy-900">Distribusi High Risk Terbaru</h2>
            <p class="text-sm text-navy-500 mt-1">Daftar ini memprioritaskan distribusi dengan skor risiko tertinggi yang sudah tercatat pada snapshot backend saat ini.</p>
          </div>
          <div v-if="overview.recentHighRisk.length" class="divide-y divide-navy-100">
            <div
              v-for="item in overview.recentHighRisk"
              :key="item.id"
              class="px-6 py-4 grid grid-cols-1 md:grid-cols-[1.1fr,0.8fr,0.7fr,0.8fr] gap-3 hover:bg-navy-50 transition-colors"
            >
              <div>
                <p class="font-semibold text-navy-900">{{ item.schoolName }}</p>
                <p class="text-xs text-navy-500 mt-1">{{ item.vendorName }}</p>
              </div>
              <div class="text-sm text-navy-700">
                <span class="font-semibold">{{ item.riskScore }}</span> risk score
              </div>
              <div class="text-sm text-navy-700">
                {{ item.statusText }}
              </div>
              <div class="text-sm text-navy-500">
                {{ item.time }}
              </div>
            </div>
          </div>
          <div v-else class="px-6 py-10 text-sm text-navy-500">
            Belum ada distribusi high risk pada snapshot saat ini.
          </div>
        </article>

        <article class="rounded-3xl border border-navy-200 bg-white overflow-hidden">
          <div class="px-6 py-5 border-b border-navy-100">
            <h2 class="text-xl font-bold text-navy-900">Watchlist Operasional</h2>
            <p class="text-sm text-navy-500 mt-1">Angka inti yang langsung berkaitan dengan follow-up regulator dan verifikasi sekolah.</p>
          </div>
          <div class="p-6 space-y-4">
            <div
              v-for="item in watchlist"
              :key="item.label"
              class="rounded-2xl border border-navy-100 bg-navy-50 px-4 py-4"
            >
              <div class="flex items-center justify-between gap-4 mb-2">
                <p class="text-sm font-semibold text-navy-900">{{ item.label }}</p>
                <span class="text-2xl font-bold text-navy-900">{{ item.value }}</span>
              </div>
              <p class="text-sm text-navy-500 leading-relaxed">{{ item.note }}</p>
            </div>
          </div>
        </article>
      </section>

      <section class="rounded-3xl border border-navy-200 bg-white overflow-hidden">
        <div class="px-6 py-5 border-b border-navy-100 flex flex-col lg:flex-row lg:items-end lg:justify-between gap-3">
          <div>
            <h2 class="text-xl font-bold text-navy-900">Top Vendor Berdasarkan Trust Score</h2>
            <p class="text-sm text-navy-500 mt-1">Dipakai untuk memisahkan vendor yang stabil dari vendor yang butuh pengawasan lebih rapat.</p>
          </div>
          <router-link
            to="/regulator/vendors"
            class="inline-flex px-4 py-2 rounded-xl border border-navy-200 text-sm font-semibold text-navy-700 hover:bg-navy-100 transition-colors"
          >
            Buka Daftar Vendor
          </router-link>
        </div>
        <div v-if="overview.topVendors.length" class="divide-y divide-navy-100">
          <div
            v-for="(vendor, index) in overview.topVendors"
            :key="vendor.id"
            class="px-6 py-4 grid grid-cols-1 md:grid-cols-[0.2fr,1fr,0.7fr,0.8fr] gap-3 hover:bg-navy-50 transition-colors"
          >
            <div class="text-sm font-semibold text-navy-500">#{{ index + 1 }}</div>
            <div>
              <p class="font-semibold text-navy-900">{{ vendor.name }}</p>
              <p class="text-xs text-navy-500 mt-1">{{ vendor.statusText }}</p>
            </div>
            <div>
              <span class="inline-flex px-3 py-1 rounded-full text-xs font-semibold capitalize" :class="trustStatusClass(vendor.status)">
                {{ vendor.status }}
              </span>
            </div>
            <div class="text-sm text-navy-700">
              <span class="font-semibold">{{ vendor.trustScore }}</span> trust score
            </div>
          </div>
        </div>
        <div v-else class="px-6 py-10 text-sm text-navy-500">
          Belum ada vendor yang dapat dirangking pada snapshot saat ini.
        </div>
      </section>
    </template>
  </div>
</template>
