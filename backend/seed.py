from database import SessionLocal, engine
import models
from auth_utils import get_password_hash

# Membuat tabel otomatis di Neon jika belum ada
models.Base.metadata.create_all(bind=engine)
from auth_utils import get_password_hash

mock_db_state = {
    "vendors": [
        { "id": "1", "name": "PT. Nutrisi Jaya", "status": "safe", "statusText": "No Issues", "trustScore": 94.0, "trend": 5.1, "trendDir": "up", "address": "Jl. Kencana 12, Jakarta Selatan", "joinDate": "2024-01-15", "schools": ["SDN 01 Pusat", "SDN 05 Barat", "SD Harapan"] },
        { "id": "2", "name": "CV. Makan Sehat Indonesia", "status": "medium", "statusText": "2x Late Delivery", "trustScore": 74.0, "trend": 1.0, "trendDir": "up", "address": "Jl. Merdeka 45, Tangerang Selatan", "joinDate": "2024-03-10", "schools": ["SDN 05 Barat", "SDN 12 Timur"] },
        { "id": "3", "name": "Katering Ibu Nusantara", "status": "high-risk", "statusText": "High Risk Incident", "trustScore": 45.0, "trend": 10.0, "trendDir": "down", "address": "Jl. Sudirman 88, Bogor Barat", "joinDate": "2024-06-01", "schools": ["SD Harapan"] },
        { "id": "4", "name": "CV. Katering Berkah Bersama", "status": "high-risk", "statusText": "High Risk Incident", "trustScore": 38.0, "trend": 15.0, "trendDir": "down", "address": "Jl. Gatot Subroto 10, Jakarta Pusat", "joinDate": "2024-02-20", "schools": ["SDN 01 Pusat", "SDN 22 Cempaka"] },
        { "id": "5", "name": "PT. Dapur Sehat Mandiri", "status": "medium", "statusText": "Pending Review", "trustScore": 62.0, "trend": 3.0, "trendDir": "down", "address": "Jl. Thamrin 22, Jakarta Pusat", "joinDate": "2023-11-01", "schools": ["SDN 05 Barat", "SD Harapan", "SDN 18 Utara"] },
        { "id": "6", "name": "PT. Nutrisi Abadi Sejahtera", "status": "safe", "statusText": "No Issues", "trustScore": 95.0, "trend": 2.0, "trendDir": "up", "address": "Jl. Asia Afrika 5, Bandung", "joinDate": "2023-09-15", "schools": ["SDN 01 Pusat", "SDN 05 Barat"] },
        { "id": "7", "name": "CV. Sajian Prima Utama", "status": "safe", "statusText": "No Issues", "trustScore": 91.0, "trend": 3.2, "trendDir": "up", "address": "Jl. Diponegoro 33, Semarang", "joinDate": "2023-08-01", "schools": ["SDN 07 Selatan", "SDN 14 Menteng"] },
        { "id": "8", "name": "PT. Gizi Cemerlang", "status": "safe", "statusText": "No Issues", "trustScore": 89.0, "trend": 1.8, "trendDir": "up", "address": "Jl. Pemuda 17, Surabaya", "joinDate": "2024-04-12", "schools": ["SD Al-Azhar", "SDN 18 Utara", "SDN 22 Cempaka"] },
        { "id": "9", "name": "Katering Sekolah Bahagia", "status": "medium", "statusText": "1x Porsi Kurang", "trustScore": 68.0, "trend": 2.5, "trendDir": "down", "address": "Jl. Veteran 8, Depok", "joinDate": "2024-05-20", "schools": ["SDN 12 Timur", "SD Bina Bangsa"] },
        { "id": "10", "name": "PT. Santap Nikmat Sejahtera", "status": "safe", "statusText": "No Issues", "trustScore": 92.0, "trend": 4.0, "trendDir": "up", "address": "Jl. Kartini 56, Bekasi Timur", "joinDate": "2023-07-10", "schools": ["SDN 07 Selatan", "MI Nurul Huda"] },
        { "id": "11", "name": "CV. Dapur Bunda Kreatif", "status": "medium", "statusText": "Dokumen Pending", "trustScore": 71.0, "trend": 0.5, "trendDir": "up", "address": "Jl. Raya Bogor Km 30, Jakarta Timur", "joinDate": "2024-07-01", "schools": ["SD Bina Bangsa", "SDN 14 Menteng"] },
        { "id": "12", "name": "PT. Makanan Bergizi Nusantara", "status": "high-risk", "statusText": "Fraud Detected", "trustScore": 32.0, "trend": 22.0, "trendDir": "down", "address": "Jl. Pahlawan 19, Tangerang", "joinDate": "2024-01-25", "schools": ["SDN 22 Cempaka"] },
        { "id": "13", "name": "CV. Rasa Ibu Sejati", "status": "safe", "statusText": "No Issues", "trustScore": 88.0, "trend": 2.1, "trendDir": "up", "address": "Jl. Cikini Raya 42, Jakarta Pusat", "joinDate": "2023-10-18", "schools": ["SDN 01 Pusat", "MI Nurul Huda", "SD Al-Azhar"] },
        { "id": "14", "name": "PT. Kuliner Anak Bangsa", "status": "medium", "statusText": "1x Telat Kirim", "trustScore": 76.0, "trend": 1.2, "trendDir": "down", "address": "Jl. Margonda Raya 100, Depok", "joinDate": "2024-08-15", "schools": ["SDN 18 Utara", "SDN 12 Timur"] },
        { "id": "15", "name": "Katering Cita Rasa Sekolah", "status": "safe", "statusText": "No Issues", "trustScore": 90.0, "trend": 3.5, "trendDir": "up", "address": "Jl. Dago 77, Bandung", "joinDate": "2023-06-05", "schools": ["SD Al-Azhar", "SDN 07 Selatan"] },
    ],
    "schools": [
        { "id": "1", "name": "SDN 01 Pusat", "npsn": "20101234", "address": "Jl. Kencana 12, Jakarta Selatan", "vendorId": "1", "vendorName": "PT. Nutrisi Jaya", "trustScore": 94.0, "status": "safe", "statusText": "No Issues" },
        { "id": "2", "name": "SDN 05 Barat", "npsn": "20105678", "address": "Jl. Mangga 5, Tangerang", "vendorId": "2", "vendorName": "CV. Makan Sehat Indonesia", "trustScore": 74.0, "status": "medium", "statusText": "2x Late Delivery" },
        { "id": "3", "name": "SD Harapan", "npsn": "20109012", "address": "Jl. Harapan 1, Bogor", "vendorId": "3", "vendorName": "Katering Ibu Nusantara", "trustScore": 45.0, "status": "high-risk", "statusText": "High Risk Incident" },
        { "id": "4", "name": "SDN 07 Selatan", "npsn": "20112345", "address": "Jl. Melati 9, Semarang", "vendorId": "7", "vendorName": "CV. Sajian Prima Utama", "trustScore": 91.0, "status": "safe", "statusText": "No Issues" },
        { "id": "5", "name": "SDN 12 Timur", "npsn": "20113456", "address": "Jl. Anggrek 14, Depok", "vendorId": "9", "vendorName": "Katering Sekolah Bahagia", "trustScore": 68.0, "status": "medium", "statusText": "1x Porsi Kurang" },
        { "id": "6", "name": "SDN 14 Menteng", "npsn": "20114567", "address": "Jl. Menteng Raya 21, Jakarta Pusat", "vendorId": "7", "vendorName": "CV. Sajian Prima Utama", "trustScore": 91.0, "status": "safe", "statusText": "No Issues" },
        { "id": "7", "name": "SDN 18 Utara", "npsn": "20118901", "address": "Jl. Sunter Agung 8, Jakarta Utara", "vendorId": "8", "vendorName": "PT. Gizi Cemerlang", "trustScore": 89.0, "status": "safe", "statusText": "No Issues" },
        { "id": "8", "name": "SDN 22 Cempaka", "npsn": "20122345", "address": "Jl. Cempaka Putih 3, Jakarta Pusat", "vendorId": "4", "vendorName": "CV. Katering Berkah Bersama", "trustScore": 38.0, "status": "high-risk", "statusText": "High Risk Incident" },
        { "id": "9", "name": "SD Al-Azhar", "npsn": "20130001", "address": "Jl. Sisingamangaraja 15, Jakarta Selatan", "vendorId": "8", "vendorName": "PT. Gizi Cemerlang", "trustScore": 89.0, "status": "safe", "statusText": "No Issues" },
        { "id": "10", "name": "SD Bina Bangsa", "npsn": "20130002", "address": "Jl. Raya Pajajaran 44, Bogor", "vendorId": "9", "vendorName": "Katering Sekolah Bahagia", "trustScore": 68.0, "status": "medium", "statusText": "1x Porsi Kurang" },
        { "id": "11", "name": "MI Nurul Huda", "npsn": "20130003", "address": "Jl. KH. Mas Mansyur 11, Bekasi", "vendorId": "10", "vendorName": "PT. Santap Nikmat Sejahtera", "trustScore": 92.0, "status": "safe", "statusText": "No Issues" },
        { "id": "12", "name": "SD Muhammadiyah 4", "npsn": "20130004", "address": "Jl. Kramat Jati 26, Jakarta Timur", "vendorId": "13", "vendorName": "CV. Rasa Ibu Sejati", "trustScore": 88.0, "status": "safe", "statusText": "No Issues" },
    ],
    "distributions": [
        { "id": "1", "vendorId": "1", "schoolName": "SDN 01 Pusat", "porsi": 450, "status": "safe", "statusText": "Safe", "time": "19 Mar 2026", "riskScore": 94.0, "menuName": "Nasi Kuning Special", "menuUtama": "Nasi kuning, Ayam bakar, Lalapan, Sambal", "suhu": 24.0, "durasi": 35, "levelRisiko": "LOW RISK", "catatan": "Sistem memvalidasi bahwa waktu paparan bakteri sangat rendah karena suhu udara optimal dan durasi pengiriman cepat." },
        { "id": "2", "vendorId": "1", "schoolName": "SDN 05 Barat", "porsi": 380, "status": "medium", "statusText": "Medium", "time": "19 Mar 2026", "riskScore": 74.0, "menuName": "Nasi Goreng Spesial", "menuUtama": "Nasi goreng, Telur dadar, Sayur asem", "suhu": 30.0, "durasi": 55, "levelRisiko": "MEDIUM", "catatan": "Suhu agak tinggi, perlu perhatian pada ventilasi kendaraan pengiriman." },
        { "id": "3", "vendorId": "1", "schoolName": "SD Harapan", "porsi": 320, "status": "high-risk", "statusText": "High Risk", "time": "19 Mar 2026", "riskScore": 45.0, "menuName": "Nasi Padang Lengkap", "menuUtama": "Nasi, Rendang, Gulai nangka, Daun singkong", "suhu": 34.0, "durasi": 120, "levelRisiko": "HIGH RISK", "catatan": "Waktu tempuh terlalu lama dan suhu lingkungan tinggi. Menu santan rentan kontaminasi bakteri." },
        { "id": "4", "vendorId": "2", "schoolName": "SDN 05 Barat", "porsi": 400, "status": "safe", "statusText": "Safe", "time": "19 Mar 2026", "riskScore": 88.0, "menuName": "Ayam Teriyaki", "menuUtama": "Nasi putih, Ayam teriyaki, Tumis kangkung", "suhu": 26.0, "durasi": 30, "levelRisiko": "LOW RISK", "catatan": "Pengiriman tepat waktu. Suhu lingkungan optimal untuk keamanan pangan." },
        { "id": "5", "vendorId": "2", "schoolName": "SDN 12 Timur", "porsi": 350, "status": "medium", "statusText": "Medium", "time": "18 Mar 2026", "riskScore": 71.0, "menuName": "Soto Ayam", "menuUtama": "Soto ayam, Nasi putih, Perkedel, Kerupuk", "suhu": 29.0, "durasi": 50, "levelRisiko": "MEDIUM", "catatan": "Durasi pengiriman mendekati batas. Soto kuah panas perlu perhatian suhu." },
        { "id": "6", "vendorId": "3", "schoolName": "SD Harapan", "porsi": 280, "status": "high-risk", "statusText": "High Risk", "time": "19 Mar 2026", "riskScore": 35.0, "menuName": "Nasi Uduk Betawi", "menuUtama": "Nasi uduk, Semur jengkol, Tempe orek", "suhu": 33.0, "durasi": 95, "levelRisiko": "HIGH RISK", "catatan": "Vendor terlambat memasak. Waktu pengiriman melebihi batas aman signifikan." },
        { "id": "7", "vendorId": "4", "schoolName": "SDN 01 Pusat", "porsi": 500, "status": "high-risk", "statusText": "High Risk", "time": "18 Mar 2026", "riskScore": 38.0, "menuName": "Nasi Liwet", "menuUtama": "Nasi liwet, Ikan teri, Labu siam, Sambal", "suhu": 35.0, "durasi": 140, "levelRisiko": "HIGH RISK", "catatan": "Anomali jumlah porsi terdeteksi. Selisih 120 porsi antara klaim vendor dan laporan guru di lapangan." },
        { "id": "8", "vendorId": "4", "schoolName": "SDN 22 Cempaka", "porsi": 420, "status": "high-risk", "statusText": "Fraud Alert", "time": "17 Mar 2026", "riskScore": 28.0, "menuName": "Nasi Tim Ayam", "menuUtama": "Nasi tim, Ayam suwir, Sayur bening", "suhu": 32.0, "durasi": 110, "levelRisiko": "HIGH RISK", "catatan": "Fraud terdeteksi. Foto produksi tidak sesuai dengan foto penerimaan sekolah. Porsi terlihat lebih kecil dari standar." },
        { "id": "9", "vendorId": "5", "schoolName": "SDN 18 Utara", "porsi": 360, "status": "medium", "statusText": "Medium", "time": "19 Mar 2026", "riskScore": 65.0, "menuName": "Mie Goreng Jawa", "menuUtama": "Mie goreng, Telur ceplok, Kerupuk, Acar", "suhu": 28.0, "durasi": 45, "levelRisiko": "MEDIUM", "catatan": "Dokumen vendor masih dalam proses review. Distribusi diizinkan sementara." },
        { "id": "10", "vendorId": "6", "schoolName": "SDN 01 Pusat", "porsi": 450, "status": "safe", "statusText": "Safe", "time": "18 Mar 2026", "riskScore": 96.0, "menuName": "Nasi Bakar Ikan", "menuUtama": "Nasi bakar, Ikan bakar, Sambal matah, Lalapan", "suhu": 25.0, "durasi": 28, "levelRisiko": "LOW RISK", "catatan": "Kualitas sangat baik. Vendor memiliki track record konsisten selama 6 bulan terakhir." },
        { "id": "11", "vendorId": "6", "schoolName": "SDN 05 Barat", "porsi": 400, "status": "safe", "statusText": "Safe", "time": "17 Mar 2026", "riskScore": 93.0, "menuName": "Ayam Penyet", "menuUtama": "Nasi putih, Ayam penyet, Sambal ulek, Lalapan", "suhu": 26.0, "durasi": 32, "levelRisiko": "LOW RISK", "catatan": "Distribusi lancar. Guru memberikan konfirmasi positif atas kualitas dan kuantitas." },
        { "id": "12", "vendorId": "7", "schoolName": "SDN 07 Selatan", "porsi": 300, "status": "safe", "statusText": "Safe", "time": "19 Mar 2026", "riskScore": 91.0, "menuName": "Nasi Pecel", "menuUtama": "Nasi, Pecel sayur, Tempe goreng, Rempeyek", "suhu": 27.0, "durasi": 25, "levelRisiko": "LOW RISK", "catatan": "Pengiriman sangat cepat. Kualitas terjaga dengan baik." },
        { "id": "13", "vendorId": "7", "schoolName": "SDN 14 Menteng", "porsi": 280, "status": "safe", "statusText": "Safe", "time": "18 Mar 2026", "riskScore": 90.0, "menuName": "Lontong Sayur", "menuUtama": "Lontong, Sayur labu, Telur balado", "suhu": 26.0, "durasi": 30, "levelRisiko": "LOW RISK", "catatan": "Semua parameter dalam batas aman. Vendor termasuk top performer." },
        { "id": "14", "vendorId": "8", "schoolName": "SD Al-Azhar", "porsi": 520, "status": "safe", "statusText": "Safe", "time": "19 Mar 2026", "riskScore": 89.0, "menuName": "Nasi Kebuli Kambing", "menuUtama": "Nasi kebuli, Kambing guling, Acar, Sambal", "suhu": 27.0, "durasi": 38, "levelRisiko": "LOW RISK", "catatan": "Menu premium. Kualitas bahan baku terverifikasi A oleh tim lapangan." },
        { "id": "15", "vendorId": "8", "schoolName": "SDN 18 Utara", "porsi": 380, "status": "safe", "statusText": "Safe", "time": "18 Mar 2026", "riskScore": 87.0, "menuName": "Rawon Surabaya", "menuUtama": "Rawon daging, Nasi putih, Telur asin, Kerupuk", "suhu": 28.0, "durasi": 42, "levelRisiko": "LOW RISK", "catatan": "Distribusi berjalan lancar. Menu diterima baik oleh siswa." },
        { "id": "16", "vendorId": "9", "schoolName": "SDN 12 Timur", "porsi": 310, "status": "medium", "statusText": "Medium", "time": "19 Mar 2026", "riskScore": 66.0, "menuName": "Nasi Campur Bali", "menuUtama": "Nasi campur, Ayam suwir, Sate lilit, Sayur urap", "suhu": 31.0, "durasi": 60, "levelRisiko": "MEDIUM", "catatan": "Porsi sedikit di bawah standar. Telah diberikan peringatan pertama ke vendor." },
        { "id": "17", "vendorId": "9", "schoolName": "SD Bina Bangsa", "porsi": 290, "status": "medium", "statusText": "Medium", "time": "18 Mar 2026", "riskScore": 64.0, "menuName": "Capcay Goreng", "menuUtama": "Nasi putih, Capcay goreng, Bakso, Kerupuk", "suhu": 29.0, "durasi": 48, "levelRisiko": "MEDIUM", "catatan": "Kualitas bahan baku grade B. Perlu peningkatan standar sayuran." },
        { "id": "18", "vendorId": "10", "schoolName": "MI Nurul Huda", "porsi": 340, "status": "safe", "statusText": "Safe", "time": "19 Mar 2026", "riskScore": 92.0, "menuName": "Nasi Gudeg Jogja", "menuUtama": "Gudeg, Nasi putih, Ayam opor, Krecek", "suhu": 25.0, "durasi": 30, "levelRisiko": "LOW RISK", "catatan": "Kualitas premium. Vendor menyediakan kemasan terbaik untuk menjaga suhu." },
        { "id": "19", "vendorId": "11", "schoolName": "SD Bina Bangsa", "porsi": 270, "status": "medium", "statusText": "Medium", "time": "19 Mar 2026", "riskScore": 70.0, "menuName": "Nasi Timbel Sunda", "menuUtama": "Nasi timbel, Ayam goreng, Lalap, Sambal terasi", "suhu": 30.0, "durasi": 52, "levelRisiko": "MEDIUM", "catatan": "Dokumen izin dalam proses perpanjangan. Distribusi berjalan kondisional." },
        { "id": "20", "vendorId": "12", "schoolName": "SDN 22 Cempaka", "porsi": 400, "status": "high-risk", "statusText": "Fraud Alert", "time": "18 Mar 2026", "riskScore": 25.0, "menuName": "Nasi Ayam Geprek", "menuUtama": "Nasi, Ayam geprek, Sambal, Sayur asem", "suhu": 34.0, "durasi": 130, "levelRisiko": "HIGH RISK", "catatan": "Fraud confirmed: 200 porsi tidak sampai ke sekolah. Klaim vendor tidak sesuai realitas lapangan." },
        { "id": "21", "vendorId": "13", "schoolName": "SDN 01 Pusat", "porsi": 430, "status": "safe", "statusText": "Safe", "time": "19 Mar 2026", "riskScore": 88.0, "menuName": "Nasi Sarden Pedas", "menuUtama": "Nasi putih, Sarden pedas, Tempe orek, Sayur bayam", "suhu": 26.0, "durasi": 33, "levelRisiko": "LOW RISK", "catatan": "Distribusi lancar. Bahan baku segar terverifikasi." },
        { "id": "22", "vendorId": "14", "schoolName": "SDN 18 Utara", "porsi": 350, "status": "medium", "statusText": "Medium", "time": "18 Mar 2026", "riskScore": 72.0, "menuName": "Bakso Kuah", "menuUtama": "Bakso kuah, Mie, Tahu, Siomay", "suhu": 29.0, "durasi": 46, "levelRisiko": "MEDIUM", "catatan": "Pengiriman sedikit terlambat 15 menit dari jadwal." },
        { "id": "23", "vendorId": "15", "schoolName": "SD Al-Azhar", "porsi": 480, "status": "safe", "statusText": "Safe", "time": "19 Mar 2026", "riskScore": 90.0, "menuName": "Nasi Bakmoy", "menuUtama": "Nasi putih, Bakmoy ayam, Pangsit goreng", "suhu": 25.0, "durasi": 28, "levelRisiko": "LOW RISK", "catatan": "Vendor konsisten dalam kualitas dan ketepatan waktu selama 3 bulan terakhir." },
        { "id": "24", "vendorId": "15", "schoolName": "SDN 07 Selatan", "porsi": 310, "status": "safe", "statusText": "Safe", "time": "17 Mar 2026", "riskScore": 91.0, "menuName": "Nasi Opor Ayam", "menuUtama": "Nasi putih, Opor ayam, Perkedel, Timun", "suhu": 26.0, "durasi": 32, "levelRisiko": "LOW RISK", "catatan": "Semua parameter dalam batas aman. Konfirmasi guru positif." },
    ],
    "alerts": [
        { "id": "1", "type": "CRITICAL", "vendorName": "CV. Katering Berkah Bersama", "description": "Risiko Keracunan Tinggi: Suhu BMKG 35°C + Waktu Tempuh > 2 Jam untuk SDN 01 Pusat", "time": "5 menit yang lalu", "statusTag": "Telegram Sent" },
        { "id": "2", "type": "FRAUD", "vendorName": "PT. Dapur Sehat Mandiri", "description": "Anomali Klaim: Selisih 150 porsi antara klaim vendor vs laporan guru SDN 18 Utara", "time": "20 menit yang lalu", "statusTag": "Pending Review" },
        { "id": "3", "type": "CRITICAL", "vendorName": "Katering Ibu Nusantara", "description": "Suhu kendaraan pengiriman 38°C. Makanan berpotensi terkontaminasi bakteri Salmonella untuk SD Harapan", "time": "45 menit yang lalu", "statusTag": "Telegram Sent" },
        { "id": "4", "type": "FRAUD", "vendorName": "PT. Makanan Bergizi Nusantara", "description": "Fraud Confirmed: 200 porsi hilang dari total klaim 400 porsi ke SDN 22 Cempaka. Foto tidak sesuai.", "time": "1 jam yang lalu", "statusTag": "Under Investigation" },
        { "id": "5", "type": "CRITICAL", "vendorName": "CV. Katering Berkah Bersama", "description": "Duplikasi pengiriman terdeteksi: Dua klaim distribusi ke SDN 22 Cempaka pada tanggal yang sama", "time": "2 jam yang lalu", "statusTag": "Pending Review" },
        { "id": "6", "type": "FRAUD", "vendorName": "Katering Sekolah Bahagia", "description": "Anomali porsi: Laporan guru menunjukkan porsi 30% lebih kecil dari standar BNG di SDN 12 Timur", "time": "3 jam yang lalu", "statusTag": "Telegram Sent" },
        { "id": "7", "type": "CRITICAL", "vendorName": "PT. Makanan Bergizi Nusantara", "description": "Sertifikat Laik Higiene expired sejak 2 bulan lalu. Vendor masih melakukan distribusi tanpa izin valid", "time": "5 jam yang lalu", "statusTag": "License Suspended" },
        { "id": "8", "type": "FRAUD", "vendorName": "CV. Dapur Bunda Kreatif", "description": "Inkonsistensi data: Menu yang dilaporkan (Ayam Bakar) berbeda dengan foto aktual (Telur Ceplok) di SDN 14 Menteng", "time": "6 jam yang lalu", "statusTag": "Pending Review" },
    ],
    "documents": [
        { "id": "1", "vendorId": "2", "name": "Sertifikat Laik Higiene Sanitasi", "expiry": "20 Des 2026", "status": "Valid" },
        { "id": "2", "vendorId": "2", "name": "Surat Izin Usaha Perdagangan (SIUP)", "expiry": "15 Jun 2027", "status": "Valid" },
        { "id": "3", "vendorId": "2", "name": "Sertifikat Halal MUI", "expiry": "10 Mar 2027", "status": "Valid" },
        { "id": "4", "vendorId": "2", "name": "NPWP Perusahaan", "expiry": "-", "status": "Valid" },
        { "id": "5", "vendorId": "2", "name": "Sertifikat Pelatihan Keamanan Pangan", "expiry": "05 Sep 2026", "status": "Valid" },
        { "id": "6", "vendorId": "2", "name": "Izin Operasional Katering Sekolah", "expiry": "28 Feb 2026", "status": "Expired" },
        { "id": "7", "vendorId": "2", "name": "Surat Keterangan Domisili Usaha", "expiry": "01 Jan 2027", "status": "Valid" },
        { "id": "8", "vendorId": "2", "name": "Kontrak Kerjasama BGN 2026", "expiry": "31 Des 2026", "status": "Valid" },
        { "id": "9", "vendorId": "2", "name": "Sertifikat ISO 22000 (Food Safety)", "expiry": "12 Nov 2025", "status": "Expired" },
    ],
    "users": [
        { "id": "1", "name": "Catur Regulator", "email": "regulator@garda.id", "hashed_password": get_password_hash("password123"), "role": "regulator", "avatar": "https://i.pravatar.cc/80?u=regulator" },
        { "id": "2", "name": "Budi Vendor", "email": "vendor@garda.id", "hashed_password": get_password_hash("password123"), "role": "vendor", "avatar": "https://i.pravatar.cc/80?u=vendor" }
    ]
}

def seed_database():
    db = SessionLocal()
    try:
        if "vendors" in mock_db_state:
            for v_data in mock_db_state["vendors"]:
                db.merge(models.Vendor(**v_data))
        if "schools" in mock_db_state:
            for s_data in mock_db_state["schools"]:
                db.merge(models.School(**s_data))
        if "distributions" in mock_db_state:
            for d_data in mock_db_state["distributions"]:
                db.merge(models.Distribution(**d_data))
        if "alerts" in mock_db_state:
            for a_data in mock_db_state["alerts"]:
                db.merge(models.Alert(**a_data))
        if "documents" in mock_db_state:
            for doc_data in mock_db_state["documents"]:
                db.merge(models.Document(**doc_data))
        if "users" in mock_db_state:
            for u_data in mock_db_state["users"]:
                db.merge(models.User(**u_data))
        db.commit()
        print("Database seeded successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
