# Product Requirements Document (PRD)

# Predictive Food Safety Operational Monitoring (MBG)

---

# 1. Product Overview

## Product Name

**Predictive Food Safety Operational Monitoring**

Alternative positioning:

* Operational Food Safety Intelligence Platform
* HACCP-Based Distribution Monitoring System

---

## Product Summary

Predictive Food Safety Operational Monitoring adalah platform operational intelligence untuk memonitor food safety pada distribusi makanan skala besar.

Sistem ini membantu:

* memonitor exposure makanan,
* mendeteksi SOP violation,
* menghitung realtime food safety risk,
* dan memberikan alert sebelum makanan menjadi unsafe untuk dikonsumsi.

---

# 2. Problem Statement

## Background

Distribusi makanan skala besar memiliki risiko tinggi terhadap:

* keterlambatan distribusi,
* suhu lingkungan tinggi,
* improper holding,
* prolonged exposure,
* dan unsafe food consumption.

Saat ini sebagian besar operasional:

* tidak memiliki realtime visibility,
* tidak memiliki exposure tracking,
* dan tidak memiliki early warning system.

Akibatnya:

* makanan bisa menjadi unsafe,
* namun operator baru mengetahui setelah terjadi incident atau complaint.

---

## Core Problem

```text id="x1m7oq"
Large-scale food distribution operations lack realtime operational visibility and predictive food safety monitoring, making it difficult to detect unsafe exposure conditions before food is consumed.
```

---

# 3. Product Vision

## Vision

Membangun platform operational intelligence yang mampu:

* memberikan visibility realtime,
* mengurangi probabilitas makanan unsafe,
* meningkatkan SOP compliance,
* dan membantu preventive food safety monitoring.

---

# 4. Goals & Objectives

# Primary Goals

| Goal                   | Description                                   |
| ---------------------- | --------------------------------------------- |
| Operational Visibility | Monitoring lifecycle distribusi makanan       |
| Risk Monitoring        | Menghitung realtime exposure risk             |
| SOP Compliance         | Mendeteksi pelanggaran SOP                    |
| Early Warning          | Alert sebelum makanan unsafe                  |
| Operational Analytics  | Monitoring kitchen & distribution performance |

---

# Non-Goals

## Product TIDAK Fokus Pada:

| Non-Goal                | Reason                       |
| ----------------------- | ---------------------------- |
| Computer Vision         | Tidak reliable               |
| AI deteksi basi visual  | Tidak scientific             |
| Deep Learning           | Tidak dibutuhkan untuk MVP   |
| Consumer App            | Fokus operational monitoring |
| Predictive microbiology | Scope terlalu besar          |

---

# 5. Target Users

# Primary Users

## 1. Kitchen Operator

### Responsibilities

* create food batch,
* update operational timeline,
* monitor risk status.

### Pain Points

* tidak tahu batch paling risky,
* sulit monitor exposure,
* tidak tahu kapan risk meningkat.

---

## 2. Distribution Operator

### Responsibilities

* pickup batch,
* delivery monitoring,
* route tracking.

### Pain Points

* tidak tahu keterlambatan berbahaya atau tidak,
* tidak ada ETA-based exposure monitoring.

---

## 3. Supervisors / Auditors

### Responsibilities

* SOP monitoring,
* kitchen performance monitoring,
* operational analytics.

### Pain Points

* tidak ada centralized visibility,
* sulit audit distribusi realtime.

---

## 4. Program Management

### Responsibilities

* operational oversight,
* risk monitoring,
* compliance monitoring.

### Pain Points

* sulit memonitor distribusi skala besar,
* tidak ada predictive visibility.

---

# 6. User Stories

# Kitchen Operator

```text id="rw1tdw"
Sebagai kitchen operator,
saya ingin melihat realtime risk score batch makanan,
agar saya tahu batch mana yang harus diprioritaskan.
```

---

# Distribution Operator

```text id="3h4jho"
Sebagai distribution operator,
saya ingin mengetahui apakah keterlambatan distribusi meningkatkan food safety risk,
agar saya bisa mengambil tindakan lebih cepat.
```

---

# Supervisor

```text id="3rhmco"
Sebagai supervisor,
saya ingin melihat dashboard operational risk,
agar saya dapat memonitor kitchen dan distribusi secara realtime.
```

---

# Auditor

```text id="bgx9zb"
Sebagai auditor,
saya ingin melihat histori SOP violations dan exposure logs,
agar saya dapat melakukan audit food safety.
```

---

# 7. Product Scope (MVP)

# Included Features

