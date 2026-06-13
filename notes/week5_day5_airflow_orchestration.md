# Week 5 Day 5

# Airflow Fundamentals & Orchestration

---

# Main Learning Goal

Today I learned that building data pipelines and operating data pipelines are two different problems.

A pipeline may work perfectly once, but production systems require:

* Scheduling
* Dependency Management
* Failure Handling
* Retries
* Monitoring
* Backfills

This is why orchestration exists.

---

# What Is Airflow?

## Definition

Apache Airflow is an open-source workflow orchestration platform used to define, schedule, monitor, and manage data pipelines.

---

## Mental Model

```plaintext
Spark
=
Processes Data
```

```plaintext
Athena
=
Queries Data
```

```plaintext
Airflow
=
Coordinates Data Pipelines
```

---

Airflow does NOT:

```plaintext
Store Data

Transform Data

Execute Spark Logic
```

Instead it orchestrates workflows:

```plaintext
Run Task A
↓
If Successful
↓
Run Task B
↓
If Successful
↓
Run Task C
```

---

# Why Airflow Exists

Imagine:

```plaintext
bronze.py

silver.py

gold.py

dashboard_refresh.py
```

Manually executing:

```bash
python bronze.py
python silver.py
python gold.py
```

works initially.

---

Now imagine:

```plaintext
50 Pipelines

200 Jobs

10 Engineers

Daily Schedules

Failures

Reruns
```

Manual management becomes impossible.

---

Airflow provides:

```plaintext
Scheduling

Dependencies

Monitoring

Retries

Backfills

Alerting
```

---

# Workflow Orchestration

Important realization:

Do NOT think:

```plaintext
Airflow = Scheduler
```

Think:

```plaintext
Airflow = Workflow Orchestrator
```

Scheduling is only one feature.

---

# DAG

## Definition

DAG stands for:

```plaintext
Directed Acyclic Graph
```

---

Practical meaning:

```plaintext
Tasks
+
Dependencies
```

---

Example:

```plaintext
Extract
↓
Transform
↓
Load
```

This is a DAG.

---

# Shipment Pipeline DAG

Our platform:

```plaintext
Ingest Raw Data To Bronze
            ↓
Build Silver
            ↓
Build Gold
            ↓
Refresh Dashboard
```

---

Dependencies:

```plaintext
Bronze >> Silver >> Gold >> Dashboard
```

---

# DAG Thinking

Question:

Can Gold run before Silver?

Answer:

```plaintext
No
```

because Gold depends on Silver.

---

Question:

Can Dashboard refresh before Gold?

Answer:

```plaintext
No
```

because dashboard data depends on Gold.

---

# Core Airflow Concepts

## DAG

Workflow definition.

---

## Task

Single unit of work.

Examples:

```plaintext
Build Silver

Build Gold

Refresh Dashboard
```

---

## Operator

How a task executes.

Examples:

```plaintext
PythonOperator

BashOperator

SparkSubmitOperator
```

---

## Scheduler

Responsible for triggering workflows according to schedule.

---

# Scheduling

Example:

```plaintext
Daily Shipment Pipeline
```

runs:

```plaintext
2:00 AM
```

every day.

---

Important realization:

Pipeline schedules should align with:

```plaintext
Data Availability
```

not simply:

```plaintext
Midnight
```

---

Example:

```plaintext
OMS Ready At 1:00 AM

Inventory Ready At 1:15 AM

CSV Uploads Complete At 1:30 AM
```

Pipeline:

```plaintext
2:00 AM
```

provides a safe buffer.

---

# Retries

Example failure:

```plaintext
Database Timeout

Network Failure

Temporary API Issue
```

These are often transient failures.

---

Airflow can automatically retry:

```plaintext
Attempt 1
❌

Attempt 2
❌

Attempt 3
✅
```

---

Typical configuration:

```plaintext
Retries = 3

Retry Delay = 5 Minutes
```

---

# Why Retries Matter

Retries allow recovery from:

```plaintext
Temporary Failures
```

without requiring engineer intervention.

---

Important realization:

Retries help with:

```plaintext
Network Issues

Temporary Outages

Rate Limits
```

---

Retries do NOT fix:

```plaintext
Broken Code

Schema Changes

Missing Columns

Configuration Errors
```

---

# Failure Handling

Scenario:

```plaintext
Bronze
✅

Silver
❌
```

After all retries fail:

```plaintext
Retry 1
❌

Retry 2
❌

Retry 3
❌
```

