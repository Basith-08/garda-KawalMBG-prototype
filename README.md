# 🛡️ KawalMBG (Monorepo)

**KawalMBG** adalah aplikasi _Monitoring Program Makan Bergizi Gratis (MBG)_. Aplikasi ini dirancang dengan dua _role_ utama: **Regulator** (untuk mengawasi, menerima alert, dan melihat performa) dan **Vendor** (untuk input data distribusi dan manajemen dokumen izin). 
Saat ini platform juga memiliki **Super Admin** untuk governance data, pengawasan akun, dan kontrol arsitektur operasional sistem.

Proyek ini telah dikonversi dari _single repository_ menjadi **Monorepo** fungsional penuh, yang terdiri dari:
1. **Frontend (`app/`)**: Aplikasi SPA berbasis Vue 3, Vite, dan Tailwind CSS.
2. **Backend (`backend/`)**: Aplikasi REST API performa tinggi berbasis Python FastAPI.
3. **Database**: PostgreSQL lokal dari Supabase Local via SQLAlchemy ORM.

---

## 🚀 Fitur Utama

- **Public Dashboard**: Pencarian vendor, melihat trust score _(Skor Kepercayaan)_, dan detail analisis nutrisi.
- **Regulator Portal**:
  - Peta risiko distribusi & analitik performa vendor.
  - Notifikasi / peringatan dini ancaman (contoh: risiko fraud atau bahaya mikrobiologi/suhu).
  - _Generate_ laporan.
- **Super Admin Control Center**:
  - Snapshot kesehatan platform, kualitas relasi data, dan kepatuhan akun.
  - Monitoring user access, vendor yang butuh intervensi, dokumen mendekati jatuh tempo, dan pengelolaan role/aktivasi user.
- **Vendor Portal**:
  - _Real-time_ input distribusi berdasar kondisi aktual (suhu dan durasi).
  - Integrasi cek risiko dari AI saat pelaporan distribusi.
  - Manajemen masa kedaluwarsa dokumen sertifikasi dapur/halal.
- **Database Driven Auth**: Akses sistem tersimpan persisten dalam database, dilindungi dengan _password hashing_ (bcrypt).
- **Governed Local Schema**: Migrasi versioned ringan untuk perubahan relasi user/vendor, governance fields, dan foreign key vendor lintas tabel.

---

## 🛠️ Tech Stack

### Frontend (`app/`)
- **Framework:** [Vue 3](https://vuejs.org/) + [TypeScript](https://www.typescriptlang.org/)
- **Build Tool:** [Vite](https://vitejs.dev/)
- **State Management:** [Pinia](https://pinia.vuejs.org/)
- **UI & Styling:** TailwindCSS v4 + PrimeVue + PrimeIcons
- **API Client:** Axios

### Backend (`backend/`)
- **Web Framework:** [FastAPI](https://fastapi.tiangolo.com/) + Uvicorn
- **Database ORM:** [SQLAlchemy](https://www.sqlalchemy.org/)
- **Database Stack:** [Supabase Local](https://supabase.com/docs/guides/local-development) (PostgreSQL) + `psycopg2-binary`
- **Security:** `passlib` (bcrypt)

---

## 💻 Cara Menjalankan Aplikasi

Anda perlu menjalankan kedua *service* (Backend & Frontend) secara bersamaan di terminal terpisah.

### 1. Menjalankan Backend (FastAPI)

Pastikan Anda memiliki Python 3, lalu masuk ke folder `backend/`:

```bash
cd backend

# Buat virtual environment (jika belum ada)
python -m venv venv

# Aktivasi virtual environment
source venv/bin/activate

# Install dependensi
pip install -r requirements.txt

# Optional: jalankan migrasi schema manual
python migrations.py

# Jalankan server
python -m uvicorn main:app --reload
```
API akan berjalan di `http://127.0.0.1:8000`.

Backend sekarang akan:
- membuat tabel otomatis saat startup,
- menjalankan migrasi database versioned saat startup,
- mengisi seed data otomatis jika database masih kosong,
- menyediakan health endpoint di `http://127.0.0.1:8000/api/health`.
- membatasi CORS sesuai `CORS_ALLOW_ORIGINS` dan memakai secret token dari env.

### 1a. Menjalankan Database Supabase Local

Sebelum backend dijalankan, pastikan PostgreSQL lokal Supabase aktif.

Default koneksi backend sekarang adalah:

```bash
postgresql://postgres:postgres@127.0.0.1:54322/postgres
```

Itu adalah port database bawaan Supabase local. Jalankan Supabase local dari folder project Supabase Anda:

```bash
supabase start
```

Jika Anda memakai port atau password lain, ubah `DATABASE_URL` di `backend/.env`.

### 1b. Menjalankan Regression Check Backend

Untuk memverifikasi migrasi, auth, dan scope data vendor pada database lokal:

```bash
cd backend
source venv/bin/activate
python -m unittest tests.test_runtime_contracts
```

### 2. Menjalankan Frontend (Vue)

Buka terminal **baru**, lalu masuk ke folder `app/`:

```bash
cd app

# Install dependensi Node (jika belum)
npm install

# Optional: override backend target jika FastAPI tidak jalan di port 8000
cp .env.example .env

# Jalankan server vite
npm run dev
```
Aplikasi frontend akan menyala di alamat [http://localhost:5173](http://localhost:5173). Seluruh panggilan `/api` secara otomatis akan di-proxy oleh Vite menuju `http://localhost:8000`.
Jika backend berjalan di port lain, ubah `VITE_API_TARGET` di `app/.env`.
Pada environment lokal repo ini, port `8000` sering sudah dipakai service lain, jadi default frontend lokal diarahkan ke `http://127.0.0.1:8001` melalui `VITE_API_TARGET` dan `VITE_API_BASE_URL`.

---

## 🔑 Panduan Login

Saat backend pertama kali dijalankan pada database kosong, seed data default akan otomatis dibuat. Kredensial bawaan:

- Akses sebagai **Regulator**: 
  - Email: `regulator@garda.id`
  - Password: `password123`
- Akses sebagai **Super Admin**:
  - Email: `superadmin@garda.id`
  - Password: `password123`
- Akses sebagai **Vendor**: 
  - Email: `vendor@garda.id`
  - Password: `password123`

---

## 📂 Struktur Monorepo

```text
garda/
├── app/                    # Frontend Vue.js
│   ├── public/             
│   ├── src/
│   │   ├── services/       # Komunikasi Axios dengan backend (api.ts)
│   │   ├── stores/         # Global states (Pinia)
│   │   ├── views/          # Regulator, Vendor, Public, dan Auth pages
│   │   └── ...
│   ├── .env.example        # Override optional target backend
│   ├── vite.config.ts      # Konfigurasi bundler + API Proxy
│   └── package.json        
├── backend/                # Backend Python FastAPI
│   ├── .env                # Override koneksi database lokal
│   ├── .env.example        # Default koneksi Supabase local
│   ├── auth_utils.py       # Logika hash & verifikasi password
│   ├── database.py         # SQLAlchemy engine setup
│   ├── main.py             # Endpoint API & Routing
│   ├── migrations.py       # Migrasi schema versioned ringan
│   ├── models.py           # Definisi tabel PostgreSQL
│   ├── requirements.txt    # Daftar dependensi PIP
│   └── seed.py             # Script inisiasi & baseline data lokal
├── README.md               # Dokumentasi Root Monorepo
└── .gitignore              # Global git ignores (Node, Python, .env)
```

---

_Dikembangkan sebagai platform operational monitoring untuk distribusi MBG_
