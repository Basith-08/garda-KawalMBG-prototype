# MVP Scope — Predictive Food Safety Operational Monitoring

## MVP Objective

Tujuan MVP bukan membuat:

* AI deteksi makanan basi,
* machine learning kompleks,
* atau predictive spoilage model.

Tujuan MVP adalah:

# Membuktikan bahwa sistem mampu:

* memonitor operational food safety,
* menghitung realtime risk,
* mendeteksi SOP violation,
* dan memberikan operational visibility.

---

# MVP Core Problem

```text id="f4ew4n"
Operator distribusi makanan tidak memiliki visibility realtime terhadap food safety risk selama proses distribusi.
```

---

# MVP Success Criteria

MVP dianggap berhasil jika sistem mampu:

* menunjukkan batch berisiko tinggi,
* mendeteksi keterlambatan distribusi,
* menghitung exposure risk,
* memberikan alert sebelum makanan dikonsumsi,
* dan menampilkan operational timeline.

---

# MVP Scope Boundary

# MVP HARUS Fokus Pada:

| Fokus                   | Included |
| ----------------------- | -------- |
| Risk Monitoring         | YES      |
| SOP Violation Detection | YES      |
| Operational Timeline    | YES      |
| Realtime Dashboard      | YES      |
| BMKG Integration        | YES      |
| Google Maps ETA         | YES      |
| Rule-Based Scoring      | YES      |

---

# MVP TIDAK Fokus Pada:

| Feature               | Excluded |
| --------------------- | -------- |
| Computer Vision       | NO       |
| AI Deteksi Basi       | NO       |
| Deep Learning         | NO       |
| IoT Sensor            | NO       |
| Predictive ML Complex | NO       |
| Mobile App            | NO       |
| QR Tracking           | NO       |
| WhatsApp Bot          | NO       |

---

# MVP SYSTEM FLOW

```text id="wq9hr2"
Kitchen Input
    ↓
Create Food Batch
    ↓
Track Operational Timeline
    ↓
Calculate Risk Score
    ↓
Detect SOP Violations
    ↓
Show Dashboard Monitoring
    ↓
Trigger Alerts
```

---

# MVP USER ROLES

# 1. Admin

## Access

* full dashboard,
* manage kitchens,
* manage menu items,
* monitor all batches,
* analytics.

---

# 2. Kitchen Operator

## Access

* create food batch,
* update operational timestamps,
* monitor risk status.

---

# 3. Distribution Operator

## Access

* update delivery status,
* monitor route,
* view alerts.

---

# 4. Auditor / Supervisor

## Access

* monitoring only,
* analytics,
* SOP violation review.

---

# MVP CORE FEATURES

# FEATURE 1 — Authentication

## Objective

Mengamankan akses dashboard berdasarkan role.

---

## Included

* JWT login,
* role-based access,
* protected routes,
* session persistence.

---

## Excluded

* OAuth,
* SSO,
* multi-factor authentication.

---

# FEATURE 2 — Food Batch Management

# Objective

Mencatat operational lifecycle makanan.

---

# Included

## Create Batch

Input:

* menu,
* kitchen,
* cooked time,
* packaging type.

---

## Update Timeline

Update:

* packaged_at,
* pickup_at,
* delivered_at,
* consumed_at.

---

## View Batch

Menampilkan:

* timeline,
* risk score,
* exposure duration,
* SOP violations.

---

# Excluded

* QR scan,
* barcode tracking,
* IoT integration.

---

# FEATURE 3 — Rule-Based Risk Engine

# Objective

Menghitung food safety risk berbasis operational exposure.

---

# Included

## Time Exposure Calculation

Menghitung:

* holding duration,
* transport duration,
* total exposure.

---

## Temperature Risk

Menggunakan:

* ambient temperature,
* manual temperature input.

---

## Food Sensitivity

Menu classification:

* low risk,
* medium risk,
* high risk.

---

## Packaging Risk

Packaging:

* vacuum,
* sealed,
* standard,
* open.

---

## Final Weighted Score

```text id="i9vpd6"
Final Risk =
(Time × 0.35)
+ (Temperature × 0.35)
+ (Food × 0.20)
+ (Packaging × 0.10)
```

---

# Included Output

| Output           | Description         |
| ---------------- | ------------------- |
| final score      | 0–100               |
| risk status      | LOW/MEDIUM/HIGH     |
| risk explanation | explainable factors |

---

# Excluded

* predictive spoilage AI,
* bacterial simulation,
* deep learning.

---

# FEATURE 4 — Operational Timeline

# Objective

Menampilkan lifecycle distribusi makanan.

---

# Included

## Timeline Events

```text id="xw94b4"
Cooked
→ Packaged
→ Pickup
→ Distribution
→ Delivered
→ Consumed
```

---

## Exposure Duration

Menampilkan:

* total exposure,
* estimated danger-zone exposure.

---

## SOP Violation Detection

Deteksi:

* delayed pickup,
* excessive holding,
* delayed delivery.

---

# FEATURE 5 — Dashboard Monitoring

# Objective

Memberikan operational visibility realtime.

---

# Included

## Dashboard Overview

Menampilkan:

* total active batches,
* HIGH risk count,
* delayed deliveries,
* active alerts.

---

## Batch Monitoring Table

Menampilkan:

* batch status,
* kitchen,
* exposure duration,
* risk score,
* risk status.

---

## Kitchen Analytics

Menampilkan:

* average kitchen risk,
* violation frequency,
* delayed distribution count.

---

# Excluded

