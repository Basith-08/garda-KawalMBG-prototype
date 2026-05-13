# TASK BREAKDOWN

# Predictive Food Safety Operational Monitoring (MBG)

Dokumen ini menurunkan `BUILDING_PLAN.MD` menjadi backlog implementasi yang detail dan bisa dieksekusi.

Prinsip:
- urutan task mengikuti critical path produk
- task dibagi per phase dan epic
- setiap task punya tujuan jelas, dependency, dan acceptance criteria
- ML/anomaly diletakkan di fase akhir

## Current Progress

Implemented:
- `T-004` partial: frontend structure sudah konsisten memakai `frontend/src/pages`, `components`, `services`, `types`, `styles`; backend mulai dipisah ke `schemas`, `services`, `utils`
- `T-004` partial lanjut: helper serialisasi data privat/publik, trust profile vendor, dan admin overview sudah dipindah dari `backend/main.py` ke `backend/services/serialization.py` dan `backend/services/admin.py`
- `T-004` partial lanjut: orchestration login auth dan persistence `POST /api/data` sudah dipindah dari `backend/main.py` ke `backend/services/auth.py` dan `backend/services/runtime_data.py`
- `T-004` partial lanjut: mutasi akses user admin sudah dipindah dari `backend/main.py` ke `backend/services/admin.py`
- `T-004` partial lanjut: folder `backend/api/` mulai dibentuk; auth dependency dipindah ke `backend/api/deps.py`, route auth ke `backend/api/auth.py`, dan route public/system ke `backend/api/public.py`
- `T-004` partial lanjut: route distribusi/receipt, runtime data, regulator overview, dan admin access sudah dipindah dari `backend/main.py` ke modul `backend/api/` terpisah
- `T-007` partial lanjut: side effect koneksi DB saat import backend dihapus; `create_all` tidak lagi berjalan di import `main.py` dan `seed.py`, inisialisasi schema dipindah ke jalur explicit migration/bootstrap; auto-seed startup sekarang butuh `AUTO_SEED_ON_STARTUP`
- `T-005` partial: placeholder visual eksternal pada halaman publik utama sudah dihapus; wording AI-first yang paling misleading di runtime UI sudah dikoreksi
- `T-019` baseline: receipt verification sudah terstruktur dengan `issueType`, `evidenceUploaded`, `note`, `verifiedAt`
- `T-020` baseline: receipt bermasalah memicu alert regulator
- `T-012` baseline: histori risk minimal sudah tersimpan di tabel `risk_scores`
- `T-014` baseline: audit log minimal sudah tersimpan di tabel `audit_logs`
- `T-033` baseline: regulator overview endpoint tersedia dengan guard role; dashboard regulator sekarang membaca service backend khusus `GET /api/regulator/overview`, bukan lagi state mock umum; kontrak test dasar sudah ditambahkan

Not yet complete:
- modularisasi backend penuh
- historical analytics
- anomaly layer
- deployment hardening

---

# 0. Planning Rules

## Priority Order

1. data contract
2. timeline and evidence capture
3. rule-based risk engine
4. alerts
5. role dashboards
6. external context
7. analytics
8. anomaly detection
9. hardening and deployment

## Definition of Done

Sebuah task dianggap selesai bila:
- code sudah diimplementasikan
- kontrak data tervalidasi
- regression test area terdampak tersedia atau diperbarui
- tidak ada placeholder yang menyamar sebagai fitur final
- docs teknis yang terdampak ikut diperbarui bila kontraknya berubah

---

# Phase 0 — Scope Lock

## Epic P0.1 — Product Language Lock

### T-001 Finalize product glossary

Goal:
- samakan istilah lintas backend, frontend, docs, dan alert copy

Work:
- tetapkan istilah resmi untuk `unsafe`, `operational risk`, `SOP violation`, `receipt verification`, `evidence completeness`
- larang istilah seperti `basi`, `busuk`, `AI deteksi basi`
- definisikan status risiko `LOW`, `MEDIUM`, `HIGH`

Output:
- glossary internal
- mapping istilah lama ke istilah baru

Acceptance criteria:
- semua output assessment memakai istilah operasional
- tidak ada label publik yang kontradiktif dengan positioning produk

### T-002 Finalize role matrix

