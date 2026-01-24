# Data Engineering Zoomcamp 2026 - Module 1 Homework

## Project Overview

This repository contains the solution for Module 1 of the Data Engineering Zoomcamp. It includes a Dockerized environment for PostgreSQL and pgAdmin, a Python ingestion script for NYC Green Taxi data (November 2025), and Terraform configuration for GCP.

## Technologies

- **Docker & Docker Compose**: For containerizing the Database and UI.
- **PostgreSQL 17**: Data Warehouse.
- **Python 3.13**: Data Ingestion using Pandas, SQLAlchemy, and Parquet.
- **Terraform**: Infrastructure as Code (GCP).

## Setup Instructions

### 1. Start the Infrastructure

```bash
docker-compose up -d
```

### 2. Install Dependencies

(Recommended to use a virtual environment)

```bash
pip install -r requirements.txt
```

### 3. Ingest Data

Run the Python script to download the November 2025 Parquet file and load it into Postgres.

```bash
python ingest_data.py
```

### 4. Access the Database

- **URL**: http://localhost:8080 (pgAdmin)
- **User**: admin@admin.com
- **Password**: pgadmin (or check docker-compose)
- **Host (Internal Docker Network)**: postgres
- **Port**: 5432

## Homework Solutions

### Question 1: Understanding Docker images

**Answer**: 24.3.1 (pip version in python:3.13 image)

### Question 2: Understanding Docker networking and docker-compose

**Answer**: postgres:5432

### Question 3: Counting short trips

**Answer**: 8007

**Logic**: Count trips with distance ≤ 1 mile within the November 2025 range.

```sql
SELECT COUNT(*) 
FROM green_taxi_trips
WHERE lpep_pickup_datetime >= '2025-11-01' 
  AND lpep_pickup_datetime < '2025-12-01'
  AND trip_distance <= 1.0;
```

### Question 4: Longest trip for each day

**Answer**: 2025-11-14

**Logic**: Find the day with the maximum trip distance (filtered < 100 miles to exclude outliers).

```sql
SELECT 
    DATE(lpep_pickup_datetime) AS pickup_day, 
    MAX(trip_distance) AS max_dist
FROM green_taxi_trips
WHERE trip_distance < 100
GROUP BY pickup_day
ORDER BY max_dist DESC
LIMIT 1;
```

**Resulting Top 3**:
- 2025-11-14 (88.03 miles)
- 2025-11-20 (73.84 miles)
- 2025-11-23 (45.26 miles)

### Question 5: Biggest pickup zone

**Answer**: East Harlem North

**Logic**: Sum of total_amount for pickups on 2025-11-18.

```sql
SELECT 
    z."Zone", 
    SUM(t.total_amount) AS total_revenue
FROM green_taxi_trips t
JOIN zones z ON t."PULocationID" = z."LocationID"
WHERE DATE(t.lpep_pickup_datetime) = '2025-11-18'
GROUP BY z."Zone"
ORDER BY total_revenue DESC
LIMIT 1;
```

### Question 6: Largest tip

**Answer**: Yorkville West

**Logic**: Filter pickups by "East Harlem North" and find the drop-off zone with the single largest tip amount.

```sql
SELECT 
    z_drop."Zone" AS dropoff_zone, 
    MAX(t.tip_amount) AS max_tip
FROM green_taxi_trips t
JOIN zones z_pick ON t."PULocationID" = z_pick."LocationID"
JOIN zones z_drop ON t."DOLocationID" = z_drop."LocationID"
WHERE z_pick."Zone" = 'East Harlem North'
  AND t.lpep_pickup_datetime >= '2025-11-01' 
  AND t.lpep_pickup_datetime < '2025-12-01'
GROUP BY z_drop."Zone"
ORDER BY max_tip DESC
LIMIT 1;
```

### Question 7: Terraform Workflow

**Answer**: terraform init, terraform apply -auto-approve, terraform destroy

**Logic**:
- `init`: Download providers and initialize the working directory.
- `apply -auto-approve`: Generate and execute the plan automatically without prompting for approval.
- `destroy`: Clean up and remove all resources created by Terraform.