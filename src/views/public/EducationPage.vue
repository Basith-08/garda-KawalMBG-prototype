<script setup lang="ts">
import { ref } from 'vue'

const articles = ref([
  {
    title: 'Panduan Standar Higiene Dapur 2026',
    desc: 'Pelajari standar wajib BGN untuk mencegah kontaminasi silang dan menjaga suhu aman makanan sebelum didistribusikan.',
    date: '10 Feb 2026',
    readTime: '4 Min Read',
    img: 'https://images.unsplash.com/photo-1577219491135-ce391730fb2c?auto=format&fit=crop&q=80&w=400&h=250'
  },
  {
    title: 'Memahami Cara Kerja AI Risk Engine',
    desc: 'Penjelasan detail bagaimana korelasi suhu lingkungan dan durasi rute memengaruhi kalkulasi tingkat risiko bakteri Salmonella.',
    date: '15 Jan 2026',
    readTime: '6 Min Read',
    img: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&q=80&w=400&h=250'
  },
  {
    title: 'Prosedur Banding Status "Fraud Alert"',
    desc: 'Langkah resmi mengajukan validasi klaim jumlah porsi jika terdapat selisih laporan penerimaan foto dari pihak guru di sekolah.',
    date: '02 Mar 2026',
    readTime: '5 Min Read',
    img: 'https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&q=80&w=400&h=250'
  }
])

