# ERD / Database Schema

# Predictive Food Safety Operational Monitoring (MBG)

---

# 1. Database Overview

## Database Type

* PostgreSQL (Supabase)

---

# Core Design Principles

Database dirancang untuk:

* operational tracking,
* realtime risk monitoring,
* SOP violation detection,
* auditability,
* dan scalability.

---

# Main Operational Flow

```text id="8xl89v"
Kitchen
    ↓
Food Batch
    ↓
Distribution
    ↓
Temperature Logs
    ↓
Risk Calculation
    ↓
Alerts
    ↓
Anomaly Detection
```

---

# 2. High-Level ERD

```text id="1ehvyt"
users
 ├── roles

kitchens
 ├── food_batches
 │     ├── menu_items
 │     ├── distribution_routes
 │     ├── temperature_logs
 │     ├── risk_scores
 │     ├── alerts
 │     └── anomaly_logs
```

---

# 3. Tables Overview

| Table               | Purpose                  |
| ------------------- | ------------------------ |
| users               | authentication & RBAC    |
| kitchens            | kitchen master data      |
| menu_items          | food classification      |
| food_batches        | operational tracking     |
| distribution_routes | route & delivery         |
| temperature_logs    | temperature history      |
| risk_scores         | risk calculation history |
| alerts              | operational alerts       |
| anomaly_logs        | anomaly detection        |
| audit_logs          | activity tracking        |

---

# 4. users

# Purpose

Authentication & role management.

---

# Columns

| Column        | Type         | Constraints   |
| ------------- | ------------ | ------------- |
| id            | UUID         | PK            |
| full_name     | VARCHAR(100) | NOT NULL      |
| email         | VARCHAR(255) | UNIQUE        |
| password_hash | TEXT         | NOT NULL      |
| role          | VARCHAR(50)  | NOT NULL      |
| is_active     | BOOLEAN      | DEFAULT TRUE  |
| created_at    | TIMESTAMP    | DEFAULT NOW() |
| updated_at    | TIMESTAMP    | DEFAULT NOW() |

---

# Roles

| Role     |
| -------- |
| admin    |
| kitchen  |
| operator |
| auditor  |

---

# SQL

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(50) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

---

# 5. kitchens

# Purpose

Master data dapur produksi.

---

# Columns

| Column     | Type             |
| ---------- | ---------------- |
| id         | UUID             |
| name       | VARCHAR(255)     |
| address    | TEXT             |
| latitude   | DOUBLE PRECISION |
| longitude  | DOUBLE PRECISION |
| capacity   | INTEGER          |
| status     | VARCHAR(50)      |
| created_at | TIMESTAMP        |
| updated_at | TIMESTAMP        |

---

# Relationships

* One kitchen has many food_batches

---

# SQL

```sql
CREATE TABLE kitchens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    address TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    capacity INTEGER,
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

---

# 6. menu_items

# Purpose

Master data klasifikasi makanan.

---

# Columns

| Column          | Type         |
| --------------- | ------------ |
| id              | UUID         |
| name            | VARCHAR(255) |
| category        | VARCHAR(100) |
| moisture_level  | INTEGER      |
| protein_level   | INTEGER      |
| base_risk_score | INTEGER      |
| created_at      | TIMESTAMP    |

---

# Example Data

| name          | base_risk_score |
| ------------- | --------------- |
| Fried Chicken | 70              |
| Rice          | 50              |
| Bread         | 10              |
| Seafood       | 85              |

---

# SQL

```sql
CREATE TABLE menu_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    moisture_level INTEGER,
    protein_level INTEGER,
    base_risk_score INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

# 7. food_batches

# Purpose

Representasi satu batch distribusi makanan.

---

# Important Concept

Semua operational exposure tracking berpusat di tabel ini.

---

# Columns

| Column         | Type         |
| -------------- | ------------ |
| id             | UUID         |
| batch_code     | VARCHAR(100) |
| kitchen_id     | UUID FK      |
| menu_item_id   | UUID FK      |
| total_portions | INTEGER      |
| packaging_type | VARCHAR(50)  |
| cooked_at      | TIMESTAMP    |
| packaged_at    | TIMESTAMP    |
| pickup_at      | TIMESTAMP    |
| delivered_at   | TIMESTAMP    |
| consumed_at    | TIMESTAMP    |
| status         | VARCHAR(50)  |
| notes          | TEXT         |
| created_by     | UUID FK      |
| created_at     | TIMESTAMP    |
| updated_at     | TIMESTAMP    |

---

# Status Enum

| Status    |
| --------- |
| prepared  |
| packaged  |
| picked_up |
| delivered |
| consumed  |
| discarded |

