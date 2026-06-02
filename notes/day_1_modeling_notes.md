# Week 4 Day 1

# OLTP vs OLAP + Data Warehouse Fundamentals

---

# Main Learning Goal

Today I learned that there are two fundamentally different types of data workloads:

```plaintext
OLTP
=
Run the business
```

and

```plaintext
OLAP
=
Analyze the business
```

Trying to use the same system for both often leads to performance and scalability problems.

---

# OLTP

OLTP = Online Transaction Processing

Purpose:

```plaintext
Run operational applications
```

Examples:

* Shipment tracking application
* Banking application
* E-commerce checkout
* Ride booking platform

Typical operations:

* Create shipment
* Update shipment status
* Cancel shipment
* Lookup shipment

Example query:

```sql
SELECT *
FROM shipments
WHERE ShipmentID = 'SHP1002';
```

Characteristics:

* Small reads
* Small writes
* Low latency
* High concurrency
* Transactional workloads
* Often highly normalized

Typical databases:

* PostgreSQL
* MySQL
* Oracle

---

# OLAP

OLAP = Online Analytical Processing

Purpose:

```plaintext
Understand the business
```

Examples:

* Revenue analysis
* Delivery performance
* Customer analytics
* Executive dashboards
* Historical reporting

Example query:

```sql
SELECT
    DestinationCity,
    SUM(ShippingCostUSD)
FROM shipments
GROUP BY DestinationCity;
```

Characteristics:

* Large scans
* Aggregations
* Historical analysis
* Reporting
* Business intelligence

Typical platforms:

* Snowflake
* Databricks SQL
* BigQuery
* Redshift

---

# OLTP vs OLAP

OLTP asks:

```plaintext
What is happening right now?
```

Examples:

```plaintext
Get shipment
Create shipment
Update shipment
Delete shipment
```

---

OLAP asks:

```plaintext
What can we learn from history?
```

Examples:

```plaintext
Revenue trends
Top customers
Average delivery times
Delayed shipment %
```

---

# Why Not Use PostgreSQL For Everything?

Example:

Customer query:

```sql
SELECT *
FROM shipments
WHERE ShipmentID = 'SHP1002';
```

Expected:

```plaintext
Fast lookup
One row
```

Often uses:

```plaintext
Indexes
```

---

CEO query:

```sql
SELECT
    DestinationCity,
    SUM(ShippingCostUSD)
FROM shipments
GROUP BY DestinationCity;
```

Requires:

```plaintext
Large table scans
Aggregations
Grouping
```

Potentially millions of rows.

---

# Resource Contention

If both workloads run on the same database:

```plaintext
Customer query
+
CEO analytics query
```

they compete for:

* CPU
* Memory
* Disk I/O
* Cache

Result:

```plaintext
Slower application
Poor user experience
```

---

# Key Insight

Operational systems and analytical systems have different access patterns.

Therefore:

```plaintext
OLTP
↓
Run the business

OLAP
↓
Analyze the business
```

should usually be separated.

---

# What Is A Data Warehouse?

Definition:

A data warehouse is a centralized analytical database designed for reporting, business intelligence, and historical analysis.

Purpose:

```plaintext
Store analytical data
```

Optimized for:

```plaintext
OLAP workloads
```

Examples:

* Snowflake
* Redshift
* BigQuery

---

# What Is A Lakehouse?

Definition:

A lakehouse combines:

```plaintext
Data Lake
+
Warehouse Features
```

Benefits:

* Cheap scalable storage
* ACID transactions
* Schema enforcement
* Analytics
* Machine learning support

Examples:

* Delta Lake
* Apache Iceberg
* Apache Hudi

---

# Data Lake vs Warehouse vs Lakehouse

## Data Lake

Stores:

* Raw files
* CSV
* JSON
* Parquet
* Logs

Optimized for:

```plaintext
Storage and flexibility
```

---

## Data Warehouse

Stores:

```plaintext
Structured analytical data
```

Optimized for:

```plaintext
Business reporting
Analytics
```

---

## Lakehouse

Stores:

```plaintext
Raw + Curated + Analytics Data
```

Optimized for:

```plaintext
Data engineering
Analytics
Streaming
Machine learning
```

---

# Why PostgreSQL Exists Before The Lakehouse

Important realization:

PostgreSQL is not there because we need raw data.

PostgreSQL exists because:

```plaintext
The application needs a database.
```

Example:

```plaintext
Customer
↓
Frontend
↓
Backend API
↓
PostgreSQL
```

The shipment is created in PostgreSQL first.

Later:

```plaintext
PostgreSQL
↓
ETL / CDC / Streaming
↓
Bronze
```

Data is copied into the lakehouse.

---

# Shipment Platform Architecture

```plaintext
Customer
    ↓
Frontend
    ↓
Backend APIs
    ↓
PostgreSQL
    ↓
ETL / CDC
    ↓
Bronze
    ↓
Silver
    ↓
Gold
    ↓
Power BI / Tableau
    ↓
Managers / Analysts
```

---

# Mapping My Current Project

## OLTP World

```plaintext
PostgreSQL
```

Tables:

* shipments
* customers
* orders
* tracking_events

Used for:

```plaintext
Application operations
```

---

## OLAP World

```plaintext
Bronze
↓
Silver
↓
Gold
```

Used for:

```plaintext
Analytics
Reporting
KPIs
Business insights
```

---

# Gold Layer Purpose

Example:

```plaintext
Revenue By Destination
```

Instead of:

```sql
SELECT
    DestinationCity,
    SUM(ShippingCostUSD)
FROM shipments
GROUP BY DestinationCity;
```

every dashboard refresh,

we precompute:

```plaintext
Mumbai      12M
Delhi        9M
Pune         6M
```

Benefits:

* Faster dashboards
* Lower compute cost
* Better user experience

---

# Interview Definitions

## OLTP

Online Transaction Processing.

Optimized for:

```plaintext
Fast transactional reads and writes.
```

---

## OLAP

Online Analytical Processing.

Optimized for:

```plaintext
Historical analysis,
aggregations,
reporting,
business intelligence.
```

---

## Data Warehouse

A specialized analytical database optimized for OLAP workloads.

---

## Lakehouse

A platform that combines the scalability of a data lake with the reliability and analytical capabilities of a data warehouse.

---

# Important Interview Answers

## Why separate OLTP and OLAP?

Because they have fundamentally different workload patterns and resource requirements.

Mixing them can cause:

* CPU contention
* Memory contention
* Disk I/O contention
* Cache pollution
* Poor application performance

---

## Why use a warehouse?

To perform large-scale analytics without impacting operational systems.

---

## Why use a lakehouse?

To combine flexible storage with warehouse-style reliability and analytics capabilities.

---

# Biggest Takeaway

A business has two different needs:

```plaintext
Run the business
```

and

```plaintext
Understand the business
```

OLTP systems handle operations.

OLAP systems handle analysis.

Modern data platforms exist because these workloads are fundamentally different and should be optimized separately.

---
