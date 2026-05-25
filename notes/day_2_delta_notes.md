# Week 3 — Day 2
# Delta Lake Internals + Transaction Log + Time Travel

---

# Main Learning Goal

Today I learned that Delta is not just:

```plaintext
Parquet + logs
```

A better mental model:

```plaintext
Delta
=
Parquet files
+
Transaction log
+
Version history
+
Metadata
+
ACID guarantees
```

Delta behaves more like:

```plaintext
Database table
```

than:

```plaintext
Folder of files
```

---

# Important Mindset Shift

Do NOT think:

```plaintext
_delta_log = audit folder
```

Think:

```plaintext
_delta_log
=
Book of truth
```

Spark reads:

```plaintext
_delta_log
↓
Determines active table state
↓
Reads only valid files
```

---

# Transaction Log Structure

Created:

```plaintext
delta_shipments/

├── _delta_log/
│      ├── 00000000000000000000.json
│      ├── 00000000000000000001.json
│      ├── 00000000000000000002.json
│
├── part-0000.parquet
├── part-0001.parquet
...
```

Observed:

```plaintext
Version 0
Version 1
Version 2
```

Mental model:

```plaintext
Git commit history
```

---

# Understanding Commit Files

Example:

```json
{
   "commitInfo":{
      "operation":"WRITE",
      "readVersion":1,
      "isolationLevel":"Serializable"
   }
}
```

---

## commitInfo

Purpose:

```plaintext
Describes what operation happened
```

Examples:

```plaintext
WRITE
APPEND
OVERWRITE
MERGE
UPDATE
DELETE
```

Stores:

- operation type
- timestamp
- read version
- transaction information

Think:

```plaintext
Transaction history
```

---

# readVersion

Example:

```plaintext
readVersion = 1
```

Meaning:

```plaintext
Started from table version 1
↓
Created next version
```

Observed:

```plaintext
Version 0
↓
Initial write

Version 1
↓
Append

Version 2
↓
Append
```

---

# Serializable Isolation

Observed:

```plaintext
isolationLevel=Serializable
```

Meaning:

```plaintext
Transactions behave as if
they happened one after another
```

Prevents:

```plaintext
half Pipeline A
+
half Pipeline B
```

Result:

```plaintext
Consistent table state
```

---

# Blind Append

Observed:

```plaintext
isBlindAppend=true
```

Meaning:

```plaintext
Append only operation
```

Delta simply:

```plaintext
Create new file
↓
Register file
```

No row inspection required.

---

# Understanding add

Observed:

```json
{
   "add":{
      "path":"part-00007....parquet"
   }
}
```

Purpose:

```plaintext
Register new file
as active table data
```

Important:

Delta does NOT say:

```plaintext
Read every parquet file in folder
```

Instead:

```plaintext
Read metadata
↓
Determine active files
```

---

# File Statistics

Observed:

```json
"stats":
{
    "numRecords":1,
    "minValues":{},
    "maxValues":{},
    "nullCount":{}
}
```

Initially thought:

```plaintext
Extra metadata
```

Actual purpose:

```plaintext
Performance optimization
```

---

# Data Skipping

Example:

Files:

```plaintext
File A:

min cost=100
max cost=400

File B:

min cost=500
max cost=700

File C:

min cost=1500
max cost=3000
```

Query:

```sql
SELECT *
FROM shipments
WHERE ShippingCostUSD >1000
```

Without metadata:

```plaintext
Read A
Read B
Read C
```

With Delta stats:

```plaintext
File A:

max=400
↓
Skip

File B:

max=700
↓
Skip

File C:

max=3000
↓
Read
```

Result:

```plaintext
Read fewer files
↓
Lower I/O
↓
Faster queries
```

This is:

```plaintext
Data skipping
```

---

# Delta History

Used:

```python
deltaTable.history().show()
```

Observed:

```plaintext
version
timestamp
operation
readVersion
isolationLevel
operationMetrics
```

Mental model:

```plaintext
git log
```

for tables.

---

# Time Travel

Used:

```python
old_df = spark.read \
    .format("delta") \
    .option(
        "versionAsOf",
        0
    ) \
    .load(
        "data/delta_shipments"
    )
```

Observed:

```plaintext
Version 0:

20 rows

Current:

22 rows
```

Important realization:

Delta did NOT:

```plaintext
Restore backup
```

Instead:

```plaintext
Read transaction log
↓
Determine files belonging to version 0
↓
Load only those files
```

---

# Why Time Travel Matters

Initial thought:

```plaintext
Cool feature
```

Better understanding:

```plaintext
Recovery feature
+
Production safety feature
```

Example:

```plaintext
Nightly pipeline writes
corrupted shipment costs
```

Without Delta:

```plaintext
Find corrupted files
Restore backup
Rerun jobs
```

With Delta:

```python
.option(
    "versionAsOf",
    previous_version
)
```

or later:

```sql
RESTORE TABLE
```

Recovery becomes:

```plaintext
Minutes instead of hours
```

---

# Schema Lesson Today

Encountered:

```plaintext
DELTA_FAILED_TO_MERGE_FIELDS
```

Cause:

```plaintext
Existing:

OrderDate → DateType

Incoming:

OrderDate → StringType
```

Important realization:

Problem:

```plaintext
String vs Date mismatch
```

NOT:

```plaintext
Delta cannot handle dates
```

Lesson:

```plaintext
Do not blindly trust schema inference
```

Production preference:

```plaintext
Explicit schemas
OR
Reuse existing schema
```

---

# Final Mental Model

Parquet:

```plaintext
Stores bytes
```

Delta:

```plaintext
Stores data
+
Tracks history
+
Tracks state
+
Tracks metadata
+
Provides recovery
```

---

# Key Takeaways

- Delta maintains version history
- _delta_log determines table truth
- commit files behave like Git commits
- Delta stores statistics for optimization
- Data skipping reduces unnecessary file reads
- Time travel is a recovery mechanism
- Delta enforces schema consistency
- Delta behaves like a database table rather than a folder of files

---