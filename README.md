# ETL Pipeline: On-Prem MySQL to Cloud Analytics

## Project Overview
This project demonstrates an end-to-end ETL pipeline starting from an on-premise relational database and preparing data for downstream cloud analytics use cases.

The project is designed to simulate real-world data engineering workflows, including schema design, transaction data modeling, and incremental ETL pipeline development.

The implementation follows a step-by-step, day-based approach to clearly demonstrate how an ETL system is built from the ground up.

---

## Tech Stack
**Current**
- MySQL (On-Premise Database)
- SQL
- Python
- Pandas
- SQLAlchemy
- GitHub (Version Control)

**Planned in later stages**
- Google BigQuery
- Cloud-based analytics and reporting

---

## Data Flow
On-Prem MySQL → Python (ETL) → Cloud Data Warehouse → Analytics

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
Represents customer master data extracted from upstream systems.

Key characteristics:
- `custid` as primary key
- One record per customer
- Functions as a dimension table in analytics use cases

#### 2. transactions
Represents betting transaction records and serves as the fact table.

Key characteristics:
- `transid` as primary key
- Time-based columns:
  - `transdate` (transaction time)
  - `winlostdate` (settlement time)
- Optimized for time-driven analytical queries rather than customer-centric lookups

---

### Index Design Strategy
Indexes are designed based on real ETL and reporting access patterns:

- `idx_transdate`  
  Optimizes queries for recent transaction data (daily / weekly ETL jobs)

- `idx_winlostdate`  
  Optimizes settlement-based reporting and reconciliation processes

Customer-based indexes are intentionally omitted at this stage, as transaction analysis is primarily time-driven.

---

### ETL Considerations
- The schema supports idempotent ETL patterns using primary keys
- Sample data is included to simulate realistic transaction ingestion
- The database can be fully recreated using SQL scripts stored in the repository

---

## Day 3: Data Extraction (Extract Layer)

### Objectives
- Connect Python to the on-prem MySQL database
- Extract transaction data using a configurable date range
- Return raw data as a Pandas DataFrame for downstream processing

---

### Extract Design
The extract layer is responsible for reading raw data from MySQL without modifying business logic.

Key characteristics:
- Uses SQLAlchemy for database connectivity
- Supports incremental extraction by `transdate`
- Preserves source schema and values
- Designed to be idempotent and re-runnable

---

### Extract Responsibilities
- Database connection handling
- SQL query construction
- Raw data retrieval into Pandas

No transformations are applied at this stage.

---

### Local Validation
The extract module supports standalone execution for testing:

```python
if __name__ == "__main__":
```

---

### ✅ 新增 Day 4（Transform）

```markdown
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
- ETL metadata enrichment (`etl_load_time` with company timezone)

---

### Design Principles
- Pure function design (input → output)
- No side effects on source data
- Deterministic and idempotent transformations
- Safe handling of dirty or malformed values

---

### Local Validation
The transform module can be executed independently to:

- Compare raw vs transformed schemas
- Validate dtype consistency
- Inspect transformation correctness

---

## Day 5: Load to BigQuery (Cloud Load)

### Objectives
- Load transformed transaction data into Google BigQuery
- Validate end-to-end ETL flow from on-prem MySQL to cloud warehouse
- Establish a foundation for incremental and idempotent loading

---

### BigQuery Setup
- BigQuery API enabled
- Dataset created: `etl_demo`
- Target table:
  - `O_transactions`
  - Schema auto-inferred from Pandas DataFrame

---

### Load Strategy
- Data is loaded using BigQuery Python client
- Load method: `load_table_from_dataframe`
- Write disposition:
  - `WRITE_APPEND`
  - Future stages will introduce `MERGE` for idempotency

---

### Result
- Successfully loaded transformed records into BigQuery
- Schema correctly inferred for:
  - Numeric fields
  - Datetime fields
  - Boolean fields
- End-to-end pipeline validated

---

### Current Pipeline Status
MySQL → Extract → Transform → **Load (BigQuery)** ✅


---

### Repository Structure
.
├── config/
├── logs/
├── sql/
│   └── mysql_schema.sql
├── src/
│   ├── extract.py      # Day 3: Extract layer
│   ├── transform.py   # Day 4: Transform layer
│   ├── load.py        # Day 5: Load layer 
│   └── main.py        # Pipeline orchestration
└── README.md