Goal:
- kunci role dan batas akses

Work:
- definisikan role final: `regulator`, `vendor`, `super-admin`, `public`
- petakan role dokumen lama ke role runtime
- definisikan read/write scope tiap role

Acceptance criteria:
- role matrix terdokumentasi
- semua endpoint private punya owner role jelas

## Epic P0.2 — Scope Boundary Lock

### T-003 Freeze MVP in-scope and out-of-scope features

Goal:
- cegah scope creep

Work:
- tandai fitur MVP wajib
- tandai fitur MVP+ opsional
- tandai fitur non-goal

Acceptance criteria:
- roadmap build tidak memasukkan deep learning, computer vision, atau mobile app sebagai blocker MVP

---

# Phase 1 — Foundation

## Epic P1.1 — Repository and Structure Cleanup

### T-004 Normalize repo folder structure

Dependency:
- T-001, T-002

Goal:
- sejajarkan repo dengan struktur target yang realistis

Work:
- pastikan frontend konsisten di `frontend/src/`
- pastikan `pages`, `components`, `services`, `types`, `styles` terpisah
- hapus penyimpanan type domain di file service yang tidak semestinya
- siapkan folder backend modular: `api`, `schemas`, `services`, `rules`, `db`, `utils`

Acceptance criteria:
- frontend tidak lagi memakai `views/`
- type domain tidak lagi ditaruh di local storage service
- backend punya target struktur modular walau migrasi dilakukan bertahap

### T-005 Remove legacy placeholders and dead paths

Goal:
- mengurangi drift dan dependency palsu

Work:
- identifikasi file placeholder, data dummy, route mati, dan assets non-operasional
- hapus atau ganti dengan fallback yang jujur

Acceptance criteria:
- halaman detail tidak memakai dummy evidence yang menyesatkan
- service lama yang tidak lagi jadi source of truth dihapus

## Epic P1.2 — Environment and Runtime Setup

### T-006 Standardize local environment setup

Goal:
- setup lokal reproducible

Work:
- lengkapi `.env.example` frontend dan backend
- validasi mandatory env
- dokumentasikan port, DB URL, auth secret, CORS origin

Acceptance criteria:
- repo bisa dijalankan dari nol tanpa menebak env penting

### T-007 Add health and boot diagnostics

Goal:
- percepat troubleshooting runtime

Work:
- health endpoint backend
- DB connectivity signal
- seed status signal
- migration status signal

Acceptance criteria:
- satu endpoint bisa menunjukkan status minimum sistem

## Epic P1.3 — Authentication and RBAC

### T-008 Implement login/session flow

Goal:
- semua role inti bisa masuk sistem dengan aman

Work:
- login API
- signed session token
- session restore
- logout cleanup

Acceptance criteria:
- session survive refresh
- unauthorized state fallback aman

### T-009 Enforce role-based route protection

Goal:
- cegah akses silang role

Work:
- router guard frontend
- role guard backend
- forbidden response handling

Acceptance criteria:
- vendor tidak bisa buka dashboard regulator
- regulator tidak bisa buka governance super-admin

---

# Phase 2 — Core Data Model

## Epic P2.1 — Domain Entity Baseline

### T-010 Define canonical runtime entities

Goal:
- tetapkan entity runtime yang benar

Work:
- kunci entity inti runtime: `users`, `vendors`, `schools`, `distributions`, `documents`, `alerts`
- buat mapping eksplisit dari ERD konseptual ke runtime model
- tentukan field wajib vs optional

Acceptance criteria:
- tidak ada ambiguity antara ERD konseptual dan schema runtime

### T-011 Add relational constraints and indexes

Goal:
- jaga integritas data

Work:
- FK users -> vendor
- FK school -> vendor
- FK distribution -> vendor
- FK alert -> vendor
- index untuk lookup per vendor, risk, time, status

Acceptance criteria:
- query scope vendor efisien
- relasi lintas tabel tervalidasi

## Epic P2.2 — Historical Logging

### T-012 Add risk history persistence

Goal:
- risk score tidak hanya state saat ini

Work:
- simpan snapshot risk per distribution event
- simpan component score breakdown
- simpan timestamp per assessment

Acceptance criteria:
- histori risk bisa direview untuk audit

### T-013 Add alert history persistence

