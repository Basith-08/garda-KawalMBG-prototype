# Core Problem

Problem utama yang sebenarnya diselesaikan sistem lu bukan:

> “mendeteksi makanan basi”

Tapi:

# “ketidakmampuan memonitor food safety risk pada distribusi makanan skala besar.”

Karena dalam distribusi massal:

* makanan berpindah banyak titik,
* exposure panjang,
* suhu tidak stabil,
* distribusi terlambat,
* dan tidak ada visibility realtime.

Akibatnya:

* makanan bisa menjadi unsafe,
* tapi operator tidak tahu kapan risk mulai naik.

---

# Problem Breakdown

## 1. Tidak Ada Visibility Operational

Operator tidak tahu:

* batch mana terlambat,
* batch mana terlalu lama di jalan,
* batch mana terlalu lama holding,
* kitchen mana paling risky.

Semua masih manual.

---

## 2. Tidak Ada Exposure Tracking

Saat ini kebanyakan sistem hanya tracking:

* makanan dikirim atau belum.

Padahal yang penting:

* berapa lama exposure,
* suhu lingkungan,
* danger-zone duration,
* delay distribusi.

---

## 3. SOP Sulit Diawasi

Dalam skala besar:

* sulit memastikan semua kitchen patuh SOP,
* sulit audit distribusi realtime,
* sulit deteksi operational bottleneck.

---

## 4. Tidak Ada Early Warning System

Biasanya problem baru ketahuan:

* setelah makanan dikonsumsi,
* setelah komplain,
* setelah food poisoning.

Padahal harusnya:

# risk bisa diprediksi sebelum makanan dikonsumsi.

---

# Actual Product Problem Statement

Versi yang lebih professional:

```text id="k8h4rw"
Large-scale food distribution operations lack realtime operational visibility and predictive food safety monitoring, making it difficult to detect unsafe exposure conditions before food is consumed.
```

---

# Simpler Version

```text id="z67h7h"
Distribusi makanan skala besar tidak memiliki sistem monitoring realtime untuk mendeteksi risiko makanan unsafe sebelum dikonsumsi.
```

---

# User Utama (PRIMARY USERS)

# 1. Kitchen Operator / Dapur MBG

## Mereka siapa?

Orang yang:

* memasak,
* packaging,
* dispatch makanan.

---

## Problem mereka

Mereka tidak tahu:

* apakah distribusi masih aman,
* apakah keterlambatan sudah dangerous,
* batch mana yang harus diprioritaskan.

---

## Yang mereka butuhkan

* realtime risk score,
* SOP warning,
* dispatch monitoring,
* batch timeline.

---

# 2. Distribution Operator

## Mereka siapa?

Tim:

* driver,
* dispatcher,
* logistics coordinator.

---

## Problem mereka

Mereka tidak tahu:

* route mana terlalu lama,
* traffic menyebabkan unsafe exposure,
* keterlambatan sudah berbahaya atau belum.

---

## Yang mereka butuhkan

* ETA monitoring,
* route risk,
* exposure duration,
* delay alert.

---

# 3. Supervisors / Auditors

## Mereka siapa?

Orang yang:

* audit SOP,
* monitoring kitchen,
* monitoring distribusi.

---

## Problem mereka

Mereka tidak punya:

* operational visibility,
* centralized monitoring,
* anomaly detection,
* kitchen performance analytics.

---

## Yang mereka butuhkan

* dashboard analytics,
* kitchen ranking,
* anomaly alerts,
* SOP compliance tracking.

---

# 4. Government / Program Management

## Mereka siapa?

Instansi:

* MBG operator,
* pemerintah daerah,
* kementerian,
* program manager.

---

## Problem mereka

Mereka sulit:

* memonitor ribuan distribusi,
* mendeteksi kitchen bermasalah,
* melakukan preventive monitoring.

---

## Yang mereka butuhkan

* regional monitoring,
* operational analytics,
* compliance intelligence,
* incident prevention.

---

# Secondary Users

# 5. Food Safety Auditor

## Butuh:

* exposure logs,
* SOP logs,
* risk history,
* audit trail.

---

# 6. Logistics Analyst

## Butuh:

* route analytics,
* traffic analysis,
* dispatch optimization,
* delay patterns.

---

# User Journey

# Kitchen Staff

```text id="8m5o6i"
Cook Food
→ Package
→ Create Batch
→ Monitor Risk
→ Dispatch
→ Receive Alerts
```

---

# Distribution Team

```text id="qg4m5j"
Pickup Batch
→ Route Tracking
→ Delay Monitoring
→ Delivery Confirmation
```

---

# Supervisor

```text id="4gh24g"
Monitor Dashboard
→ Detect High Risk
→ Investigate Violations
→ Take Action
```

---

# Real Core Value

Produk lu sebenarnya memberikan:

# “Operational Visibility”

Bukan:

* AI chatbot,
* scanner makanan,
* AI vision gimmick.

---

# What Users Actually Buy

User tidak membeli:

> “AI”

Mereka membeli:

* monitoring,
* visibility,
* prevention,
* operational control,
* compliance.

---

# Biggest Pain Point

Yang paling sakit di operational food distribution:

# “Tidak tahu kapan makanan mulai menjadi risky.”

Dan sistem lu menyelesaikan itu.

---

# Most Important Insight

Produk lu sebenarnya lebih dekat ke:

| Mirip                  | Bukan            |
| ---------------------- | ---------------- |
| logistics intelligence | AI scanner       |
| operational monitoring | chatbot          |
| HACCP compliance       | image classifier |
| risk analytics         | food camera AI   |

---

# Positioning yang Lebih Tepat

## Jangan bilang:

```text id="4dnndh"
AI Deteksi Makanan Basi
```

---

# Bilang:

```text id="z2qfhq"
Predictive Food Safety Operational Monitoring
```

atau:

```text id="q7jmmq"
Operational Food Safety Intelligence Platform
```

---

# Market yang Sebenernya Bisa Masuk

Setelah MBG:

* catering,
* airline food,
* hospital food,
* school meals,
* cloud kitchen,
* food logistics,
* cold chain distribution.

Karena problemnya universal:

# operational food safety visibility.
