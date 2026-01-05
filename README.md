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

### Repository Structure (Day 3)
.
├── config/
├── logs/
├── sql/
│   └── mysql_schema.sql
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── main.py
└── README.md
