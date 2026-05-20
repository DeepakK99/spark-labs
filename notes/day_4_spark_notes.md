# Week 2 - Day 4
# Spark Partitions, Shuffle and Skew

---

## Main Learning Goal

Today I learned that partitions are not random chunks of data.

Partitions determine:

- parallelism
- execution strategy
- performance
- cost
- execution time

Spark performance is heavily affected by how data is distributed.

---

# Why do partitions exist?

Partitions allow Spark to process data in parallel.

Example:

1000 rows:

```plaintext
P1 → 250 rows
P2 → 250 rows
P3 → 250 rows
P4 → 250 rows
```

Execution:

```plaintext
Executor A → P1
Executor B → P2
Executor C → P3
Executor D → P4
```

Multiple executors can work simultaneously.

Without partitions Spark would process everything sequentially.

---

# Problem with uneven partitions

Example:

```plaintext
P1 → 900 rows
P2 → 20 rows
P3 → 40 rows
P4 → 40 rows
```

Problem:

- Executor A keeps working
- Other executors finish early
- Resources become idle
- Spark waits for the slowest task

Important idea:

```plaintext
Stage completion time ≈ slowest task time
```

not:

```plaintext
Average task time
```

---

# Repartition()

Purpose:

Increase or redistribute partitions.

Example:

```python
df.repartition(10)
```

Characteristics:

- causes full shuffle
- redistributes data across partitions
- creates more balanced partitions
- expensive operation

Use when:

- increasing parallelism
- fixing skew
- preparing downstream work

---

# Coalesce()

Purpose:

Reduce number of partitions.

Example:

```python
df.coalesce(2)
```

Characteristics:

- reduces partitions
- avoids full shuffle when possible
- cheaper than repartition
- mainly used when reducing partitions

Use when:

- too many small partitions exist
- reducing output files

---

# Difference: Repartition vs Coalesce

| Repartition | Coalesce |
|-------------|-----------|
| Full shuffle | Avoids full shuffle when possible |
| Expensive | Cheaper |
| Increase or decrease partitions | Mainly decrease partitions |
| Better balancing | Less redistribution |

---

# Why was coalesce(2) still giving 1 partition?

Original dataframe:

```plaintext
Partitions = 1
```

Code:

```python
df.coalesce(2)
```

Coalesce reduces partitions.

Spark cannot reduce:

```plaintext
1 → 2
```

so partition count stayed:

```plaintext
1
```

Working example:

```python
df2=df.repartition(10)

df3=df2.coalesce(2)
```

Result:

```plaintext
10 → 2
```

---

# What is Shuffle?

Definition:

Movement of data across partitions.

Example:

```python
df.groupBy("status").count()
```

Spark must gather identical keys together.

Before shuffle:

```plaintext
P1 → delayed, delivered
P2 → delayed
P3 → returned, delivered
```

After shuffle:

```plaintext
P1 → delayed
P2 → delivered
P3 → returned
```

---

# Why is shuffle expensive?

Shuffle involves:

- network transfer
- disk I/O
- serialization
- coordination overhead
- intermediate shuffle files

Because data moves across machines/partitions.

---

# Spark UI observations

Observed:

### Shuffle Write

Spark writes intermediate data before redistribution.

---

### Exchange

Represents actual movement of data across partition boundaries.

Usually indicates:

```plaintext
Shuffle happening
```

---

### AQE Shuffle Read

AQE:

```plaintext
Adaptive Query Execution
```

Spark can optimize at runtime by:

- combining small partitions
- adjusting shuffle partitions
- improving execution plan

---

### WholeStageCodeGen

Spark generates optimized JVM code for execution.

Flow:

```plaintext
DataFrame logic
        ↓
Catalyst optimization
        ↓
Generated JVM code
        ↓
Execution
```

---

# Data Skew

Definition:

Uneven distribution of data causing one task to process much more data than others.

Example:

```plaintext
Delayed → 900 rows
Delivered → 50 rows
Returned → 50 rows
```

After:

```python
groupBy("status")
```

Possible result:

```plaintext
Task1 → 900 rows
Task2 → 50 rows
Task3 → 50 rows
```

Problem:

- one task runs for a long time
- other tasks finish early
- executors become idle
- overall job becomes slow

---

# Why is skew dangerous?

Because:

```plaintext
More machines ≠ faster execution
```

If one task owns most of the data:

```plaintext
Executor1 → huge task
Executor2 → idle
Executor3 → idle
Executor4 → idle
```

Spark still waits for the slowest task.

---

# Handling skew (initial idea)

Idea:

Split heavily repeated keys into multiple temporary groups.

Example:

Instead of:

```plaintext
customer_id=1
```

temporarily create:

```plaintext
customer_id=1_1
customer_id=1_2
customer_id=1_3
customer_id=1_4
```

Process separately and merge later.

This concept leads toward:

```plaintext
Salting
```

---

# Why too many partitions are bad

Example:

```plaintext
20 MB data
1000 partitions
```

Approximate:

```plaintext
20KB per partition
```

Problems:

- many tasks created
- scheduler overhead
- metadata overhead
- coordination cost
- many tiny output files

Important idea:

```plaintext
Too few partitions
    ↓
Poor parallelism

Too many partitions
    ↓
High overhead

Balanced partitions
    ↓
Best throughput
```

---

# Key Takeaways

- Partitions determine execution behavior
- Repartition causes shuffle
- Coalesce reduces partitions efficiently
- groupBy often triggers shuffle
- Shuffle is expensive
- Skew creates bottlenecks
- Spark job time often depends on the slowest task
- Spark UI gives visibility into execution behavior

---