Absolutely. Copy this into:

`notes/week5_day1_s3_data_lake_design.md`

# Week 5 Day 1

# S3 Deep Dive & Data Lake Design

---

# Main Learning Goal

Today I learned how modern AWS data platforms store data and how S3 fits into a lakehouse architecture.

The biggest realization:

```plaintext
Spark processes data

S3 stores data
```

Data is not owned by Spark.

Data lives independently in S3 and multiple services can access it.

---

# S3 Overview

S3 is AWS's object storage service.

Stores:

```plaintext
Parquet

Delta Tables

CSV

JSON

Logs

Images

Backups
```

S3 is the foundation of many AWS data platforms.

---

# Most Important Realization

Before:

```plaintext
Source
↓
Databricks
```

---

Now:

```plaintext
Source
↓
S3
↓
Databricks / Spark
```

S3 becomes the storage layer.

Spark becomes the compute layer.

---

# Object Storage vs File System

Important distinction.

---

# Traditional File System

Example:

```plaintext
C:
└── data
    └── bronze
        └── shipments
            └── file1.parquet
```

Contains:

```plaintext
Directories

Parent/Child Relationships

Folders
```

---

# S3

S3 stores:

```plaintext
Object Key
+
Object Content
```

Example:

```plaintext
bronze/shipments/file1.parquet
```

The entire string is simply an object key.

---

# Key Realization

S3 does NOT have real folders.

Example:

```plaintext
bronze/
shipments/
```

are not actual directories.

They are:

```plaintext
Prefixes
```

used as naming conventions.

---

# Bucket

Definition:

```plaintext
Top-Level Container
```

Example:

```plaintext
brewery-data-lake
```

---

# Object

Definition:

```plaintext
Actual Stored File
```

Examples:

```plaintext
shipments.parquet

customers.json

orders.csv
```

---

# Prefix

Definition:

```plaintext
Logical Grouping Of Objects
```

Examples:

```plaintext
bronze/

silver/

gold/
```

These are naming conventions, not real folders.

---

# Why Data Engineers Love S3

Benefits:

```plaintext
Cheap

Durable

Scalable

Cloud Native

Integrates With Everything
```

---

# S3 Scale

Same service supports:

```plaintext
10 GB

10 TB

10 PB
```

without changing architecture.

---

# Integrations

Many services read directly from S3:

```plaintext
Spark

Databricks

Athena

Glue

EMR

Airflow
```

---

# Data Lake Design

Bad design:

```plaintext
s3://data-lake/

everything.parquet
```

---

Problems:

```plaintext
Poor Organization

Difficult Maintenance

No Domain Separation
```

---

# Better Design

```plaintext
s3://brewery-data-lake/

bronze/
silver/
gold/
```

---

# Recommended Design

```plaintext
s3://brewery-data-lake/

bronze/
    shipments/
    customers/
    inventory/
    payments/

silver/
    shipments/
    customers/
    inventory/
    payments/

gold/
    revenue_by_state/
    shipment_metrics/
    delayed_shipment_metrics/
    route_performance/
    top_distributors/
```

---

# Why Separate Domains?

Benefits:

## Read Only Required Data

Customer jobs read:

```plaintext
customers/
```

without scanning:

```plaintext
shipments/

inventory/
```

---

## Easier Maintenance

Predictable structure.

---

## Independent Pipelines

Example:

```plaintext
bronze/customers/
↓
silver/customers/
```

can run independently from:

```plaintext
bronze/shipments/
↓
silver/shipments/
```

---

## Ownership

Different teams can own different domains.

---

## Security

Permissions can be applied by domain.

---

# Medallion Architecture On S3

---

# Bronze

Purpose:

```plaintext
Raw Truth
```

Example:

```plaintext
s3://brewery-data-lake/

bronze/
    shipments/
```

Contains:

```plaintext
Raw CSV

Raw JSON

Raw API Responses

Raw Events
```

---

# Why Bronze Exists

```plaintext
Auditing

Debugging

Reprocessing

Source Of Truth
```

---

Bronze acts as:

```plaintext
Evidence Locker
```

---

# Silver

Purpose:

```plaintext
Current Trusted State
```

Example:

```plaintext
s3://brewery-data-lake/

silver/
    shipments/
```

Contains:

```plaintext
Validated

Deduplicated

Standardized

Enriched
```

---

Examples:

```plaintext
delivery_days

delayed_days

high_cost_flag
```

---

# Gold

Purpose:

```plaintext
Business Consumption
```

Contains:

```plaintext
KPIs

Aggregations

Metrics
```

Examples:

```plaintext
Revenue By State

Route Performance

Delayed Shipment Metrics

Top Distributors
```

---

# Gold Principle

```plaintext
Compute Once

Read Many Times
```

---

# AWS Medallion Architecture

```plaintext
OMS
Shipment System
Inventory System
        ↓

S3 Bronze
        ↓

Spark
        ↓

S3 Silver
        ↓

Spark
        ↓

S3 Gold
        ↓

Athena
        ↓

Dashboard
```