---

# Relationships

* belongs to kitchen
* belongs to menu_item
* has many temperature_logs
* has many risk_scores
* has many alerts
* has one distribution_route

---

# SQL

```sql
CREATE TABLE food_batches (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    batch_code VARCHAR(100) UNIQUE NOT NULL,
    kitchen_id UUID REFERENCES kitchens(id),
    menu_item_id UUID REFERENCES menu_items(id),
    total_portions INTEGER,
    packaging_type VARCHAR(50),
    cooked_at TIMESTAMP,
    packaged_at TIMESTAMP,
    pickup_at TIMESTAMP,
    delivered_at TIMESTAMP,
    consumed_at TIMESTAMP,
    status VARCHAR(50),
    notes TEXT,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

---

# 8. distribution_routes

# Purpose

Monitoring distribusi makanan.

---

# Columns

| Column                     | Type             |
| -------------------------- | ---------------- |
| id                         | UUID             |
| food_batch_id              | UUID FK          |
| driver_name                | VARCHAR(255)     |
| vehicle_type               | VARCHAR(100)     |
| destination_name           | VARCHAR(255)     |
| destination_address        | TEXT             |
| destination_latitude       | DOUBLE PRECISION |
| destination_longitude      | DOUBLE PRECISION |
| distance_km                | DOUBLE PRECISION |
| estimated_duration_minutes | INTEGER          |
| actual_duration_minutes    | INTEGER          |
| traffic_condition          | VARCHAR(50)      |
| route_status               | VARCHAR(50)      |
| created_at                 | TIMESTAMP        |

---

# Relationships

* belongs to food_batch

---

# SQL

```sql
CREATE TABLE distribution_routes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    food_batch_id UUID REFERENCES food_batches(id),
    driver_name VARCHAR(255),
    vehicle_type VARCHAR(100),
    destination_name VARCHAR(255),
    destination_address TEXT,
    destination_latitude DOUBLE PRECISION,
    destination_longitude DOUBLE PRECISION,
    distance_km DOUBLE PRECISION,
    estimated_duration_minutes INTEGER,
    actual_duration_minutes INTEGER,
    traffic_condition VARCHAR(50),
    route_status VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

# 9. temperature_logs

# Purpose

Menyimpan histori suhu.

---

# Why Important

Temperature exposure adalah faktor utama food safety risk.

---

# Columns

| Column              | Type             |
| ------------------- | ---------------- |
| id                  | UUID             |
| food_batch_id       | UUID FK          |
| temperature         | DOUBLE PRECISION |
| ambient_temperature | DOUBLE PRECISION |
| humidity            | DOUBLE PRECISION |
| source              | VARCHAR(50)      |
| recorded_at         | TIMESTAMP        |

---

# Source Enum

| Source |
| ------ |
| manual |
| sensor |
| BMKG   |

---

# SQL

```sql
CREATE TABLE temperature_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    food_batch_id UUID REFERENCES food_batches(id),
    temperature DOUBLE PRECISION,
    ambient_temperature DOUBLE PRECISION,
    humidity DOUBLE PRECISION,
    source VARCHAR(50),
    recorded_at TIMESTAMP DEFAULT NOW()
);
```

---

# 10. risk_scores

# Purpose

Menyimpan histori risk calculation.

---

# Important

Risk score bersifat dynamic dan historical.

---

# Columns

| Column                    | Type        |
| ------------------------- | ----------- |
| id                        | UUID        |
| food_batch_id             | UUID FK     |
| time_score                | INTEGER     |
| temperature_score         | INTEGER     |
| food_score                | INTEGER     |
| packaging_score           | INTEGER     |
| environmental_score       | INTEGER     |
| final_score               | INTEGER     |
| risk_status               | VARCHAR(50) |
| exposure_duration_minutes | INTEGER     |
| danger_zone_minutes       | INTEGER     |
| explanation               | JSONB       |
| calculated_at             | TIMESTAMP   |

---

# Risk Status Enum

| Status |
| ------ |
| LOW    |
| MEDIUM |
| HIGH   |

---

# Example explanation JSON

```json
{
  "factors": [
    "high ambient temperature",
    "extended holding duration",
    "delayed delivery"
  ]
}
```

---

# SQL

```sql
CREATE TABLE risk_scores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    food_batch_id UUID REFERENCES food_batches(id),
    time_score INTEGER,
    temperature_score INTEGER,
    food_score INTEGER,
    packaging_score INTEGER,
    environmental_score INTEGER,
    final_score INTEGER,
    risk_status VARCHAR(50),
    exposure_duration_minutes INTEGER,
    danger_zone_minutes INTEGER,
    explanation JSONB,
    calculated_at TIMESTAMP DEFAULT NOW()
);
```

