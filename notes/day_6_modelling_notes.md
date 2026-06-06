# Week 4 Day 6

# Snowflake Fundamentals

---

# Main Learning Goal

Today I learned what Snowflake actually is, how it works internally, and where it fits in the modern data ecosystem.

Most important realization:

```plaintext
Spark != Snowflake

Spark = Processing Engine

Snowflake = Cloud Data Warehouse Platform
```

They solve different problems.

---

# Biggest Misconception

Before today, it was easy to think:

```plaintext
Snowflake vs Spark
```

But this is not the correct comparison.

A better comparison is:

```plaintext
Databricks vs Snowflake
```

because both are data platforms.

Even then:

```plaintext
Databricks
=
Engineering First

Snowflake
=
Analytics First
```

---

# Snowflake Architecture

Snowflake uses three layers:

```plaintext
Cloud Services
        ↑

Virtual Warehouses
(Compute)
        ↑

Storage
```

---

# Storage Layer

Responsible for storing data.

Examples:

```plaintext
Tables

Facts

Dimensions

Analytics Data
```

Snowflake manages storage internally.

Typically backed by:

```plaintext
AWS S3

Azure Blob Storage

Google Cloud Storage
```

---

# Compute Layer

Called:

```plaintext
Virtual Warehouses
```

This is one of Snowflake's most important concepts.

A Virtual Warehouse is essentially:

```plaintext
CPU

Memory

Workers
```

used to execute queries.

---

# Cloud Services Layer

Responsible for:

```plaintext
Authentication

Security

Metadata

Query Planning

Optimization

Access Control
```

Acts as the control plane.

---

# Storage And Compute Separation

Snowflake's biggest architectural idea:

```plaintext
Storage
and
Compute
```

scale independently.

---

# Traditional Databases

Historically:

```plaintext
CPU
+
Memory
+
Storage
```

were tightly coupled.

If storage increased:

```plaintext
100 TB
↓
500 TB
```

you often needed to buy:

```plaintext
More CPU

More RAM

More Storage
```

even when compute demand had not changed.

Wasteful.

---

# Snowflake Approach

Storage grows independently.

Example:

```plaintext
100 TB
↓
500 TB
```

Storage cost increases.

Compute remains unchanged.

---

Likewise:

```plaintext
Query Load
```

can increase dramatically while storage remains the same.

Only compute needs scaling.

---

# Why This Matters

Benefits:

```plaintext
Lower Cost

Independent Scaling

Operational Simplicity
```

Pay for what you actually need.

---

# Virtual Warehouses

Definition:

```plaintext
Independent Compute Clusters
```

that all access the same storage.

---

Example:

```plaintext
                 Storage

          /        |        \

         /         |         \

 ETL WH      BI WH      DS WH
```

---

# Why Virtual Warehouses Exist

Without them:

```plaintext
ETL

Dashboards

Data Science
```

all compete for:

```plaintext
CPU

Memory

Disk I/O
```

Result:

```plaintext
Resource Contention
```

---

# Resource Contention

Example:

```plaintext
Large ETL Job
```

consumes most resources.

CEO dashboard suddenly becomes slow.

Data science jobs slow everyone down.

---

# Snowflake Solution

Separate compute.

Example:

```plaintext
ETL Warehouse

BI Warehouse

Data Science Warehouse
```

Each gets dedicated compute.

Workloads do not interfere with each other.

---

# Warehouse Terminology Confusion

Today I learned there are two meanings of:

```plaintext
Warehouse
```

---

# Meaning 1

Data Warehouse

Example:

```plaintext
FactShipment

DimCustomer

DimLocation
```

This is:

```plaintext
The Data
```

---

# Meaning 2

Virtual Warehouse

Example:

```plaintext
Small WH

Medium WH

Large WH
```

This is:

```plaintext
The Compute
```

used to query the data.

---

# Mental Model

```plaintext
Data Warehouse
=
The Data

Virtual Warehouse
=
The Engine
```

---

# Comparison To Databricks SQL Warehouse

Databricks SQL Warehouse is also:

```plaintext
Compute
```

not the data itself.

The actual data lives in:

```plaintext
Delta Tables

Unity Catalog

Cloud Storage
```

---

# Micro-Partitions

Snowflake internally organizes data into:

```plaintext
Micro-Partitions
```

Typically:

```plaintext
Tens to Hundreds of MB
```

in size.

---

# Why Micro-Partitions Matter

Suppose:

```plaintext
500 TB
```

of shipment data exists.

Query:

```sql
SELECT *
FROM shipments
WHERE shipment_date = '2026-01-01'
```

---

Without optimization:

```plaintext
Scan 500 TB
```

Terrible.

---

With micro-partitions:

Snowflake stores metadata about:

```plaintext
Date Ranges

Column Statistics

Partition Information
```

and only reads relevant partitions.

---

# Connection To Spark

Spark:

```plaintext
Partition Pruning
```

often uses:

```plaintext
year=2026

month=01
```

directory structures.

---

Snowflake:

```plaintext
Micro-Partition Metadata
```

performs similar pruning automatically.

---

# Time Travel

Snowflake supports:

```plaintext
Time Travel
```

which allows querying historical versions of tables.

Example:

```sql
SELECT *
FROM shipments
AT(TIMESTAMP => '2026-01-01');
```

---

# Why Time Travel Exists

Useful for:

```plaintext
Bad ETL Jobs

Data Corruption

Accidental Deletes

Auditing

Debugging
```

---

# Example

Bad source data enters pipeline.

Results become incorrect.

Time Travel allows:

```plaintext
View table before failure

Compare versions

Recover data
```

---

# Connection To Delta Lake

Delta:

```plaintext
versionAsOf

timestampAsOf
```

---

Snowflake:

```plaintext
Time Travel
```

---

Both solve:

```plaintext
Historical Table Access
```

---

# Databricks vs Snowflake

---

# Databricks Strengths

```plaintext
Spark

Streaming

Delta Lake

Machine Learning

Data Engineering

Lakehouse Architecture
```

---

# Snowflake Strengths

```plaintext
Analytics

SQL

BI

Warehousing

Data Sharing

Ease of Use
```

---

# Simplified Comparison

Databricks:

```plaintext
Engineering First
```

---

Snowflake:

```plaintext
Analytics First
```

---

# When To Choose Databricks

Requirements:

```plaintext
Heavy Spark Processing

Streaming

ML Workloads

Lakehouse Design
```

Databricks is usually the stronger fit.

---

# When To Choose Snowflake

Requirements:

```plaintext
Business Analytics

Dashboards

SQL Workloads

Reporting
```

Snowflake is often the stronger fit.

---

# Mental Model Going Forward

Think:

```plaintext
Spark
=
Compute Engine
```

---

Think:

```plaintext
Delta Lake
=
Storage Format
+
Table Features
```

---

Think:

```plaintext
Databricks
=
Data Platform
+
Lakehouse Platform
```

---

Think:

```plaintext
Snowflake
=
Cloud Data Warehouse Platform
```

---

# Biggest Takeaways

Storage and compute can scale independently.

---

Virtual Warehouses are isolated compute clusters.

---

Micro-partitions provide automatic pruning.

---

Time Travel is Snowflake's version of historical table access.

---

Databricks excels at engineering workloads.

---

Snowflake excels at analytics workloads.

---