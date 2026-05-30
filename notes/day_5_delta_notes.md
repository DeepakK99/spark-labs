# Week 3 — Day 5
# Incremental Processing, MERGE, Upserts, and CDC

---

# Main Learning Goal

Today I learned that production systems do not usually:

```plaintext
Delete everything
↓
Reload everything
```

Instead they do:

```plaintext
Process only changes
```

using:

```plaintext
Incremental Processing
+
MERGE
+
CDC
```

---

# Mindset Shift

Wrong mindset:

```plaintext
Every run recreates the table
```

Correct mindset:

```plaintext
Every run updates the current state
```

---

# Full Load vs Incremental Load

## Full Load

Example:

```plaintext
Day 1:
100M rows

Day 2:
Delete
Reload 100M rows

Day 3:
Delete
Reload 100M rows
```

Problems:

- expensive
- slow
- unnecessary compute
- unnecessary storage I/O

---

## Incremental Load

Example:

```plaintext
Day 1:
100M rows

Day 2:
5000 changed rows

Day 3:
7000 changed rows
```

Only process:

```plaintext
Changes
```

Benefits:

- lower cost
- lower latency
- less compute
- less storage I/O

---

# Why Full Reload Is Wasteful

Example:

```plaintext
500M shipments
```

Daily changes:

```plaintext
50,000 rows
```

Processing:

```plaintext
500,000,000 rows
```

when only:

```plaintext
50,000 rows
```

changed.

---

## Compute Impact

Full reload:

```plaintext
Process 500M rows
```

Incremental:

```plaintext
Process 50K rows
```

Most work is unnecessary.

---

## Storage I/O Impact

Full reload:

```plaintext
Read everything
↓
Rewrite everything
```

Large amount of disk activity.

Incremental:

```plaintext
Read changes
↓
Update affected records
```

Much smaller I/O footprint.

---

## Latency Impact

Full reload:

```plaintext
Business update
↓
Wait for large reload
```

Incremental:

```plaintext
Business update
↓
Apply change quickly
```

Much fresher data.

---

## Operational Risk

Full reload:

```plaintext
Delete old table
↓
Failure during reload
```

Risk of incomplete data.

Incremental:

```plaintext
Update existing state
```

Safer.

---

# Base Delta Table

Created:

```plaintext
shipment_id
status
```

Initial data:

```plaintext
101 In Transit
102 Delivered
103 Pending
```

---

# Append Problem

Incoming updates:

```plaintext
101 Delivered
999 In Transit
```

Using:

```python
.mode("append")
```

Result:

```plaintext
101 In Transit
101 Delivered
102 Delivered
103 Pending
999 In Transit
```

Problem:

```plaintext
Duplicate business entity
```

Shipment 101 exists twice.

---

# Upsert

Definition:

```plaintext
If exists
    update

If doesn't exist
    insert
```

Example:

```plaintext
101
↓
Update

999
↓
Insert
```

---

# MERGE

Used:

```python
delta_table.alias("target") \
    .merge(
        updates_df.alias("source"),
        "target.shipment_id = source.shipment_id"
    ) \
    .whenMatchedUpdateAll() \
    .whenNotMatchedInsertAll() \
    .execute()
```

---

# MERGE Result

Before:

```plaintext
101 In Transit
102 Delivered
103 Pending
```

Updates:

```plaintext
101 Delivered
999 In Transit
```

After:

```plaintext
101 Delivered
102 Delivered
103 Pending
999 In Transit
```

Behavior:

```plaintext
101 updated
999 inserted
```

No duplicates.

---

# DeltaTable vs DataFrame

## DataFrame

Created using:

```python
spark.read...
```

Purpose:

```plaintext
Read and transform data
```

Examples:

```python
filter()
groupBy()
select()
```

---

## DeltaTable

Created using:

```python
DeltaTable.forPath(...)
```

Purpose:

```plaintext
Operate on table
```

Examples:

```python
merge()
delete()
update()
history()
```

Mental model:

```plaintext
DataFrame
=
Data

DeltaTable
=
Managed Delta table
```

---

# Idempotency

Definition:

Running pipeline multiple times produces:

```plaintext
Same final state
```

---

# Example

Run MERGE once:

```plaintext
101 Delivered
999 In Transit
```

Run MERGE again:

```plaintext
No change
```

Final state remains:

```plaintext
101 Delivered
102 Delivered
103 Pending
999 In Transit
```

---

# Why Idempotency Matters

Production systems experience:

- retries
- cluster failures
- orchestrator restarts
- network issues

Idempotent pipelines remain safe.

---

# Mental Model

Append:

```plaintext
Apply event again
```

MERGE:

```plaintext
Enforce desired state again
```

---

# CDC (Change Data Capture)

Definition:

Instead of sending:

```plaintext
Entire table
```

send:

```plaintext
Only changes
```

---

# Example

Before:

```plaintext
Shipment 101

Status:
In Transit
```

After:

```plaintext
Shipment 101

Status:
Delivered
```

CDC sends:

```plaintext
Shipment 101
Status = Delivered
```

Not:

```plaintext
Entire shipment table
```

---

# Why CDC Is Powerful

Benefits:

### Lower Compute

Process:

```plaintext
50K changes
```

instead of:

```plaintext
500M rows
```

---

### Lower Storage I/O

Read and write fewer files.

---

### Lower Latency

Changes become visible much faster.

---

### Better Scalability

Works even when datasets become huge.

---

# CDC + MERGE

Natural combination:

```plaintext
CDC Event
↓
MERGE
↓
New Delta Version
```

Every CDC batch becomes:

```plaintext
Change Set
↓
Transaction
↓
New Table Version
```

---

# Production Pattern

```plaintext
Incoming Updates
        ↓
Validation
        ↓
MERGE
        ↓
Updated Delta Table

```

---

# Relation To Real Work

Incremental processing is common in:

- Databricks pipelines
- Delta Live Tables
- data warehouses
- CDC platforms
- enterprise ETL systems

Many real-world systems rely on:

```plaintext
MERGE
+
CDC
+
Idempotency
```

to stay scalable.

---

# Key Takeaways

- Full reloads are expensive
- Incremental processing scales better
- Append can create duplicates
- Upsert solves update/insert problems
- MERGE is one of Delta's most valuable features
- Idempotency is critical in production
- CDC sends changes, not full snapshots
- CDC + MERGE is a common modern architecture
- Data platforms manage state, not just files

---