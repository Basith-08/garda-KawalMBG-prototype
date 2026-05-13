<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import {
  fetchAdminOverview,
  updateAdminUser,
  type AdminDataQualityItem,
  type AdminExpiringDocumentItem,
  type AdminOverview,
  type AdminUserAccessItem,
} from '@/services/admin'

const overview = ref<AdminOverview | null>(null)
const loading = ref(true)
const error = ref('')
const saving = ref(false)
const selectedUser = ref<AdminUserAccessItem | null>(null)
const formRole = ref<AdminUserAccessItem['role']>('vendor')
const formVendorId = ref<string | null>(null)
const formIsActive = ref(true)
const formError = ref('')

const metricTiles = computed(() => {
  if (!overview.value) return []
  const metrics = overview.value.platformMetrics
  return [
    { label: 'User Aktif', value: `${metrics.activeUsers}/${metrics.totalUsers}`, tone: 'text-navy-900' },
    { label: 'Vendor Terdaftar', value: metrics.vendors, tone: 'text-navy-900' },
    { label: 'Distribusi High Risk', value: metrics.highRiskDistributions, tone: 'text-red-700' },
    { label: 'Dokumen Jatuh Tempo ≤30 Hari', value: metrics.expiringDocuments30d, tone: 'text-amber-700' },
  ]
})

const vendorOptions = computed(() => overview.value?.availableVendors ?? [])

function severityClass(item: AdminDataQualityItem) {
  if (item.severity === 'high') return 'bg-red-100 text-red-700 border-red-200'
  if (item.severity === 'medium') return 'bg-amber-100 text-amber-700 border-amber-200'
  return 'bg-sky-100 text-sky-700 border-sky-200'
}

function vendorStatusClass(status: string) {
  if (status === 'high-risk') return 'bg-red-100 text-red-700'
  if (status === 'medium') return 'bg-amber-100 text-amber-700'
  return 'bg-emerald-100 text-emerald-700'
}

function roleClass(role: AdminUserAccessItem['role']) {
  if (role === 'super-admin') return 'bg-amber-100 text-amber-700'
  if (role === 'regulator') return 'bg-rose-100 text-rose-700'
  return 'bg-emerald-100 text-emerald-700'
}

