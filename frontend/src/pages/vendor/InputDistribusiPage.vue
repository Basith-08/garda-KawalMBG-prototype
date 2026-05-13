<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const menuUtama = ref('Nasi, Ayam bakar, Lalapan')
const jumlahPorsi = ref(450)
const jamMasak = ref('06:00')
const jamPlating = ref('06:35')
const jamBerangkat = ref('08:00')
const estimasiTiba = ref('08:45')
const suhu = ref(32)
const schools = ref(['SDN 01 Pusat', 'SDN 05 Barat', 'SD Harapan'])
const qcPhotoUploaded = ref(true)
const productionPhotoUploaded = ref(true)
const packagingPhotoUploaded = ref(true)
const vehiclePhotoUploaded = ref(false)

function minutesBetween(start: string, end: string) {
  const [startHour, startMinute] = start.split(':').map(Number)
  const [endHour, endMinute] = end.split(':').map(Number)
  let startTotal = startHour * 60 + startMinute
  let endTotal = endHour * 60 + endMinute
  if (endTotal < startTotal) endTotal += 24 * 60
  return Math.max(0, endTotal - startTotal)
}

const exposureMinutes = computed(() => minutesBetween(jamMasak.value, estimasiTiba.value))
const routeMinutes = computed(() => minutesBetween(jamBerangkat.value, estimasiTiba.value))
const evidenceUploaded = computed(() => qcPhotoUploaded.value && productionPhotoUploaded.value && packagingPhotoUploaded.value && vehiclePhotoUploaded.value)

function hitungSkor() {
  localStorage.setItem('kawalmbg_draft_dist', JSON.stringify({
    menuUtama: menuUtama.value,
    jumlahPorsi: jumlahPorsi.value,
    jamMasak: jamMasak.value,
    jamPlating: jamPlating.value,
    jamBerangkat: jamBerangkat.value,
    estimasiTiba: estimasiTiba.value,
    suhu: suhu.value,
    durasi: exposureMinutes.value,
    routeMinutes: routeMinutes.value,
    qcPhotoUploaded: qcPhotoUploaded.value,
    productionPhotoUploaded: productionPhotoUploaded.value,
    packagingPhotoUploaded: packagingPhotoUploaded.value,
    vehiclePhotoUploaded: vehiclePhotoUploaded.value,
    evidenceUploaded: evidenceUploaded.value,
    schools: schools.value
  }))
  router.push('/vendor/input-distribusi/result')
}
</script>

