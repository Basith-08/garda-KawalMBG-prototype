# Project Architecture

# Predictive Food Safety Operational Monitoring (MBG)

---

# 1. Architecture Overview

## Objective

Membangun scalable operational food safety intelligence platform untuk:

* realtime monitoring,
* exposure tracking,
* SOP violation detection,
* risk scoring,
* operational analytics,
* dan anomaly detection.

---

# High-Level Architecture

```text id="rjlwmx"
┌────────────────────────────┐
│        Vue.js Frontend     │
│  Dashboard + Monitoring UI │
└─────────────┬──────────────┘
              │ REST API
              ▼
┌────────────────────────────┐
│        FastAPI Backend     │
│ Authentication + Services  │
└─────────────┬──────────────┘
              │
              ▼
┌────────────────────────────┐
│     Risk Engine Layer      │
│ Rule-Based Scoring System  │
└─────────────┬──────────────┘
              │
      ┌───────┴────────┐
      ▼                ▼
┌──────────────┐ ┌────────────────┐
│ PostgreSQL   │ │ ML Layer       │
│ Supabase DB  │ │ IsolationForest│
└──────┬───────┘ └────────────────┘
       │
       ▼
┌────────────────────────────┐
│ External APIs              │
│ - BMKG API                 │
│ - Google Maps API          │
└────────────────────────────┘
```

---

# 2. Architecture Principles

# Core Principles

| Principle    | Description                    |
| ------------ | ------------------------------ |
| Explainable  | Semua risk harus explainable   |
| Operational  | Fokus operational exposure     |
| Modular      | Mudah dikembangkan             |
| Scalable     | Siap high-volume monitoring    |
| Auditable    | Semua perubahan traceable      |
| Event-Driven | Risk berubah berdasarkan event |

---

# System Characteristics

| Characteristic     | Value             |
| ------------------ | ----------------- |
| Architecture Style | Modular Monolith  |
| API Pattern        | REST              |
| Database           | Relational        |
| Risk Engine        | Rule-Based        |
| ML Usage           | Anomaly Detection |
| Realtime Strategy  | Polling           |
| Deployment         | Cloud-native      |

---

# 3. Frontend Architecture

# Frontend Stack

| Technology   | Purpose          |
| ------------ | ---------------- |
| Vue.js 3     | SPA Framework    |
| Vite         | Build Tool       |
| Tailwind CSS | Styling          |
| Pinia        | State Management |
| Vue Router   | Routing          |
| Axios        | API Requests     |

---

# Frontend Folder Structure

```text id="pcjlwm"
src/
├── api/
├── assets/
├── components/
│   ├── common/
│   ├── dashboard/
│   ├── risk/
│   ├── analytics/
│   └── maps/
├── composables/
├── layouts/
├── pages/
├── router/
├── services/
├── stores/
├── styles/
├── types/
└── utils/
```

---

# Frontend Responsibilities

# Dashboard UI

Menampilkan:

* realtime monitoring,
* risk score,
* operational timeline,
* kitchen analytics,
* alerts.

---

# State Management

Mengelola:

* authentication,
* active batches,
* alerts,
* dashboard state.

---

# API Communication

Berkomunikasi dengan:

* FastAPI backend,
* authentication endpoints,
* monitoring endpoints.

---

# Frontend Pages

| Page              | Purpose             |
| ----------------- | ------------------- |
| Login             | authentication      |
| Dashboard         | overview monitoring |
| Batch Monitoring  | realtime batches    |
| Batch Detail      | detailed exposure   |
| Kitchen Analytics | kitchen performance |
| Alerts            | operational alerts  |
| Settings          | configurations      |

---

# Core UI Components

| Component            | Purpose               |
| -------------------- | --------------------- |
| RiskBadge.vue        | LOW/MEDIUM/HIGH       |
| RiskGauge.vue        | risk visualization    |
| BatchTimeline.vue    | operational lifecycle |
| ExposureCounter.vue  | exposure duration     |
| TemperatureChart.vue | temperature graph     |
| RouteMap.vue         | Google Maps           |
| AlertPanel.vue       | active alerts         |
| KitchenAnalytics.vue | analytics cards       |

---

# 4. Backend Architecture

# Backend Stack

| Technology | Purpose        |
| ---------- | -------------- |
| FastAPI    | REST API       |
| SQLAlchemy | ORM            |
| Pydantic   | Validation     |
| JWT        | Authentication |
| Uvicorn    | ASGI server    |

