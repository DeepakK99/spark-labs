# Week 4 Day 4

# Slowly Changing Dimensions (SCD)

---

# Main Learning Goal

Today I learned how data warehouses handle changes over time.

Important realization:

```plaintext
Warehouse
=
Current State
+
Historical Truth
```

Operational systems often care about:

```plaintext
What is true now?
```

Warehouses often care about:

```plaintext
What was true when the event happened?
```

This is why SCD exists.

---

# Why SCD Exists

Businesses change.

Examples:

```plaintext
Customer changes city

Customer changes region

Customer changes tier

Customer changes sales representative
```

Question:

Should the warehouse:

```plaintext
Overwrite old value?
```

or

```plaintext
Preserve historical value?
```

The answer depends on business requirements.

---

# Core Business Question

Example:

Customer:

```plaintext
Bengaluru
↓
Mumbai
```

Business asks:

```sql
Revenue by City
for the last 3 years
```

Question:

Should historical revenue remain under Bengaluru?

Answer:

```plaintext
Yes
```

because those shipments happened while the customer lived in Bengaluru.

This is called:

```plaintext
Historical Truth
```

---

# SCD Type 1

Definition:

```plaintext
Overwrite old value.
```

History is lost.

---

Example

Before:

```plaintext
customer_id = 100

city = Bengaluru
```

After:

```plaintext
customer_id = 100

city = Mumbai
```

Result:

```plaintext
Bengaluru disappears forever.
```

---

# Type 1 Characteristics

Benefits:

```plaintext
Simple
Small storage
Easy updates
```

Drawbacks:

```plaintext
No historical tracking
```

---

# When To Use Type 1

Good for:

```plaintext
Data corrections
Typos
Invalid values
Bad data fixes
```

Examples:

```plaintext
acme@gmil.com
↓
acme@gmail.com
```

Old value was never correct.

No history needed.

---

# SCD Type 2

Definition:

```plaintext
Preserve history.
```

Instead of updating:

```plaintext
Expire old row
Insert new row
```

---

# Example

Customer moves:

```plaintext
Bengaluru
↓
Mumbai
```

Before:

| customer_sk | customer_id | city      | current_flag |
| ----------- | ----------- | --------- | ------------ |
| 1           | 100         | Bengaluru | Y            |

---

After:

| customer_sk | customer_id | city      | current_flag | end_date   |
| ----------- | ----------- | --------- | ------------ | ---------- |
| 1           | 100         | Bengaluru | N            | 2026-01-01 |

New row:

| customer_sk | customer_id | city   | current_flag | start_date |
| ----------- | ----------- | ------ | ------------ | ---------- |
| 2           | 100         | Mumbai | Y            | 2026-01-01 |

---

# Important Realization

Customer remains:

```plaintext
customer_id = 100
```

because it is still the same business customer.

However:

```plaintext
customer_sk
```

changes.

Each version receives a new warehouse identifier.

---

# Natural Key

Definition:

Business identifier.

Example:

```plaintext
customer_id
```

Properties:

```plaintext
Comes from source system
Meaningful to business
```

---

# Surrogate Key

Definition:

Warehouse-generated identifier.

Example:

```plaintext
customer_sk
```

Properties:

```plaintext
No business meaning

Used to track versions

Supports SCD Type 2
```

---

# Why Surrogate Keys Exist

Without surrogate keys:

```plaintext
customer_id = 100
```

can only represent one version.

With surrogate keys:

```plaintext
customer_sk = 1
customer_id = 100
Bengaluru

customer_sk = 2
customer_id = 100
Mumbai
```

Multiple historical versions can coexist.

---

# Type 1 vs Type 2

## Type 1

Stores:

```plaintext
Current Truth
```

Question answered:

```plaintext
What is true now?
```

---

## Type 2

Stores:

```plaintext
Historical Truth
```

Question answered:

```plaintext
What was true when the event happened?
```

---

# Customer Tier Example

Customer lifecycle:

```plaintext
Silver
↓
Gold
↓
Platinum
```

Business asks:

```sql
Revenue generated while customer was Gold
```

---

Type 1:

```plaintext
Everything becomes Platinum.
```

Historical information lost.

Cannot answer correctly.

---

Type 2:

```plaintext
Silver preserved

Gold preserved

Platinum preserved
```

Question becomes answerable.

---

# Delta Lake Connection

Type 2 is commonly implemented using:

```plaintext
MERGE
```

Pattern:

```plaintext
Expire old row

Insert new row
```

This is common in:

* Databricks
* Snowflake
* Warehouse ETL pipelines

---

# Event Table vs SCD

Important distinction.

---

# Shipment Status Example

```plaintext
Created
↓
Picked Up
↓
In Transit
↓
Delivered
```

Question:

Should we use SCD Type 2?

Answer:

```plaintext
Usually No
```

---

# Why?

Shipment status changes are:

```plaintext
Business Events
```

not attribute corrections.

The change itself is meaningful.

---

# Event Table Design

Example:

| shipment_id | status     | event_time |
| ----------- | ---------- | ---------- |
| 101         | Created    | 2026-01-01 |
| 101         | Picked Up  | 2026-01-02 |
| 101         | In Transit | 2026-01-03 |
| 101         | Delivered  | 2026-01-05 |

This naturally preserves the timeline.

---

# Rule Of Thumb

Use:

```plaintext
SCD Type 2
```

when:

```plaintext
An entity changes.
```

Examples:

```plaintext
Customer city

Customer tier

Customer region

Employee department
```

---

Use:

```plaintext
Event Tables
```

when:

```plaintext
The change itself is the event.
```

Examples:

```plaintext
Shipment status updates

Order lifecycle

Payment events

User logins
```

---

# Interview Answers

## Why does SCD exist?

To manage changes in dimensional data while supporting business reporting requirements.

---

## Difference between Type 1 and Type 2?

Type 1 overwrites old values and loses history.

Type 2 preserves history by creating new records.

---

## Why use surrogate keys?

To allow multiple historical versions of the same business entity to exist in the dimension table.

---

## When would Type 2 be required?

Whenever historical reporting is required.

Examples:

```plaintext
Customer city changes

Customer tier changes

Sales territory changes
```

---

# Business Decision Framework

Ask:

```plaintext
Was the old value actually correct?
```

If:

```plaintext
Yes
```

Use:

```plaintext
Type 2
```

---

If:

```plaintext
No
```

Use:

```plaintext
Type 1
```

---

Examples

Correct historical value:

```plaintext
Bengaluru
↓
Mumbai
```

Type 2

---

Incorrect historical value:

```plaintext
gmil.com
↓
gmail.com
```

Type 1

---

# Biggest Takeaways

SCD Type 1:

```plaintext
Overwrite old value.
No history.
```

---

SCD Type 2:

```plaintext
Preserve historical changes.
Track versions.
Maintain historical truth.
```

---

Event Tables:

```plaintext
Store business events.

The change itself is meaningful.
```

---

Most Important Realization

The warehouse is not always trying to answer:

```plaintext
What is true now?
```

Often it is trying to answer:

```plaintext
What was true when the event occurred?
```

That single idea explains why SCD Type 2 exists.

---
