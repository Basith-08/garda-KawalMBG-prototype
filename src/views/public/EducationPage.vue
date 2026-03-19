<script setup lang="ts">
import { ref } from 'vue'

const faqs = ref([
  { q: 'Apa itu KawalMBG?', a: 'KawalMBG adalah sistem monitoring distribusi Makanan Bergizi Gratis berbasis AI untuk transparansi pangan nasional.', open: false },
  { q: 'Bagaimana cara kerja Risk Scoring?', a: 'Sistem menganalisis data suhu, waktu masak, dan durasi pengiriman untuk memprediksi risiko kualitas makanan.', open: false },
  { q: 'Siapa yang bisa mengakses skor vendor?', a: 'Skor vendor bersifat publik dan dapat diakses oleh siapa saja melalui halaman Vendor Score.', open: false },
  { q: 'Bagaimana cara melaporkan masalah?', a: 'Anda dapat menghubungi tim KawalMBG melalui formulir kontak atau email resmi kami.', open: false },
])
</script>

<template>
  <div class="max-w-7xl mx-auto px-8 py-8 animate-fade-in">
    <!-- Header -->
    <div class="text-center mb-12">
      <div class="flex items-center justify-center gap-6 mb-4">
        <div class="w-16 h-16 bg-blue-100 rounded-xl flex items-center justify-center">
          <i class="pi pi-graduation-cap text-3xl text-brand-accent"></i>
        </div>
        <div>
          <h1 class="text-3xl font-bold text-navy-900">Pusat Edukasi & Bantuan</h1>
          <p class="text-navy-500 mt-1">Transparansi penuh atas setiap rupiah yang dialokasikan untuk gizi anak bangsa.</p>
        </div>
        <svg width="56" height="56" viewBox="0 0 56 56" fill="none">
          <path d="M28 4L8 14v12c0 11 8 21 20 24 12-3 20-13 20-24V14L28 4z" stroke="#1e293b" stroke-width="3" fill="none"/>
          <circle cx="28" cy="28" r="7" fill="none" stroke="#1e293b" stroke-width="2.5"/>
          <circle cx="28" cy="28" r="2.5" fill="#1e293b"/>
        </svg>
      </div>
    </div>

    <!-- Articles Skeleton -->
    <div class="flex gap-8 mb-16">
      <div class="flex-1 space-y-4">
        <div class="h-8 bg-navy-200 rounded w-4/5"></div>
        <div class="h-6 bg-navy-200 rounded w-3/5"></div>
        <div class="h-8 bg-navy-200 rounded w-full"></div>
        <div class="h-8 bg-navy-200 rounded w-full"></div>
        <div class="h-8 bg-navy-200 rounded w-4/6"></div>
      </div>
      <div class="w-80 h-56 bg-navy-200 rounded-xl shrink-0"></div>
    </div>

    <!-- FAQ Section -->
    <h2 class="text-2xl font-bold text-navy-900 text-center mb-8">FAQ</h2>
    <div class="grid grid-cols-2 gap-6 max-w-5xl mx-auto">
      <div
        v-for="(faq, i) in faqs"
        :key="i"
        class="border border-navy-200 rounded-xl p-6 bg-white cursor-pointer hover:shadow-md transition-shadow"
        @click="faq.open = !faq.open"
      >
        <div class="flex justify-between items-start">
          <p class="text-sm font-medium text-navy-700 pr-4">{{ faq.q }}</p>
          <i :class="faq.open ? 'pi pi-chevron-up' : 'pi pi-chevron-down'" class="text-navy-400 shrink-0"></i>
        </div>
        <p v-if="faq.open" class="text-sm text-navy-500 mt-3">{{ faq.a }}</p>
      </div>
    </div>
  </div>
</template>