function formatDate(value?: string | null) {
  if (!value) return 'Belum ada'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value
  return new Intl.DateTimeFormat('id-ID', {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(date)
}

function documentTone(item: AdminExpiringDocumentItem) {
  if (item.daysLeft === null) return 'text-navy-500'
  if (item.daysLeft < 0) return 'text-red-700'
  if (item.daysLeft <= 7) return 'text-amber-700'
  return 'text-navy-700'
}

async function loadOverview() {
  loading.value = true
  error.value = ''
  try {
    overview.value = await fetchAdminOverview()
  } catch (err: any) {
    const detail = err?.response?.data?.detail
    error.value = typeof detail === 'string' ? detail : 'Gagal memuat control center.'
  } finally {
    loading.value = false
  }
}

function openUserEditor(user: AdminUserAccessItem) {
  selectedUser.value = user
  formRole.value = user.role
  formVendorId.value = user.vendorId ?? null
  formIsActive.value = user.isActive
  formError.value = ''
}

function closeUserEditor() {
  selectedUser.value = null
  formError.value = ''
}

async function saveUserAccess() {
  if (!selectedUser.value) return
  saving.value = true
  formError.value = ''
  try {
    await updateAdminUser(selectedUser.value.id, {
      role: formRole.value,
      vendorId: formRole.value === 'vendor' ? formVendorId.value : null,
      isActive: formIsActive.value,
    })
    await loadOverview()
    closeUserEditor()
  } catch (err: any) {
    const detail = err?.response?.data?.detail
    formError.value = typeof detail === 'string' ? detail : 'Gagal menyimpan perubahan akses user.'
  } finally {
    saving.value = false
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
        <p class="text-xs font-semibold uppercase tracking-[0.22em] text-amber-700 mb-3">Super Admin Control Center</p>
        <h1 class="text-3xl md:text-4xl font-bold text-navy-900 leading-tight">Governance, akses, dan kualitas data platform dalam satu permukaan kerja.</h1>
        <p class="text-sm text-navy-500 mt-3">Panel ini diprioritaskan untuk keputusan sistem: akun aktif, kesehatan data relasional, vendor yang perlu intervensi, dan dokumen yang mendekati risiko operasional.</p>
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
          <p class="text-xs uppercase tracking-[0.18em] text-navy-500 mb-4">{{ tile.label }}</p>
          <p class="text-3xl font-bold" :class="tile.tone">{{ tile.value }}</p>
        </article>
      </section>

      <section class="grid grid-cols-1 xl:grid-cols-[1.2fr,0.8fr] gap-6">
        <article class="rounded-3xl border border-navy-200 bg-white overflow-hidden">
          <div class="px-6 py-5 border-b border-navy-100">
            <h2 class="text-xl font-bold text-navy-900">Vendor Prioritas Intervensi</h2>
            <p class="text-sm text-navy-500 mt-1">Diurutkan dari kombinasi status risiko, trust score, alert aktif, dan beban dokumen jatuh tempo.</p>
          </div>
          <div class="divide-y divide-navy-100">
            <div
              v-for="vendor in overview.vendorAttention"
              :key="vendor.id"
              class="px-6 py-4 grid grid-cols-1 md:grid-cols-[1.2fr,0.8fr,0.8fr,0.9fr] gap-3 hover:bg-navy-50 transition-colors"
            >
              <div>
                <p class="font-semibold text-navy-900">{{ vendor.name }}</p>
                <p class="text-xs text-navy-500 mt-1">{{ vendor.schoolCount }} sekolah · {{ vendor.distributionCount }} distribusi</p>
              </div>
              <div>
                <span class="inline-flex px-3 py-1 rounded-full text-xs font-semibold capitalize" :class="vendorStatusClass(vendor.status)">
                  {{ vendor.status }}
                </span>
              </div>
              <div class="text-sm text-navy-700">
                <span class="font-semibold">{{ vendor.trustScore }}</span> trust score
              </div>
              <div class="text-sm text-navy-700">
                <span class="font-semibold">{{ vendor.alertCount }}</span> alert ·
                <span class="font-semibold">{{ vendor.expiringDocumentCount }}</span> dokumen
              </div>
            </div>
          </div>
        </article>

        <article class="rounded-3xl border border-navy-200 bg-white overflow-hidden">
          <div class="px-6 py-5 border-b border-navy-100">
            <h2 class="text-xl font-bold text-navy-900">Kualitas Arsitektur Data</h2>
            <p class="text-sm text-navy-500 mt-1">Temuan yang perlu dibersihkan agar source of truth tetap konsisten dan dapat diaudit.</p>
          </div>
          <div class="p-6 space-y-4">
            <div
              v-for="item in overview.dataQuality"
              :key="item.code"
              class="rounded-2xl border px-4 py-4"
              :class="severityClass(item)"
            >
              <div class="flex items-center justify-between gap-4 mb-2">
                <p class="text-sm font-semibold">{{ item.code }}</p>
                <span class="text-2xl font-bold">{{ item.count }}</span>
              </div>
              <p class="text-sm leading-relaxed">{{ item.description }}</p>
            </div>
          </div>
        </article>
      </section>

      <section class="grid grid-cols-1 xl:grid-cols-[1.15fr,0.85fr] gap-6">
        <article class="rounded-3xl border border-navy-200 bg-white overflow-hidden">
          <div class="px-6 py-5 border-b border-navy-100">
            <h2 class="text-xl font-bold text-navy-900">Akses & Peran Pengguna</h2>
            <p class="text-sm text-navy-500 mt-1">Super admin dapat memverifikasi role, linkage vendor, dan aktivitas login terakhir dari satu tabel kerja.</p>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full min-w-[780px]">
              <thead>
                <tr class="border-b border-navy-100">
                  <th class="px-6 py-4 text-left text-xs font-semibold uppercase tracking-[0.18em] text-navy-500">Akun</th>
                  <th class="px-6 py-4 text-left text-xs font-semibold uppercase tracking-[0.18em] text-navy-500">Role</th>
                  <th class="px-6 py-4 text-left text-xs font-semibold uppercase tracking-[0.18em] text-navy-500">Link Vendor</th>
                  <th class="px-6 py-4 text-left text-xs font-semibold uppercase tracking-[0.18em] text-navy-500">Aktif</th>
                  <th class="px-6 py-4 text-left text-xs font-semibold uppercase tracking-[0.18em] text-navy-500">Login Terakhir</th>
                  <th class="px-6 py-4 text-left text-xs font-semibold uppercase tracking-[0.18em] text-navy-500">Aksi</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="user in overview.userAccess" :key="user.id" class="border-b border-navy-50 last:border-b-0 hover:bg-navy-50 transition-colors">
                  <td class="px-6 py-4">
                    <div class="flex items-center gap-3">
                      <img :src="user.avatar" :alt="user.name" class="w-10 h-10 rounded-full object-cover border border-navy-200" />
                      <div>
                        <p class="text-sm font-semibold text-navy-900">{{ user.name }}</p>
                        <p class="text-xs text-navy-500">{{ user.email }}</p>
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-4">
                    <span class="inline-flex px-3 py-1 rounded-full text-xs font-semibold" :class="roleClass(user.role)">
                      {{ user.role }}
                    </span>
                  </td>
                  <td class="px-6 py-4 text-sm text-navy-700">
                    {{ user.vendorName || user.vendorId || 'Tidak terkait vendor' }}
                  </td>
                  <td class="px-6 py-4 text-sm">
                    <span :class="user.isActive ? 'text-emerald-700' : 'text-red-700'">{{ user.isActive ? 'Active' : 'Inactive' }}</span>
                  </td>
                  <td class="px-6 py-4 text-sm text-navy-700">
                    {{ formatDate(user.lastLoginAt) }}
                  </td>
                  <td class="px-6 py-4">
                    <button
                      @click="openUserEditor(user)"
                      class="px-3 py-2 rounded-lg border border-navy-200 text-xs font-semibold text-navy-700 hover:bg-navy-100 transition-colors"
                    >
                      Kelola Akses
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </article>

        <article class="rounded-3xl border border-navy-200 bg-white overflow-hidden">
          <div class="px-6 py-5 border-b border-navy-100">
            <h2 class="text-xl font-bold text-navy-900">Dokumen Mendekati Risiko</h2>
            <p class="text-sm text-navy-500 mt-1">Urutkan tindakan renewal dari yang paling mendesak.</p>
          </div>
          <div class="p-6 space-y-4">
            <div
              v-for="document in overview.expiringDocuments"
              :key="document.id"
              class="flex items-start justify-between gap-4 rounded-2xl border border-navy-100 px-4 py-4 hover:bg-navy-50 transition-colors"
            >
              <div>
                <p class="text-sm font-semibold text-navy-900">{{ document.name }}</p>
                <p class="text-xs text-navy-500 mt-1">Vendor ID {{ document.vendorId }} · {{ document.expiry }}</p>
              </div>
              <div class="text-right">
                <p class="text-sm font-semibold" :class="documentTone(document)">
                  {{ document.daysLeft === null ? 'Tanpa tanggal' : document.daysLeft < 0 ? `Lewat ${Math.abs(document.daysLeft)} hari` : `${document.daysLeft} hari lagi` }}
                </p>
                <p class="text-xs text-navy-500 mt-1">{{ document.status }}</p>
              </div>
            </div>
            <p v-if="overview.expiringDocuments.length === 0" class="text-sm text-navy-500">Tidak ada dokumen jatuh tempo dalam 30 hari.</p>
          </div>
        </article>
      </section>
    </template>

    <div
      v-if="selectedUser"
      class="fixed inset-0 bg-navy-950/40 backdrop-blur-sm z-50 flex items-center justify-center p-4"
      @click.self="closeUserEditor"
    >
      <div class="w-full max-w-xl rounded-3xl bg-white border border-navy-200 shadow-2xl overflow-hidden">
        <div class="px-6 py-5 border-b border-navy-100 flex items-start justify-between gap-4">
          <div>
            <p class="text-xs uppercase tracking-[0.18em] text-navy-500 mb-2">User Access Editor</p>
            <h3 class="text-xl font-bold text-navy-900">{{ selectedUser.name }}</h3>
            <p class="text-sm text-navy-500 mt-1">{{ selectedUser.email }}</p>
          </div>
          <button @click="closeUserEditor" class="w-10 h-10 rounded-full border border-navy-200 text-navy-600 hover:bg-navy-100 transition-colors">
            <i class="pi pi-times"></i>
          </button>
        </div>

        <div class="px-6 py-6 space-y-5">
          <div>
            <label class="block text-sm font-semibold text-navy-800 mb-2">Role</label>
            <select v-model="formRole" class="w-full px-4 py-3 rounded-xl border border-navy-200 bg-white text-sm text-navy-800 focus:outline-none focus:ring-2 focus:ring-brand-accent">
              <option value="super-admin">super-admin</option>
              <option value="regulator">regulator</option>
              <option value="vendor">vendor</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-semibold text-navy-800 mb-2">Link Vendor</label>
            <select
              v-model="formVendorId"
              :disabled="formRole !== 'vendor'"
              class="w-full px-4 py-3 rounded-xl border border-navy-200 bg-white text-sm text-navy-800 disabled:bg-navy-100 disabled:text-navy-400 focus:outline-none focus:ring-2 focus:ring-brand-accent"
            >
              <option :value="null">Tidak terkait vendor</option>
              <option v-for="vendor in vendorOptions" :key="vendor.id" :value="vendor.id">{{ vendor.name }}</option>
            </select>
          </div>

          <label class="flex items-center gap-3 rounded-2xl border border-navy-200 px-4 py-4">
            <input v-model="formIsActive" type="checkbox" class="w-4 h-4 rounded border-navy-300 text-brand-accent" />
            <div>
              <p class="text-sm font-semibold text-navy-900">Akun Aktif</p>
              <p class="text-xs text-navy-500 mt-1">User nonaktif tidak bisa login, tetapi tetap tercatat untuk audit.</p>
            </div>
          </label>

          <div v-if="formError" class="rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
            {{ formError }}
          </div>
        </div>

        <div class="px-6 py-5 border-t border-navy-100 flex flex-col-reverse sm:flex-row sm:justify-end gap-3">
          <button
            @click="closeUserEditor"
            class="px-5 py-3 rounded-xl border border-navy-200 text-sm font-semibold text-navy-700 hover:bg-navy-100 transition-colors"
          >
            Batal
          </button>
          <button
            @click="saveUserAccess"
            :disabled="saving"
            class="px-5 py-3 rounded-xl bg-navy-900 text-white text-sm font-semibold hover:bg-navy-800 disabled:opacity-60 disabled:cursor-not-allowed transition-colors"
          >
            {{ saving ? 'Menyimpan...' : 'Simpan Perubahan' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