Goal:
- alert punya jejak kronologis

Work:
- simpan alert source
- simpan severity
- simpan acknowledged/resolved state bila diperlukan

Acceptance criteria:
- alert lama tidak hilang ketika status distribution berubah

### T-014 Add audit log baseline

Goal:
- perubahan penting bisa ditelusuri

Work:
- log login
- log user access change
- log distribution create/update
- log receipt verification

Acceptance criteria:
- ada jejak minimal untuk tindakan sensitif

---

# Phase 3 — Operational Input and Timeline

## Epic P3.1 — Distribution Lifecycle Capture

### T-015 Build vendor distribution input schema

Goal:
- semua data operasional minimum tertangkap

Work:
- cooked time
- packaged time
- pickup time
- delivered time
- menu
- porsi
- school
- ambient temperature
- delivery duration

Acceptance criteria:
- satu record distribution cukup untuk dihitung oleh risk engine

### T-016 Add evidence capture fields

Goal:
- SOP compliance tidak hanya berdasar teks bebas

Work:
- QC evidence
- production evidence
- packaging evidence
- vehicle evidence
- evidence completeness flag

Acceptance criteria:
- backend dapat membedakan record lengkap vs tidak lengkap

### T-017 Lock operational fields after submit

Goal:
- kurangi manipulasi data

Work:
- define editable vs locked fields
- cutoff policy
- update guard

Acceptance criteria:
- field waktu penting tidak bisa diubah sembarangan setelah final submit

## Epic P3.2 — Receipt Verification Flow

### T-018 Build school receipt read endpoint

Goal:
- penerima bisa memverifikasi distribusi

Work:
- public receipt endpoint
- serialize distribution summary
- include assessment summary

Acceptance criteria:
- halaman receipt publik bisa dimuat tanpa auth internal

### T-019 Build structured receipt verification

Goal:
- receipt issue menjadi data operasional, bukan teks liar

Work:
- status receipt
- issue type
- evidence flag
- note
- verified timestamp

Acceptance criteria:
- problematic receipt wajib punya kategori
- severe receipt state menaikkan arrival risk

### T-020 Add receipt-to-alert linkage

Goal:
- masalah receipt langsung terlihat oleh regulator

Work:
- generate alert saat `received_with_issue`
- generate alert saat `not_received`
- sertakan issue type dan note

Acceptance criteria:
- receipt bermasalah menghasilkan alert baru

---

# Phase 4 — Rule-Based Risk Engine

## Epic P4.1 — Assessment Contract

### T-021 Define canonical assessment output

Goal:
- frontend dan backend memakai kontrak assessment yang sama

Output fields:
- operationalSummary
- exposureAnalysis
- sopViolations
- riskFactors
- componentScores
- finalRiskScore
- riskStatus
- recommendedAction

Acceptance criteria:
- satu distribution selalu menghasilkan shape output yang konsisten

## Epic P4.2 — Weighted Scoring

### T-022 Implement time exposure scoring

Goal:
- ukur dampak timeline pada risk

Work:
- compute cook-to-arrival duration
- fallback to route duration bila timeline tidak lengkap
- mark incomplete timeline as risk

Acceptance criteria:
- duration abnormal meningkatkan score secara deterministik

### T-023 Implement SOP compliance scoring

Goal:
- jadikan evidence completeness bagian inti risk

Work:
- hitung missing evidence
- cek note anomaly
- turunkan severity ke component score

Acceptance criteria:
- kekurangan evidence menaikkan `sopRisk`

### T-024 Implement menu sensitivity scoring

Goal:
- menu high-protein/high-moisture punya bobot risk lebih tinggi

Acceptance criteria:
- menu sensitif terlihat pada `menuRisk`

### T-025 Implement arrival verification scoring

Goal:
- receipt sekolah mempengaruhi risk secara langsung

Acceptance criteria:
- `received_ok` menurunkan risk
- `received_with_issue` menaikkan risk
- `not_received` dianggap severe

### T-026 Implement vendor history scoring

Goal:
- vendor trust/history mempengaruhi prioritization

Acceptance criteria:
- vendor dengan trust score rendah menaikkan `vendorHistoryRisk`

### T-027 Implement weather context scoring

