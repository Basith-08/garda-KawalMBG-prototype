# BUILDING PLAN

# Predictive Food Safety Operational Monitoring (MBG)

Dokumen ini disusun berdasarkan urutan analisis berikut:

1. `PORBLEM.MD` sebagai `PROBLEM`
2. `MVP.MD`
3. `PRD.MD`
4. `TRD.MD`
5. `ERD.MD`
6. `PROJECT_ARCHITECTURE.MD`
7. `AGENT_SKILL.MD`

Catatan:
- ada typo nama file: `PORBLEM.MD`
- ada perbedaan nama file skill: `AGENT_SKILL.MD` vs `AGENT_SKILLS.MD` pada referensi lama
- dokumen backend structure di `TRD` masih memakai tree `app/`, tetapi untuk implementasi repo ini sebaiknya backend tetap dipisah di `backend/`

---

# 1. Ordered Analysis Summary

## PROBLEM

Masalah inti bukan mendeteksi makanan basi, tetapi:

`ketidakmampuan memonitor food safety risk pada distribusi makanan skala besar secara realtime`

Implikasi build:
- sistem harus fokus pada visibility operasional
- exposure tracking lebih penting daripada AI
- harus ada early warning sebelum konsumsi
- audit trail dan explainability wajib

## MVP

MVP harus membuktikan:
- operational food safety monitoring
- realtime risk calculation
- SOP violation detection
- operational visibility

Batas MVP:
- wajib rule-based scoring
- wajib timeline operasional
- wajib dashboard + alerts
- tidak perlu deep learning
- tidak perlu computer vision
- tidak perlu mobile app

## PRD

PRD memperjelas:
- visi produk sebagai operational intelligence platform
- target user utama: kitchen operator, distribution operator, supervisor/auditor, program management
- fitur inti: auth, batch lifecycle, risk engine, alerts, monitoring, external context

Implikasi build:
- fitur harus disusun menurut journey operasional, bukan menurut gimmick AI
- role-based workflow adalah requirement produk, bukan tambahan

## TRD

TRD menetapkan:
- frontend Vue 3 + Tailwind + Pinia
- backend FastAPI + SQLAlchemy
- PostgreSQL Supabase
- optional ML layer
- polling untuk realtime
- struktur frontend `src/pages`, `components`, `services`, `types`

Implikasi build:
- implementasi frontend harus dipisah jelas antara page, component, service, type
- backend harus modular walau masih monolith
- risk engine harus diperlakukan sebagai service inti

## ERD

ERD memberi model data konseptual:
- users
- kitchens
- menu_items
- food_batches
- distribution_routes
- temperature_logs
- risk_scores
- alerts
- anomaly_logs
- audit_logs

Implikasi build:
- historical tracking wajib
- risk score dan alerts tidak boleh hanya state saat ini
- auditability harus dibangun dari schema, bukan ditambal di UI

## PROJECT ARCHITECTURE

Arsitektur target:
- frontend dashboard
- FastAPI backend
- rule-based risk engine
- PostgreSQL
- external APIs
- optional ML anomaly layer

Prinsip inti:
- explainable
- operational
- modular
- scalable
- auditable
- event-driven

Implikasi build:
- semua keputusan struktur harus menjaga keterbacaan modul
- risk berubah karena event operasional, jadi timeline/event model sangat penting

## AGENT SKILL

Skill requirement menegaskan:
- domain HACCP harus dipahami
- frontend perlu kuat di dashboard data-heavy
- backend perlu kuat di risk engine dan time-based logic
- database harus historical dan traceable
- ML bukan prioritas utama

Implikasi build:
- prioritas staffing/agent work harus condong ke domain + backend risk + dashboard
- ML hanya fase lanjutan

---

# 2. Core Product Decision

Produk yang harus dibangun adalah:

`operational food safety intelligence platform berbasis rule engine dan evidence tracking`

Bukan:
- AI deteksi basi
- model prediksi keracunan berbasis dataset besar
- aplikasi consumer

Keputusan ini harus mengunci semua scope berikutnya.

---

# 3. Building Principles

1. Build rule-based risk engine first.
2. Treat timeline and evidence as first-class data.
3. Keep every risk output explainable.
4. Prioritize auditability and historical logs.
5. Use external context only as modifier, not main truth.
6. Keep ML as optional MVP+ layer.
7. Optimize for regulator/vendor workflow before analytics expansion.

---

# 4. Recommended Target Structure

## Frontend

