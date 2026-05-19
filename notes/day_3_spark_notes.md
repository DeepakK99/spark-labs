# Day 3 — DAGs, Execution Plans, Stages, Tasks, Shuffle

# Core Realization

Spark does NOT execute code line-by-line like normal Python.

Spark workflow is closer to:

```text id="n1"
Python Code
     ↓
Logical Plan
     ↓
Optimized Logical Plan
     ↓
Physical Plan
     ↓
Stages
     ↓
Tasks
     ↓
Execution
```

Spark is fundamentally:

* a distributed execution planner
* a query optimizer
* a DAG execution engine

---

# DAG (Directed Acyclic Graph)

## Meaning

A DAG represents:

* operations
* dependencies
* execution flow

Example pipeline:

```python id="n2"
df.filter(...)
  .select(...)
  .groupBy(...)
  .avg(...)
```

becomes:

```text id="n3"
Read
 ↓
Filter
 ↓
Select
 ↓
GroupBy
 ↓
Aggregate
```

Spark internally models this as a graph.

---

# Why Spark Uses DAGs

Spark needs DAGs for:

### 1. Dependency Tracking

Determine which operations depend on others.

---

### 2. Optimization

Reorder or eliminate unnecessary work.

---

### 3. Failure Recovery

Recompute only lost partitions instead of entire jobs.

---

### 4. Distributed Scheduling

Break computation into stages/tasks.

---

# Important Mental Shift

Spark does NOT think:

```text id="n4"
Run line 1
Run line 2
Run line 3
```

Spark thinks:

```text id="n5"
Build dependency graph
```

This is a major conceptual difference from traditional Python execution.

---

# Logical vs Physical Plans

Running:

```python id="n6"
result.explain(True)
```

showed multiple planning layers.

---

# 1. Parsed Logical Plan

Initial interpretation of user code.

Represents:

* transformations
* operations
* column references

---

# 2. Analyzed Logical Plan

Spark validates:

* schema
* column existence
* data types

---

# 3. Optimized Logical Plan

Spark optimizes execution.

Observed optimization:

* unnecessary columns removed
* column pruning occurred

Example:
Columns selected but not needed later may disappear.

This demonstrates:

```text id="n7"
Spark rewrites plans intelligently
```

---

# 4. Physical Plan

Actual executable strategy.

Includes:

* execution operators
* shuffles
* exchanges
* stage boundaries

Physical plan represents:

```text id="n8"
how Spark will actually execute computation
```

---

# Narrow vs Wide Transformations

## Narrow Transformations

Examples:

* filter
* select
* withColumn

Characteristics:

* data remains in same partition
* no network movement
* can pipeline efficiently

Visualization:

```text id="n9"
Partition1 → Partition1
Partition2 → Partition2
Partition3 → Partition3
```

Cheap operations.

---

# Wide Transformations

Examples:

* groupBy
* join
* distinct
* repartition

Characteristics:

* require data movement between partitions
* trigger shuffle
* create stage boundaries

Visualization:

```text id="n10"
P1 ↘
P2 → regroup
P3 ↗
```

Expensive operations.

---

# Shuffle

## Core Realization

Shuffle is one of Spark’s most expensive operations.

Shuffle involves:

* network IO
* disk IO
* serialization
* repartitioning
* sorting

---

# Why groupBy Causes Shuffle

Example:

```python id="n11"
df.groupBy("Carrier")
```

Spark must ensure:

```text id="n12"
all rows with same Carrier end up together
```

Rows may initially exist across multiple partitions.

Therefore Spark redistributes data.

This redistribution is:

# shuffle

---

# Exchange Operator

Observed in physical plan:

```text id="n13"
Exchange
```

Meaning:

* Spark is redistributing data
* shuffle boundary exists
* new stage likely begins

Important insight:

```text id="n14"
Wide transformations create shuffle boundaries
```

---

# ShuffleRead

Observed:

```text id="n15"
ShuffleRead
```

Meaning:
Executors are reading shuffled intermediate data.

---

# Stages

## Definition

A stage is:

> a group of transformations that can execute together without shuffle.

---

# Example

Pipeline:

```python id="n16"
filter
→ select
→ groupBy
```

Possible execution:

## Stage 1

```text id="n17"
Read
Filter
Select
```

## Stage 2

```text id="n18"
Shuffle
GroupBy
Aggregate
```

Reason:

```text id="n19"
groupBy requires redistribution of data
```

---

# Tasks

## Definition

Tasks are smallest execution units.

Typically:

```text id="n20"
1 task per partition per stage
```

Example:

```text id="n21"
4 partitions
→
4 tasks
```

Tasks are executed by executors.

---

# Important Insight

Stages operate on:

```text id="n22"
groups of transformations
```

Tasks operate on:

```text id="n23"
individual partitions
```

---

# Spark UI Observations

Spark UI available at:

```text id="n24"
http://localhost:4040
```

Observed:

* Jobs
* Stages
* Executors
* SQL plans
* DAG visualization

---

# Important Observation

One pipeline can create multiple jobs because:

* each action may trigger execution
* internal Spark operations may create additional jobs

---

# WholeStageCodegen

Observed:

```text id="n25"
WholeStageCodegen
```

Very important optimization.

Spark dynamically generates optimized JVM bytecode.

Instead of:

* many tiny operators
* repeated function calls

Spark fuses operations into optimized execution pipelines.

This reduces:

* JVM overhead
* object allocations
* execution cost

Spark behaves similarly to:

* database engines
* query compilers

---

# MapPartitions

Observed:

```text id="n26"
MapPartitions
```

Important realization:

Spark processes:

```text id="n27"
partition-at-a-time
```

NOT:

```text id="n28"
global row-at-a-time
```

This is foundational for scalability.

---

# Important System-Level Insight

Spark optimization often becomes:

```text id="n29"
compute cost
vs
shuffle cost
```

And frequently:

```text id="n30"
shuffle dominates
```

This is why:

* joins
* groupBy
* repartitioning

must be handled carefully at scale.

---

# Biggest Concept Learned Today

Spark is fundamentally:

```text id="n31"
distributed execution orchestration
```

NOT just DataFrame manipulation.

---

# End-to-End Spark Mental Model

```text id="n32"
Python API
    ↓
Logical DAG
    ↓
Optimization
    ↓
Physical Plan
    ↓
Stages
    ↓
Tasks
    ↓
Executors
```

This is Spark execution flow.

---

# Most Important Insights

## 1. DAGs represent dependencies

Spark plans computation before execution.

---

## 2. Wide transformations are expensive

Because they require shuffle/data movement.

---

## 3. Shuffle creates stage boundaries

This is critical for understanding Spark execution.

---

## 4. Tasks execute partitions

Spark parallelism is deeply tied to partitions.

---

## 5. Spark behaves like a distributed query engine

Not merely a Python library.

---

# Questions To Explore Later

* How exactly does Catalyst optimizer work?
* How does Spark decide partitioning strategy?
* What causes skew?
* How can shuffle be minimized?
* How does AQE (Adaptive Query Execution) work?
* How do joins affect execution plans?
* How does Spark optimize memory usage?

---

# Personal Reflection

Spark increasingly feels like:

* distributed systems infrastructure
* execution orchestration software
* query optimization engine

rather than traditional programming.

The Spark UI made execution planning visible:

* stages
* shuffles
* tasks
* exchanges
* physical operators

which made Spark architecture feel concrete rather than abstract.
