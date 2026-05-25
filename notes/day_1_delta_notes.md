# Week 3 - Day 1
# Why Delta Lake Exists + ACID in Data Lakes

---

# Main Learning Goal

Today I learned that Delta is NOT a replacement for Parquet.

Important mindset:

```plaintext
Delta
=
Parquet
+
Transaction layer
+
Metadata
+
Reliability
```

Do NOT think:

```plaintext
Delta = another file format
```

Think:

```plaintext
Delta = table intelligence on top of Parquet
```

---

# Why Raw Data Lakes Become Painful

Example:

```plaintext
S3/

shipments_1.parquet
shipments_2.parquet
shipments_3.parquet
shipments_4.parquet
```

Initially this looks simple.

Problems appear when multiple pipelines:

- write data
- update data
- read data
- retry jobs

simultaneously.

---

# Problems With Raw Parquet Lakes

## Problem 1 — No ACID Transactions

Example:

```plaintext
Write starts:

file1 written ✅
file2 written ✅
file3 failed ❌
```

Result:

```plaintext
Partial state
```

Possible issues:

- missing records
- mixed old/new data
- corrupted analytics
- inconsistent reads

---

## Problem 2 — No Schema Enforcement

Today:

```plaintext
shipment_id
cost
status
```

Tomorrow:

```plaintext
shipment_id
shipment_cost
status
new_column
```

Possible issues:

```plaintext
Schema drift
↓
Broken pipelines
↓
Unexpected behavior
```

---

## Problem 3 — Updates Are Difficult

Parquet naturally supports:

```plaintext
Append new data
```

But updating:

```plaintext
shipment_id=101

Delivered
↓
Returned
```

is difficult.

Reason:

```plaintext
Parquet files are immutable
```

Spark cannot:

```plaintext
Open file
↓
Modify row
↓
Save
```

Instead:

```plaintext
Create new files
```

---

## Problem 4 — No Time Travel

Scenario:

```plaintext
Yesterday:

Bad data written
```

Questions:

```plaintext
Can I easily rollback?

Can I read previous versions?
```

Raw Parquet:

```plaintext
Very difficult
```

---

## Problem 5 — Small File Problem

Example:

```plaintext
100000 tiny parquet files
```

Problems:

```plaintext
Open files
↓
Read metadata
↓
Schedule tasks
↓
Execution overhead
```

Performance decreases.

---

# ACID Concepts

Delta introduces transactional behavior.

---

## A — Atomicity

Definition:

```plaintext
Everything succeeds
OR
Nothing succeeds
```

No partial writes.

Example:

Bad:

```plaintext
file1 written
file2 written
file3 failed
```

Delta:

```plaintext
Rollback
```

---

## C — Consistency

Definition:

```plaintext
Data remains valid after changes
```

No corrupted states.

---

## I — Isolation

Definition:

```plaintext
Multiple concurrent operations
do not interfere with each other
```

Example:

```plaintext
Pipeline A writing

Pipeline B reading
```

Readers see:

```plaintext
Consistent snapshot
```

instead of:

```plaintext
Half old
+
Half new
```

---

## D — Durability

Definition:

```plaintext
Committed changes survive failures
```

Once committed:

```plaintext
Data remains available
```

---

# Delta Setup

Installed:

```bash
pip install delta-spark
```

Spark session required:

```python
.config(
    "spark.sql.extensions",
    "io.delta.sql.DeltaSparkSessionExtension"
)

.config(
    "spark.sql.catalog.spark_catalog",
    "org.apache.spark.sql.delta.catalog.DeltaCatalog"
)
```

Important:

Do NOT memorize syntax.

Understand purpose:

```plaintext
Enable Spark + Delta capabilities
```

Examples:

```plaintext
MERGE
UPDATE
DELETE
Time Travel
```

---

# First Delta Table

Created:

```python
df.write \
    .format("delta") \
    .mode("overwrite") \
    .save(
        "data/delta_shipments"
    )
```

Generated:

```plaintext
delta_shipments/

part-0000.parquet
part-0001.parquet
...

_delta_log/
```

---

# Comparing Parquet vs Delta

Parquet:

```plaintext
Folder
↓
Files
```

Spark assumes:

```plaintext
All files in folder
=
table
```

---

Delta:

```plaintext
Folder
↓
Parquet files
+
_delta_log
```

Spark assumes:

```plaintext
Read transaction log first
↓
Determine active table state
```

---

# _delta_log Observations

Observed:

```plaintext
JSON files
```

Examples:

```plaintext
commitInfo
add
```

---

## commitInfo

Purpose:

```plaintext
What operation happened?
```

Examples:

```plaintext
WRITE
OVERWRITE
MERGE
UPDATE
DELETE
```

Stores:

- timestamp
- operation type
- metadata

Think:

```plaintext
Transaction history
```

---

## add

Purpose:

```plaintext
These files belong to current table state
```

Example:

```plaintext
Version 1:

part-0001
part-0002
part-0003
```

---

# Why Delta Needs Metadata

Initial thought:

```plaintext
Metadata stores schema
```

Correct — but incomplete.

Metadata also determines:

- current table version
- active files
- removed files
- schema
- transaction history
- table state

Important idea:

```plaintext
Metadata
↓
Defines truth
```

Think:

```plaintext
Current table:

Use:
part-0001
part-0004
part-0005

Ignore:
part-0002
part-0003
```

Without metadata:

Spark may read:

```plaintext
Old data
+
New data
+
Duplicate data
```

---

# Final Mental Model

Parquet:

```plaintext
Storage
```

Delta:

```plaintext
Storage
+
Book of truth
```

Where:

```plaintext
Book of truth
=
_delta_log
```

---

# Think Like A Platform Engineer

Scenario:

```plaintext
50 pipelines
```

simultaneously writing:

```plaintext
shipments
customers
inventory
analytics
```

Preferred:

```plaintext
Delta tables
```

Reason:

```plaintext
ACID guarantees
↓
Reliable writes
↓
Versioning
↓
Rollback capability
↓
Concurrency support
```

instead of:

```plaintext
Raw parquet files
```

---

# Key Takeaways

- Delta is not a Parquet replacement
- Delta adds reliability and transactions
- Raw Parquet struggles with updates and concurrency
- ACID prevents inconsistent states
- Metadata determines current table state
- _delta_log acts like a transaction history
- Delta feels more like a database table than a file format

---