Goal:
- cuaca jadi modifier kecil, bukan faktor dominan

Acceptance criteria:
- suhu ekstrem menambah score secara terbatas

## Epic P4.3 — Explainability

### T-028 Build risk explanation generator

Goal:
- setiap score bisa dijelaskan

Work:
- generate reasons per component
- generate recommended action
- generate SOP violation list

Acceptance criteria:
- tidak ada risk output tanpa alasan

### T-029 Normalize distribution record from assessment

Goal:
- backend write path dan read path konsisten

Acceptance criteria:
- `riskScore`, `status`, `statusText`, `levelRisiko`, dan `assessment` sinkron

---

# Phase 5 — Alerting

## Epic P5.1 — Alert Rules

### T-030 Define alert thresholds

Goal:
- klasifikasikan kapan alert muncul

Rules:
- high-risk distribution
- severe receipt issue
- not received
- anomaly signal
- expiring document threshold

Acceptance criteria:
- threshold terdokumentasi dan diuji

### T-031 Build alert creation service

Goal:
- centralize alert generation

Acceptance criteria:
- alert tidak dibuat tersebar di banyak tempat tanpa aturan tunggal

### T-032 Build alert feed serialization

Goal:
- regulator dan vendor melihat alert sesuai scope

Acceptance criteria:
- vendor hanya melihat alert miliknya
- regulator melihat semua alert relevan

---

# Phase 6 — Dashboards

## Epic P6.1 — Regulator Experience

### T-033 Build regulator overview dashboard

Goal:
- regulator langsung melihat prioritas operasional

Widgets minimum:
- high-risk distributions
- alert summary
- vendor trust ranking
- recent receipt issues

Acceptance criteria:
- dashboard pertama sudah cukup untuk triage

### T-034 Build distribution detail page

Goal:
- regulator bisa audit satu distribusi end-to-end

Must show:
- assessment
- timeline
- evidence completeness
- receipt verification
- notes

Acceptance criteria:
- detail page tidak bergantung pada dummy content

### T-035 Build vendor detail and trust profile

Goal:
- regulator bisa evaluasi vendor secara historis

Acceptance criteria:
- trust breakdown dan histori utama terlihat

## Epic P6.2 — Vendor Experience

### T-036 Build vendor dashboard

Goal:
- vendor tahu status operasionalnya sendiri

Acceptance criteria:
- vendor bisa melihat recent distributions, alert, trust status

### T-037 Build input distribution flow

Goal:
- input harian bisa dilakukan cepat dan benar

Acceptance criteria:
- form cukup singkat
- validasi kuat
- submit menghasilkan assessment

### T-038 Build history and detail pages

Goal:
- vendor bisa review distribusi, receipt, dan risk hasil submit

Acceptance criteria:
- vendor detail page memakai data aktual dari backend

### T-039 Build document management page

Goal:
- vendor bisa melihat dan mengelola status dokumen izin

Acceptance criteria:
- status valid / expired / expiring terlihat jelas

## Epic P6.3 — Super Admin Experience

### T-040 Build governance dashboard

Goal:
- super-admin punya snapshot health platform

Acceptance criteria:
- metrics user, vendor, data quality, alert, document tersedia

### T-041 Build user access editor

Goal:
- role dan vendor linkage bisa dikelola aman

Acceptance criteria:
- self-demotion/self-deactivation guard ada

---

# Phase 7 — External Context

## Epic P7.1 — BMKG Integration

### T-042 Build weather adapter

Goal:
- ambil context suhu/cuaca eksternal

Acceptance criteria:
- service punya timeout, retry ringan, dan fallback

### T-043 Inject weather into assessment pipeline

Goal:
- cuaca masuk ke assessment tanpa jadi faktor dominan

Acceptance criteria:
- weather mempengaruhi `weatherRisk` saja

## Epic P7.2 — Route / ETA Integration

### T-044 Build maps/ETA adapter

Goal:
- enrich route monitoring

Acceptance criteria:
- ETA bisa dibandingkan dengan timeline aktual

### T-045 Build route monitoring visualization

Goal:
- regulator/vendor bisa melihat keterlambatan dalam konteks route

Acceptance criteria:
- UI route tidak memblokir sistem bila API external gagal

---

# Phase 8 — Historical Analytics