---

# Backend Architecture Style

## Modular Monolith

Kenapa:

* MVP lebih cepat,
* mudah maintain,
* deployment sederhana,
* belum perlu microservices.

---

# Backend Folder Structure

```text id="arjlwm"
app/
├── api/
│   ├── auth/
│   ├── batches/
│   ├── risk/
│   ├── alerts/
│   └── analytics/
├── core/
├── db/
├── ml/
├── models/
├── rules/
├── schemas/
├── services/
├── utils/
└── main.py
```

---

# Backend Responsibilities

| Module    | Responsibility        |
| --------- | --------------------- |
| auth      | authentication        |
| batches   | operational CRUD      |
| risk      | risk calculation      |
| alerts    | alert generation      |
| analytics | operational analytics |
| services  | external integrations |
| ml        | anomaly detection     |

---

# 5. Risk Engine Architecture

# Objective

Menghitung operational food safety risk.

---

# Risk Engine Flow

```text id="xbjlwm"
Food Batch Event
        ↓
Exposure Calculation
        ↓
Temperature Analysis
        ↓
Food Sensitivity Analysis
        ↓
Weighted Scoring
        ↓
Risk Classification
        ↓
Alert Generation
```

---

# Risk Engine Modules

| Module         | Purpose           |
| -------------- | ----------------- |
| exposure.py    | exposure duration |
| temperature.py | temperature risk  |
| food_risk.py   | food sensitivity  |
| packaging.py   | packaging risk    |
| scoring.py     | weighted scoring  |
| violations.py  | SOP detection     |

---

# Risk Formula

```text id="pmjlwm"
Final Risk =
(Time × 0.35)
+ (Temperature × 0.35)
+ (Food × 0.20)
+ (Packaging × 0.10)
```

---

# Risk Categories

| Score | Status |
| ----- | ------ |
| 0–39  | LOW    |
| 40–69 | MEDIUM |
| 70+   | HIGH   |

---

# 6. Database Architecture

# Database Type

* PostgreSQL
* Managed by Supabase

---

# Database Design Pattern

## Relational + Historical Logging

Karena:

* operational tracking membutuhkan relational integrity,
* auditability penting,
* exposure history harus tersimpan.

---

# Core Tables

| Table               | Purpose              |
| ------------------- | -------------------- |
| users               | authentication       |
| kitchens            | kitchen data         |
| menu_items          | food sensitivity     |
| food_batches        | operational tracking |
| distribution_routes | distribution         |
| temperature_logs    | temperature history  |
| risk_scores         | risk history         |
| alerts              | alerts               |
| anomaly_logs        | anomaly history      |
| audit_logs          | audit trail          |

---

# Database Relationships

```text id="a9jlwm"
kitchens
    └── food_batches
            ├── menu_items
            ├── distribution_routes
            ├── temperature_logs
            ├── risk_scores
            ├── alerts
            └── anomaly_logs
```

---

# 7. External Integration Architecture

# BMKG Integration

## Purpose

Mengambil:

* ambient temperature,
* humidity,
* weather conditions.

---

# Flow

```text id="ydjlwm"
BMKG API
    ↓
Weather Service
    ↓
Environmental Risk Multiplier
    ↓
Risk Recalculation
```

---

# Google Maps Integration

## Purpose

Mengukur:

* ETA,
* traffic,
* route delay,
* exposure escalation.

---

# Flow

```text id="0kjlwm"
Google Maps API
        ↓
Route Service
        ↓
ETA Monitoring
        ↓
Delay Detection
        ↓
Risk Escalation
```

---

# 8. Machine Learning Architecture

# Objective

Mendeteksi operational anomaly.

---

# Why ML Is Secondary

Karena:

* sistem utama adalah rule engine,
* ML hanya membantu anomaly detection.

---

# ML Flow

```text id="5jlwmx"
Operational Data
        ↓
Feature Extraction
        ↓
Isolation Forest
        ↓
Anomaly Score
        ↓
Alert Generation
```

---

# ML Components

| Component            | Purpose             |
| -------------------- | ------------------- |
| training_pipeline.py | model training      |
| predictor.py         | prediction          |
| feature_builder.py   | feature engineering |
| isolation_forest.py  | anomaly model       |

---

# Feature Vector

```python
[
 exposure_time,
 avg_temperature,
 max_temperature,
 delivery_delay,
 route_duration,
 ambient_temp,
 final_risk_score
]
```

