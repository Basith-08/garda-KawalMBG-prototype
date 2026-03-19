<script setup lang="ts">
</script>

<template>
  <div class="animate-fade-in">
    <!-- Hero Section -->
    <section class="max-w-7xl mx-auto px-4 md:px-6 py-12 md:py-20 flex flex-col md:flex-row items-center justify-between gap-8 md:gap-12">
      <div class="w-full md:w-1/2 text-center md:text-left">
        <div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-brand-accent/10 text-brand-accent text-sm font-semibold mb-6">
          <i class="pi pi-shield-alt text-base"></i>
          <span>KawalMBG</span>
        </div>
        <h1 class="text-5xl font-bold text-navy-900 leading-tight mb-6">
          Tekan Risiko Distribusi<br/>Makanan Sekolah
        </h1>
        <p class="text-navy-500 text-lg mb-8 max-w-md">
          Sistem monitoring distribusi Makanan Bergizi Gratis (MBG) berbasis AI untuk transparansi dan keamanan pangan nasional.
        </p>
        <div class="flex flex-col sm:flex-row items-center justify-center md:justify-start gap-4">
          <router-link to="/login" class="px-8 py-3.5 bg-brand-accent hover:bg-brand-accent-hover text-white rounded-xl font-semibold transition-colors flex items-center gap-2 w-full sm:w-auto justify-center">
            Mulai Pantau <i class="pi pi-arrow-right text-sm"></i>
          </router-link>
          <router-link to="/vendor-score" class="px-8 py-3.5 bg-white text-navy-900 border border-navy-200 hover:border-navy-300 rounded-xl font-semibold transition-colors w-full sm:w-auto justify-center text-center">
            Cek Skor Vendor
          </router-link>
        </div>
      </div>
      <div class="w-full md:w-1/2 relative mt-8 md:mt-0 flex justify-center">
        <svg width="280" height="280" viewBox="0 0 280 280" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M140 20L40 70v60c0 60 43 116 100 129 57-13 100-69 100-129V70L140 20z" stroke="#1e293b" stroke-width="12" fill="none"/>
          <path d="M140 50L60 90v50c0 50 36 96 80 107 44-11 80-57 80-107V90L140 50z" stroke="#1e293b" stroke-width="6" fill="none" opacity="0.3"/>
          <ellipse cx="140" cy="145" rx="50" ry="35" fill="none" stroke="#1e293b" stroke-width="8"/>
          <circle cx="140" cy="145" r="14" fill="#1e293b"/>
        </svg>
      </div>
    </section>

    <!-- Features -->
    <section class="bg-white py-16 md:py-24">
      <div class="max-w-7xl mx-auto px-4 md:px-6">
        <div class="text-center max-w-2xl mx-auto mb-12 md:mb-16">
          <h2 class="text-3xl font-bold text-navy-900 mb-4">Mengapa KawalMBG?</h2>
          <p class="text-navy-600">Teknologi berbasis data untuk mencegah keracunan dan kecurangan secara real-time.</p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 md:gap-8">
        <div class="border border-navy-200 rounded-xl p-8 hover:shadow-lg transition-shadow">
          <h3 class="text-2xl font-bold text-navy-900 mb-4">Risk Scoring AI</h3>
          <p class="text-navy-500 leading-relaxed">Sistem menganalisis suhu cuaca real-time dari BMKG dan waktu masak vendor untuk memprediksi risiko makanan basi sebelum sampai ke sekolah.</p>
        </div>
        <div class="border border-navy-200 rounded-xl p-8 hover:shadow-lg transition-shadow">
          <h3 class="text-2xl font-bold text-navy-900 mb-4">Guru Verification</h3>
          <p class="text-navy-500 leading-relaxed">Hanya saat risiko tinggi terdeteksi, AI kami mengirimkan verifikasi singkat via Telegram ke guru di sekolah untuk memastikan kualitas porsi riil.</p>
        </div>
        <div class="border border-navy-200 rounded-xl p-8 hover:shadow-lg transition-shadow">
          <h3 class="text-2xl font-bold text-navy-900 mb-4">Fraud Detection</h3>
          <p class="text-navy-500 leading-relaxed">Hasil verifikasi dan audit AI dikonversi menjadi skor kepercayaan yang dapat diakses siapa saja sebagai bentuk pertanggungjawaban publik.</p>
        </div>
      </div>
      </div>
    </section>
  </div>
</template>