| Feature                 | Included      |
| ----------------------- | ------------- |
| Authentication          | YES           |
| Food Batch CRUD         | YES           |
| Operational Timeline    | YES           |
| Rule-Based Risk Engine  | YES           |
| SOP Violation Detection | YES           |
| Dashboard Monitoring    | YES           |
| BMKG Integration        | YES           |
| Google Maps Integration | YES           |
| Alert System            | YES           |
| Basic Anomaly Detection | Optional MVP+ |

---

# Excluded Features

| Feature                | Excluded |
| ---------------------- | -------- |
| Computer Vision        | NO       |
| AI food image analysis | NO       |
| Deep Learning          | NO       |
| Mobile App             | NO       |
| QR Scanning            | NO       |
| BLE Sensors            | NO       |
| WhatsApp Bot           | NO       |

---

# 8. Core Features

# Feature 1 — Authentication & Authorization

## Description

Mengamankan akses dashboard berdasarkan role.

---

## Requirements

### Functional

* login,
* logout,
* JWT authentication,
* role-based access control.

---

## Roles

| Role     | Access           |
| -------- | ---------------- |
| admin    | full access      |
| kitchen  | batch management |
| operator | monitoring       |
| auditor  | read-only        |

---

# Feature 2 — Food Batch Management

## Description

Mencatat operational lifecycle makanan.

---

## Functional Requirements

### Create Batch

Input:

* kitchen,
* menu,
* cooked time,
* packaging type.

---

### Update Batch Timeline

Update:

* packaged_at,
* pickup_at,
* delivered_at,
* consumed_at.

---

### View Batch

Display:

* risk score,
* exposure duration,
* SOP violations,
* operational timeline.

---

# Feature 3 — Rule-Based Risk Engine

## Description

Menghitung operational food safety risk.

---

## Risk Factors

| Factor                    | Description          |
| ------------------------- | -------------------- |
| Time Exposure             | Lama exposure        |
| Temperature Exposure      | Suhu exposure        |
| Food Sensitivity          | Risiko jenis makanan |
| Packaging Risk            | Risiko packaging     |
| Environmental Temperature | Suhu lingkungan      |

---

## Risk Formula

```text id="6pjlwm"
Final Risk =
(Time × 0.35)
+ (Temperature × 0.35)
+ (Food × 0.20)
+ (Packaging × 0.10)
```

---

## Risk Status

| Score | Status |
| ----- | ------ |
| 0–39  | LOW    |
| 40–69 | MEDIUM |
| 70+   | HIGH   |

---

# Feature 4 — SOP Violation Detection

## Description

Mendeteksi pelanggaran SOP distribusi.

---

## Violations

| Violation         | Description                       |
| ----------------- | --------------------------------- |
| Delayed Pickup    | pickup terlalu lama               |
| Excessive Holding | holding terlalu lama              |
| Delivery Delay    | distribusi terlambat              |
| Extended Exposure | danger-zone exposure terlalu lama |

---

# Feature 5 — Dashboard Monitoring

## Description

Memberikan operational visibility realtime.

---

## Dashboard Overview

Display:

* active batches,
* HIGH risk batches,
* delayed deliveries,
* active alerts.

---

## Batch Monitoring

Display:

* batch lifecycle,
* exposure duration,
* risk score,
* operational status.

---

## Kitchen Analytics

Display:

* average risk,
* delay frequency,
* SOP violations,
* anomaly frequency.

---

# Feature 6 — BMKG Integration

## Description

Menggunakan data cuaca sebagai exposure factor.

---

## Functional Requirements

Fetch:

* ambient temperature,
* humidity,
* weather condition.

---

## Usage

Ambient temperature digunakan untuk:

* temperature exposure multiplier,
* operational risk escalation.

---

# Feature 7 — Google Maps Integration

## Description

Monitoring route dan keterlambatan distribusi.

---

## Functional Requirements

Fetch:

* ETA,
* traffic condition,
* route duration,
* distance.

---

## Usage

Digunakan untuk:

* delay detection,
* exposure estimation,
* operational analytics.

---

# Feature 8 — Alert System

## Description

Memberikan warning sebelum makanan menjadi unsafe.

---

## Alert Types

| Alert          | Trigger        |
| -------------- | -------------- |
| HIGH RISK      | score >70      |
| HOLDING ALERT  | holding >2h    |
| DELIVERY ALERT | delay detected |
| SOP ALERT      | SOP violation  |

---

# 9. Functional Requirements

# Authentication

| ID     | Requirement            |
| ------ | ---------------------- |
| FR-001 | User dapat login       |
| FR-002 | User dapat logout      |
| FR-003 | Sistem menggunakan JWT |

---

# Batch Management

