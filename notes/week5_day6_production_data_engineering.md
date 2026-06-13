# Week 5 Day 6

# Production Data Engineering

---

# Main Learning Goal

Today I learned that building a pipeline is only part of a Data Engineer's responsibility.

A production data platform must also be:

* Reliable
* Observable
* Monitorable
* Recoverable
* Business-aligned

A pipeline can be technically successful while still being a business failure.

---

# What Is Production Data Engineering?

## Definition

Production Data Engineering is the discipline of building, operating, monitoring, and maintaining reliable data systems that consistently deliver correct data within agreed timelines.

---

## Mental Model

Junior mindset:

```plaintext
Pipeline Ran
↓
Success
```

---

Production mindset:

```plaintext
Pipeline Ran
↓
Correct Data?
↓
Complete Data?
↓
Fresh Data?
↓
On Time?
↓
Business Happy?
↓
Success
```

---

# SLA

## Definition

SLA = Service Level Agreement

An SLA is a formal commitment regarding:

* Availability
* Correctness
* Delivery Time

of a service.

---

## Example

```plaintext
Shipment Dashboard
Must Be Ready By
8:00 AM Daily
```

This is an SLA.

---

## Important Realization

A pipeline can finish successfully and still fail the SLA.

Example:

```plaintext
Dashboard Ready
9:00 AM

SLA
8:00 AM
```

Result:

```plaintext
Business Failure
```

even though the pipeline technically worked.

---

# Example Shipment Platform SLAs

```plaintext
Source Systems Ready
5:30 AM
```

↓

```plaintext
Bronze Ready
6:00 AM
```

↓

```plaintext
Silver Ready
6:30 AM
```

↓

```plaintext
Gold Ready
7:00 AM
```

↓

```plaintext
Dashboard Ready
8:00 AM
```

---

## Why Dashboard SLA = 8:00 AM?

Business users start consuming reports around:

```plaintext
10:00 AM
```

Setting SLA at:

```plaintext
8:00 AM
```

provides:

* Investigation Time
* Recovery Buffer
* Backfill Opportunity

before business impact occurs.

---

# Monitoring

## Definition

Monitoring is the continuous tracking of system and data health metrics to detect abnormal conditions.

---

Monitoring answers:

```plaintext
Did something unusual happen?
```

---

## Examples

### Pipeline Failure

```plaintext
Silver Job Failed
```

---

### Runtime Monitoring

```plaintext
Normally
20 Minutes

Today
3 Hours
```

---

### Row Count Monitoring

```plaintext
Yesterday
10M Rows

Today
5 Rows
```

Suspicious.

---

### Freshness Monitoring

```plaintext
Today's Data Arrived?
```

---

### Error Rate Monitoring

```plaintext
Rejected Records

Failed Tasks
```

---

# Important Realization

Monitoring can detect:

```plaintext
Pipeline Succeeded
```

while also detecting:

```plaintext
Data Looks Wrong
```

---

# Data Quality

## Definition

Data Quality ensures that data remains correct, complete, valid, and trustworthy.

---

## Important Realization

Many production incidents are:

```plaintext
Data Quality Problems
```

not:

```plaintext
Infrastructure Problems
```

---

Example:

```plaintext
shipment_cost
=
-500
```

Pipeline succeeded.

Data is still wrong.

---

# Data Quality Rules For Shipment Platform

### 1

```plaintext
shipment_id
cannot be null
```

---

### 2

```plaintext
shipment_id
must be unique
```

---

### 3

```plaintext
shipment_cost >= 0
```

---

### 4

```plaintext
delivery_days >= 0
```

---

### 5

```plaintext
shipment_status
must belong to valid values
```

Examples:

```plaintext
Delivered
In Transit
Delayed
Cancelled
```

---

### 6

```plaintext
customer_id
cannot be null
```

---

### 7

```plaintext
origin_location
cannot be null
```

---

### 8

```plaintext
destination_location
cannot be null
```

---

### 9

```plaintext
Today's Data Must Arrive
```

Freshness check.

---

### 10

```plaintext
Row Count
must not deviate significantly
from historical average
```

Example:

```plaintext
10M
↓
5
```

should trigger an alert.

---

# Alerting

## Definition

Alerting is the mechanism that notifies the responsible team when monitoring detects an issue.

---

Alerting answers:

```plaintext
Who needs to know?
```

---

## Examples

```plaintext
Slack

Email

PagerDuty

Microsoft Teams
```

---

# When Should Alerts Fire?

### Pipeline Failure

```plaintext
Task Failed
```

---

### SLA Breach

```plaintext
Dashboard Missed 8 AM SLA
```

