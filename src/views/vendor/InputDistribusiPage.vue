<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const menuUtama = ref('Nasi, Ayam bakar, Lalapan')
const jumlahPorsi = ref(450)
const jamMasak = ref('06:00')
const jamBerangkat = ref('08:00')
const schools = ref(['SDN 01 Pusat', 'SDN 05 Barat', 'SD Harapan'])

function hitungSkor() {
  router.push('/vendor/input-distribusi/result')
}
</script>

<template>
  <div class="animate-fade-in">
    <h1 class="text-2xl font-bold text-navy-900 mb-8">Input Distribusi Hari Ini</h1>

    <div class="flex gap-8">
      <!-- Form -->
      <div class="flex-1 space-y-6">
        <div class="flex items-center gap-8">
          <label class="text-lg font-bold text-navy-900 w-48 shrink-0">Menu Utama:</label>
          <input v-model="menuUtama" type="text" class="flex-1 px-4 py-3 border border-navy-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-brand-accent" />
        </div>
        <div class="flex items-center gap-8">
          <label class="text-lg font-bold text-navy-900 w-48 shrink-0">Jumlah Porsi/<br/>Sekolah</label>
          <input v-model="jumlahPorsi" type="number" class="w-28 px-4 py-3 border border-navy-200 rounded-lg text-sm text-center focus:outline-none focus:ring-2 focus:ring-brand-accent" />
        </div>
        <div class="flex items-center gap-8">
          <label class="text-lg font-bold text-navy-900 w-48 shrink-0">Jam Selesai Masak:</label>
          <select v-model="jamMasak" class="px-4 py-3 border border-navy-200 rounded-lg text-sm bg-white">
            <option>05:00</option><option>06:00</option><option>07:00</option>
          </select>
        </div>
        <div class="flex items-center gap-8">
          <label class="text-lg font-bold text-navy-900 w-48 shrink-0">Jam Keberangkatan:</label>
          <select v-model="jamBerangkat" class="px-4 py-3 border border-navy-200 rounded-lg text-sm bg-white">
            <option>07:00</option><option>08:00</option><option>09:00</option>
          </select>
        </div>
        <div class="flex items-start gap-8">
          <label class="text-lg font-bold text-navy-900 w-48 shrink-0 pt-2">Sekolah Tujuan:</label>
          <div>
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

        <button @click="hitungSkor" class="mt-4 px-10 py-4 bg-brand-accent hover:bg-brand-accent-hover text-white font-semibold rounded-xl transition-colors shadow-md text-lg">
          Hitung Skor Risiko
        </button>
      </div>

      <!-- Live Update Sidebar -->
      <div class="w-72 shrink-0">
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
                <p class="text-lg font-bold text-brand-danger">32°C</p>
              </div>
            </div>
            <div class="flex items-center gap-3">
              <i class="pi pi-truck text-brand-accent text-lg"></i>
              <div>
                <p class="text-sm font-bold text-navy-700">Estimasi tiba:</p>
                <p class="text-lg font-bold text-navy-900">09:30 WIB</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