const faqs = ref([
  { q: 'Apa itu platform KawalMBG?', a: 'KawalMBG adalah purwarupa sistem monitoring digital distribusi Program Makan Bergizi Gratis (MBG) berbasis AI untuk transparansi pangan dan uang negara secara real-time.', open: false },
  { q: 'Mengapa vendor perlu "Input Distribusi"?', a: 'Input ini memastikan seluruh jadwal logistik masuk ke dalam radar pengawasan AI Risk Engine, sehingga risiko basi atau keracunan dapat dicegah sedini mungkin.', open: false },
  { q: 'Siapa yang memvalidasi data penerimaan sekolah?', a: 'Pihak sekolah (Guru/Kepala Sekolah) memiliki aplikasi terpisah untuk memfoto makanan yang tiba. AI akan membandingkan foto vendor vs foto guru untuk mencegah fraud.', open: false },
  { q: 'Saya menemukan keganjilan data, lapor kemana?', a: 'Anda dapat langsung menekan tombol "Hubungi CS KawalMBG" yang tersedia di halaman ini, atau menghubungi saluran Call Center resmi BGN di 1-500-xxx.', open: false },
])
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 md:px-8 py-6 md:py-8 animate-fade-in">
    <!-- Header -->
    <div class="text-center mb-10 md:mb-14">
      <div class="flex flex-col md:flex-row items-center justify-center gap-4 md:gap-6 mb-4">
        <div class="w-16 h-16 bg-blue-100 rounded-xl flex items-center justify-center shrink-0">
          <i class="pi pi-book text-3xl text-brand-accent"></i>
        </div>
        <div>
          <h1 class="text-3xl md:text-4xl font-bold text-navy-900 leading-tight">Pusat Edukasi & Bantuan</h1>
          <p class="text-navy-500 mt-2 max-w-2xl mx-auto">Kami berdedikasi menjaga kualitas dan transparansi setiap porsi gizi anak bangsa. Temukan panduan operasional wajib dan tanya-jawab di sini.</p>
        </div>
      </div>
    </div>

    <!-- Articles Section -->
    <div class="mb-14">
      <div class="flex justify-between items-end mb-6">
        <h2 class="text-2xl font-bold text-navy-900">Artikel & Panduan Wajib</h2>
        <a href="#" class="hidden md:inline-block text-brand-accent font-semibold hover:underline">Lihat Semua Panduan <i class="pi pi-arrow-right text-sm ml-1"></i></a>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <article 
          v-for="article in articles" 
          :key="article.title"
          class="bg-white rounded-2xl border border-navy-200 overflow-hidden shadow-sm hover:shadow-lg transition-all duration-300 group cursor-pointer"
        >
          <div class="h-48 overflow-hidden relative">
            <img :src="article.img" :alt="article.title" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
            <div class="absolute top-4 left-4 bg-white/90 backdrop-blur-sm px-3 py-1 rounded-full text-xs font-bold text-navy-900">
              Dokumen Resmi
            </div>
          </div>
          <div class="p-6">
            <div class="flex items-center gap-3 text-xs text-navy-500 font-medium mb-3">
              <span>{{ article.date }}</span>
              <span class="w-1 h-1 bg-navy-300 rounded-full"></span>
              <span><i class="pi pi-clock mr-1 text-xs"></i>{{ article.readTime }}</span>
            </div>
            <h3 class="text-lg font-bold text-navy-900 mb-2 leading-snug group-hover:text-brand-accent transition-colors">{{ article.title }}</h3>
            <p class="text-sm text-navy-600 line-clamp-3 leading-relaxed">{{ article.desc }}</p>
          </div>
        </article>
      </div>
    </div>

    <!-- Two-Column Layout for FAQ & Support -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 md:gap-12">
      <!-- FAQ Section -->
      <div class="lg:col-span-2">
        <h2 class="text-2xl font-bold text-navy-900 mb-6">Pertanyaan Populer (FAQ)</h2>
        <div class="grid grid-cols-1 gap-4">
          <div
            v-for="(faq, i) in faqs"
            :key="i"
            class="border border-navy-200 rounded-xl p-6 bg-white cursor-pointer hover:border-brand-accent hover:shadow-sm transition-all"
            @click="faq.open = !faq.open"
          >
            <div class="flex justify-between items-center gap-4">
              <h4 class="text-base font-bold text-navy-800">{{ faq.q }}</h4>
              <div 
                class="w-8 h-8 rounded-full flex items-center justify-center shrink-0 transition-colors"
                :class="faq.open ? 'bg-brand-accent text-white' : 'bg-navy-100 text-navy-500'"
              >
                <i :class="faq.open ? 'pi pi-minus' : 'pi pi-plus'" class="text-xs transition-transform duration-300" :style="faq.open ? 'transform: rotate(180deg)' : ''"></i>
              </div>
            </div>
            <!-- FAQ Answer with smooth open -->
            <div class="overflow-hidden transition-all duration-300" :style="faq.open ? 'max-height: 200px; opacity: 1; margin-top: 1rem;' : 'max-height: 0px; opacity: 0;'">
              <p class="text-sm text-navy-600 leading-relaxed">{{ faq.a }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Live Support Section -->
      <div class="lg:col-span-1">
        <div class="bg-navy-900 rounded-2xl p-8 text-white sticky top-24 shadow-xl">
          <div class="w-14 h-14 bg-brand-accent/20 rounded-2xl flex items-center justify-center mb-6 border border-brand-accent/30">
            <i class="pi pi-headphones text-2xl text-brand-accent"></i>
          </div>
          <h3 class="text-2xl font-bold mb-3">Butuh Bantuan Langsung?</h3>
          <p class="text-navy-300 text-sm leading-relaxed mb-8">Tim Satgas KawalMBG siap membantu Anda mendampingi proses monitoring, audit sistem, dan validasi data distribusi.</p>
          
          <div class="space-y-4">
            <a href="mailto:support@kawalmbg.go.id" class="flex items-center gap-4 p-4 bg-navy-800 rounded-xl hover:bg-navy-700 transition-colors border border-navy-700 hover:border-navy-600">
              <i class="pi pi-envelope text-brand-accent text-xl"></i>
              <div>
                <div class="text-xs text-navy-400 mb-0.5">Email Dukungan</div>
                <div class="text-sm font-semibold">support@kawalmbg.go.id</div>
              </div>
            </a>
            <a href="https://wa.me/628111222333" target="_blank" class="flex items-center gap-4 p-4 bg-brand-success text-white rounded-xl hover:bg-green-600 transition-colors shadow-lg shadow-green-900/20">
              <i class="pi pi-whatsapp text-2xl"></i>
              <div>
                <div class="text-xs text-green-100 mb-0.5">WhatsApp Triage 24/7</div>
                <div class="text-sm font-bold">Hubungi CS KawalMBG</div>
              </div>
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
