# Distributed Shipment Analytics Pipeline

## Project Overview

This project is an end-to-end Spark data pipeline built as part of Week 2 learning.

The goal of the project is not only to process shipment data, but also to apply Spark optimization concepts learned throughout the week:

- distributed execution
- partitions
- shuffle
- Parquet storage
- partition pruning
- caching
- execution plans
- performance thinking

The pipeline reads shipment data from CSV, transforms and enriches the data, stores optimized output as partitioned Parquet, and generates analytical insights.

---

## Architecture

```plaintext
Shipment CSV
      ↓
Ingestion Layer
      ↓
Transformation Layer
      ↓
Optimized Partitioned Parquet
      ↓
Analytics Layer
      ↓
Performance Optimization
      ↓
Execution Analysis
```

---

## Project Structure

```plaintext
spark-labs/

│
├── data/
│   ├── raw/
│   │   └── shipments.csv
│   │
│   └── processed/
│       └── shipments_parquet/
│
├── src/
│   ├── ingestion.py
│   ├── transformation.py
│   ├── analytics.py
│   ├── optimization.py
│   └── main.py
│
├── notes/
│
└── README.md
```

---

## Pipeline Flow

### 1. Ingestion Layer

Reads shipment CSV data.

Features:

- schema inference
- row count logging
- schema validation

Example:

```python
df = spark.read.csv(
    "data/raw/shipments.csv",
    header=True,
    inferSchema=True
)
```

---

### 2. Transformation Layer

Performs cleaning and enrichment.

Cleaning:

- remove null shipment IDs
- remove duplicate shipment IDs

Derived Columns:

### delivery_days

Calculated:

```plaintext
DeliveryDate − ShipDate
```

---

### delivery_category

Rules:

```plaintext
<=2      → Fast
<=5      → Normal
>5       → Delayed
```

---

### high_cost_flag

Rules:

```plaintext
ShippingCostUSD > 1000
```

---

### 3. Storage Layer

Writes optimized output using Parquet.

Format:

```python
df.write \
    .partitionBy("Status") \
    .mode("overwrite") \
    .parquet(...)
```

Output example:

```plaintext
shipments_parquet/

Status=Cancelled/

Status=Delivered/

Status=Pending/

Status=In Transit/
```

---

## Why Partition By Status?

Chosen because:

- low cardinality
- frequently queried field
- supports partition pruning
- manageable number of partition directories

Bad candidate example:

```plaintext
CustomerName
```

because:

```plaintext
High cardinality
        ↓
Many directories
        ↓
Small file problem
        ↓
Metadata overhead
```

---

## Analytics Layer

Generated insights:

### Average delivery days by status

Example:

```plaintext
Delivered → 2.1 days
Pending → 4.8 days
```

---

### Shipment count by route

```plaintext
OriginCity
        ↓
DestinationCity
```

---

### Delayed shipment percentage

Measures operational performance.

---

### Revenue by destination

Aggregates shipping revenue.

---

### Top customers by shipment cost

Ranks customers based on total shipment spending.

---

## Optimizations Applied

### Partitioned Parquet

Benefits:

- reduced I/O
- partition pruning
- faster filtering

---

### Column Pruning

Spark reads only required columns.

Example:

```python
df.select("Status")
```

instead of reading all columns.

---

### Caching

Candidate:

```python
transformed_df.cache()
```

Reason:

- expensive transformations
- reused multiple times
- avoids recomputation

---

### Execution Plan Analysis

Used:

```python
df.explain(True)
```

Observed:

- Exchange nodes
- HashAggregate
- BroadcastHashJoin
- Sort operations

---

## Performance Observations

Suspicious operations:

```python
groupBy()

distinct()

join()

orderBy()

repartition()
```

Reason:

```plaintext
Potential shuffle
↓
Data movement
↓
Higher execution cost
```

---

## Technologies Used

- Python
- PySpark
- Spark SQL
- Parquet
- Spark UI

---

## How To Run

Run:

```bash
python src/main.py
```

Open Spark UI:

```plaintext
http://localhost:4040
```

Inspect:

- jobs
- stages
- tasks
- execution timeline

---

## Future Improvements

Possible production enhancements:

### Delta Lake

- ACID transactions
- schema evolution
- time travel

---

### Airflow Integration

- workflow orchestration
- scheduling
- dependency management

---

### Kafka Integration

- streaming ingestion

---

### AWS S3 Integration

- cloud storage
- scalable data lake

---

### Databricks / DLT Pipeline

- managed Spark environment
- production-grade pipelines

---

## Key Learnings

Through this project:

- Spark execution became easier to understand
- partitioning decisions started making sense
- execution plans became more readable
- optimization thinking became more natural
- Spark started feeling like a distributed system rather than a library

---