---

### Data Quality Failure

```plaintext
Negative Costs

Null Shipment IDs
```

---

### Missing Data

```plaintext
Today's Shipment Data Not Arrived
```

---

# Monitoring vs Alerting

Monitoring:

```plaintext
Detect Problem
```

---

Alerting:

```plaintext
Notify People
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

---

Question:

Should Gold Run?

Answer:

```plaintext
No
```

---

Question:

Should Dashboard Refresh?

Answer:

```plaintext
No
```

---

Reason:

```plaintext
Bad Data Propagates Downstream
```

---

Expected Flow:

```plaintext
Retry
↓
Failure
↓
Alert
↓
Stop Downstream Tasks
```

---

# Observability

## Definition

Observability is the ability to understand why a system behaved the way it did using logs, metrics, lineage, and historical context.

---

Observability answers:

```plaintext
Why did it happen?
```

---

## Examples

### Logs

```plaintext
Exceptions

Warnings

Schema Errors
```

---

### Metrics

```plaintext
Runtime

Row Counts

Failures
```

---

### Historical Runs

```plaintext
What Changed?
```

---

### Data Flow Visibility

```plaintext
Where Did Problem Start?
```

---

# Monitoring vs Observability

Monitoring:

```plaintext
Detect Problem
```

Example:

```plaintext
Revenue = 0
```

---

Observability:

```plaintext
Explain Problem
```

Example:

```plaintext
OMS Delivered Only 5 Rows

Silver Processed 5 Rows

Revenue Became 0
```

---

# Lineage

## Definition

Lineage is the record of how data flows and transforms from source systems through downstream datasets, reports, and dashboards.

---

Lineage answers:

```plaintext
Where did this data come from?

What downstream assets are impacted?
```

---

# Shipment Platform Lineage

```plaintext
OMS
Inventory
Payments
CSV Uploads
        ↓

Bronze
        ↓

Silver
        ↓

Warehouse

FactShipment
DimCustomer
DimLocation
        ↓

Gold KPIs

Revenue By State
Delayed Shipment %
Top Distributors
        ↓

Dashboard
```

---

# Why Lineage Matters

Suppose:

```plaintext
Revenue Dashboard
=
Wrong
```

Lineage helps identify:

```plaintext
Dashboard
↓
Gold
↓
FactShipment
↓
Silver
↓
Bronze
↓
OMS
```

instead of randomly searching the platform.

---

# Logs vs Lineage

Logs:

```plaintext
What Happened During Execution?
```

---

Lineage:

```plaintext
Where Did Data Come From?
```

---

Together they help identify:

```plaintext
Root Cause
```

---

# Production Incident Example

Scenario:

```plaintext
Revenue Yesterday
=
₹5.2M

Revenue Today
=
₹0
```

---

Airflow:

```plaintext
DAG Success
```

---

Monitoring:

```plaintext
Revenue Drop Alert
```

---

Investigation:

```plaintext
Logs
↓
Lineage
↓
Observability
↓
Data Quality Results
```

---

Finding:

```plaintext
OMS Export Incomplete

Only 5 Rows Delivered
```

---

Fix:

```plaintext
Source Issue Fixed
```

---

Recovery:

```plaintext
Airflow Backfill
```

---

Pipeline:

```plaintext
Silver
↓
Gold
↓
Dashboard
```

reruns successfully.

---

SLA still met.

Business unaffected.

---

# Production Readiness Checklist

Before deployment:

### SLA Defined?

---

### Retry Strategy Defined?

---

### Backfill Strategy Defined?

---

### Monitoring Configured?

---

### Alerting Configured?

---

### Data Quality Checks Added?

---

### Ownership Defined?

---

### Lineage Available?

---

### Logs Available?

---

### Recovery Process Documented?

---

# Interview Question

How would you ensure reliability of a shipment analytics platform?

Strong Answer:

```plaintext
Monitoring

Alerting

Retries

Backfills

Data Quality Checks

Observability

Lineage

SLAs
```

---

Weak Answer:

```plaintext
Use Spark
```

---

# Definitions Summary

## Monitoring

Detect that something happened.

---

## Alerting

Notify someone that it happened.

---

## Observability

Understand why it happened.

---

## Lineage

Trace where the data came from and where it went.

---

# Biggest Takeaway

A pipeline can be:

```plaintext
Technically Successful
```

and still be:

```plaintext
Business Failure
```

because of:

```plaintext
Wrong Data

Missing Data

Stale Data

Missed SLA
```

Strong Data Engineers think beyond code and focus on operating reliable, observable, and trustworthy data platforms.

---
