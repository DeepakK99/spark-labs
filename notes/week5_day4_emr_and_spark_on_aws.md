# Week 5 Day 4

# EMR + Spark on AWS

---

# Main Learning Goal

Today I learned where EMR fits into the AWS analytics ecosystem and when to choose:

```plaintext
Athena
```

vs

```plaintext
Spark (EMR)
```

The biggest realization:

```plaintext
Athena
=
Query Engine

Spark
=
Processing Engine
```

They are not competitors.

They solve different problems.

---

# AWS Analytics Stack So Far

After four days, the AWS data platform looks like:

```plaintext
S3
↓
Storage

IAM
↓
Permissions

Glue Catalog
↓
Metadata

EMR / Spark
↓
Processing

Athena
↓
Analytics

Power BI
↓
Visualization
```

---

# What Is EMR?

EMR stands for:

```plaintext
Elastic MapReduce
```

Historically:

```plaintext
Hadoop Platform
```

Today it commonly runs:

```plaintext
Spark

Hive

Trino/Presto

Iceberg

Hudi
```

---

For Data Engineering:

```plaintext
EMR
=
Spark on AWS
```

---

# Why EMR Exists

Suppose we have:

```plaintext
500 GB shipment data
```

Tasks:

```plaintext
Deduplicate

Join Customers

Join Inventory

Apply Business Rules

Calculate Delivery Days

Calculate Delayed Days

Write Silver Tables
```

This is:

```plaintext
Data Processing
```

not:

```plaintext
Analytics
```

---

Spark is designed for:

```plaintext
Large-scale ETL

Distributed Processing

Complex Joins

Transformations

Writing New Datasets
```

---

This is exactly why EMR exists.

---

# Athena vs Spark

## Athena

Best for:

```plaintext
Read + Analyze
```

Examples:

```sql
SELECT

GROUP BY

SUM

AVG

COUNT
```

---

Example:

```sql
SELECT
    destination,
    AVG(delivery_days)
FROM shipments
GROUP BY destination;
```

Excellent Athena workload.

---

## Spark

Best for:

```plaintext
Read + Transform + Write
```

Examples:

```plaintext
Deduplication

Joins

Validation

Enrichment

Incremental Processing

Silver Creation

Gold Creation
```

---

Example:

```plaintext
Read Bronze
↓
Clean
↓
Deduplicate
↓
Join Customer Data
↓
Write Silver
```

Perfect Spark workload.

---

# Mental Model

Question:

```plaintext
Am I consuming data?
```

Examples:

```plaintext
Reports

Dashboards

Analytics
```

Answer:

```plaintext
Athena
```

---

Question:

```plaintext
Am I creating data?
```

Examples:

```plaintext
ETL

Transformations

Joins

Curated Tables
```

Answer:

```plaintext
Spark
```

---

# Architecture Comparison

## Athena Flow

```plaintext
S3
↓
Athena
↓
Results
```

Purpose:

```plaintext
Analytics
```

---

## Spark Flow

```plaintext
S3
↓
Spark
↓
Transform
↓
Write S3
```

Purpose:

```plaintext
Processing
```

---

# Shipment Platform Example

```plaintext
Raw Shipment Data
↓
Bronze
↓
Spark
↓
Silver
↓
Spark
↓
Gold
```

---

Business Query:

```sql
Revenue By Month
```

Should use:

```plaintext
Athena
```

---

Silver Processing:

```plaintext
Deduplication

Standardization

Customer Joins
```

Should use:

```plaintext
Spark
```

---

# EMR Cluster Basics

Typical EMR Cluster:

```plaintext
Master Node
↓
Worker Nodes
```

---

Spark Mapping:

```plaintext
Driver
↓
Executors
```

---

Visualization:

```plaintext
EMR Cluster

Master
↓
Worker
Worker
Worker
```

Spark tasks run across worker nodes.

---

# Cost Thinking

Important realization:

Not every workload needs Spark.

---

Scenario:

```plaintext
Revenue Dashboard
```

Query:

```sql
SELECT
    month,
    SUM(revenue)
FROM revenue_metrics
GROUP BY month;
```

Use:

```plaintext
Athena
```

Reason:

