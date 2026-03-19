# 🛡️ KawalMBG (Monorepo)

**KawalMBG** adalah aplikasi _Monitoring Program Makan Bergizi Gratis (MBG)_. Aplikasi ini dirancang dengan dua _role_ utama: **Regulator** (untuk mengawasi, menerima alert, dan melihat performa) dan **Vendor** (untuk input data distribusi dan manajemen dokumen izin). 

Proyek ini telah dikonversi dari _single repository_ menjadi **Monorepo** fungsional penuh, yang terdiri dari:
1. **Frontend (`app/`)**: Aplikasi SPA berbasis Vue 3, Vite, dan Tailwind CSS.
2. **Backend (`backend/`)**: Aplikasi REST API performa tinggi berbasis Python FastAPI.
3. **Database**: PostgreSQL (Neon Serverless DB) via SQLAlchemy ORM.

---

## 🚀 Fitur Utama

- **Public Dashboard**: Pencarian vendor, melihat trust score _(Skor Kepercayaan)_, dan detail analisis nutrisi.
- **Regulator Portal**:
  - Peta risiko distribusi & analitik performa vendor.
  - Notifikasi / peringatan dini ancaman (contoh: risiko fraud atau bahaya mikrobiologi/suhu).
  - _Generate_ laporan.
- **Vendor Portal**:
  - _Real-time_ input distribusi berdasar kondisi aktual (suhu dan durasi).
  - Integrasi cek risiko dari AI saat pelaporan distribusi.
  - Manajemen masa kedaluwarsa dokumen sertifikasi dapur/halal.
- **Database Driven Auth**: Akses sistem tersimpan persisten dalam database, dilindungi dengan _password hashing_ (bcrypt).

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
- **Database Stack:** [Neon DB](https://neon.tech/) (PostgreSQL) + `psycopg2-binary`
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

# Menjalankan Database Seeder (Hanya 1x untuk inisialisasi tabel Neon DB)
# Pastikan Anda sudah mengisi DATABASE_URL= di file backend/.env
python seed.py

# Jalankan server
python -m uvicorn main:app --reload
```
API akan berjalan di `http://127.0.0.1:8000`.

### 2. Menjalankan Frontend (Vue)

Buka terminal **baru**, lalu masuk ke folder `app/`:

```bash
cd app

# Install dependensi Node (jika belum)
npm install

# Jalankan server vite
npm run dev
```
Aplikasi frontend akan menyala di alamat [http://localhost:5173](http://localhost:5173). Seluruh panggilan `/api` secara otomatis akan di-proxy oleh Vite menuju `http://localhost:8000`.

---

## 🔑 Panduan Login (Seeded Credentials)

Jika Anda sudah menjalankan `python seed.py`, database default sudah mengandung dua jenis akun untuk pengetesan:

- Akses sebagai **Regulator**: 
  - Email: `regulator@garda.id`
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
│   ├── vite.config.ts      # Konfigurasi bundler + API Proxy
│   └── package.json        
├── backend/                # Backend Python FastAPI
│   ├── .env                # Kredensial Database Neon
│   ├── auth_utils.py       # Logika hash & verifikasi password
│   ├── database.py         # SQLAlchemy engine setup
│   ├── main.py             # Endpoint API & Routing
│   ├── models.py           # Definisi tabel PostgreSQL
│   ├── requirements.txt    # Daftar dependensi PIP
│   └── seed.py             # Script inisiasi & dummy data
├── README.md               # Dokumentasi Root Monorepo
└── .gitignore              # Global git ignores (Node, Python, .env)
```

---

_Dikembangkan untuk Prototype Pengawasan Program MBG_