---

# 11. alerts

# Purpose

Menyimpan operational alerts.

---

# Columns

| Column          | Type         |
| --------------- | ------------ |
| id              | UUID         |
| food_batch_id   | UUID FK      |
| alert_type      | VARCHAR(100) |
| severity        | VARCHAR(50)  |
| title           | VARCHAR(255) |
| message         | TEXT         |
| acknowledged    | BOOLEAN      |
| acknowledged_by | UUID FK      |
| acknowledged_at | TIMESTAMP    |
| created_at      | TIMESTAMP    |

---

# Alert Types

| Type           |
| -------------- |
| HIGH_RISK      |
| DELIVERY_DELAY |
| SOP_VIOLATION  |
| HOLDING_ALERT  |
| ANOMALY_ALERT  |

---

# Severity

| Severity |
| -------- |
| low      |
| medium   |
| high     |
| critical |

---

# SQL

```sql
CREATE TABLE alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    food_batch_id UUID REFERENCES food_batches(id),
    alert_type VARCHAR(100),
    severity VARCHAR(50),
    title VARCHAR(255),
    message TEXT,
    acknowledged BOOLEAN DEFAULT FALSE,
    acknowledged_by UUID REFERENCES users(id),
    acknowledged_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

# 12. anomaly_logs

# Purpose

Menyimpan hasil anomaly detection.

---

# Columns

| Column        | Type             |
| ------------- | ---------------- |
| id            | UUID             |
| food_batch_id | UUID FK          |
| anomaly_score | DOUBLE PRECISION |
| anomaly_type  | VARCHAR(100)     |
| explanation   | TEXT             |
| created_at    | TIMESTAMP        |

---

# Example Types

| Type                 |
| -------------------- |
| abnormal_delivery    |
| abnormal_temperature |
| unusual_exposure     |
| operational_spike    |

---

# SQL

```sql
CREATE TABLE anomaly_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    food_batch_id UUID REFERENCES food_batches(id),
    anomaly_score DOUBLE PRECISION,
    anomaly_type VARCHAR(100),
    explanation TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

# 13. audit_logs

# Purpose

Audit trail seluruh aktivitas sistem.

---

# Columns

| Column      | Type         |
| ----------- | ------------ |
| id          | UUID         |
| user_id     | UUID FK      |
| action      | VARCHAR(255) |
| entity_type | VARCHAR(100) |
| entity_id   | UUID         |
| old_data    | JSONB        |
| new_data    | JSONB        |
| created_at  | TIMESTAMP    |

---

# SQL

```sql
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    action VARCHAR(255),
    entity_type VARCHAR(100),
    entity_id UUID,
    old_data JSONB,
    new_data JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

# 14. Suggested Indexes

# High Priority Indexes

```sql
CREATE INDEX idx_food_batches_kitchen
ON food_batches(kitchen_id);

CREATE INDEX idx_food_batches_status
ON food_batches(status);

CREATE INDEX idx_temperature_logs_batch
ON temperature_logs(food_batch_id);

CREATE INDEX idx_risk_scores_batch
ON risk_scores(food_batch_id);

CREATE INDEX idx_alerts_batch
ON alerts(food_batch_id);

CREATE INDEX idx_alerts_acknowledged
ON alerts(acknowledged);
```

---

# 15. Operational Data Lifecycle

```text id="x5mjlwm"
Kitchen creates batch
        ↓
Food batch lifecycle updates
        ↓
Temperature logs recorded
        ↓
Risk score recalculated
        ↓
Alerts generated
        ↓
Anomaly detection executed
        ↓
Audit logs stored
```

---

# 16. Database Design Principles

# Principles

## 1. Historical Tracking

Risk score dan exposure HARUS historical.

Jangan overwrite data lama.

---

## 2. Auditability

Semua operational change harus traceable.

---

## 3. Explainability

Risk score harus punya explanation.

---

## 4. Scalability

Database harus siap:

* ribuan batch,
* ribuan logs,
* realtime monitoring.

---

# 17. Future Schema Extensions

# Future Tables

| Table             | Purpose               |
| ----------------- | --------------------- |
| qr_scans          | QR tracking           |
| sensor_devices    | BLE thermometer       |
| route_tracking    | GPS realtime          |
| incidents         | food incident reports |
| predictive_models | ML model versioning   |

---

# 18. Final Database Objective

Tujuan schema ini bukan hanya menyimpan data makanan.

Tetapi:

# membangun operational food safety intelligence layer yang:

* traceable,
* explainable,
* auditable,
* dan scalable untuk monitoring distribusi makanan skala besar.
