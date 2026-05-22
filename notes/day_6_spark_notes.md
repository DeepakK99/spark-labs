# Week 2 - Day 6
# Spark Optimization, Caching and Performance Thinking

---

# Main Learning Goal

Today I learned that optimization is not:

```plaintext
How do I make Spark code work?
```

Optimization is:

```plaintext
Why is this Spark job slow?
```

Important mindset:

```plaintext
Good Spark engineers write code

Strong Spark engineers predict bottlenecks
before execution
```

---

# Transformations vs Actions Review

Transformations:

- lazy
- build lineage/DAG
- do not execute immediately

Examples:

```python
select()

filter()

groupBy()

join()

withColumn()
```

Actions:

- trigger execution
- materialize results

Examples:

```python
show()

count()

collect()

write()

take()
```

---

# Important count() confusion

Case 1:

```python
df.count()
```

Action

Reason:

```plaintext
Spark must immediately return a number
```

Execution happens immediately.

---

Case 2:

```python
df.groupBy("Status").count()
```

Transformation

Reason:

```plaintext
Count here means:

"Define aggregation for each group"
```

Spark only builds a plan.

Execution happens later.

---

# Lineage and Recomputation

Example:

```python
df1 = df.filter(...)

df2 = (
    df1.groupBy(...)
       .count()
)

df2.show()

df2.write.parquet(...)
```

Without caching:

Spark may execute:

```plaintext
Read
↓
Filter
↓
GroupBy
↓
Count
↓
Show
```

then later:

```plaintext
Read
↓
Filter
↓
GroupBy
↓
Count
↓
Write
```

again.

Spark stores lineage, not results.

---

# Caching

Purpose:

Store intermediate results for reuse.

Example:

```python
processed.cache()
```

Flow:

Without cache:

```plaintext
Read
↓
Transform
↓
Action
↓
Recompute later
```

With cache:

```plaintext
Read
↓
Transform
↓
Store in memory
↓
Reuse later
```

---

# Important Observation

```python
processed.cache()
```

does NOT immediately cache data.

Cache itself is lazy.

Data is cached only after:

```python
processed.show()

processed.count()

processed.write()
```

or another action.

---

# Why cache can initially become slower

First cached execution:

```plaintext
Compute
+
Store in memory
```

Spark performs extra work.

Later executions:

```plaintext
Read from memory
```

instead of recomputing.

---

# When should cache be used?

Good cases:

- expensive transformations
- reused multiple times
- data reasonably fits in memory

Example:

```python
processed.cache()

processed.show()

processed.write()

processed.collect()
```

---

# Why not cache everything?

Example:

```python
huge_df.cache()

another_huge_df.cache()

everything.cache()
```

Problems:

```plaintext
Memory pressure
↓
Eviction
↓
Disk spill
↓
Garbage collection overhead
↓
Slow jobs
```

Important mindset:

```plaintext
Cache selectively
```

---

# Wide vs Narrow Transformations

Narrow:

```python
select()

filter()

withColumn()
```

Characteristics:

```plaintext
No data movement
Usually cheaper
```

---

Wide:

```python
groupBy()

join()

distinct()

orderBy()

repartition()
```

Characteristics:

```plaintext
Often trigger shuffle
Potentially expensive
```

---

# Reading Physical Plans

Important nodes:

### Exchange

Meaning:

```plaintext
Shuffle happening
```

Data moves across partition boundaries.

---

### HashAggregate

Meaning:

```plaintext
Aggregation work
```

Spark often performs:

```plaintext
Partial aggregation
↓
Shuffle
↓
Final aggregation
```

---

### Sort

Meaning:

```plaintext
Global sorting operation
```

Potentially expensive.

---

# Shuffle Partition Observation

Observed:

```plaintext
hashpartitioning(Status,200)
```

Spark default:

```python
spark.sql.shuffle.partitions
```

Default:

```plaintext
200
```

Meaning:

```plaintext
Create 200 shuffle partitions
```

Problem with tiny data:

```plaintext
20 rows
200 partitions
```

Possible result:

```plaintext
Many tiny tasks
↓
High scheduling overhead
```

Important rule:

```plaintext
Too few partitions
↓
Poor parallelism

Too many partitions
↓
High overhead

Balanced partitions
↓
Better performance
```

---

# Join Optimization

Normal join:

```plaintext
Big DF
↔ Shuffle ↔
Big DF
```

Potential problems:

- network transfer
- shuffle files
- skew
- expensive execution

---

# Broadcast Join

Purpose:

Copy small dataset to executors.

Example:

```python
from pyspark.sql.functions import broadcast

df.join(
    broadcast(small_df),
    "customer_id"
)
```

Flow:

```plaintext
Small DF
↓
Broadcast to executors
↓
Avoid large shuffle
```

---

# Automatic Broadcast Join

Spark can automatically decide:

```plaintext
Small table
↓
Broadcast automatically
```

Controlled by:

```python
spark.sql.autoBroadcastJoinThreshold
```

Usually around:

```plaintext
10MB
```

---

# Why large broadcast is dangerous

Example:

```plaintext
50GB table
```

Broadcast:

```plaintext
50GB
↓
Copied to every executor
```

Problems:

```plaintext
Memory pressure
↓
GC pauses
↓
Spilling
↓
Possible OutOfMemory
```

Rule:

```plaintext
Small table
↓
Broadcast

Huge table
↓
Avoid broadcasting
```

---

# Spark Execution Model

Structure:

```plaintext
Machine
↓
Executors
↓
Executor Cores
↓
Tasks
↓
Partitions
```

Important relationship:

```plaintext
One partition
↓
One task
```

Tasks execute inside executors.

---

# Broadcast vs Shuffle

Broadcast:

```plaintext
Driver
↓
Executors
```

Pattern:

```plaintext
One → Many
```

---

Shuffle:

```plaintext
Executor ↔ Executor
```

Pattern:

```plaintext
Many ↔ Many
```

---

# Bad Pipeline Exercise

Pipeline:

```python
bad_pipeline = (
    df.distinct()
      .repartition(50)
      .groupBy("Status")
      .count()
      .orderBy("count")
)
```

Suspicious operations:

### distinct()

```plaintext
Global duplicate detection
↓
Shuffle
```

---

### repartition()

```plaintext
Full redistribution
↓
Shuffle
```

---

### groupBy()

```plaintext
Same keys together
↓
Shuffle
```

---

### orderBy()

```plaintext
Global sorting
↓
Shuffle
```

Observed:

```plaintext
Multiple Exchange nodes
```

Meaning:

```plaintext
Multiple expensive data movements
```

---

# Performance Engineer Checklist

Before running a job ask:

```plaintext
□ Any joins?

□ Any groupBy?

□ Any distinct?

□ Any orderBy?

□ Any repartition?

□ Any skew possibility?

□ Can broadcast help?

□ Is storage format okay?

□ Output file count okay?

□ Is cache useful?
```

---

# Key Takeaways

- Spark stores lineage, not results
- Cache stores reusable computation
- Cache is lazy
- Not everything should be cached
- Wide transformations often trigger shuffle
- Exchange usually indicates expensive movement
- Broadcast helps for small datasets
- Large broadcast can hurt memory
- Execution plans reveal bottlenecks
- Good optimization starts before execution

---