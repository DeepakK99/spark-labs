# Week 5 Day 3

# AWS Glue + Athena

---

# Main Learning Goal

Today I learned how AWS provides analytics directly on top of a data lake.

The biggest realization:

```plaintext
S3
↓
Stores Data

Glue
↓
Stores Metadata

Athena
↓
Executes Queries
```

Together they form the foundation of a serverless AWS analytics stack.

---

# The Problem Athena Solves

Suppose we have:

```plaintext
s3://brewery-data-lake/

silver/
    shipments/

gold/
    revenue_metrics/
```

containing:

```plaintext
part-0001.parquet
part-0002.parquet
```

Question:

```plaintext
How does Athena know:

- table names?
- columns?
- data types?
- partitions?
- S3 locations?
```

S3 only knows:

```plaintext
Object Keys

Object Content
```

It does not know:

```plaintext
Tables

Schemas

Columns

Data Types
```

We need metadata.

---

# Metadata

Metadata is:

```plaintext
Data About Data
```

Examples:

```plaintext
Table Name

Column Names

Column Types

Partitions

Storage Location
```

Metadata allows SQL engines to understand files as tables.

---

# AWS Glue

AWS Glue provides multiple capabilities:

```plaintext
ETL

Crawlers

Data Catalog

Schema Management

Data Quality
```

For today the focus was:

```plaintext
Glue Data Catalog
```

---

# Glue Data Catalog

Think of it as:

```plaintext
AWS Hive Metastore
```

or

```plaintext
Database Of Metadata
```

---

Example

Table:

```plaintext
shipments
```

Catalog stores:

```plaintext
Location:
s3://brewery-data-lake/silver/shipments/

Columns:

shipment_id BIGINT
status STRING
cost DOUBLE
delivery_days INT

Partitions:

year
month
day
```

---

Important:

Glue Catalog stores:

```plaintext
Metadata
```

not:

```plaintext
Actual Data
```

Actual data remains in S3.

---

# Mental Model

```plaintext
S3
=
Data
```

---

```plaintext
Glue Catalog
=
Metadata
```

---

# Glue Crawlers

Purpose:

```plaintext
Discover Metadata
```

---

Crawler Flow

```plaintext
Scan S3
↓
Inspect Files
↓
Infer Schema
↓
Create/Update Catalog Tables
```

---

Example

Crawler scans:

```plaintext
s3://brewery-data-lake/silver/customers/
```

and creates:

```plaintext
customers
```

table in Glue Catalog.

---

Important:

Crawler does NOT:

```plaintext
Move Data

Transform Data

Store Data
```

It only discovers metadata.

---

# Athena

Athena is:

```plaintext
Serverless SQL Query Engine
```

---

Athena is NOT:

```plaintext
Storage
```

Storage remains:

```plaintext
S3
```

---

Athena is NOT:

```plaintext
Metadata Storage
```

Metadata remains:

```plaintext
Glue Catalog
```

---

Athena's responsibility:

```plaintext
Execute Queries
```

---

Example

```sql
SELECT
    status,
    COUNT(*)
FROM shipments
GROUP BY status;
```

Athena performs:

```plaintext
Query Planning

File Reading

Aggregation

Result Generation
```

---

# Query Flow

Complete flow:

```plaintext
Athena
↓
Ask Glue Catalog

"Where is shipments?"
↓
Glue returns:

Schema
Location
Partitions
↓
Athena reads S3 files
↓
Executes query
↓
Returns results
```

---

# Architecture

```plaintext
S3
↓
Glue Catalog
↓
Athena
↓
Dashboard / BI Tool
```

---

# Schema-on-Read

Traditional warehouse:

```plaintext
Load Data
↓
Define Schema
↓
Store
```

Schema first.

---

Athena / Lakehouse:

```plaintext
Store Data
↓
Apply Schema Later
```

This is called:

```plaintext
Schema-on-Read
```

---

Benefits:

```plaintext
Flexible

Fast Ingestion

Easy To Add New Data
```

---

# Athena And Partitioning

Athena works very well with partitions.

Example:

```plaintext
year=2026/
month=05/
day=01/
```

---

Query:

```sql
WHERE year=2026
```

Athena can skip:

```plaintext
2024

2025
```

partitions.

This is:

```plaintext
Partition Pruning
```

---

Benefits:

```plaintext
Less Data Scanned

Lower Cost

Faster Queries
```

---

# Athena Cost Model

Important realization:

Athena charges based on:

```plaintext
Data Scanned
```

---

Bad query:

```sql
SELECT *
FROM shipments
```

Potentially scans:

```plaintext
Entire Dataset
```

---

Good query:

```sql
SELECT shipment_id, status
FROM shipments
WHERE year=2026
```

Scans significantly less data.

---

# Why Parquet Is Cheaper Than CSV

CSV:

```plaintext
Read Entire Rows

Parse Entire File
```

No column pruning.

---

Parquet:

```plaintext
Column Pruning

Compression

Predicate Pushdown

Partition Pruning
```

---

Result:

```plaintext
Less Data Scanned
↓
Lower Athena Cost
```

---

# Silver vs Gold

## Silver

Good for:

```plaintext
Data Science

Ad-hoc Analytics

Exploration

Detailed Investigations
```

Contains:

```plaintext
Cleaned

Deduplicated

Enriched

Row-Level Data
```

---

## Gold

Good for:

```plaintext
Dashboards

Business KPIs

Executive Reporting
```

Contains:

```plaintext
Precomputed Metrics
```

Examples:

```plaintext
Revenue By State

Delayed Shipment %

Top Distributors

Route Efficiency
```

---

# Dashboard Query Flow

Business user opens dashboard.

Flow:

```plaintext
Power BI
↓
Athena
↓
Glue Catalog
↓
S3 Gold
↓
Results Returned
↓
Charts Rendered
```

---

Important realization:

Dashboards typically do NOT read S3 files directly.

They usually query Athena.

---

# When To Use Athena

Good for:

```plaintext
Interactive SQL

Business Reporting

Ad-hoc Queries

Dashboards
```

---

# When Spark Is Better

Good for:

```plaintext
ETL

Large Transformations

Complex Joins

Streaming

Batch Processing
```

---

# Connection To Previous Days

Day 1:

```plaintext
S3
=
Storage Layer
```

---

Day 2:

```plaintext
IAM
=
Access Control Layer
```

---

Day 3:

```plaintext
Glue
=
Metadata Layer

Athena
=
Query Layer
```

---

# AWS Analytics Architecture

```plaintext
Shipment API
↓
S3 Bronze

Spark
↓
S3 Silver

Spark
↓
S3 Gold

Glue Catalog
↓
Athena
↓
Power BI
```

---

# Interview Question

Company stores:

```plaintext
500 TB
```

in S3.

Business users need SQL analytics.

Recommended approach:

```plaintext
Glue Catalog
+
Athena
```

instead of:

```plaintext
Loading Everything Into PostgreSQL
```

because:

```plaintext
More Scalable

Lower Cost

Less Operational Overhead

Designed For Data Lake Analytics
```

---

# Biggest Takeaways

Glue Catalog stores metadata, not data.

---

Glue Crawlers discover metadata from S3.

---

Athena is a serverless SQL engine.

---

Athena uses Glue Catalog to understand S3 data.

---

Schema-on-read is a key lakehouse concept.

---

Partitioning and Parquet directly reduce Athena costs.

---

Business dashboards commonly query Gold through Athena.

---

# Most Important Realization

```plaintext
S3 stores data.

Glue explains the data.

Athena queries the data.
```

Together they provide a complete AWS analytics foundation without requiring a traditional database.

---