<template>
  <div class="animate-fade-in">
    <h1 class="text-2xl font-bold text-navy-900 mb-8">Input Distribusi Hari Ini</h1>

    <div class="flex flex-col lg:flex-row gap-6 lg:gap-8">
      <!-- Form -->
      <div class="flex-1 space-y-4 md:space-y-6">
        <div class="flex flex-col md:flex-row md:items-center gap-2 md:gap-8">
          <label class="text-base md:text-lg font-bold text-navy-900 md:w-48 shrink-0">Menu Utama:</label>
          <input v-model="menuUtama" type="text" class="w-full md:flex-1 px-4 py-3 border border-navy-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-brand-accent" />
        </div>
        <div class="flex flex-col md:flex-row md:items-center gap-2 md:gap-8">
          <label class="text-base md:text-lg font-bold text-navy-900 md:w-48 shrink-0">Jumlah Porsi/<br class="hidden md:block"/>Sekolah</label>
          <input v-model="jumlahPorsi" type="number" class="w-full md:w-28 px-4 py-3 border border-navy-200 rounded-lg text-sm text-center focus:outline-none focus:ring-2 focus:ring-brand-accent" />
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 md:pl-56">
          <label class="block">
            <span class="block text-sm font-bold text-navy-700 mb-2">Jam Selesai Masak</span>
            <input v-model="jamMasak" type="time" class="w-full px-4 py-3 border border-navy-200 rounded-lg text-sm bg-white" />
          </label>
          <label class="block">
            <span class="block text-sm font-bold text-navy-700 mb-2">Jam Plating</span>
            <input v-model="jamPlating" type="time" class="w-full px-4 py-3 border border-navy-200 rounded-lg text-sm bg-white" />
          </label>
          <label class="block">
            <span class="block text-sm font-bold text-navy-700 mb-2">Jam Berangkat</span>
            <input v-model="jamBerangkat" type="time" class="w-full px-4 py-3 border border-navy-200 rounded-lg text-sm bg-white" />
          </label>
          <label class="block">
            <span class="block text-sm font-bold text-navy-700 mb-2">Estimasi Tiba</span>
            <input v-model="estimasiTiba" type="time" class="w-full px-4 py-3 border border-navy-200 rounded-lg text-sm bg-white" />
          </label>
        </div>
        <div class="flex flex-col md:flex-row md:items-center gap-2 md:gap-8">
          <label class="text-base md:text-lg font-bold text-navy-900 md:w-48 shrink-0">Suhu Lingkungan:</label>
          <div class="flex items-center gap-3">
            <input v-model.number="suhu" type="number" min="20" max="45" class="w-28 px-4 py-3 border border-navy-200 rounded-lg text-sm text-center focus:outline-none focus:ring-2 focus:ring-brand-accent" />
            <span class="text-sm font-bold text-navy-600">°C</span>
          </div>
        </div>
        <div class="flex flex-col md:flex-row md:items-start gap-2 md:gap-8">
          <label class="text-base md:text-lg font-bold text-navy-900 md:w-48 shrink-0 pt-1">Bukti QC:</label>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full">
            <label class="flex items-center gap-3 text-sm text-navy-700">
              <input v-model="qcPhotoUploaded" type="checkbox" class="w-4 h-4 accent-brand-accent" />
              Foto QC makanan
            </label>
            <label class="flex items-center gap-3 text-sm text-navy-700">
              <input v-model="productionPhotoUploaded" type="checkbox" class="w-4 h-4 accent-brand-accent" />
              Foto area produksi
            </label>
            <label class="flex items-center gap-3 text-sm text-navy-700">
              <input v-model="packagingPhotoUploaded" type="checkbox" class="w-4 h-4 accent-brand-accent" />
              Foto kemasan batch
            </label>
            <label class="flex items-center gap-3 text-sm text-navy-700">
              <input v-model="vehiclePhotoUploaded" type="checkbox" class="w-4 h-4 accent-brand-accent" />
              Foto kendaraan siap kirim
            </label>
          </div>
        </div>
        <div class="flex flex-col md:flex-row md:items-start gap-2 md:gap-8">
          <label class="text-base md:text-lg font-bold text-navy-900 md:w-48 shrink-0 pt-0 md:pt-2">Sekolah Tujuan:</label>
          <div class="w-full">
            <div class="flex flex-wrap gap-3 mb-3">
              <span v-for="s in schools" :key="s" class="inline-flex items-center gap-2 px-5 py-2.5 bg-navy-500 text-white rounded-full text-sm font-medium">
                <i class="pi pi-check-circle text-brand-success"></i> {{ s }}
              </span>
            </div>
            <button class="px-5 py-2.5 border border-navy-200 rounded-full text-sm text-navy-600 hover:bg-navy-100 transition-colors">
              Tambah Sekolah +
            </button>
          </div>
        </div>

        <button @click="hitungSkor" class="mt-4 w-full md:w-auto px-10 py-4 bg-brand-accent hover:bg-brand-accent-hover text-white font-semibold rounded-xl transition-colors shadow-md text-lg">
          Hitung Skor Risiko
        </button>
      </div>

      <!-- Live Update Sidebar -->
      <div class="w-full lg:w-72 shrink-0">
        <div class="bg-white rounded-xl border border-navy-200 shadow-sm p-5">
          <div class="flex items-center gap-2 mb-4">
            <span class="w-3 h-3 rounded-full bg-brand-danger animate-pulse-dot"></span>
            <h3 class="font-bold text-navy-900">Live Update</h3>
          </div>
          <div class="space-y-4">
            <div class="flex items-center gap-3">
              <i class="pi pi-sun text-amber-500 text-lg"></i>
              <div>
                <p class="text-sm font-bold text-navy-700">Suhu:</p>
                <p class="text-lg font-bold text-brand-danger">{{ suhu }}°C</p>
              </div>
            </div>
            <div class="flex items-center gap-3">
              <i class="pi pi-truck text-brand-accent text-lg"></i>
              <div>
                <p class="text-sm font-bold text-navy-700">Estimasi tiba:</p>
                <p class="text-lg font-bold text-navy-900">{{ estimasiTiba }} WIB</p>
              </div>
            </div>
            <div class="flex items-center gap-3">
              <i class="pi pi-clock text-brand-success text-lg"></i>
              <div>
                <p class="text-sm font-bold text-navy-700">Total exposure:</p>
                <p class="text-lg font-bold text-navy-900">{{ exposureMinutes }} menit</p>
                <p class="text-xs text-navy-500">Rute {{ routeMinutes }} menit</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
