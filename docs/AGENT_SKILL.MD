# Required Skills / Agent Skills

# Predictive Food Safety Operational Monitoring (MBG)

---

# 1. Overview

Project ini bukan sekadar:

* dashboard biasa,
* CRUD app,
* atau AI gimmick.

Tetapi gabungan dari:

* operational intelligence,
* food safety monitoring,
* logistics analytics,
* risk assessment,
* dan realtime monitoring system.

Karena itu skill yang dibutuhkan harus dibagi menjadi:

| Area                  | Focus                   |
| --------------------- | ----------------------- |
| Product Understanding | operational food safety |
| Frontend              | monitoring dashboard    |
| Backend               | risk engine & APIs      |
| Data                  | exposure analytics      |
| ML                    | anomaly detection       |
| Infrastructure        | deployment & monitoring |

---

# 2. Core Product Knowledge

# Required Domain Understanding

## 1. HACCP Fundamentals

Developer HARUS paham basic:

* danger zone,
* exposure duration,
* holding time,
* contamination risk,
* SOP compliance.

---

# Important Concepts

| Concept           | Description               |
| ----------------- | ------------------------- |
| Danger Zone       | 5°C–60°C                  |
| Exposure Duration | lama exposure             |
| Holding Time      | waktu sebelum distribusi  |
| High-Risk Food    | protein & moisture tinggi |
| SOP Violation     | pelanggaran operational   |

---

# Kenapa Penting?

Karena:

* logic utama sistem berbasis food safety,
* bukan sekadar CRUD.

---

# 3. Frontend Skills

# Required Frontend Skills

| Skill                    | Priority |
| ------------------------ | -------- |
| Vue.js 3                 | HIGH     |
| Tailwind CSS             | HIGH     |
| State Management (Pinia) | HIGH     |
| Realtime Dashboard UI    | HIGH     |
| Data Visualization       | MEDIUM   |
| Maps Integration         | MEDIUM   |

---

# Frontend Responsibilities

## Dashboard Monitoring

Membangun:

* realtime monitoring dashboard,
* risk visualization,
* operational timeline,
* analytics UI.

---

# Critical Frontend Skills

# 1. Data Visualization

Karena dashboard sangat data-heavy.

Developer harus mampu:

* membuat chart,
* status indicators,
* operational timelines,
* alert visualization.

---

# 2. State Management

Karena:

* batch data realtime,
* alerts berubah realtime,
* monitoring bersifat dynamic.

---

# 3. Google Maps Integration

Untuk:

* ETA monitoring,
* route visualization,
* traffic analytics.

---

# Suggested Frontend Libraries

| Library    | Purpose   |
| ---------- | --------- |
| ApexCharts | charts    |
| VueUse     | utilities |
| Vue Router | routing   |
| Axios      | API       |
| Day.js     | datetime  |

---

# 4. Backend Skills

# Required Backend Skills

| Skill              | Priority |
| ------------------ | -------- |
| FastAPI            | HIGH     |
| PostgreSQL         | HIGH     |
| SQLAlchemy         | HIGH     |
| REST API Design    | HIGH     |
| JWT Authentication | HIGH     |
| Background Jobs    | MEDIUM   |
| Caching            | LOW      |

---

# Backend Responsibilities

## Operational APIs

Membangun:

* batch lifecycle API,
* risk engine API,
* alert system,
* analytics API.

---

# Critical Backend Skills

# 1. Risk Engine Development

Paling penting.

Developer harus mampu:

* membuat weighted scoring,
* exposure calculation,
* SOP violation logic,
* explainable outputs.

---

# 2. Time-Based Logic

Karena sistem heavily bergantung:

* timestamp,
* exposure duration,
* ETA,
* cumulative exposure.

---

# 3. External API Integration

Integrasi:

* BMKG API,
* Google Maps API.

---

# 5. Database Skills

# Required Skills

| Skill               | Priority |
| ------------------- | -------- |
| PostgreSQL          | HIGH     |
| Relational Modeling | HIGH     |
| Query Optimization  | MEDIUM   |
| Historical Logging  | HIGH     |
| JSONB Usage         | MEDIUM   |

---

# Database Responsibilities

## Historical Tracking

Karena:

* risk score historical,
* alerts historical,
* exposure tracking historical.

---

# Critical Concepts

# 1. Auditability

Semua perubahan harus traceable.

---

# 2. Time-Series Thinking

Temperature dan exposure bersifat time-series.

---

# 6. ML / AI Skills

# IMPORTANT

ML BUKAN PRIORITAS UTAMA.

---

# Required ML Skills