Airflow should:

```plaintext
Mark Task Failed
↓
Mark DAG Failed
↓
Block Downstream Tasks
↓
Send Alert
```

---

Result:

```plaintext
Bronze
✅

Silver
❌

Gold
⛔

Dashboard
⛔
```

---

# Why Gold Should Not Run

If Silver fails:

```plaintext
New Data
=
Unavailable
```

Running Gold would create:

```plaintext
Incomplete Metrics

Incorrect KPIs

Stale Dashboards
```

---

# Alerting

When a DAG fails:

```plaintext
Email

Slack

PagerDuty
```

notifications should be sent.

---

Purpose:

```plaintext
Detect Problems Early
```

before business users notice.

---

# Backfills

## Definition

Backfill means:

```plaintext
Reprocess Historical Dates
```

---

Example:

```plaintext
May 1
❌ Failed

May 2
✅ Success

May 3
✅ Success
```

---

Issue fixed later.

Airflow can run:

```plaintext
Backfill May 1
```

---

This creates a new DAG run for:

```plaintext
Execution Date
=
May 1
```

and reprocesses the data.

---

# Why Backfills Matter

Without backfills:

```plaintext
Manual Scripts

Manual Data Selection

Manual Recovery
```

---

With Airflow:

```plaintext
Controlled Historical Reprocessing
```

---

# Idempotency Returns

This connects directly to Week 3.

---

Suppose May 1 is rerun.

Bad implementation:

```sql
INSERT INTO silver_shipments
```

---

Result:

```plaintext
Duplicate Records
```

---

Good implementation:

```sql
MERGE INTO silver_shipments
```

---

Result:

```plaintext
Same Final State
```

even if rerun multiple times.

---

# Definition Of Idempotency

A process is idempotent if:

```plaintext
Running It Multiple Times
Produces The Same Final State
```

---

Example:

```plaintext
Run Once
↓
100,000 Rows
```

---

```plaintext
Run Again
↓
Still 100,000 Rows
```

---

Not:

```plaintext
200,000 Rows
```

---

# Why Idempotency Matters

Production systems constantly perform:

```plaintext
Retries

Backfills

Recovery Runs

Manual Reruns
```

Without idempotency:

```plaintext
Duplicates

Incorrect Metrics

Corrupted Data
```

become common.

---

# Production Scenario

Pipeline:

```plaintext
Bronze
↓
Silver
↓
Gold
↓
Dashboard
```

---

Silver fails.

Flow:

```plaintext
Task Failure
↓
DAG Failure
↓
Gold Blocked
↓
Dashboard Blocked
↓
Alert Sent
↓
Engineer Investigates
↓
Root Cause Fixed
↓
Backfill Triggered
↓
Silver Re-runs
↓
MERGE Prevents Duplicates
↓
Gold Runs
↓
Dashboard Refreshes
↓
Pipeline Success
```

---

# Airflow In AWS Architecture

Example:

```plaintext
Airflow
↓
EMR Job
↓
Silver Layer

Airflow
↓
EMR Job
↓
Gold Layer

Airflow
↓
Athena Refresh
```

---

Important realization:

```plaintext
Airflow
=
Orchestration
```

---

```plaintext
Spark
=
Processing
```

---

```plaintext
Athena
=
Analytics
```

---

Airflow coordinates the work.

---

# Interview Question

Design:

```plaintext
Daily Shipment Processing
```

Requirements:

```plaintext
Bronze

Silver

Gold

Dashboard
```

Recommended DAG:

```plaintext
Bronze
↓
Silver
↓
Gold
↓
Dashboard
```

---

Failure Handling:

```plaintext
Retries

Alerts

Block Downstream Tasks
```

---

Recovery:

```plaintext
Backfills

Idempotent MERGE Logic
```

---

# Biggest Takeaways

Airflow is a workflow orchestrator, not just a scheduler.

---

A DAG is a collection of tasks and dependencies.

---

Tasks should execute only when dependencies succeed.

---

Retries help recover from temporary failures.

---

Alerts notify engineers when intervention is required.

---

Backfills allow historical reprocessing.

---

Idempotency is essential because reruns are normal in production.

---

# Most Important Realization

```plaintext
Building Pipelines Is Not Enough.

Production Data Engineering Requires Operating Pipelines Reliably.
```

Airflow provides the framework to do that through orchestration, monitoring, retries, alerts, and backfills.

---