| ID     | Requirement                       |
| ------ | --------------------------------- |
| FR-004 | User dapat membuat batch          |
| FR-005 | User dapat update timeline        |
| FR-006 | Sistem menyimpan exposure history |

---

# Risk Engine

| ID     | Requirement                         |
| ------ | ----------------------------------- |
| FR-007 | Sistem menghitung realtime risk     |
| FR-008 | Sistem mendeteksi SOP violation     |
| FR-009 | Sistem menghasilkan LOW/MEDIUM/HIGH |

---

# Dashboard

| ID     | Requirement                             |
| ------ | --------------------------------------- |
| FR-010 | Dashboard menampilkan realtime batches  |
| FR-011 | Dashboard menampilkan alerts            |
| FR-012 | Dashboard menampilkan kitchen analytics |

---

# 10. Non-Functional Requirements

| Requirement        | Target |
| ------------------ | ------ |
| API Response       | <500ms |
| Dashboard Load     | <3s    |
| Uptime             | >99%   |
| Risk Recalculation | <2s    |

---

# 11. System Architecture

```text id="x7m4sd"
Vue.js Dashboard
    ↓
FastAPI Backend
    ↓
Rule-Based Risk Engine
    ↓
Isolation Forest (Optional MVP+)
    ↓
Supabase PostgreSQL
    ↓
BMKG API + Google Maps API
```

---

# 12. Database Requirements

# Core Tables

| Table               | Purpose              |
| ------------------- | -------------------- |
| users               | authentication       |
| kitchens            | kitchen data         |
| menu_items          | food classification  |
| food_batches        | operational tracking |
| distribution_routes | delivery tracking    |
| temperature_logs    | temperature history  |
| risk_scores         | risk history         |
| alerts              | alert history        |

---

# 13. API Requirements

# Authentication

```text id="w2ptt0"
POST /auth/login
POST /auth/register
```

---

# Batches

```text id="sg2yur"
GET /batches
POST /batches
PUT /batches/{id}
```

---

# Risk

```text id="dct1ud"
GET /risk/{batch_id}
POST /risk/recalculate
```

---

# Alerts

```text id="tjlwmq"
GET /alerts
POST /alerts/acknowledge
```

---

# 14. UI/UX Requirements

# Dashboard Requirements

## Must Have

* responsive,
* realtime monitoring,
* clear risk indicators,
* operational timeline.

---

# UI Components

| Component       | Purpose            |
| --------------- | ------------------ |
| RiskBadge       | risk visualization |
| BatchTimeline   | lifecycle          |
| ExposureCounter | duration           |
| AlertPanel      | alerts             |
| RouteMap        | route visibility   |

---

# 15. Analytics Requirements

# Kitchen Analytics

Metrics:

* average risk,
* delay frequency,
* SOP violations,
* high-risk batches.

---

# Distribution Analytics

Metrics:

* average ETA,
* delay duration,
* traffic impact,
* route exposure.

---

# 16. MVP Success Metrics

# Technical Metrics

| Metric           | Target   |
| ---------------- | -------- |
| API response     | <500ms   |
| Dashboard load   | <3s      |
| Risk calculation | realtime |

---

# Operational Metrics

| Metric                 | Target |
| ---------------------- | ------ |
| Exposure visibility    | YES    |
| SOP detection          | YES    |
| Operational monitoring | YES    |
| Early warning          | YES    |

---

# 17. Risks & Assumptions

# Risks

| Risk                     | Impact            |
| ------------------------ | ----------------- |
| inaccurate timestamps    | wrong risk score  |
| manual data entry        | inconsistent data |
| missing temperature data | lower accuracy    |

---

# Assumptions

* kitchen operator menginput data dengan benar,
* internet tersedia,
* BMKG API accessible,
* Google Maps API active.

---

# 18. Future Roadmap

# Phase 2

* QR batch tracking,
* mobile app,
* BLE thermometer integration.

---

# Phase 3

* predictive ML,
* spoilage forecasting,
* advanced anomaly detection.

---

# Phase 4

* national monitoring dashboard,
* regional analytics,
* operational benchmarking.

---

# 19. Final Product Positioning

## Recommended Positioning

```text id="1sqrxr"
Predictive Food Safety Operational Monitoring
```

atau:

```text id="ntzbb7"
Operational Food Safety Intelligence Platform
```

---

# Avoid Positioning

```text id="mjlwmz"
AI Deteksi Makanan Basi
```

---

# 20. Final Success Definition

Success metric utama sistem ini bukan:

> “AI mengetahui makanan basi”

Tetapi:

> “Sistem mampu memberikan operational food safety visibility dan early warning sebelum makanan menjadi unsafe untuk dikonsumsi.”
