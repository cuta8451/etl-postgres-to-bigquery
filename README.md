# ETL Pipeline: On-Prem MySQL to Cloud Analytics

## Project Overview
This project demonstrates an end-to-end ETL pipeline that ingests transactional data
from an on-premise MySQL database and loads it into Google BigQuery for cloud analytics.

The project is designed to simulate real-world data engineering workflows, including:

- Relational schema design
- Incremental data extraction
- Deterministic data transformation
- Idempotent cloud data loading

The implementation follows a step-by-step, day-based approach to clearly illustrate
how a production-grade ETL system is built from the ground up.

---

## Tech Stack

**Current**
- MySQL (On-Premise Database)
- SQL
- Python
- Pandas
- SQLAlchemy
- Google BigQuery
- Google Cloud SDK
- GitHub (Version Control)

---

## Data Flow
On-Prem MySQL → Python (ETL) → Google BigQuery → Analytics / BI

---

## Day 2: On-Prem MySQL Schema Design

### Objectives
- Design a production-oriented MySQL schema for ETL use
- Model transaction and customer data following fact/dimension principles
- Prepare the database for time-based analytical queries

---

### Database Schema
The on-prem database `etl_project` contains two core tables:

#### 1. customers
Represents customer master data.

Key characteristics:
- `custid` as primary key
- One record per customer
- Functions as a dimension table

#### 2. transactions
Represents betting transaction records and serves as the fact table.

Key characteristics:
- `transid` as primary key
- Time-based columns:
  - `transdate` (transaction time)
  - `winlostdate` (settlement time)
- Optimized for time-driven analytics

---

### Index Design Strategy
Indexes are designed based on actual ETL and reporting access patterns:

- `idx_transdate`  
  Optimizes incremental extraction (daily / weekly ETL jobs)

- `idx_winlostdate`  
  Optimizes settlement-based reporting

Customer-based indexes are intentionally omitted, as analytics are primarily time-driven.

---

## Day 3: Data Extraction (Extract Layer)

### Objectives
- Connect Python to the on-prem MySQL database
- Extract transaction data using a configurable date range
- Return raw data as a Pandas DataFrame

---

### Extract Design
The extract layer is responsible for **reading raw data only**, without applying
any business logic or transformations.

Key characteristics:
- Uses SQLAlchemy for database connectivity
- Supports incremental extraction by `transdate`
- Preserves source schema and values
- Designed to be idempotent and re-runnable

---

### Responsibilities
- Database connection handling
- SQL query construction
- Raw data retrieval into Pandas

No transformations are applied at this stage.

---

## Day 4: Data Transformation (Transform Layer)

### Objectives
- Normalize raw transaction data for analytics
- Enforce consistent data types
- Standardize business fields
- Enrich records with ETL metadata

---

### Transform Design
The transform layer converts raw extracted data into an analytics-ready format.

Key transformations:
- Datetime normalization (`transdate`, `winlostdate`)
- Numeric coercion with safe error handling
- Boolean normalization (`liveindicator`)
- Status standardization (uppercase, trimmed)
- ETL metadata enrichment (`etl_load_time`, company timezone)

---

### Design Principles
- Pure function design (input → output)
- No side effects on source data
- Deterministic and idempotent transformations
- Safe handling of malformed or dirty values

---

## Day 5: Load to BigQuery (Initial Load)

### Objectives
- Load transformed data into Google BigQuery
- Validate end-to-end ETL connectivity
- Establish cloud warehouse schema

---

### Load Strategy
- Data loaded using BigQuery Python client
- Method: `load_table_from_dataframe`
- Write disposition: `WRITE_APPEND`

This stage validates the full pipeline from on-prem MySQL to BigQuery.

---

### Result
- BigQuery dataset created: `etl_demo`
- Table created: `O_transactions`
- Schema auto-inferred from Pandas DataFrame
- End-to-end ETL flow successfully validated

---

## Day 6: Idempotent Load with MERGE (Production-Grade)

### Objectives
- Prevent duplicate data during re-runs
- Support incremental and backfill ETL
- Align with production data engineering best practices

---

### Idempotent Load Strategy
Instead of appending directly to the target table, the pipeline now uses:

1. A temporary **staging table** (unique per run)
2. A BigQuery `MERGE` statement using `transid` as the natural key

---

### MERGE Logic
- **WHEN MATCHED**  
  Update mutable fields (status, stake, settlement time, etc.)
- **WHEN NOT MATCHED**  
  Insert new records

This ensures:
- Safe re-runs
- No duplicate `transid`
- Deterministic outcomes

---

### Billing & Execution
- BigQuery billing enabled (required for DML operations)
- All load and merge jobs are executed synchronously
  using `.result()` to ensure correctness

---

### Current Pipeline Status
MySQL → Extract → Transform → Load → **MERGE (Idempotent)** ✅

---

## Repository Structure
.
├── config/
├── logs/
├── sql/
│ └── mysql_schema.sql
├── src/
│ ├── extract.py # Day 3: Extract layer
│ ├── transform.py # Day 4: Transform layer
│ ├── load.py # Day 5 & 6: BigQuery load & MERGE
│ └── main.py # Pipeline orchestration
└── README.md