---

# Partitioning

Purpose:

```plaintext
Read Less Data
```

---

Without Partitioning

Query:

```sql
WHERE shipment_date='2026-05-01'
```

may require scanning years of data.

---

With Partitioning

Example:

```plaintext
shipments/

year=2026/
    month=05/
        day=01/
```

Spark reads only relevant partitions.

---

# Partition Pruning

Query:

```sql
WHERE year=2026
AND month=05
AND day=01
```

Spark can skip all other partitions.

---

Benefits:

```plaintext
Less I/O

Less Network Transfer

Lower Cost

Faster Queries
```

---

# Why Partition By shipment_date?

Chosen strategy:

```plaintext
shipment_date
```

instead of:

```plaintext
shipment_id
```

---

Reason:

Most analytical queries are time-based.

Example:

```sql
WHERE shipment_date BETWEEN ...
```

---

Shipment IDs have:

```plaintext
Very High Cardinality
```

which would create millions of partitions.

---

# Over-Partitioning

Bad example:

```plaintext
customer_name=John/

customer_name=Jane/

customer_name=Amazon/
```

---

Problems:

```plaintext
Millions Of Partitions

Small Files

Metadata Overhead
```

---

# Good Partition Columns

Characteristics:

```plaintext
Frequently Filtered

Reasonable Cardinality

Balanced Distribution
```

Examples:

```plaintext
Date

Year

Month

Region
```

---

# CSV vs Parquet vs Delta

---

# CSV

Problems:

```plaintext
Row Based

Read Entire Row

Parse Entire File

No Column Pruning
```

---

# Parquet

Benefits:

```plaintext
Columnar Storage

Column Pruning

Compression

Efficient Analytics
```

---

# Delta

Benefits:

```plaintext
ACID Transactions

Time Travel

MERGE

Concurrency

Schema Enforcement
```

---

# Delta Lake On S3

Important realization:

Delta tables are commonly stored directly in S3.

Example:

```plaintext
s3://brewery-data-lake/

silver/shipments/
    _delta_log/
    part-0001.parquet
    part-0002.parquet
```

---

# Spark + S3

Biggest realization of the day.

Before:

```plaintext
S3
↓
Download File
↓
Spark
```

---

Actual Architecture:

```plaintext
Spark
↓
Read Directly From S3
```

Example:

```python
spark.read.parquet(
    "s3://brewery-data-lake/silver/shipments/"
)
```

---

# What Spark Actually Does

```plaintext
Read Metadata
↓
Discover Partitions
↓
Read Required Columns
↓
Read Required Byte Ranges
↓
Process Data
```

---

# S3 Range Reads

Important concept.

Spark does NOT download the entire file.

Instead:

```plaintext
Read Parquet Metadata
↓
Find Required Column Locations
↓
Request Only Relevant Byte Ranges
```

from S3.

---

# Why Parquet Matters More In The Cloud

Without Parquet:

```plaintext
More Data Transfer

More Parsing

Higher Cost
```

---

With Parquet:

```plaintext
Less Network Transfer

Less I/O

Faster Queries
```

---

# Storage vs Compute

Most important architecture realization.

---

S3:

```plaintext
Storage Layer
```

---

Spark:

```plaintext
Compute Layer
```

---

Athena:

```plaintext
Query Layer
```

---

Airflow:

```plaintext
Orchestration Layer
```

---

Multiple services can access the same data.

---

# Bronze Retention

Question:

Should Bronze be deleted after Silver is built?

Answer:

```plaintext
No
```

because Bronze supports:

```plaintext
Auditing

Debugging

Reprocessing
```

---

However:

```plaintext
Retention Policies
```

can archive older data.

Example:

```plaintext
Move Old Bronze Data
to Glacier
```

instead of deleting it.

---

# Interview Question

Design storage for:

```plaintext
2 Billion Shipments

5 Years Of Data
```

Common query:

```sql
WHERE shipment_date BETWEEN ...
```

Answer:

Partition by:

```plaintext
year/month/day
```

based on:

```plaintext
shipment_date
```

because:

```plaintext
Most Queries Are Time-Based

Enables Partition Pruning

Scales Well

Avoids High Cardinality Problems
```

---

# Biggest Takeaways

S3 is not a cloud hard drive.

It is object storage.

---

S3 does not have real folders.

It uses object key prefixes.

---

Spark reads directly from S3.

No manual download is required.

---

Parquet and Delta dramatically reduce network and storage costs.

---

Partitioning is one of the most important storage design decisions.

---

Medallion Architecture maps naturally onto S3:

```plaintext
Bronze
↓
Silver
↓
Gold
```

---

Most Important Realization

```plaintext
Spark does not own the data.

S3 owns the data.

Spark is a compute engine that reads from and writes to S3.
```

This is the foundation of modern AWS data engineering.

---