```text
frontend/src/
├── assets/
├── components/
│   ├── common/
│   ├── dashboard/
│   ├── risk/
│   ├── analytics/
│   ├── maps/
│   └── distribution/
├── composables/
├── layouts/
├── pages/
│   ├── auth/
│   ├── public/
│   ├── regulator/
│   ├── vendor/
│   └── admin/
├── router/
├── services/
├── stores/
├── styles/
├── types/
└── utils/
```

## Backend

```text
backend/
├── main.py
├── models.py
├── migrations.py
├── settings.py
├── auth_utils.py
├── token_utils.py
├── risk_assessment.py
├── seed.py
├── tests/
├── api/
├── schemas/
├── services/
├── rules/
├── db/
└── utils/
```

Catatan:
- bila backend belum dipisah penuh, lakukan bertahap
- jangan refactor besar sebelum kontrak fitur inti stabil

---

# 5. Build Phases

## Phase 0 — Scope Lock

Objective:
- kunci positioning produk
- singkirkan asumsi AI-first
- tetapkan glossary operasional

Deliverables:
- final product terminology
- finalized MVP boundary
- role matrix
- risk status definitions

Exit criteria:
- seluruh tim memakai istilah `operational food safety risk`
- non-goals tertulis jelas

## Phase 1 — Foundation

Objective:
- siapkan pondasi engineering dan akses sistem

Scope:
- monorepo / repo structure cleanup
- environment setup
- auth
- RBAC
- migration framework
- seed data
- health endpoint
- baseline CI checks

Deliverables:
- login/logout/session
- protected routes
- DB migration runner
- seed dataset
- `.env.example`
- health checks

Exit criteria:
- semua role inti bisa login
- database bisa bootstrap dari nol
- local environment reproducible

## Phase 2 — Core Data Model

Objective:
- implement schema inti untuk lifecycle distribusi

Scope:
- users
- kitchens
- menu_items
- food_batches
- distribution_routes
- temperature_logs
- risk_scores
- alerts
- audit_logs

Important decision:
- kalau implementasi nyata memakai vendor/school/distribution model, mapping ke ERD harus dibuat eksplisit
- jangan biarkan model konseptual dan model runtime berbeda tanpa adapter/normalization layer

Deliverables:
- schema migration
- relational constraints
- indexes penting
- serialization contract

Exit criteria:
- semua entity inti punya relasi jelas
- historisasi risk dan alert sudah tersimpan

## Phase 3 — Operational Input & Timeline

Objective:
- membangun pencatatan lifecycle distribusi yang bisa diaudit

Scope:
- create batch / distribution
- update operational timestamps
- capture evidence
- record route and arrival data

Minimum data:
- cooked time
- packaged time
- pickup time
- delivered time
- menu
- porsi
- ambient temperature
- evidence completeness
- school receipt status

Deliverables:
- vendor input form
- backend write API
- timeline serializer
- validation rules

Exit criteria:
- satu distribusi bisa ditelusuri dari produksi sampai receipt

## Phase 4 — Rule-Based Risk Engine

Objective:
- jadikan risk engine sebagai core differentiator

Scope:
- weighted scoring
- exposure calculation
- SOP violation logic
- explainable output

Recommended factor set:
- time exposure
- SOP compliance
- menu sensitivity
- arrival verification
- vendor history
- weather context

Deliverables:
- risk assessment service
- component score breakdown
- risk status mapping
- recommended action output

Exit criteria:
- setiap distribusi menghasilkan assessment explainable
- output tidak bergantung pada placeholder manual

## Phase 5 — Alerting & Early Warning

Objective:
- ubah assessment menjadi intervensi operasional

Scope:
- threshold-based alerts
- regulator alert queue
- receipt-triggered alerts
- anomaly flags

Deliverables:
- alert generation rules
- alert history
- alert severity categories
- dashboard surfaces

Exit criteria:
- kondisi high-risk dan receipt issue benar-benar memicu alert

## Phase 6 — Monitoring Dashboards

Objective:
- menyajikan visibility untuk semua role utama

Scope:
- regulator dashboard
- vendor dashboard
- admin/governance dashboard
- public information pages bila diperlukan

Regulator needs:
- high-risk distributions
- vendor ranking
- alert list
- distribution detail
- trust profile

Vendor needs:
- input distribusi
- history
- receipt follow-up
- dokumen izin

Admin needs:
- user access
- data quality
- vendor linkage
- governance overview

Exit criteria:
- tiap role melihat data sesuai scope
- dashboard memakai data nyata, bukan placeholder

## Phase 7 — External Context Integration

Objective:
- melengkapi risk engine dengan context operasional

Scope:
- BMKG
- Google Maps ETA/route

Rules:
- cuaca hanya contextual modifier
- ETA memperkaya time risk, bukan menggantikan timestamp aktual

