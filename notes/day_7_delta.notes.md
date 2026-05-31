# Week 3 Day 7
# Lakehouse Mini Project

---

# Project Goal

Build an end-to-end lakehouse pipeline using:

- Delta Lake
- Medallion Architecture
- Incremental Processing
- Business Aggregations

---

# Final Architecture

Raw Data
↓
Bronze
↓
Silver
↓
Gold

---

# Bronze Layer

Purpose:

Store raw source data.

Characteristics:

- append-only
- preserves duplicates
- preserves bad records
- preserves source truth

Added metadata:

- ingestion_timestamp
- source_file

Question Bronze answers:

"What happened?"

---

# Silver Layer

Purpose:

Store trusted business entities.

Transformations:

- standardization
- validation
- enrichment
- deduplication

Added columns:

- delivery_days
- high_cost_flag

Question Silver answers:

"What is true right now?"

---

# Gold Layer

Purpose:

Store business-ready answers.

Datasets:

- revenue_by_destination
- delayed_shipment_percentage
- top_customers
- route_performance

Question Gold answers:

"What does the business need?"

---

# Revenue By Destination

DestinationCity
↓
SUM(ShippingCostUSD)

Purpose:

Revenue reporting.

---

# Delayed Shipment %

Formula:

Delayed Delivered Shipments
/
Total Delivered Shipments

Important:

Only delivered shipments included.

---

# Top Customers

CustomerName
↓
SUM(ShippingCostUSD)

Purpose:

Customer revenue analysis.

---

# Route Performance

OriginCity
DestinationCity
↓
AVG(delivery_days)

Purpose:

Logistics optimization.

---

# Incremental Processing

Bronze:

Append new events.

Silver:

MERGE updates.

Gold:

Recompute business metrics.

---

# MERGE Pattern

Load Delta Table
↓
Match business key
↓
Update existing rows
↓
Insert new rows

Common pattern:

target
MERGE source
ON key

WHEN MATCHED
UPDATE

WHEN NOT MATCHED
INSERT

---

# Production Design Principle

Update only mutable fields.

Avoid:

whenMatchedUpdateAll()

Prefer:

Update only business fields that can change.

Example:

- Status
- DeliveryDate

---

# Medallion Philosophy

Bronze:

What happened?

Silver:

What is true?

Gold:

What answer is needed?

---

# Week 3 Summary

Learned:

- Delta Lake fundamentals
- Transaction Logs
- Time Travel
- Schema Evolution
- Medallion Architecture
- MERGE
- Incremental Processing
- Structured Streaming Fundamentals
- Lakehouse Design

---

# Biggest Takeaway

Modern data platforms are not just pipelines.

They are systems for managing:

- state
- history
- correctness
- reliability
- business consumption

at scale.

---