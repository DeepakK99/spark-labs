# Week 5 Day 2

# IAM For Data Engineers

---

# Main Learning Goal

Today I learned how AWS controls access to resources and how permissions are designed for production data platforms.

The biggest realization:

```plaintext
IAM is not a login system.

IAM is an authorization system.
```

Its purpose is to answer:

```plaintext
Who can do what
on which resource?
```

---

# Why IAM Matters

A data platform is not only about:

```plaintext
How data flows
```

It is also about:

```plaintext
Who is allowed to move it
```

Many production issues are caused by:

```plaintext
Missing Permissions

Wrong Permissions

Overly Broad Permissions
```

rather than Spark code itself.

---

# Core IAM Concepts

Everything is built on three concepts:

```plaintext
User

Role

Policy
```

---

# IAM User

Represents:

```plaintext
Human Identity
```

Examples:

```plaintext
Rahul

Priya

Amit
```

Example user:

```plaintext
data-engineer-rahul
```

---

Users may have:

```plaintext
Password

Access Keys
```

---

# IAM Role

Represents:

```plaintext
Service Identity
```

Examples:

```plaintext
Databricks Job

Glue Job

Lambda

EMR Cluster

Airflow
```

---

Important rule:

```plaintext
Humans → Users

Services → Roles
```

---

# Why Pipelines Use Roles

Bad:

```plaintext
Silver Pipeline
↓
Uses Rahul's Credentials
```

Problems:

```plaintext
Rahul leaves company

Password changes

Credentials rotate

Pipeline breaks
```

---

Good:

```plaintext
Silver Pipeline
↓
Uses SilverPipelineRole
```

Benefits:

```plaintext
Independent Of Humans

More Secure

Easier Auditing

No Hardcoded Credentials
```

---

# IAM Policy

Definition:

```plaintext
Permission Document
```

Policy defines:

```plaintext
What actions
can be performed
on what resources
```

---

Example:

```json
{
  "Effect": "Allow",
  "Action": "s3:GetObject",
  "Resource": "bronze/*"
}
```

Translation:

```plaintext
Can read Bronze data
```

---

# Relationship

```plaintext
User
    ↓
Attached Policies

Role
    ↓
Attached Policies
```

Policies define permissions.

Users and Roles receive permissions through policies.

---

# Service-to-Service Access

Major realization:

Services do not use usernames and passwords.

They use:

```plaintext
IAM Roles
```

---

Example:

```plaintext
Databricks Job
↓
Assume SilverPipelineRole
↓
Read Bronze
Write Silver
```

---

AWS automatically provides temporary credentials.

No hardcoded secrets required.

---

# Principle Of Least Privilege

Most important concept of the day.

Rule:

```plaintext
Grant only the permissions required.
```

---

Bad:

```plaintext
AdministratorAccess
```

for everything.

---

Good:

```plaintext
Read Bronze

Write Silver
```

only.

---

# Why Least Privilege Matters

Benefits:

```plaintext
Limits Mistakes

Limits Security Incidents

Reduces Blast Radius

Protects Production Data
```

---

Example

Suppose a buggy pipeline executes:

```python
delete("gold/")
```

---

If role has:

```plaintext
AdministratorAccess
```

Gold may be deleted.

---

If role has:

```plaintext
Read Bronze

Write Silver
```

only:

```plaintext
Access Denied
```

and production remains safe.

---

# Brewery Data Lake Example

Architecture:

```plaintext
Bronze
↓
Silver
↓
Gold
```

Each layer gets its own role.

---

# BronzePipelineRole

Purpose:

```plaintext
Ingest Raw Data
```

Permissions:

```plaintext
Write Bronze
```

Only.

---

Why?

Pipeline's responsibility ends after data lands in Bronze.

No need to access Silver or Gold.

---

# SilverPipelineRole

Purpose:

```plaintext
Read Raw Data

Clean Data

Write Trusted Data
```

Permissions:

```plaintext
Read Bronze

Write Silver
```

Only.

---

Why?

Silver consumes Bronze and produces Silver.

No need for Gold access.

---

# GoldPipelineRole

Purpose:

```plaintext
Generate Business Metrics
```

Permissions:

```plaintext
Read Silver

Write Gold
```

Only.

---

Examples:

```plaintext
Revenue By State

Delayed Shipment %

Top Distributors
```

---

# AnalyticsRole

Purpose:

```plaintext
Business Reporting
```

Permissions:

```plaintext
Read Gold
```

Only.

---

Why?

Analysts consume metrics.

They do not modify data.

---

# DataScienceRole

Purpose:

```plaintext
Model Training

Feature Engineering

Exploration
```

Permissions:

```plaintext
Read Silver

Read Gold (if required)
```

---

Why Not Gold Only?

Gold contains:

```plaintext
Aggregated KPIs
```

Examples:

```plaintext
Revenue By State

Delayed Shipment %
```

---

Data Scientists often need:

```plaintext
Row-Level Data

Customer Features

Shipment Features

Historical Records
```

which usually live in Silver.

---

# Access Model Summary

```plaintext
BronzePipelineRole
    Write Bronze

SilverPipelineRole
    Read Bronze
    Write Silver

GoldPipelineRole
    Read Silver
    Write Gold

AnalyticsRole
    Read Gold

DataScienceRole
    Read Silver
    Read Gold
```

---

# Administrator Access

Question:

Should every pipeline receive:

```plaintext
AdministratorAccess
```

Answer:

```plaintext
No
```

---

Reason:

Violates:

```plaintext
Least Privilege
```

and creates unnecessary risk.

---

Strong Interview Answer:

```plaintext
Each pipeline should receive only the permissions required to perform its task. Granting AdministratorAccess increases security risk and the impact of accidental or malicious actions.
```

---

# Auditing Benefits

Roles improve traceability.

Example:

Logs show:

```plaintext
SilverPipelineRole
```

instead of:

```plaintext
RahulUser
```

---

Now we know:

```plaintext
Pipeline Action
```

rather than:

```plaintext
Human Action
```

---

# Connection To Week 4

Week 4:

```plaintext
How Data Is Modeled
```

---

Week 5 Day 1:

```plaintext
Where Data Lives
```

Answer:

```plaintext
S3
```

---

Week 5 Day 2:

```plaintext
Who Can Access Data
```

Answer:

```plaintext
IAM
```

---

# Real Data Platform View

A production platform requires:

```plaintext
Storage
+
Compute
+
Permissions
```

Working together.

---

Example:

```plaintext
S3
    ↓

IAM Roles
    ↓

Spark Jobs
    ↓

Bronze
Silver
Gold
```

---

# Interview Question

Question:

```plaintext
How would you design access control for a Bronze/Silver/Gold architecture?
```

Strong answer:

```plaintext
Separate IAM roles for each pipeline.

Bronze ingestion writes only Bronze.

Silver pipeline reads Bronze and writes Silver.

Gold pipeline reads Silver and writes Gold.

Analysts receive read-only Gold access.

Data Scientists receive access only to curated datasets required for their work.

Follow least privilege throughout the platform.
```

---

# Biggest Takeaways

Users represent humans.

Roles represent services.

Policies define permissions.

---

Pipelines should use roles, not user credentials.

---

Least privilege is one of the most important AWS principles.

---

Each layer of the data platform should have its own permissions boundary.

---

IAM is fundamentally about:

```plaintext
Who can do what
on which resource.
```

---

# Most Important Realization

```plaintext
Data Engineering is not only about moving data.

It is also about controlling access to data safely.
```

A production platform needs both.

---