```plaintext
Simple Analytics

No ETL

Already Curated Data
```

---

Starting a Spark cluster would be unnecessary.

---

Scenario:

```plaintext
500 GB Daily ETL
```

Tasks:

```plaintext
Joins

Deduplication

Validation

Data Quality
```

Use:

```plaintext
Spark
```

Reason:

```plaintext
Large-scale Processing
```

---

# EMR vs Databricks

Very common interview topic.

---

## EMR

Advantages:

```plaintext
AWS Native

Flexible

Deep AWS Integration

Potentially Lower Infrastructure Cost
```

---

Disadvantages:

```plaintext
More Configuration

More Cluster Management

More Operational Responsibility
```

---

Think:

```plaintext
More Control

More Responsibility
```

---

## Databricks

Advantages:

```plaintext
Managed Spark Experience

Delta Lake

Workflows

Monitoring

Alerting

Auto Scaling

Notebooks

Collaboration
```

---

Disadvantages:

```plaintext
Additional Platform Cost

Vendor Dependency
```

---

Think:

```plaintext
More Productivity

Less Operational Work
```

---

# Connection To Current Job

Current Databricks project benefits from:

```plaintext
Managed Jobs

Managed Clusters

Built-in Monitoring

Notifications

Retry Handling

Easy Workflow Creation

Unified UI
```

---

Instead of building:

```plaintext
EMR

Glue

Monitoring

Alerting

Scheduling
```

separately.

---

This significantly reduces operational effort.

---

# Can Databricks Be Replaced By EMR?

Answer:

```plaintext
Yes
```

because:

```plaintext
Both Run Spark
```

---

However:

EMR requires more management.

Databricks provides:

```plaintext
Better Developer Experience

Built-in Platform Features

Operational Simplicity
```

---

# Modern AWS Data Platform

A common architecture:

```plaintext
Source Systems
↓
S3 Bronze
↓
Spark (EMR)
↓
S3 Silver
↓
Spark (EMR)
↓
S3 Gold
↓
Glue Catalog
↓
Athena
↓
Power BI
```

---

Important realization:

Spark and Athena coexist.

---

Not:

```plaintext
Athena vs Spark
```

---

But:

```plaintext
Spark creates datasets

Athena consumes datasets
```

---

# Architecture Decision Exercise

## Scenario 1

```plaintext
Revenue Dashboard
```

Choice:

```plaintext
Athena
```

Reason:

```plaintext
Simple Analytics

Read Existing Data
```

---

## Scenario 2

```plaintext
Daily ETL

500 GB
```

Choice:

```plaintext
Spark (EMR)
```

Reason:

```plaintext
Large Transformations

Distributed Processing
```

---

## Scenario 3

```plaintext
Ad-hoc Analyst Queries
```

Choice:

```plaintext
Athena
```

Reason:

```plaintext
Interactive SQL
```

---

## Scenario 4

```plaintext
Customer Deduplication Pipeline
```

Choice:

```plaintext
Spark (EMR)
```

Reason:

```plaintext
ETL Processing
```

---

## Scenario 5

```plaintext
Data Quality Processing
```

Choice:

```plaintext
Spark (EMR)
```

Reason:

```plaintext
Validation

Rule Enforcement

Data Transformation
```

---

# Interview Question

Company has:

```plaintext
100 TB
```

in S3.

Requirements:

```plaintext
Daily ETL

Joins

Data Quality

Business Reports
```

Recommended Architecture:

```plaintext
S3
↓
Spark (EMR)
↓
S3 Curated
↓
Glue Catalog
↓
Athena
↓
BI Tool
```

---

Reason:

```plaintext
Spark
=
Processing

Athena
=
Analytics
```

---

# Biggest Takeaways

Athena is a query engine.

---

Spark is a processing engine.

---

EMR is AWS's platform for running Spark workloads.

---

Athena is ideal for analytics.

---

Spark is ideal for ETL and transformations.

---

EMR and Athena are complementary technologies.

---

Databricks provides a more managed Spark experience than EMR.

---

# Most Important Realization

```plaintext
Athena answers questions.

Spark creates the data that Athena queries.
```

A modern AWS data platform typically needs both.

---
