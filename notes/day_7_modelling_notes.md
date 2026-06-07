# Week 4 Day 7

# End-to-End Data Platform Design

---

# Main Learning Goal

Today I connected everything learned during the first month into a single end-to-end data platform architecture.

This was the first time all concepts fit together:

```plaintext
SQL
↓
ETL
↓
Spark
↓
Delta Lake
↓
Streaming
↓
Medallion Architecture
↓
Data Warehousing
↓
Gold KPIs
↓
Dashboards
```

The focus was no longer individual technologies but how entire systems are designed.

---

# Brewery Shipment Analytics Platform

Business Requirements:

## Operational Tracking

```plaintext
Where is shipment 123?
```

---

## Analytics

```plaintext
Revenue by State

Delayed Shipment %

Top Distributors

Route Efficiency
```

---

## Historical Reporting

```plaintext
Last 3 Years
```

---

## Future Requirement

```plaintext
Near Real-Time Dashboards
```

---

# Source Systems

Realistic source systems:

## Order Management System

```plaintext
Orders

Order Updates

Order Cancellations
```

---

## Shipment Management System

```plaintext
Shipment Creation

Status Changes

Delivery Events
```

---

## Inventory Management System

```plaintext
Stock Levels

Warehouse Inventory

Product Availability
```

---

## Payment System

```plaintext
Payments

Refunds

Transaction Status
```

---

## Distributor Uploads

```plaintext
CSV Files

Excel Files

Partner Reports
```

---

## Optional Future Source

```plaintext
GPS Events

Vehicle Tracking

Route Monitoring
```

---

# Batch vs Streaming

Important realization:

Batch vs Streaming is NOT:

```plaintext
Updates vs Inserts
```

Instead:

```plaintext
Batch
=
Process On Schedule

Streaming
=
Process As Data Arrives
```

---

## Batch Candidates

```plaintext
OMS

Inventory

ERP

CSV Uploads
```

---

## Streaming Candidates

```plaintext
Shipment Status Events

GPS Events

Real-Time Tracking
```

---

# Platform Architecture

```plaintext
Source Systems
        ↓

Batch / Streaming Ingestion
        ↓

Checkpoint
        ↓

Bronze
        ↓

Silver
        ↓

Warehouse
(Facts + Dimensions)
        ↓

Gold
        ↓

Dashboards
```

---

# Checkpoints

Purpose:

```plaintext
Track Processing Progress
```

Stores:

```plaintext
Offsets

Files Processed

Batch IDs
```

---

Benefits:

```plaintext
Recovery

Fault Tolerance

Avoid Duplicate Processing
```

---

# Bronze Layer

Purpose:

```plaintext
Preserve Truth
```

Contains:

```plaintext
Raw Payload

Raw Status

Raw Customer Data

Ingestion Timestamp

Source Metadata
```

---

# Why Bronze Exists

## Source Of Truth

Store exactly what arrived.

---

## Auditing

Answer:

```plaintext
What did the source actually send?
```

---

## Debugging

Trace bad data back to its origin.

---

## Reprocessing

If Silver logic changes:

```plaintext
delivery_days
```

can be recalculated from raw data.

---

# Bronze Principle

```plaintext
Evidence Locker
```

Never lose source data.

---

# Silver Layer

Purpose:

```plaintext
Current Trusted State
```

---

Operations:

```plaintext
Validation

Deduplication

Standardization

Enrichment
```

---

Examples:

```plaintext
DELIVERED
Delivered
delivered
```

becomes:

```plaintext
Delivered
```

---

Derived Columns

Examples:

```plaintext
delivery_days

delayed_days

high_cost_flag
```

---

# Why Dashboards Should Not Query Bronze

Reasons:

## Duplicates

Bronze may contain repeated events.

---

## Historical States

Contains all raw versions.

---

## Data Quality Issues

Not standardized.

---

## Performance

Much larger than Silver.

---

# Silver Principle

```plaintext
Current Business Truth
```

---

# Data Warehouse Layer

Major realization of Week 4:

Architecture is:

```plaintext
Bronze
↓
Silver
↓
Warehouse
↓
Gold
```

not:

```plaintext
Bronze
↓
Silver
↓
Gold
```

---

# Purpose Of Warehouse

```plaintext
Business Model
```

for flexible analytics.

---

Contains:

```plaintext
Fact Tables

Dimension Tables
```

---

# Grain

Most important modeling decision.

Chosen grain:

```plaintext
One Row = One Shipment
```

---

# FactShipment

Stores measurable facts.

Example columns:

```plaintext
shipment_sk

customer_sk

origin_location_sk

destination_location_sk

date_sk

status_sk

shipment_cost

delivery_days

delayed_days

weight_kg
```

---

# Dimensions