* advanced BI,
* predictive forecasting,
* national analytics.

---

# FEATURE 6 — Google Maps Integration

# Objective

Mengukur keterlambatan distribusi.

---

# Included

## ETA Calculation

Menggunakan:

* route duration,
* traffic condition,
* estimated arrival.

---

## Delay Detection

Mendeteksi:

* abnormal route duration,
* operational bottleneck.

---

# Excluded

* route optimization AI,
* live driver tracking.

---

# FEATURE 7 — BMKG Integration

# Objective

Menggunakan cuaca sebagai exposure factor.

---

# Included

## Weather Data

* ambient temperature,
* humidity,
* weather condition.

---

## Risk Multiplier

Contoh:

```text id="ytwuk4"
Ambient Temp > 32°C
→ Increase risk by 20%
```

---

# Excluded

* climate prediction,
* advanced environmental simulation.

---

# FEATURE 8 — Alerting System

# Objective

Memberikan warning sebelum makanan menjadi unsafe.

---

# Included

## Alert Types

| Alert          | Trigger               |
| -------------- | --------------------- |
| HIGH RISK      | risk >70              |
| HOLDING ALERT  | holding >2h           |
| DELIVERY DELAY | ETA exceeded          |
| SOP ALERT      | operational violation |

---

## Notification Channels

* dashboard popup,
* email.

---

# Excluded

* WhatsApp automation,
* SMS gateway,
* push notification.

---

# FEATURE 9 — Anomaly Detection (Optional MVP+)

# Objective

Mendeteksi operational anomaly sederhana.

---

# Included

## Isolation Forest

Detect:

* abnormal delays,
* unusual exposure,
* operational spikes.

---

# Excluded

* predictive ML,
* advanced forecasting,
* reinforcement learning.

---

# MVP DATABASE TABLES

# Required Tables

| Table               | Purpose              |
| ------------------- | -------------------- |
| users               | authentication       |
| kitchens            | kitchen data         |
| menu_items          | food sensitivity     |
| food_batches        | operational tracking |
| distribution_routes | delivery data        |
| temperature_logs    | temperature history  |
| risk_scores         | risk history         |
| alerts              | alert history        |

---

# MVP FRONTEND PAGES

| Page              | Purpose              |
| ----------------- | -------------------- |
| Login             | authentication       |
| Dashboard         | overview             |
| Batch Monitoring  | operational tracking |
| Batch Detail      | detailed exposure    |
| Kitchen Analytics | kitchen performance  |
| Alerts            | active alerts        |
| Settings          | config               |

---

# MVP BACKEND MODULES

| Module       | Purpose        |
| ------------ | -------------- |
| auth         | authentication |
| batches      | batch CRUD     |
| risk_engine  | scoring        |
| alerts       | alerting       |
| maps_service | ETA            |
| bmkg_service | weather        |
| anomaly      | optional ML    |

---

# MVP API ENDPOINTS

# Authentication

```text id="skjx7d"
POST /auth/login
POST /auth/register
```

---

# Batches

```text id="m9d3m0"
GET /batches
POST /batches
GET /batches/{id}
PUT /batches/{id}
```

---

# Risk

```text id="3v6h3w"
GET /risk/{batch_id}
POST /risk/recalculate
```

---

# Alerts

```text id="gwfcz1"
GET /alerts
POST /alerts/acknowledge
```

---

# MVP UI COMPONENTS

| Component        | Purpose            |
| ---------------- | ------------------ |
| RiskBadge        | LOW/MEDIUM/HIGH    |
| RiskGauge        | risk visualization |
| BatchTimeline    | lifecycle          |
| ExposureCounter  | exposure duration  |
| TemperatureChart | temp graph         |
| RouteMap         | ETA monitoring     |
| AlertPanel       | alerts             |

---

# MVP DEVELOPMENT PRIORITY

# WEEK 1

## Foundation

* frontend setup,
* backend setup,
* database setup,
* authentication.

---

# WEEK 2

## Operational CRUD

* food batches,
* timeline updates,
* menu management.

---

# WEEK 3

## Risk Engine

* weighted scoring,
* exposure calculation,
* SOP violation detection.

---

# WEEK 4

## Dashboard Monitoring

* dashboard overview,
* batch table,
* risk visualization.

---

# WEEK 5

## API Integrations

* BMKG integration,
* Google Maps integration.

---

# WEEK 6

## Alerting & Polish

* alert system,
* UI improvement,
* bug fixing,
* deployment.

---

# MVP SUCCESS METRICS

# Technical

| Metric             | Target |
| ------------------ | ------ |
| API response       | <500ms |
| Dashboard load     | <3s    |
| Risk recalculation | <2s    |

---

# Operational

| Metric                  | Target |
| ----------------------- | ------ |
| realtime visibility     | YES    |
| SOP violation detection | YES    |
| exposure tracking       | YES    |
| operational alerting    | YES    |

---

# FINAL MVP POSITIONING

## Jangan Positioning Sebagai:

```text id="1g0qpk"
AI Deteksi Makanan Basi
```

---

# Positioning Yang Tepat

```text id="ex2m5u"
Predictive Food Safety Operational Monitoring
```

atau:

```text id="ez4o7j"
Operational Food Safety Intelligence Platform
```

---

# Final MVP Goal

Tujuan MVP:

# Membuktikan bahwa operational food safety visibility dapat:

* mengurangi unsafe food probability,
* meningkatkan SOP compliance,
* dan memberikan early warning sebelum makanan dikonsumsi.
