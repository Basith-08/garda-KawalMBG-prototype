# Technical Requirements Document (TRD)

# Predictive Food Safety Operational Monitoring (MBG)

---

# 1. Document Overview

## Purpose

Dokumen ini menjelaskan technical architecture, infrastructure, implementation requirements, dan engineering specification untuk sistem:

# Predictive Food Safety Operational Monitoring

Dokumen ini menjadi acuan untuk:

* frontend development,
* backend development,
* database implementation,
* deployment,
* monitoring,
* dan scalability planning.

---

# 2. System Overview

## System Objective

Membangun platform operational food safety intelligence yang mampu:

* memonitor lifecycle distribusi makanan,
* menghitung realtime operational risk,
* mendeteksi SOP violation,
* melakukan anomaly detection,
* dan memberikan alert sebelum makanan menjadi unsafe.

---

# 3. High-Level Architecture

```text id="ndhkt8"
Frontend (Vue.js + Tailwind)
        ↓
FastAPI Backend API
        ↓
Risk Engine Service
        ↓
PostgreSQL (Supabase)
        ↓
External Services
 ├── BMKG API
 └── Google Maps API
        ↓
Optional ML Layer
 └── Isolation Forest
```

---

# 4. Technology Stack

# Frontend

| Technology   | Purpose          |
| ------------ | ---------------- |
| Vue.js 3     | SPA frontend     |
| Vite         | Build tool       |
| Tailwind CSS | Styling          |
| Pinia        | State management |
| Vue Router   | Routing          |
| Axios        | API requests     |
| Day.js       | Date handling    |

---

# Backend

| Technology | Purpose        |
| ---------- | -------------- |
| FastAPI    | REST API       |
| SQLAlchemy | ORM            |
| Pydantic   | Validation     |
| JWT        | Authentication |
| Uvicorn    | ASGI server    |

---

# Database

| Technology          | Purpose          |
| ------------------- | ---------------- |
| Supabase PostgreSQL | Main database    |
| Supabase Storage    | Optional storage |

---

# Machine Learning

| Technology       | Purpose               |
| ---------------- | --------------------- |
| Scikit-learn     | ML framework          |
| Isolation Forest | Anomaly detection     |
| Pandas           | Data processing       |
| NumPy            | Numerical computation |

---

# External Services

| Service         | Purpose                |
| --------------- | ---------------------- |
| BMKG API        | Weather & temperature  |
| Google Maps API | ETA & route monitoring |

---

# 5. Frontend Technical Requirements

# Frontend Architecture

```text id="xptskc"
src/
├── api/
├── assets/
├── components/
│   ├── common/
│   ├── dashboard/
│   ├── risk/
│   └── maps/
├── composables/
├── layouts/
├── pages/
├── router/
├── services/
├── stores/
├── types/
└── utils/
```

---

# Frontend Requirements

# FR-001 — Authentication UI

## Description

Frontend harus menyediakan:

* login,
* logout,
* session persistence,
* protected routes.

---

## Technical Requirements

* JWT token storage,
* auth middleware,
* automatic logout,
* token refresh handling.

---

# FR-002 — Dashboard Monitoring

## Description

Dashboard realtime monitoring food batches.

---

## Requirements

Display:

* active batches,
* HIGH risk batches,
* alerts,
* kitchen analytics,
* operational timeline.

---

# FR-003 — Batch Monitoring Page

## Requirements

Display:

* batch lifecycle,
* timestamps,
* risk score,
* exposure duration,
* SOP violations.

---

# FR-004 — Route Monitoring

## Requirements

* Google Maps integration,
* ETA display,
* traffic monitoring,
* delay alerts.

---

# FR-005 — Realtime Risk Updates

## Requirements

* polling every 30–60s,
* dynamic risk updates,
* realtime alerts.

---

# UI Components

| Component            | Purpose            |
| -------------------- | ------------------ |
| RiskBadge.vue        | LOW/MEDIUM/HIGH    |
| RiskGauge.vue        | risk visualization |
| BatchTimeline.vue    | lifecycle tracking |
| ExposureCounter.vue  | exposure duration  |
| TemperatureChart.vue | temperature graph  |
| RouteMap.vue         | maps integration   |
| AlertPanel.vue       | alerts             |
| KitchenAnalytics.vue | analytics          |

---

# 6. Backend Technical Requirements

# Backend Architecture

