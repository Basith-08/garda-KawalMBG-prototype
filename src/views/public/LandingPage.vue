<script setup lang="ts">
</script>

<template>
  <div class="animate-fade-in">
    <!-- Hero Section -->
    <section class="px-8 py-16 max-w-7xl mx-auto flex items-center gap-12">
      <div class="flex-1">
        <h1 class="text-5xl font-bold text-navy-900 leading-tight mb-6">
          Tekan Risiko Distribusi<br/>Makanan Sekolah
        </h1>
        <p class="text-navy-500 text-lg mb-8 max-w-md">
          Sistem monitoring distribusi Makanan Bergizi Gratis (MBG) berbasis AI untuk transparansi dan keamanan pangan nasional.
        </p>
        <router-link
          to="/vendor-score"
          class="inline-block bg-brand-accent hover:bg-brand-accent-hover text-white font-semibold px-8 py-3.5 rounded-lg transition-colors shadow-md hover:shadow-lg"
        >
          Cek Vendor Sekolah
        </router-link>
      </div>
      <div class="flex-1 flex justify-center">
        <svg width="280" height="280" viewBox="0 0 280 280" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M140 20L40 70v60c0 60 43 116 100 129 57-13 100-69 100-129V70L140 20z" stroke="#1e293b" stroke-width="12" fill="none"/>
          <path d="M140 50L60 90v50c0 50 36 96 80 107 44-11 80-57 80-107V90L140 50z" stroke="#1e293b" stroke-width="6" fill="none" opacity="0.3"/>
          <ellipse cx="140" cy="145" rx="50" ry="35" fill="none" stroke="#1e293b" stroke-width="8"/>
          <circle cx="140" cy="145" r="14" fill="#1e293b"/>
        </svg>
      </div>
    </section>

    <!-- Features Section -->
    <section class="px-8 py-16 bg-white">
      <div class="max-w-7xl mx-auto text-center mb-12">
        <h2 class="text-3xl font-bold text-navy-900 mb-3">Bagaimana Kami Menjaga Kualitas?</h2>
        <p class="text-navy-500">Teknologi KawalMBG bekerja 24/7 di balik layar.</p>
      </div>
      <div class="max-w-7xl mx-auto grid grid-cols-3 gap-8">
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
    </section>
  </div>
</template>
