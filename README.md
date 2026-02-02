# Data Engineering Zoomcamp 2026 - Modules 1 & 2 Homework

## 🚀 Project Overview

This repository contains the solutions for **Module 1 (Docker & Terraform)** and **Module 2 (Workflow Orchestration with Kestra)** of the Data Engineering Zoomcamp.

It implements a local Data Platform using Docker containers to ingest, store, and orchestrate NYC Taxi data analysis.

## 🛠 Technologies

- **Docker & Docker Compose**: Containerization of services.
- **PostgreSQL 17**: Local Data Warehouse.
- **pgAdmin 4**: Database UI management.
- **Kestra v1.1**: Workflow Orchestration (ETL Pipelines).
- **Python 3.13**: Data Ingestion logic.
- **Terraform**: Infrastructure as Code (GCP).

---

## ⚙️ Setup Instructions

### 1. Configure Environment Variables
**Security First:** Create a `.env` file in the root directory to store credentials. Docker Compose and the Python scripts will read from this file.

```ini
# Postgres Database Credentials
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=ny_taxi
POSTGRES_PORT=5432

# pgAdmin Credentials
PGADMIN_EMAIL=admin@admin.com
PGADMIN_PASSWORD=root

# Local Host Port Mapping (To avoid conflicts on Mac/Linux)
HOST_DB_PORT=5433
HOST_PGADMIN_PORT=8080

# Kestra System Database (Internal Brain)
KESTRA_DB_USER=kestra
KESTRA_DB_PASSWORD=k3str4
KESTRA_DB_NAME=kestra
```

### 2. Start Infrastructure

Run the complete stack (Postgres + pgAdmin + Kestra).

```bash
docker-compose up -d
```

### 3. Access Services

| Service | URL | Credentials (Default) |
|---------|-----|----------------------|
| Kestra UI | http://localhost:8081 | admin@kestra.io / Admin1234! |
| pgAdmin | http://localhost:8080 | admin@admin.com / root |
| Postgres | localhost:5433 | User/Pass from .env |

---

## 📂 Module 1: Docker & Terraform

### Ingestion Logic

A Python script (ingest_data.py) downloads the November 2025 Green Taxi data (Parquet format) and loads it into Postgres using SQLAlchemy.

### Homework Solutions

**Question 1: Understanding Docker images**

Answer: 24.3.1 (pip version in python:3.13 image)

**Question 2: Understanding Docker networking**

Answer: postgres:5432

**Question 3: Counting short trips**

Answer: 8007

Logic: Count trips with distance ≤ 1 mile within the November 2025 range.

```sql
SELECT COUNT(*) 
FROM green_taxi_trips
WHERE lpep_pickup_datetime >= '2025-11-01' 
  AND lpep_pickup_datetime < '2025-12-01'
  AND trip_distance <= 1.0;
```

**Question 4: Longest trip for each day**

Answer: 2025-11-14

Logic: Find the day with the maximum trip distance (filtered < 100 miles).

```sql
SELECT DATE(lpep_pickup_datetime) AS pickup_day, MAX(trip_distance) AS max_dist
FROM green_taxi_trips
WHERE trip_distance < 100
GROUP BY pickup_day
ORDER BY max_dist DESC
LIMIT 1;
```

**Question 5: Biggest pickup zone**

Answer: East Harlem North

Logic: Sum of total_amount for pickups on 2025-11-18.

**Question 6: Largest tip**

Answer: Yorkville West

Logic: Filter pickups by "East Harlem North" and find the drop-off zone with the largest tip.

**Question 7: Terraform Workflow**

Answer: terraform init, terraform apply -auto-approve, terraform destroy

---

## 🔄 Module 2: Workflow Orchestration (Kestra)

### Flow Logic

We moved from manual scripts to automated flows using Kestra. The flow 02_postgres_taxi_ingest.yaml creates a dynamic ETL pipeline.

Inputs: taxi_type (yellow/green), year, month.

Tasks:
- Construct URL.
- Download file from GitHub.
- Run Python script in a Docker container (attached to the taxi_network) to ingest data.

### Homework Solutions

**Question 1: Uncompressed file size (Yellow Taxi, Dec 2020)**

Answer: 128.3 MiB

Verification:

```bash
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2020-12.csv.gz
gunzip -c yellow_tripdata_2020-12.csv.gz | wc -c
# Output matches ~134MB (Decimal) or 128MiB (Binary)
```

**Question 2: Rendered Variable**

Answer: green_tripdata_2020-04.csv

Logic: Kestra template expansion `{{inputs.taxi}}_tripdata_{{inputs.year}}-{{inputs.month}}.csv`

**Question 3: Rows in Yellow Taxi 2020**

Answer: 24,648,499

Logic: Backfilled Yellow Taxi data for all months of 2020 via Kestra and ran a SQL count.

**Question 4: Rows in Green Taxi 2020**

Answer: 1,734,051

**Question 5: Rows in Yellow Taxi March 2021**

Answer: 1,925,152

Logic: Counted physical lines in the file (wc -l) minus the header. Note: SQL counts of valid dates might be slightly lower due to dirty data rows.

**Question 6: Timezone Configuration**

Answer: Add a timezone property set to America/New_York in the Schedule trigger configuration.

```yaml
triggers:
  - id: daily
    type: io.kestra.plugin.core.trigger.Schedule
    cron: "0 9 * * *"
    timezone: "America/New_York"
```