```text id="xocjmo"
app/
├── api/
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

| Module       | Responsibility    |
| ------------ | ----------------- |
| auth         | authentication    |
| batches      | CRUD              |
| risk_engine  | scoring           |
| alerts       | notifications     |
| bmkg_service | weather           |
| maps_service | ETA               |
| ml           | anomaly detection |

---

# BR-001 — Authentication API

## Endpoints

```text id="8o3g9o"
POST /auth/login
POST /auth/register
POST /auth/refresh
```

---

## Requirements

* JWT authentication,
* password hashing,
* refresh token,
* role validation.

---

# BR-002 — Food Batch API

## Endpoints

```text id="vcm9so"
GET /batches
POST /batches
GET /batches/{id}
PUT /batches/{id}
DELETE /batches/{id}
```

---

## Requirements

* create food batch,
* update timestamps,
* retrieve exposure data,
* store operational history.

---

# BR-003 — Risk Engine API

## Endpoints

```text id="gynrju"
GET /risk/{batch_id}
POST /risk/recalculate
```

---

## Requirements

* calculate risk,
* calculate exposure duration,
* classify LOW/MEDIUM/HIGH,
* detect SOP violations.

---

# BR-004 — Alert API

## Endpoints

```text id="0jvkhw"
GET /alerts
POST /alerts/acknowledge
```

---

## Requirements

* realtime alerts,
* alert persistence,
* alert acknowledgment.

---

# 7. Database Technical Requirements

# Database Engine

* PostgreSQL 15+
* Supabase managed database

---

# Core Tables

| Table               | Purpose              |
| ------------------- | -------------------- |
| users               | authentication       |
| kitchens            | kitchen data         |
| menu_items          | food sensitivity     |
| food_batches        | operational tracking |
| distribution_routes | delivery monitoring  |
| temperature_logs    | temperature history  |
| risk_scores         | risk history         |
| alerts              | alert persistence    |
| anomaly_logs        | anomaly history      |

---

# users

| Column        | Type      |
| ------------- | --------- |
| id            | UUID      |
| email         | VARCHAR   |
| password_hash | TEXT      |
| role          | VARCHAR   |
| created_at    | TIMESTAMP |

---

# kitchens

| Column    | Type    |
| --------- | ------- |
| id        | UUID    |
| name      | VARCHAR |
| address   | TEXT    |
| latitude  | FLOAT   |
| longitude | FLOAT   |
| capacity  | INTEGER |

---

# menu_items

| Column          | Type    |
| --------------- | ------- |
| id              | UUID    |
| name            | VARCHAR |
| category        | VARCHAR |
| base_risk_score | INTEGER |
| moisture_level  | INTEGER |

---

# food_batches

| Column       | Type      |
| ------------ | --------- |
| id           | UUID      |
| kitchen_id   | UUID      |
| menu_item_id | UUID      |
| cooked_at    | TIMESTAMP |
| packaged_at  | TIMESTAMP |
| pickup_at    | TIMESTAMP |
| delivered_at | TIMESTAMP |
| consumed_at  | TIMESTAMP |

---

# risk_scores

| Column            | Type    |
| ----------------- | ------- |
| id                | UUID    |
| food_batch_id     | UUID    |
| time_score        | INTEGER |
| temperature_score | INTEGER |
| final_score       | INTEGER |
| risk_status       | VARCHAR |

---

# 8. Rule-Based Risk Engine

# Objective

Menghitung operational food safety risk.

---

# Risk Factors

## Time Exposure

| Duration | Score |
| -------- | ----- |
| <1h      | 10    |
| 1–2h     | 30    |
| 2–4h     | 60    |
| >4h      | 90    |

---

## Temperature Exposure

| Temperature | Score |
| ----------- | ----- |
| <5°C        | 5     |
| 5–20°C      | 20    |
| 20–40°C     | 60    |
| >40°C       | 85    |

---

## Food Sensitivity

| Food Type    | Score |
| ------------ | ----- |
| dry_food     | 10    |
| egg          | 30    |
| rice         | 50    |
| chicken      | 70    |
| seafood      | 85    |
| coconut_milk | 90    |

---

## Packaging Risk

| Packaging | Score |
| --------- | ----- |
| vacuum    | 5     |
| sealed    | 15    |
| standard  | 35    |
| open      | 70    |

---

# Risk Formula

```text id="8gwjlwm"
Final Risk =
(Time × 0.35)
+ (Temperature × 0.35)
+ (Food × 0.20)
+ (Packaging × 0.10)
```

---

# Risk Status

| Score | Status |
| ----- | ------ |
| 0–39  | LOW    |
| 40–69 | MEDIUM |
| 70+   | HIGH   |

---

# Risk Engine Functions

```python
calculate_time_exposure()

calculate_temperature_risk()

calculate_food_risk()

calculate_packaging_risk()

calculate_final_score()

