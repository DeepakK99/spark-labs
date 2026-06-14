# Week 5 Day 7

# AWS Data Platform Design Review

---

# Goal

Combine all Week 5 concepts into a single production-ready AWS data platform.

---

# Final Architecture

```plaintext
Business Requirements
        ↓

Source Systems

GPS Events (Streaming)
OMS (Batch)
Inventory (Batch)
Payments (Batch)
CSV Uploads (Batch)

        ↓

Ingestion Layer
        ↓

S3 Data Lake

bronze/
silver/
gold/

        ↓

Spark Processing
(EMR or Databricks)

        ↓

Silver Layer

Deduplication
Validation
Standardization
Enrichment

        ↓

Warehouse Layer

FactShipment

DimCustomer (SCD Type 2)
DimLocation
DimDate
DimStatus

        ↓

Gold Layer

Revenue Metrics
Route Performance
Delivery SLA Metrics

        ↓

Glue Catalog

Metadata:
- Tables
- Columns
- Types
- Partitions

        ↓

Athena

SQL Analytics

        ↓

Power BI / Dashboards

Business Consumption
```

---

# S3 Design

```plaintext
s3://brewery-data-lake/
```

```plaintext
bronze/
├── gps/
├── oms/
├── inventory/
├── payments/
└── csv_uploads/

silver/
├── shipments/
├── customers/
├── inventory/

gold/
├── fact_shipment/
├── dim_customer/
├── dim_location/
└── metrics/
```

---

# Partition Strategy

Use:

```plaintext
year=yyyy/month=mm/day=dd
```

for Bronze, Silver and Gold.

Reason:

* Partition pruning
* Faster Spark processing
* Lower Athena scan costs
* Easier backfills

---

# IAM Design

BronzePipelineRole

```plaintext
Write Bronze
```

---

SilverPipelineRole

```plaintext
Read Bronze
Write Silver
```

---

GoldPipelineRole

```plaintext
Read Silver
Write Gold
```

---

AnalyticsRole

```plaintext
Read Gold
```

---

Principle:

```plaintext
Least Privilege
```

---

# Spark Responsibilities

Spark is used for:

* Deduplication
* Validation
* Standardization
* Enrichment
* Warehouse Builds
* Gold Metric Generation

Spark creates data.

---

# Athena Responsibilities

Athena is used for:

* Ad-hoc analytics
* BI queries
* Dashboard queries

Athena consumes data.

---

# Warehouse Design

FactShipment

Grain:

```plaintext
One Row = One Shipment
```

Measures:

```plaintext
shipment_cost
delivery_days
```

---

Dimensions:

```plaintext
DimCustomer
DimLocation
DimDate
DimStatus
```

---

Customer uses:

```plaintext
SCD Type 2
```

to preserve history.

---

# Airflow DAG

```plaintext
Ingestion
      ↓

Bronze Validation
      ↓

Silver Build
      ↓

Warehouse Build
      ↓

Gold Build
      ↓

Dashboard Refresh
      ↓

Notification
```

---

Failure Handling

```plaintext
Task Fail
↓
Retry
↓
DAG Fail
↓
Alert
↓
Investigation
↓
Fix
↓
Backfill
↓
Successful Rerun
```

---

# Production Operations

Monitoring:

* Runtime
* Row Counts
* Freshness
* Failure Rates
* SLA Compliance

---

Data Quality:

* shipment_id NOT NULL
* shipment_id UNIQUE
* cost >= 0
* delivery_days >= 0
* Freshness Checks

---

Alerting:

* Slack
* Email

---

Observability:

Answer:

```plaintext
Why did it happen?
```

using:

* Logs
* Metrics
* Historical Runs
* Data Quality Results

---

Lineage

```plaintext
Source
↓
Bronze
↓
Silver
↓
Warehouse
↓
Gold
↓
Dashboard
```

Used to trace the origin of data issues.

---

# Key Week 5 Learnings

```plaintext
S3
=
Storage

Glue
=
Metadata

Athena
=
Analytics

Spark
=
Processing

Airflow
=
Orchestration

IAM
=
Security

Monitoring
=
Detect Issues

Alerting
=
Notify Issues

Observability
=
Explain Issues

Lineage
=
Trace Data Flow
```

---

# Biggest Takeaway

Modern Data Engineering is not just:

```plaintext
Write Spark Code
```

It is:

```plaintext
Build
Secure
Orchestrate
Monitor
Operate
Recover
```

reliable data platforms.