| Skill               | Priority |
| ------------------- | -------- |
| Isolation Forest    | MEDIUM   |
| Anomaly Detection   | MEDIUM   |
| Feature Engineering | HIGH     |
| Pandas              | HIGH     |
| Scikit-learn        | MEDIUM   |

---

# ML Responsibilities

## Anomaly Detection

Mendeteksi:

* abnormal delays,
* unusual exposure,
* operational spikes.

---

# Yang TIDAK Dibutuhkan

| Skill           | Reason       |
| --------------- | ------------ |
| Computer Vision | not relevant |
| CNN             | unnecessary  |
| LLM Fine-Tuning | unnecessary  |
| Deep Learning   | overkill     |

---

# Most Important ML Skill

# Feature Engineering

Karena data utama:

* structured,
* tabular,
* operational.

---

# 7. DevOps / Infrastructure Skills

# Required Skills

| Skill      | Priority |
| ---------- | -------- |
| Deployment | HIGH     |
| CI/CD      | MEDIUM   |
| Monitoring | MEDIUM   |
| Docker     | LOW      |
| Scaling    | LOW      |

---

# Infrastructure Responsibilities

## Deployment

Deploy:

* frontend,
* backend,
* monitoring stack.

---

# Monitoring

Track:

* API performance,
* errors,
* alert latency,
* uptime.

---

# Suggested Platforms

| Service  | Purpose        |
| -------- | -------------- |
| Vercel   | frontend       |
| Railway  | backend        |
| Supabase | database       |
| Sentry   | error tracking |

---

# 8. Product / Business Skills

# Required Product Thinking

Developer HARUS paham:

# Sistem ini adalah:

* operational monitoring platform,
* bukan AI gimmick.

---

# Important Thinking

## Focus On:

* operational visibility,
* explainability,
* auditability,
* monitoring.

---

# Avoid Thinking:

* chatbot AI,
* image scanner,
* “AI deteksi basi”.

---

# 9. Architecture Skills

# Required Skills

| Skill                 | Priority |
| --------------------- | -------- |
| Modular Architecture  | HIGH     |
| Event-Driven Thinking | HIGH     |
| Scalability Thinking  | MEDIUM   |
| Realtime Systems      | MEDIUM   |

---

# Important Concepts

# 1. Event-Driven Thinking

Karena:

* risk berubah ketika event berubah.

Contoh:

* pickup delay,
* temperature update,
* delivery delay.

---

# 2. Historical State

Risk harus tersimpan historical.

Jangan overwrite.

---

# 10. UX/UI Skills

# Required Skills

| Skill                       | Priority |
| --------------------------- | -------- |
| Monitoring Dashboard Design | HIGH     |
| Alert Design                | HIGH     |
| Data UX                     | HIGH     |
| Responsive Layout           | MEDIUM   |

---

# UX Objective

Dashboard HARUS:

* cepat dibaca,
* operational,
* actionable.

---

# Good UX Principles

## GOOD

* clear status colors,
* explainable alerts,
* operational timelines,
* readable analytics.

---

## BAD

* terlalu banyak AI gimmick,
* chat UI,
* random scoring visual.

---

# 11. Suggested Team Structure

# MVP Team

| Role                   | Responsibility        |
| ---------------------- | --------------------- |
| Product Owner          | operational logic     |
| Frontend Dev           | dashboard             |
| Backend Dev            | APIs & risk engine    |
| DB Engineer            | schema & optimization |
| ML Engineer (optional) | anomaly detection     |
| UI/UX                  | monitoring UX         |

---

# 12. Most Critical Skills

# TOP 5 MOST IMPORTANT

| Skill                   | Why                 |
| ----------------------- | ------------------- |
| Risk Engine Logic       | core system         |
| Time-Based Calculations | exposure tracking   |
| Operational Thinking    | product alignment   |
| Dashboard Monitoring UI | user visibility     |
| PostgreSQL Modeling     | historical tracking |

---

# 13. Skills That Matter LESS

| Skill           | Why              |
| --------------- | ---------------- |
| Deep Learning   | unnecessary      |
| Computer Vision | not core problem |
| LLM Fine-Tuning | overkill         |
| Generative AI   | not needed       |

---

# 14. Engineering Mindset Required

Developer HARUS berpikir seperti:

# “Operational Risk Monitoring Engineer”

BUKAN:

* AI engineer gimmick,
* chatbot builder,
* image classifier developer.

---

# 15. Final Skill Objective

Tujuan skillset project ini adalah:

# membangun engineering capability untuk:

* operational visibility,
* realtime monitoring,
* exposure analytics,
* explainable risk scoring,
* dan preventive food safety intelligence.