get_risk_status()
```

---

# 9. BMKG Integration

# Objective

Mengambil realtime environmental data.

---

# Requirements

Fetch:

* ambient temperature,
* humidity,
* weather condition.

---

# Service File

```text id="yyg3cb"
app/services/bmkg_service.py
```

---

# Polling Interval

* every 30 minutes

---

# Failure Handling

* retry mechanism,
* cached fallback response,
* logging failures.

---

# 10. Google Maps Integration

# Objective

Mengukur operational delay.

---

# Features

| Feature         | Purpose             |
| --------------- | ------------------- |
| ETA             | exposure estimation |
| Traffic         | delay detection     |
| Distance Matrix | route analytics     |

---

# Service File

```text id="wjlwmx"
app/services/maps_service.py
```

---

# Refresh Interval

* every 5–10 minutes

---

# 11. Machine Learning Layer (Optional MVP+)

# Objective

Mendeteksi operational anomalies.

---

# ML Model

* Isolation Forest

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

# File Structure

```text id="vjlwmf"
app/ml/
├── isolation_forest.py
├── training_pipeline.py
└── predictor.py
```

---

# Training Frequency

* weekly retraining

---

# Output

```json
{
  "anomaly_score": 0.87,
  "anomaly_type": "abnormal delivery delay"
}
```

---

# 12. Alerting System

# Alert Types

| Alert          | Trigger        |
| -------------- | -------------- |
| HIGH RISK      | score >70      |
| HOLDING ALERT  | holding >2h    |
| DELIVERY ALERT | delay detected |
| SOP ALERT      | SOP violation  |
| ANOMALY ALERT  | ML anomaly     |

---

# Notification Channels

| Channel         | MVP |
| --------------- | --- |
| Dashboard Popup | YES |
| Email           | YES |
| WhatsApp        | NO  |
| SMS             | NO  |

---

# 13. Security Requirements

# Authentication

* JWT access token,
* refresh token,
* secure password hashing.

---

# Authorization

* RBAC (Role-Based Access Control)

---

# API Security

* request validation,
* rate limiting,
* CORS policy,
* input sanitization.

---

# Logging

* audit logging,
* auth logging,
* risk calculation logs.

---

# 14. Performance Requirements

| Requirement        | Target   |
| ------------------ | -------- |
| API response       | <500ms   |
| Dashboard load     | <3s      |
| Risk recalculation | <2s      |
| Alert latency      | realtime |

---

# 15. Reliability Requirements

# Requirements

* retry external APIs,
* fallback cached weather,
* graceful degradation,
* database backup.

---

# Backup Strategy

* daily DB backup,
* weekly snapshot.

---

# 16. Monitoring & Observability

# Required Logs

| Log        | Purpose           |
| ---------- | ----------------- |
| API Logs   | request tracking  |
| Risk Logs  | exposure history  |
| Alert Logs | alerts            |
| ML Logs    | anomaly detection |
| Error Logs | debugging         |

---

# Monitoring Tools

| Tool       | Purpose          |
| ---------- | ---------------- |
| Sentry     | error monitoring |
| Grafana    | dashboards       |
| Prometheus | metrics          |

---

# 17. Cron Jobs

| Job                | Frequency    |
| ------------------ | ------------ |
| Risk recalculation | every 5 min  |
| Weather sync       | every 30 min |
| Alert processing   | every 1 min  |
| ML retraining      | weekly       |

---

# 18. Testing Requirements

# Backend Testing

| Test             | Purpose         |
| ---------------- | --------------- |
| Unit Test        | validate logic  |
| Integration Test | API testing     |
| ML Validation    | anomaly testing |

---

# Frontend Testing

| Test           | Purpose       |
| -------------- | ------------- |
| Component Test | UI validation |
| Route Test     | navigation    |
| Dashboard Test | rendering     |

---

# 19. Deployment Requirements

# Frontend

Recommended:

* Vercel
* Netlify

---

# Backend

Recommended:

* Railway
* Render
* Fly.io

---

# Database

* Supabase PostgreSQL

---

# CI/CD

Suggested:

* GitHub Actions,
* Docker,
* automated deployment.

---

# 20. MVP Technical Scope

# Included

| Feature                 | MVP |
| ----------------------- | --- |
| Authentication          | YES |
| Food Batch CRUD         | YES |
| Rule-Based Risk Engine  | YES |
| Dashboard Monitoring    | YES |
| BMKG Integration        | YES |
| Google Maps Integration | YES |
| Alerts                  | YES |

---

# Excluded

| Feature         | Reason       |
| --------------- | ------------ |
| Computer Vision | unnecessary  |
| Deep Learning   | overkill     |
| Mobile App      | outside MVP  |
| IoT Sensor      | future phase |

---

# 21. Future Technical Roadmap

# Phase 2

* QR batch tracking,
* BLE thermometer,
* mobile operator app.

---

# Phase 3

* predictive ML,
* spoilage forecasting,
* route optimization.

---

# Phase 4

* nationwide monitoring,
* regional analytics,
* advanced benchmarking.

---

# 22. Final Technical Objective

Tujuan technical system ini bukan:

> “mendeteksi makanan basi menggunakan AI”

Tetapi:

> “membangun realtime operational food safety intelligence system yang mampu memberikan visibility, risk monitoring, dan early warning sebelum makanan menjadi unsafe untuk dikonsumsi.”
