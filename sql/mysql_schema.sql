-- =====================================================
-- MySQL On-Prem Schema for ETL Project
-- =====================================================
-- This script creates database, tables, indexes,
-- and inserts sample data for ETL practice.
-- =====================================================

/* ---------------------------
   Database
----------------------------*/
CREATE DATABASE IF NOT EXISTS etl_project
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE etl_project;


/* ---------------------------
   Customers Table
----------------------------*/
CREATE TABLE IF NOT EXISTS customers (
    custid        BIGINT PRIMARY KEY,
    createdate    DATETIME,
    username      VARCHAR(100),
    currency      INT,
    site          VARCHAR(20),
    inserttime    DATETIME
);

-- Sample customer data
INSERT INTO customers (
    custid,
    createdate,
    username,
    currency,
    site,
    inserttime
)
VALUES
(115076215, '2024-11-25 21:07:00', 'NR97S8768', 61, 'ABDD', '2024-11-30 01:08:01'),
(116082264, '2024-11-28 21:49:00', 'SL8S1411', 51, 'CHINAIN', '2024-11-30 01:50:07');


/* ---------------------------
   Transactions Table
----------------------------*/
CREATE TABLE IF NOT EXISTS transactions (
    transid        BIGINT PRIMARY KEY,
    custid         BIGINT,
    transdate      DATETIME,
    stake          DECIMAL(18,2),
    status         VARCHAR(20),
    liveindicator  BOOLEAN,
    betteam        VARCHAR(10),
    winlostdate    DATETIME,
    betfrom        VARCHAR(20),
    actualrate     DECIMAL(10,4),
    bettype        INT,
    currency       INT,
    currencyname   VARCHAR(20),
    betsiteid      INT,
    matchid        BIGINT,
    sporttype      INT,
    inserttime     DATETIME,

    -- Index for transaction date based queries
    INDEX idx_transdate (transdate),

    -- Index for settlement date based queries
    INDEX idx_winlostdate (winlostdate)
);

-- Sample transaction data (ETL example)
INSERT INTO transactions (
    transid, custid, transdate, stake, status, liveindicator,
    betteam, winlostdate, betfrom, actualrate, bettype,
    currency, currencyname, betsiteid, matchid, sporttype, inserttime
)
VALUES
(472141562915182029, 44552488, '2025-11-24 02:50:24.900000', 48.00, 'DRAW', TRUE,
 'a', '2025-11-24 00:00:00', 'n', 0.2363, 1,
 33, 'USS', 11, 119129564, 1, '2025-12-25 04:20:01'),

(472395246987258502, 12238541, '2025-11-24 02:09:39.613000', 3.00, 'WON', FALSE,
 'a', '2025-11-24 00:00:00', 'k', 3.7242, 3,
 3, 'USS', 1048, 11913778, 1, '2025-12-25 04:20:01')
AS new
ON DUPLICATE KEY UPDATE
    stake       = new.stake,
    status      = new.status,
    winlostdate = new.winlostdate,
    inserttime  = new.inserttime;
