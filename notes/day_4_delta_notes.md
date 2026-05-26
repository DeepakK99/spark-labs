# Week 3 — Day 4
# Medallion Architecture Deep Dive

---

# Main Learning Goal

Today I learned that:

```plaintext
Bronze
Silver
Gold
```

is NOT:

```plaintext
Three folders
```

Better mental model:

```plaintext
Bronze
↓
Preserve reality

Silver
↓
Clean reality

Gold
↓
Serve business
```

---

# Important Mindset Shift

Bad data platforms:

```plaintext
One giant pipeline
```

Good data platforms:

```plaintext
Layered responsibility
```

---

# Why One Big Pipeline Becomes Painful

Example:

```plaintext
Shipment API
↓
Cleaning
↓
Validation
↓
Transformation
↓
Business logic
↓
Aggregation
↓
Dashboard
```

Problems:

### Debugging difficulty

If dashboard breaks:

```plaintext
Where is issue?

API?
Cleaning?
Transformation?
Aggregation?
```

Hard to identify.

---

### Large blast radius

Example:

```plaintext
status
↓
shipment_status
```

Can affect:

- transformations
- dashboards
- backend services
- ML pipelines

One change:

```plaintext
Many downstream failures
```

---

### Schema changes become dangerous

No clear separation:

```plaintext
Raw data
+
Partially cleaned data
+
Business outputs
```

---

### Ownership becomes messy

Questions become difficult:

```plaintext
Who produced this data?

When did it arrive?

Where did it come from?
```

---

# Medallion Architecture

Structure:

```plaintext
Raw Sources
     ↓
Bronze
     ↓
Silver
     ↓
Gold
```

---

# Bronze Layer

Purpose:

```plaintext
Preserve raw truth
```

Characteristics:

- append-only
- minimal transformation
- retain raw values
- store metadata
- preserve lineage

Example:

```plaintext
ShipmentID
CustomerName
Status
ingestion_timestamp
source_file
```

---

# Bronze Metadata

Added:

```python
.withColumn(
    "ingestion_timestamp",
    current_timestamp()
)

.withColumn(
    "source_file",
    input_file_name()
)
```

---

## Why ingestion_timestamp?

### Track arrival time

Example:

```plaintext
Event Date:

May 20

Actually arrived:

May 25
```

Useful for:

- late arriving data
- auditing
- replay
- deduplication

---

### Partitioning

Can create:

```plaintext
ingestion_date=2026-05-26
```

Benefits:

- filter recent data
- incremental processing
- retention management
- easier cleanup

---

## Why source_file?

Useful for debugging.

Example:

Bad records:

```plaintext
ShippingCostUSD=-500
```

Find:

```plaintext
Which file caused issue?
```

instead of scanning entire dataset.

---

# Bronze Mental Model

Bronze:

```plaintext
Raw truth
+
Lineage
+
Recovery information
```

NOT:

```plaintext
Business data
```

---

# Silver Layer

Purpose:

```plaintext
Clean and standardize
```

Operations performed:

### Remove duplicates

```python
dropDuplicates()
```

---

### Standardize status

Used:

```python
initcap(Status)
```

Examples:

Before:

```plaintext
DELIVERED
delivered
Delivered
```

After:

```plaintext
Delivered
```

Reason:

Analytics should not miss:

```plaintext
DELIVERED
```

vs

```plaintext
Delivered
```

---

### Validation

Removed:

- null ShipmentID
- invalid ShippingCostUSD

---

### Enrichment

Created:

```plaintext
delivery_days
high_cost_flag
```

Purpose:

Reusable features.

Instead of every downstream consumer doing:

```python
datediff()
```

again.

---

# Silver Mental Model

Silver:

```plaintext
Raw reality
↓
Standardized reality
```

Contains:

```plaintext
Reusable cleaned features
```

NOT:

```plaintext
Final KPIs
```

---

# Gold Layer

Purpose:

```plaintext
Business consumption
```

Created:

```plaintext
avg_delivery_days
shipment_count
total_revenue
```

Examples:

Questions Gold answers:

```plaintext
How many delivered shipments?

Revenue by status?

Average delivery time?
```

---

# Gold Mental Model

Gold:

```plaintext
Business-ready answers
```

NOT:

```plaintext
Raw building blocks
```

---

# Layer Summary

Bronze:

```plaintext
What happened?
```

Silver:

```plaintext
What is correct?
```

Gold:

```plaintext
What matters?
```

---

# Why Not One shipment_final Table?

Problems:

### No lineage

Questions become difficult:

```plaintext
Where did record come from?

When was it ingested?
```

---

### Debugging difficulty

With Medallion:

```plaintext
Gold wrong
↓
Check Silver

Silver wrong
↓
Check Bronze

Bronze wrong
↓
Check API
```

---

### Large blast radius

Schema changes affect:

- dashboards
- backend services
- ML pipelines
- transformations

---

### Mixed responsibilities

Bad:

```plaintext
Raw records
+
Cleaning
+
KPIs
```

Good:

```plaintext
Separate responsibilities
```

---

# Production Mental Model

One giant table:

```plaintext
High coupling
↓
Large blast radius
↓
Hard debugging
```

Medallion:

```plaintext
Layered responsibility
↓
Controlled changes
↓
Easier debugging
↓
Easier recovery
```

---

# Relation To Real Work

This connects directly with:

- Databricks
- DLT pipelines
- shipment systems
- production data engineering

Many companies already use:

```plaintext
Bronze
Silver
Gold
```

but today I understood:

```plaintext
Why it exists
```

instead of:

```plaintext
Because Databricks recommends it
```

---

# Key Takeaways

- Bronze preserves truth
- Silver cleans and standardizes
- Gold serves business
- Metadata helps debugging
- Layering reduces blast radius
- Medallion improves maintainability
- Good platforms separate responsibilities

---