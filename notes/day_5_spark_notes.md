# Week 2 - Day 5
# Parquet, Columnar Storage and Data Layout

---

# Main Learning Goal

Today I learned that Spark performance is not only about writing efficient code.

Performance also depends on:

- storage format
- data layout
- partitioning strategy
- amount of data read

Important mindset:

```plaintext
Good performance
≠ only good code

Good performance
=
good execution
+
good storage layout
+
good partitioning
```

---

# CSV vs Parquet Mindset

Do NOT think:

```plaintext
CSV = data storage
```

Think:

```plaintext
CSV = data interchange

Parquet = analytical storage
```

CSV is useful for exchanging data between systems.

Parquet is designed for analytical workloads.

---

# Why CSV is bad for analytics

CSV uses row-based storage.

Example:

```plaintext
Row1:
1,Rahul,Mumbai,Delhi,Delayed,500

Row2:
2,Ananya,Chennai,Pune,Delivered,700
```

Suppose query:

```python
df.select("Status")
```

Spark still has to:

```plaintext
Read row
↓
Parse commas
↓
Identify columns
↓
Extract Status
↓
Ignore remaining columns
```

Even if only one column is required.

Problems:

- reads unnecessary data
- parsing overhead
- schema inference cost
- inefficient at scale

---

# Columnar Storage

Parquet uses column-based storage.

Instead of:

```plaintext
Row1:
1,Rahul,Delayed,500

Row2:
2,Ananya,Delivered,700
```

Think:

```plaintext
ShipmentID:
1
2

CustomerName:
Rahul
Ananya

Status:
Delayed
Delivered

ShippingCost:
500
700
```

Now if query asks:

```python
df.select("Status")
```

Spark can read:

```plaintext
Status only
```

instead of reading all columns.

---

# Why Parquet is efficient

Parquet stores:

- data
- metadata
- schema

Unlike CSV:

```python
spark.read.csv(
    ...,
    header=True,
    inferSchema=True
)
```

Parquet can do:

```python
spark.read.parquet(...)
```

because schema already exists inside the files.

Benefits:

- no schema inference
- less parsing
- lower I/O
- faster reads

---

# Parquet Output Structure

Observed files:

```plaintext
_SUCCESS

part-00000-xxxxx.snappy.parquet

.crc files
```

Meaning:

### part-xxxxx.parquet

Actual data file.

Spark writes:

```plaintext
One partition
        ↓
One task
        ↓
One output file
```

---

### _SUCCESS

Marker indicating:

```plaintext
Write completed successfully
```

Used by pipelines and systems to verify job completion.

---

### .crc files

Checksum files for validating file integrity.

---

# Small File Problem

Example:

```python
df.repartition(1000)

df.write.parquet(...)
```

Results:

```plaintext
1000 partitions
↓
1000 tasks
↓
1000 parquet files
```

Problems:

- scheduler overhead
- metadata overhead
- many file open operations
- slower reads
- many tiny files

Example:

Bad:

```plaintext
10000 files × 100 KB
```

Better:

```plaintext
10 files × 100 MB
```

---

# Column Pruning

Definition:

Spark reads only required columns.

Observed using:

```python
parquet_df.select(
    "Status"
).explain(True)
```

Observed:

```plaintext
FileScan parquet [Status]

ReadSchema:
struct<Status:string>
```

Meaning:

Spark only loaded:

```plaintext
Status
```

instead of:

```plaintext
ShipmentID
OrderDate
CustomerName
...
```

Benefits:

- less memory usage
- less disk I/O
- faster processing

---

# Compression

Parquet automatically compresses data.

Repeated values:

```plaintext
Delivered
Delivered
Delivered
Delivered
```

compress well.

Benefits:

- reduced storage cost
- reduced I/O
- faster reads

Observed:

Parquet files use:

```plaintext
snappy
```

compression.

---

# Partitioned Parquet

Created:

```python
df.write.mode("overwrite") \
    .partitionBy(
        "Status"
    ) \
    .parquet(
        "data/partitioned_shipments"
    )
```

Generated:

```plaintext
partitioned_shipments/

Status=Cancelled/
Status=Delivered/
Status=Pending/
Status=In Transit/
```

These are called:

```plaintext
Partition directories
```

not just folders.

Spark interprets:

```plaintext
Status=Delivered/
```

as:

```plaintext
Status = Delivered
```

---

# Partition Pruning

Definition:

Spark skips unnecessary partition directories.

Query:

```python
partition_df.filter(
    partition_df.Status=="Delivered"
)
```

Observed:

```plaintext
PartitionFilters:
(Status = Delivered)
```

Meaning:

Spark skipped:

```plaintext
Status=Cancelled/
Status=Pending/
Status=In Transit/
```

and read only:

```plaintext
Status=Delivered/
```

Benefits:

- less data scanned
- less I/O
- faster execution

---

# Difference: Column Pruning vs Partition Pruning

Column Pruning:

```plaintext
Skip unnecessary columns
```

Partition Pruning:

```plaintext
Skip unnecessary files/directories
```

---

# Choosing Good Partition Columns

Good partition columns:

- frequently filtered
- low/moderate cardinality
- meaningful access patterns

Examples:

```plaintext
date
year
month
country
region
status
```

Bad partition columns:

```plaintext
customer_id
email
tracking_number
```

because:

```plaintext
Millions of unique values
↓
Millions of directories/files
↓
Metadata explosion
```

---

# Production Thinking Exercise

Scenario:

```sql
SELECT *
FROM shipments
WHERE shipment_date='2026-05-22'
```

Dataset size:

```plaintext
100 TB
```

Best design:

```plaintext
Partitioned Parquet by shipment_date
```

Reason:

```plaintext
Parquet
    ↓
Column pruning

Partitioning
    ↓
Partition pruning

Less data read
↓
Faster queries
```

---

# Key Takeaways

- CSV is poor for analytical workloads
- Parquet stores schema and metadata
- Parquet uses columnar storage
- Column pruning reduces data read
- Partition pruning skips unnecessary files
- One partition usually creates one output file
- Too many partitions create small file problems
- Storage layout is as important as code

---