---

# 9. Authentication Architecture

# Authentication Flow

```text id="jlwmx6"
Login Request
      ↓
JWT Generation
      ↓
Frontend Storage
      ↓
Protected API Access
```

---

# Authorization

## RBAC

| Role     | Access           |
| -------- | ---------------- |
| admin    | full access      |
| kitchen  | batch management |
| operator | monitoring       |
| auditor  | read-only        |

---

# Security Features

| Feature       | Purpose          |
| ------------- | ---------------- |
| JWT           | authentication   |
| bcrypt        | password hashing |
| RBAC          | authorization    |
| rate limiting | abuse prevention |
| audit logs    | traceability     |

---

# 10. Alerting Architecture

# Alert Flow

```text id="jlwmx7"
Risk Recalculation
        ↓
Threshold Check
        ↓
Alert Generator
        ↓
Database Storage
        ↓
Dashboard Notification
```

---

# Alert Types

| Alert          | Trigger     |
| -------------- | ----------- |
| HIGH_RISK      | score >70   |
| DELIVERY_DELAY | delay       |
| SOP_VIOLATION  | violation   |
| HOLDING_ALERT  | holding >2h |
| ANOMALY_ALERT  | ML anomaly  |

---

# 11. Realtime Architecture

# MVP Strategy

## Polling-Based Realtime

Kenapa:

* sederhana,
* cepat implementasi,
* cukup untuk MVP.

---

# Polling Intervals

| Resource         | Interval |
| ---------------- | -------- |
| dashboard        | 30s      |
| alerts           | 15s      |
| risk score       | 30s      |
| route monitoring | 60s      |

---

# Future Upgrade

## WebSocket / Realtime Streaming

Setelah:

* scale meningkat,
* active monitoring tinggi.

---

# 12. Logging & Observability Architecture

# Logging Flow

```text id="jlwmx8"
Application Event
        ↓
Structured Logging
        ↓
Monitoring Stack
        ↓
Analytics & Debugging
```

---

# Required Logs

| Log        | Purpose          |
| ---------- | ---------------- |
| API Logs   | request tracing  |
| Risk Logs  | exposure history |
| Alert Logs | alerts           |
| Auth Logs  | security         |
| ML Logs    | anomaly tracking |

---

# Monitoring Tools

| Tool       | Purpose          |
| ---------- | ---------------- |
| Sentry     | error monitoring |
| Grafana    | dashboards       |
| Prometheus | metrics          |

---

# 13. Deployment Architecture

# Frontend Deployment

Recommended:

* Vercel
* Netlify

---

# Backend Deployment

Recommended:

* Railway
* Render
* Fly.io

---

# Database

* Supabase PostgreSQL

---

# CI/CD Flow

```text id="jlwmx9"
Git Push
    ↓
GitHub Actions
    ↓
Build & Test
    ↓
Deploy
```

---

# 14. Scalability Considerations

# MVP Scale

Designed for:

* hundreds of kitchens,
* thousands of batches/day,
* realtime dashboard monitoring.

---

# Scalability Strategy

## Horizontal Scaling

Future:

* split services,
* queue processing,
* event streaming.

---

# Future Improvements

| Future     | Purpose         |
| ---------- | --------------- |
| Redis      | caching         |
| Celery     | async jobs      |
| Kafka      | event streaming |
| WebSockets | realtime        |
| Kubernetes | orchestration   |

---

# 15. Architecture Decisions

# Why Rule-Based First?

Karena:

* explainable,
* aligned with HACCP,
* easier validation,
* low operational complexity.

---

# Why Isolation Forest?

Karena:

* anomaly detection cocok,
* tidak butuh labeled data besar,
* ringan untuk MVP.

---

# Why Modular Monolith?

Karena:

* MVP lebih cepat,
* maintainable,
* deployment sederhana,
* belum butuh distributed architecture.

---

# Why PostgreSQL?

Karena:

* relational integrity,
* auditability,
* historical tracking,
* strong analytics support.

---

# 16. Final Architecture Objective

Tujuan architecture ini bukan:

> “membangun AI scanner makanan basi”

Tetapi:

# membangun operational food safety intelligence platform yang:

* realtime,
* explainable,
* auditable,
* scalable,
* dan mampu memberikan early warning sebelum makanan menjadi unsafe untuk dikonsumsi.
