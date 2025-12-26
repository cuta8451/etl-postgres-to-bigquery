# ETL Pipeline: On-Prem MySQL to Cloud Analytics

## Project Overview
This project demonstrates an end-to-end ETL pipeline starting from an on-premise relational database and preparing data for downstream analytics use cases.

The project is designed to simulate real-world data engineering workflows, including schema design, transaction data modeling, and ETL-friendly database structures.

Day 2 focuses on building a reliable on-prem MySQL schema as the foundation of the ETL pipeline.

---

## Tech Stack
- MySQL (On-Premise Database)
- SQL
- GitHub (Version Control)

*Planned in later stages:*
- Python
- Pandas
- Google BigQuery

---

## Data Flow (Planned)
On-Prem MySQL → Python (ETL) → Cloud Data Warehouse → Analytics

---

## Day 2: On-Prem MySQL Schema Design (Current Progress)

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
- Used as a dimension table for analytics

#### 2. transactions
Represents betting transaction records and serves as the fact table.

Key characteristics:
- `transid` as primary key
- Time-based columns:
  - `transdate` (transaction time)
  - `winlostdate` (settlement time)
- Optimized for analytical queries rather than customer lookups

---

### Index Design Strategy
Indexes are designed based on actual ETL and reporting access patterns:

- `idx_transdate`  
  Optimizes queries for recent transaction data (daily / weekly ETL jobs)

- `idx_winlostdate`  
  Optimizes settlement-based reporting and reconciliation processes

Customer-based indexes are intentionally omitted at this stage, as transaction analysis is primarily time-driven.

---

### ETL Considerations
- The schema supports idempotent ETL patterns using primary keys
- Sample data is included to demonstrate realistic insert operations
- The database can be fully recreated using SQL scripts stored in the repository

---

### Repository Structure (Relevant to Day 2)
```text
.
├── README.md
└── sql/
    └── mysql_schema.sql
