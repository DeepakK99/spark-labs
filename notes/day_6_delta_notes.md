# Week 3 — Day 6
# Structured Streaming Fundamentals

---

# Main Learning Goal

Today I learned that batch systems process:

```plaintext
Existing data
```

while streaming systems process:

```plaintext
Continuously arriving events
```

Streaming is not just faster batch processing.

It introduces:

- state management
- checkpoints
- recovery
- output modes
- long-running queries

---

# Events vs Current State

Example:

Current State:

```plaintext
Shipment 101
Status = Delivered
```

This tells us:

```plaintext
Where we are
```

but not:

```plaintext
How we got here
```

---

Events:

```plaintext
Shipment Created
↓
Shipment Picked Up
↓
Shipment In Transit
↓
Shipment Delivered
```

Events provide:

- full history
- audit trail
- timeline
- ability to reconstruct current state

---

# Streaming Mental Model

Batch:

```plaintext
Read data
↓
Process
↓
Finish
```

Streaming:

```plaintext
Listen
↓
Process new events
↓
Update state
↓
Repeat forever
```

---

# Structured Streaming

Created stream:

```python
stream_df = spark.readStream \
    .schema(schema) \
    .csv("data/stream_input")
```

---

# Why Schema Is Required

Batch:

```python
spark.read.csv(...)
```

can infer schema because:

```plaintext
Files already exist
```

---

Streaming:

```python
spark.readStream.csv(...)
```

may start with:

```plaintext
No files
```

Spark cannot infer schema from future data.

Therefore:

```plaintext
Explicit schema required
```

---

# isStreaming

Checked:

```python
stream_df.isStreaming
```

Result:

```plaintext
True
```

Meaning:

```plaintext
This DataFrame is backed by a streaming source
```

---

# Why show() Does Not Work

Batch:

```python
df.show()
```

works because:

```plaintext
Dataset is finite
```

---

Streaming:

```python
stream_df.show()
```

does not make sense because:

```plaintext
Stream never ends
```

---

# Stateful Aggregations

Created:

```python
stream_df.groupBy("status").count()
```

---

Batch Meaning

```plaintext
Count statuses once
```

---

Streaming Meaning

```plaintext
Maintain counts forever
```

Example:

Batch 0:

```plaintext
Delivered = 2
Delayed = 1
```

Batch 1:

```plaintext
Delivered = 3
Delayed = 1
Pending = 1
```

Spark remembers previous counts.

---

# State

Key realization:

Spark must remember:

```plaintext
Delivered = 3
Delayed = 1
Pending = 1
```

between micro-batches.

Streaming introduces:

```plaintext
State
```

which batch jobs usually discard after completion.

---

# Micro-Batches

Input files:

```plaintext
batch1.csv
batch2.csv
```

Each became:

```plaintext
Batch 0
Batch 1
```

inside Spark.

Structured Streaming uses:

```plaintext
Micro-batch processing
```

rather than processing every event individually.

---

# Complete Output Mode

Used:

```python
.outputMode("complete")
```

Meaning:

```plaintext
Print entire current state every trigger
```

Example:

```plaintext
Delivered = 3
Delayed = 1
Pending = 1
```

all rows are emitted.

---

# Update Output Mode

Used:

```python
.outputMode("update")
```

Meaning:

```plaintext
Emit only changed rows
```

Example:

Current state:

```plaintext
Delivered = 3
Delayed = 1
Pending = 1
```

New events:

```plaintext
Delivered +2
```

New state:

```plaintext
Delivered = 5
```

Output:

```plaintext
Delivered = 5
```

only.

---

# Important Insight

Update mode tracks:

```plaintext
Output state changes
```

not:

```plaintext
Input rows
```

---

# Append Output Mode

Append mode requires:

```plaintext
Final rows
```

For:

```python
groupBy().count()
```

rows are never final.

Counts can always change.

Therefore append mode is generally not valid for this aggregation.

---

# Checkpointing

Added:

```python
.option(
    "checkpointLocation",
    "data/checkpoints"
)
```

Purpose:

```plaintext
Recovery
```

---

# Why Checkpoints Exist

Without checkpoint:

```plaintext
Crash
↓
Lose progress
```

Spark cannot know:

```plaintext
Which files were already processed
```

---

Checkpoint stores:

- progress information
- processed source metadata
- state information
- recovery metadata

---

# Checkpoint Structure

Observed:

```plaintext
checkpoints/
├── commits
├── offsets
├── sources
└── state
```

---

# Commits

Tracks:

```plaintext
Completed micro-batches
```

Observed:

```plaintext
0
1
```

for Batch 0 and Batch 1.

---

# Offsets

Tracks:

```plaintext
What input data belonged to each batch
```

---

# Sources

Tracks:

```plaintext
Files already processed
```

Example:

```plaintext
batch1.csv
batch2.csv
```

will not be reprocessed after restart.

---

# State Store

Most interesting component.

Stores:

```plaintext
Aggregation state
```

Example:

```plaintext
Delivered = 3
Pending = 1
Delayed = 1
```

---

# Why 200 State Partitions

Observed:

```plaintext
state/
├── 0
├── 1
...
├── 199
```

Reason:

```python
spark.sql.shuffle.partitions
```

defaults to:

```plaintext
200
```

---

Flow:

```plaintext
groupBy
↓
Shuffle
↓
200 partitions
↓
State Store
↓
200 state partitions
```

Streaming reuses distributed processing concepts learned in Week 2.

---

# State Store Files

Observed:

```plaintext
.delta files
```

Important:

These are NOT:

```plaintext
Delta Lake tables
```

They are internal state store files used by Spark Streaming.

---

# Recovery

After restart:

Spark loads:

```plaintext
Checkpoint
+
State
```

and continues processing only new files.

Already processed files are skipped.

---

# Exactly Once Intuition

Goal:

```plaintext
Process every event exactly once
```

Problems:

- machine crashes
- network failures
- executor failures

Streaming systems need:

```plaintext
State
+
Checkpointing
+
Recovery
```

to achieve reliable processing.

---

# At Least Once

Meaning:

```plaintext
Event processed one or more times
```

Duplicates possible.

---

# At Most Once

Meaning:

```plaintext
Event processed zero or one times
```

Data loss possible.

---

# Exactly Once

Meaning:

```plaintext
Event affects final state exactly once
```

Ideal but harder to achieve.

---

# Streaming vs Batch

Streaming candidates:

```plaintext
Shipment status updates
Customer notifications
Fraud detection
IoT events
```

Need low latency.

---

Batch candidates:

```plaintext
Daily revenue reports
Monthly executive reports
Historical analytics
```

Can tolerate delay.

---

# Architectural Lesson

Streaming is not automatically better.

Streaming adds:

- state management
- checkpointing
- recovery logic
- operational complexity

Use streaming only when the business benefits from low latency.

---

# Connections To Previous Days

Week 2:

```plaintext
groupBy
↓
Shuffle
↓
Partitions
```

Week 3 Day 6:

```plaintext
Streaming groupBy
↓
Shuffle
↓
State Store
↓
Checkpoint
```

Same distributed systems principles.

Streaming simply adds:

```plaintext
Memory
Persistence
Recovery
```

on top.

---

# Key Takeaways

- Streaming processes events continuously
- Events contain more information than current state
- Structured Streaming uses micro-batches
- Stateful aggregations require maintained state
- State is stored in the State Store
- Checkpoints enable recovery
- Complete mode emits full state
- Update mode emits changed state
- Append mode requires final rows
- Streaming introduces operational complexity
- Use streaming only when low latency matters
- Streaming builds directly on partitioning and shuffle concepts learned earlier

---