Deliverables:
- weather service adapter
- route service adapter
- fallback behaviour jika API gagal

Exit criteria:
- sistem tetap jalan tanpa ketergantungan keras ke API eksternal

## Phase 8 — Historical Analytics

Objective:
- gunakan data historis untuk insight operasional

Scope:
- trend per vendor
- repeated delay pattern
- SOP breach frequency
- route bottleneck
- kitchen performance

Deliverables:
- analytics endpoints
- summary cards
- historical charts

Exit criteria:
- regulator dan auditor bisa melihat pola, bukan hanya snapshot

## Phase 9 — Optional MVP+ Intelligence

Objective:
- tambah anomaly detection setelah data dasar kuat

Scope:
- Isolation Forest
- statistical anomaly rules
- vendor anomaly profiling

Rules:
- hanya aktif setelah data historis cukup
- output tetap explainable
- jangan menggantikan rule engine

Exit criteria:
- anomaly layer menambah signal, bukan noise

## Phase 10 — Security, Reliability, Deployment

Objective:
- siapkan sistem untuk dipakai lebih serius

Scope:
- API auth hardening
- audit logging
- CORS policy
- secrets management
- backup strategy
- deployment pipeline
- monitoring and observability

Deliverables:
- environment validation
- runtime logs
- regression tests
- deployment checklist

Exit criteria:
- deployment tidak bergantung setup manual rapuh

---

# 6. Build Order by Dependency

Urutan kerja yang paling aman:

1. Scope lock
2. Foundation
3. Core data model
4. Operational input and timeline
5. Rule-based risk engine
6. Alerting
7. Role dashboards
8. External context
9. Historical analytics
10. Optional anomaly detection
11. Security and deployment hardening

Alasan:
- risk engine tidak bisa benar tanpa data timeline
- dashboard tidak berguna tanpa assessment yang stabil
- anomaly detection tidak layak sebelum history cukup

---

# 7. Must-Have MVP Deliverables

Minimum deliverables untuk MVP yang sesuai dokumen:

- authenticated multi-role access
- operational input for distribution lifecycle
- explainable rule-based risk assessment
- SOP violation detection
- operational timeline view
- alert generation
- regulator dashboard
- vendor dashboard
- receipt verification flow
- historical record for audit

Kalau salah satu item di atas belum ada, MVP belum lengkap.

---

# 8. Risks and Corrections

## Risk 1 — AI Scope Creep

Masalah:
- dokumen bisa dibaca seolah sistem perlu ML sejak awal

Keputusan:
- tahan ML sampai sesudah rule engine, history, dan alerts stabil

## Risk 2 — Conceptual ERD vs Runtime Model

Masalah:
- ERD sangat kitchen/batch-centric
- implementasi nyata bisa vendor/distribution-centric

Keputusan:
- buat mapping eksplisit atau normalization layer
- jangan campur dua model tanpa kontrak jelas

## Risk 3 — Backend Structure Ambiguity

Masalah:
- TRD menulis backend tree di `app/`

Keputusan:
- untuk repo ini backend tetap di `backend/`
- struktur modular diterapkan di dalam `backend/`, bukan memindahkan root secara gegabah

## Risk 4 — Overbuilding Dashboard Before Data Contract

Masalah:
- mudah tergoda membangun UI lebih dulu

Keputusan:
- data contract, timeline, dan risk engine harus stabil lebih dulu

## Risk 5 — Weak Auditability

Masalah:
- jika risk, alert, dan receipt hanya overwrite state saat ini, audit hilang

Keputusan:
- histori dan logs wajib jadi bagian schema dan API

---

# 9. Suggested Sprint Breakdown

## Sprint 1

- scope lock
- auth
- migration runner
- seed data
- base schema

## Sprint 2

- operational input flow
- timeline persistence
- evidence capture
- receipt baseline

## Sprint 3

- rule-based risk engine
- explainable assessment contract
- alert rules

## Sprint 4

- regulator dashboard
- vendor dashboard
- distribution detail
- alert detail

## Sprint 5

- external API integration
- analytics
- hardening
- regression coverage

## Sprint 6

- optional anomaly detection
- deployment polish
- observability

---

# 10. Final Build Recommendation

Fokus build yang benar adalah:

`bangun sistem monitoring distribusi makanan yang event-driven, explainable, dan audit-friendly, dengan rule-based operational risk engine sebagai inti, bukan AI model sebagai inti.`

Jika harus memilih prioritas paling kecil namun paling benar:

1. auth + roles
2. timeline + evidence data model
3. risk engine
4. alerts
5. dashboards
6. external context
7. analytics
8. optional anomaly detection
