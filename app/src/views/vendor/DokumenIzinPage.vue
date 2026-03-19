<script setup lang="ts">
import { ref } from 'vue'
import { getData, saveData, type Document } from '@/services/api'
import { useToast } from 'primevue/usetoast'

const toast = useToast()
const data = getData()
const documents = ref<Document[]>(data.documents)
const showModal = ref(false)
const newDocName = ref('')
const newDocExpiry = ref('')

function addDocument() {
  if (!newDocName.value || !newDocExpiry.value) return
  const doc: Document = {
    id: Date.now().toString(),
    vendorId: '2',
    name: newDocName.value,
    expiry: newDocExpiry.value,
    status: 'Valid',
  }
  documents.value.push(doc)
  data.documents.push(doc)
  saveData(data)
  newDocName.value = ''
  newDocExpiry.value = ''
  showModal.value = false
  toast.add({ severity: 'success', summary: 'Success', detail: 'Dokumen berhasil ditambahkan', life: 3000 })
}
</script>

<template>
  <div class="animate-fade-in">
    <div class="flex flex-col sm:flex-row justify-between items-start gap-4 sm:gap-0 mb-8">
      <div>
        <h1 class="text-2xl font-bold text-navy-900 mb-2">Pusat Sertifikasi & Izin</h1>
        <p class="text-navy-500 text-sm">Pastikan semua dokumen aktif untuk menjaga kontrak dengan BGN.</p>
      </div>
      <button @click="showModal = true" class="px-6 py-3 bg-navy-900 text-white text-sm font-semibold rounded-xl hover:bg-navy-800 transition-colors">
        Tambah Data +
      </button>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 lg:gap-6">
      <div v-for="doc in documents" :key="doc.id" class="bg-white rounded-xl border border-navy-200 shadow-sm p-6 relative hover:shadow-md transition-shadow">
        <span
          class="absolute top-4 right-4 text-white text-xs font-bold px-3 py-1 rounded-full"
          :class="doc.status === 'Valid' ? 'bg-brand-success' : 'bg-brand-danger'"
        >{{ doc.status }}</span>
        <div class="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center mb-4">
          <i class="pi pi-file text-brand-accent text-xl"></i>
        </div>
        <h3 class="font-bold text-navy-900 mb-1 text-sm">{{ doc.name }}</h3>
        <p class="text-xs text-navy-500 mb-4">Kedaluwarsa: {{ doc.expiry }}</p>
        <button class="px-4 py-2 border border-navy-200 rounded-lg text-xs font-medium text-navy-600 hover:bg-navy-50 transition-colors">
          Pratinjau
        </button>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50" @click.self="showModal = false">
      <div class="bg-white rounded-2xl shadow-xl w-full max-w-lg p-6 sm:p-8 animate-fade-in">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-lg font-bold text-navy-900">Tambah Dokumen Baru</h2>
          <button @click="showModal = false" class="text-navy-500 hover:text-navy-900">
            <i class="pi pi-times text-xl"></i>
          </button>
        </div>
        <form @submit.prevent="addDocument" class="space-y-5">
          <div>
            <label class="block text-sm font-medium text-navy-700 mb-2">Nama Dokumen</label>
            <input v-model="newDocName" type="text" placeholder="Contoh: Sertifikat Laik Higiene" class="w-full px-4 py-3 border border-navy-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-brand-accent" />
          </div>
          <div>
            <label class="block text-sm font-medium text-navy-700 mb-2">Tanggal Kedaluwarsa</label>
            <input v-model="newDocExpiry" type="text" placeholder="Contoh: 20 Des 2026" class="w-full px-4 py-3 border border-navy-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-brand-accent" />
          </div>
          <button type="submit" class="w-full py-3.5 bg-brand-accent hover:bg-brand-accent-hover text-white font-semibold rounded-lg transition-colors">
            Simpan Dokumen
          </button>
        </form>
      </div>
    </div>
  </div>
</template>