Provide descriptive context.

---

## DimCustomer

SCD Type 2

```plaintext
customer_sk

customer_id

customer_name

customer_type

start_date

end_date

current_flag
```

---

## DimLocation

```plaintext
location_sk

city

state

country
```

---

## DimDate

```plaintext
date_sk

month

quarter

year
```

---

## DimStatus

```plaintext
status_sk

status_name
```

---

# Why Fact + Dimensions Exist

Benefits:

```plaintext
Reduced Duplication

Flexible Analytics

Easier SCD Management

Business-Friendly Modeling
```

---

# Warehouse Principle

```plaintext
Flexible Analytics
```

Can answer:

```plaintext
Known Questions

Unknown Future Questions
```

---

# Gold Layer

Purpose:

```plaintext
Business Consumption
```

---

Examples:

```plaintext
Revenue By State

Top Distributors

Delayed Shipment %

Route Performance
```

---

# Why Gold Exists

Instead of:

```plaintext
Recalculate Same KPI
100 Times
```

we:

```plaintext
Compute Once
Read Many Times
```

---

# Gold Principle

```plaintext
Frequently Asked Questions
```

stored as precomputed analytics.

---

# Warehouse vs Gold

Warehouse:

```plaintext
Flexible

Ad-Hoc Analytics
```

---

Gold:

```plaintext
Fast

Precomputed

Frequently Used
```

---

Example

CEO asks:

```plaintext
Revenue By Customer Tier

for Delayed Shipments

during Q2
```

---

No Gold table exists.

Use:

```plaintext
FactShipment

DimCustomer

DimDate
```

to answer.

---

If question becomes common:

Create Gold KPI.

---

# Incremental Processing

Important realization:

Never reload everything.

---

Bad:

```plaintext
Read 500M Rows

Rewrite 500M Rows
```

daily.

---

Good:

```plaintext
Process Only Changes
```

---

Pattern:

```plaintext
Incoming Updates
        ↓

Validation
        ↓

MERGE
        ↓

Silver Delta Table
```

---

Benefits:

```plaintext
Scalable

Faster

Cheaper
```

---

# Deduplication

Correct layer:

```plaintext
Silver
```

---

Why Not Bronze?

Bronze stores reality.

If source sends duplicates:

Store duplicates.

---

Why Not Gold?

Gold should never fix data quality.

---

# Schema Evolution

Example:

Before:

```plaintext
customer_name
```

After:

```plaintext
customer_first_name

customer_last_name
```

---

Bronze:

Store raw source structure.

---

Silver:

Adapt schema.

Example:

```plaintext
first_name + last_name
```

↓

```plaintext
customer_name
```

---

Result:

Warehouse and Gold remain unchanged.

---

# Stable Data Contract

Silver acts as a shield between:

```plaintext
Unstable Sources
```

and:

```plaintext
Business Consumers
```

---

# Storage Format Decisions

---

## CSV

Problems:

```plaintext
Row-Based

Full File Reads

Expensive Parsing
```

---

## Parquet

Benefits:

```plaintext
Columnar Storage

Read Required Columns Only

Compression

Better Performance
```

---

## Delta

Benefits:

```plaintext
ACID Transactions

MERGE

Time Travel

Concurrency

Schema Enforcement
```

---

# Delta Realization

CSV stores:

```plaintext
Current File
```

---

Delta stores:

```plaintext
History Of Table States
```

through transaction logs.

---

# Optimization Thinking

Important realization:

Do not choose partition columns based only on:

```plaintext
WHERE clause
```

---

Also consider:

```plaintext
Cardinality

Data Distribution

Data Skew

Partition Count
```

---

Good partition examples:

```plaintext
shipment_date

year

month
```

---

Not always:

```plaintext
status

customer_name
```

even if used in filters.

---

# Final Platform Summary

```plaintext
Source Systems
(Generate Data)
        ↓

Batch / Streaming Ingestion
(Move Data)
        ↓

Checkpoint
(Track Progress)
        ↓

Bronze
(Raw Truth)
        ↓

Silver
(Current Trusted State)
        ↓

Warehouse
(Facts + Dimensions)
        ↓

Gold
(Precomputed KPIs)
        ↓

Dashboards / BI
(Business Consumption)
```

---

# Biggest Realization Of Week 4

Every layer exists for a different purpose.

---

Bronze:

```plaintext
Evidence
```

---

Silver:

```plaintext
Truth
```

---

Warehouse:

```plaintext
Business Model
```

---

Gold:

```plaintext
Business Answers
```

---

# Biggest Takeaway

The goal of data engineering is not:

```plaintext
Move Data
```

The goal is:

```plaintext
Build Reliable Systems
that turn business events
into trustworthy business decisions.
```

---
