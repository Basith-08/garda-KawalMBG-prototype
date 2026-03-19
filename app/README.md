# 🛡️ KawalMBG Prototype

**KawalMBG** adalah purwarupa (prototype) aplikasi _Monitoring Program Makan Bergizi Gratis (MBG)_. Aplikasi ini dirancang dengan dua _role_ utama: **Regulator** (untuk mengawasi, menerima alert, dan melihat performa) dan **Vendor** (untuk input data distribusi dan manajemen dokumen izin). 

Seluruh penyajian data saat ini di-mock menggunakan `localStorage` agar dapat berjalan mandiri (standalone) tanpa memerlukan setup database atau backend tambahan.

---

## 🚀 Fitur Utama

- **Public Dashboard**: Pencarian vendor, melihat trust score _(Skor Kepercayaan)_, dan detail analisis nutrisi per sekolah.
- **Regulator Portal**:
  - Peta risiko distribusi & analitik performa vendor.
  - Notifikasi / peringatan dini ancaman (contoh: risiko fraud atau bahaya mikrobiologi/suhu).
  - _Generate_ laporan.
- **Vendor Portal**:
  - _Real-time_ input distribusi berdasar kondisi aktual (suhu dan durasi).
  - Integrasi cek risiko dari AI saat pelaporan distribusi.
  - Manajemen masa kedaluwarsa dokumen sertifikasi dapur/halal.
- **Role-based Authentication**: Akses halaman berdasarkan role yang dipilih ketika Sign-In (Regulator / Vendor).

---

## 🛠️ Tech Stack

Aplikasi prototype ini dikembangkan menggunakan teknologi modern _frontend_:
- **Framework:** [Vue 3](https://vuejs.org/) + [TypeScript](https://www.typescriptlang.org/)
- **Build Tool:** [Vite](https://vitejs.dev/)
- **UI & Styling:** 
  - [TailwindCSS v4](https://tailwindcss.com/) (Custom Design Tokens)
  - [PrimeVue](https://primevue.org/) (Preset Aura) + PrimeIcons
  - [clsx](https://github.com/lukeed/clsx) & [tailwind-merge](https://github.com/dcastil/tailwind-merge) untuk manajemen class.
- **State Management:** [Pinia](https://pinia.vuejs.org/)
- **Routing:** [Vue Router 4](https://router.vuejs.org/)
- **Form Validation:** [Zod](https://zod.dev/)
- **Testing:** [Vitest](https://vitest.dev/) & Vue Test Utils

---

## 💻 Cara Menjalankan Aplikasi

Karena menggunakan `localStorage` API, Anda tidak perlu repot setup environment khusus selain Node.js.

### 1. Prerequisites
Pastikan **Node.js** (rekomendasi versi: 18+ atau 20+) sudah ter-install di sistem Anda.

### 2. Instalasi Dependensi
Jalankan perintah berikut di dalam direktori `app/`:

```bash
npm install
```

### 3. Menjalankan Development Server
```bash
npm run dev
```

Server akan nyala di alamat [http://localhost:5173](http://localhost:5173).

---

## 🔑 Panduan Login (Test Credentials)

Aplikasi akan membagi akses otomatis berdasarkan kata kunci dari **email** yang diketik tanpa mempedulikan _password_-nya:

- Akses sebagai **Regulator**: 
  - Gunakan email yang mengandung kata `regulator`, misalnya `regulator@example.com`
- Akses sebagai **Vendor**: 
  - Gunakan email yang mengandung kata `vendor`, misalnya `vendor@example.com`
- Password: Boleh diisi bebas (misal: `123123`)

*(Data awal / mock data akan tersimpan secara otomatis di localStorage saat aplikasi pertama kali di-load.)*

---

## 🧪 Testing

Untuk menjalankan suite testing menggunakan Vitest:

```bash
# Menjalankan unit test reguler
npm run test:unit
```

---

## 📂 Struktur Direktori

```text
app/
├── public/                 # Static assets (favicon, dll)
├── src/
│   ├── assets/             # Gambar & ikon
│   ├── components/         # Reusable Vue components 
│   ├── layouts/            # Template layout (PublicLayout, DashboardLayout)
│   ├── router/             # Definisi route & navigasi
│   ├── services/           # Logika data handling (ex: Mock via localStorage)
│   ├── stores/             # Global states (Pinia)
│   ├── views/              # Halaman / page utuh (Regulator, Vendor, Public, Auth)
│   ├── App.vue             # Root component
│   ├── main.ts             # Entry point
│   └── style.css           # Global style & konfig warna Tailwind
├── index.html              # HTML template
├── package.json            # Daftar dependensi & script runner
├── tsconfig.json           # Konfigurasi typescript
└── vite.config.ts          # Konfigurasi bundler Vite + plugin
```

---

_Dikembangkan oleh [Basith-08]_
