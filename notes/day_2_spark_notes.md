# Day 2 — Spark DataFrames, Transformations, Actions, Lazy Evaluation

# Core Realization

Spark is NOT just:

* a DataFrame library
* pandas at scale

Spark is:

* a distributed execution engine
* a query planner
* a lazy computation system

A Spark DataFrame is not merely data in memory.

It is:

```text
distributed dataset + logical execution plan
```

---

# Spark DataFrames

## Important Properties

Spark DataFrames are:

* distributed
* schema-aware
* immutable
* lazily evaluated

Unlike pandas, Spark avoids immediate in-place mutation.

Example:

```python
df = df.withColumn("cost_with_tax", col("cost") * 1.18)
```

This creates:

* a new DataFrame
* a new transformation plan

Spark does not immediately process data.

---

# Immutability

## Meaning

DataFrames cannot be modified in place.

Every transformation creates:

* a new logical DataFrame
* a new execution plan node

---

## Why Immutability Matters

Immutability helps with:

### 1. Fault Tolerance

Spark can recompute lost partitions.

### 2. Optimization

Spark can globally optimize transformations before execution.

### 3. Distributed Consistency

Avoids synchronization complexity across machines.

### 4. Safer Parallelism

No shared mutable distributed state.

---

# Transformations vs Actions

## Transformations

Transformations define computation.

Examples:

```python
filter()
select()
groupBy()
withColumn()
```

Transformations:

* do NOT execute immediately
* build logical execution plans

Example:

```python
filtered_df = df.filter(df.cost > 500)
```

This mostly creates a plan, not actual computation.

---

## Actions

Actions trigger execution.

Examples:

```python
show()
count()
collect()
write()
```

Example:

```python
filtered_df.count()
```

This causes Spark to:

* generate physical execution plan
* schedule tasks
* process partitions
* execute computation

---

# Lazy Evaluation

## Core Idea

Spark delays execution until an action occurs.

Example:

```python
df1 = df.filter(...)
df2 = df1.select(...)
df3 = df2.groupBy(...)

df3.show()
```

Spark does NOT execute:

* filter
* select
* groupBy

individually.

Instead:

```text
Build logical plan
        ↓
Optimize plan
        ↓
Execute optimized computation
```

---

# Why Lazy Evaluation Is Powerful

Without lazy execution:

```text
filter → execute
select → execute
groupBy → execute
```

Problems:

* repeated scans
* unnecessary intermediate computation
* excessive data movement
* no global optimization

With lazy execution:
Spark can:

* combine operations
* prune columns
* optimize filters
* reduce shuffles
* minimize work

---

# Spark Feels Different From Pandas

## Pandas

* eager execution
* single-machine memory model
* immediate mutation
* local computation

## Spark

* distributed execution model
* partition-based processing
* lazy planning
* execution optimization
* DAG-oriented computation

Spark feels more like:

* infrastructure software
* distributed systems runtime
* query optimizer

than a normal Python library.

---

# Distributed Thinking

Even local Spark execution uses:

* partitions
* tasks
* scheduling
* execution planning

Spark always thinks in distributed terms.

Local mode is effectively:

```text
cluster of one machine
```

---

# Partitions

Partitions are:

* chunks of distributed data
* units of parallelism

Observed:

```python
df.rdd.getNumPartitions()
```

returned:

```text
1
```

Reason:

* small CSV
* local execution
* Spark determined one partition was sufficient

Important realization:

```text
parallelism is heavily tied to partitions
```

---

# Important Mental Shift

Transformations are not:

```text
doing work
```

They are:

```text
describing work
```

Spark behaves like:

* a distributed execution planner
* a computation graph builder

---

# Most Important Concepts Learned Today

## 1. Spark is lazy

Execution happens only during actions.

---

## 2. DataFrames are immutable

New transformations create new plans.

---

## 3. Spark optimizes globally

Spark delays execution to optimize computation.

---

## 4. Spark is system-oriented

Driver
→ scheduler
→ partitions
→ tasks
→ executors

Everything is designed around distributed computation.

---

# Biggest Insight Today

Spark is fundamentally about:

```text
distributed execution planning
```

NOT merely DataFrame syntax.

---

# Questions To Revisit Later

* How exactly does Spark optimize DAGs?
* What is a stage?
* What is a task?
* What causes shuffles?
* How do partitions affect execution speed?
* How does Catalyst optimizer work?
* How does Spark decide physical execution plans?

These likely become clearer during:

* DAGs
* execution plans
* shuffles
* Catalyst optimizer
* Spark internals

---

# Personal Reflection

Spark feels intuitive because:

* it resembles distributed systems orchestration
* execution planning is explicit
* architecture concepts are visible
* computation flow is observable

Spark already feels more like:

```text
systems engineering
```

than traditional Python programming.