## Epic P8.1 — Vendor and Distribution Trends

### T-046 Build historical aggregation queries

Goal:
- siapkan data analytics yang benar

Metrics:
- repeated delay
- evidence completeness trend
- receipt issue frequency
- risk trend per vendor

Acceptance criteria:
- analytics tidak menghitung dari array frontend mentah

### T-047 Build analytics endpoints

Goal:
- frontend mengonsumsi summary dari backend

Acceptance criteria:
- payload analytics terpisah dari feed CRUD dasar

### T-048 Build analytics UI

Goal:
- tampilkan trend dan hotspot operasional

Acceptance criteria:
- chart/card menjawab kebutuhan regulator dan auditor, bukan dekorasi

---

# Phase 9 — Optional Intelligence Layer

## Epic P9.1 — Statistical/Anomaly Layer

### T-049 Define readiness gate for ML/anomaly

Goal:
- anomaly layer hanya aktif saat data cukup

Criteria:
- volume distributions minimum
- receipt labels cukup
- baseline rule outputs stabil

Acceptance criteria:
- ML tidak masuk sebelum readiness gate lulus

### T-050 Build anomaly baseline using rules/statistics

Goal:
- mulai dari signal sederhana

Examples:
- duplicate route
- unusual duration
- portion mismatch
- inconsistent receipt pattern

Acceptance criteria:
- anomaly rules explainable

### T-051 Implement optional Isolation Forest prototype

Goal:
- validasi MVP+ layer

Acceptance criteria:
- model tidak menggantikan rule engine
- output dipresentasikan sebagai additional signal

---

# Phase 10 — Security, Reliability, Deployment

## Epic P10.1 — Security Hardening

### T-052 Enforce token and session hardening

Goal:
- private data tetap terlindungi

Acceptance criteria:
- token validation kuat
- unauthorized fallback aman

### T-053 Lock down CORS and secrets handling

Goal:
- kurangi misconfiguration runtime

Acceptance criteria:
- default insecure config ditolak di non-local env

## Epic P10.2 — Reliability

### T-054 Build regression suites for critical contracts

Target area:
- auth
- role scope
- risk assessment
- receipt verification
- admin governance
- migration compatibility

Acceptance criteria:
- critical path punya regression suite

### T-055 Add runtime observability

Goal:
- insiden mudah didiagnosis

Work:
- structured logs
- request error logs
- background failure logs

Acceptance criteria:
- error operasional utama muncul jelas di logs

## Epic P10.3 — Deployment Readiness

### T-056 Define deployment topology

Goal:
- frontend, backend, DB, env, and secrets siap dipasang

Acceptance criteria:
- arsitektur deployment terdokumentasi

### T-057 Add deployment checklist and smoke tests

Goal:
- setiap deploy bisa diverifikasi cepat

Acceptance criteria:
- ada daftar smoke test minimum pasca deploy

---

# Critical Path

Task kritis yang tidak boleh tertukar urutannya:

1. T-001 sampai T-003
2. T-006 sampai T-009
3. T-010 sampai T-020
4. T-021 sampai T-029
5. T-030 sampai T-039
6. T-052 sampai T-057

Kalau critical path ini belum selesai, analytics dan anomaly jangan diprioritaskan.

---

# MVP Release Gate

MVP siap release internal bila kondisi berikut terpenuhi:

- auth dan RBAC stabil
- distribution lifecycle lengkap
- receipt verification lengkap
- rule-based assessment explainable
- alerts berjalan
- regulator dashboard usable
- vendor dashboard usable
- dokumen vendor minimal terbaca
- regression suite critical path hijau

---

# Recommended Execution Order

## Sprint 1

- T-001 sampai T-009

## Sprint 2

- T-010 sampai T-020

## Sprint 3

- T-021 sampai T-032

## Sprint 4

- T-033 sampai T-041

## Sprint 5

- T-042 sampai T-048

## Sprint 6

- T-049 sampai T-057

---

# Final Note

Jika terjadi konflik antara dokumen ideal dan repo aktual:
- utamakan correctness kontrak data
- pertahankan MVP tetap kecil
- jangan memaksa refactor besar sebelum flow inti stabil
- rule engine, timeline, evidence, receipt, dan alert harus selalu didahulukan dari fitur turunan
