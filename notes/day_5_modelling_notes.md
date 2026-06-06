# Week 4 Day 5

# End-to-End Warehouse Design

---

# Main Learning Goal

Today I combined everything learned during Week 4 into a complete warehouse architecture.

The goal was to answer:

```plaintext
How do I design a warehouse from scratch?
```

using:

* Business Process
* Grain
* Facts
* Dimensions
* SCD
* Gold KPIs

---

# The Warehouse Design Process

A warehouse should not start with:

```plaintext
Tables
```

It should start with:

```plaintext
Business Process
```

The correct order is:

```plaintext
Business Process
↓
Grain
↓
Facts
↓
Dimensions
↓
SCD Strategy
↓
Gold KPIs
```

---

# Business Process

Shipment company scenario:

```plaintext
Deliver beverages from breweries
to warehouses, distributors,
retail stores and customers.
```

More formal definition:

```plaintext
Product Distribution
and Shipment Fulfillment
```

---

# Grain

Definition:

```plaintext
What does one row represent?
```

Most important warehouse modeling question.

---

# Grain Options Considered

## One Row Per Shipment

```plaintext
Shipment 1001
```

---

## One Row Per Status Change

```plaintext
Shipment 1001 Created

Shipment 1001 Picked Up

Shipment 1001 Delivered
```

---

## Daily Aggregated Summary

```plaintext
Revenue by City by Day
```

---

# Chosen Grain

```plaintext
One Row = One Shipment
```

Reason:

Provides maximum flexibility.

Can answer:

* Revenue by Route
* Revenue by Region
* Revenue by Product
* Revenue by Customer
* Delayed Shipment %
* Average Delivery Days

Lower grain can always be aggregated.

Higher grain cannot be decomposed later.

---

# Fact Table Design

FactShipment

Contains measurable business metrics.

---

# Facts

```plaintext
shipment_cost

delivery_days

weight_kg

shipment_count

delayed_days
```

---

# Why delayed_days?

Alternative:

```plaintext
is_delayed
```

only stores:

```plaintext
0 or 1
```

---

Using:

```plaintext
delayed_days
```

allows:

```plaintext
is_delayed = delayed_days > 0
```

and also enables:

```plaintext
Average Delay

Maximum Delay

Delay Distribution
```

More information with one metric.

---

# FactShipment

Possible structure:

```plaintext
shipment_sk

shipment_id

customer_sk

origin_location_sk

destination_location_sk

shipment_date_sk

delivery_date_sk

status_sk

shipment_cost

delivery_days

delayed_days

weight_kg

shipment_count
```

---

# Dimensions

Dimensions provide descriptive context.

Dimensions answer:

```plaintext
Who?

What?

Where?

When?
```

---

# DimCustomer

```plaintext
customer_sk

customer_id

customer_name

customer_type

city

state

country
```

---

# DimLocation

```plaintext
location_sk

city

state

country

region
```

---

# DimDate

```plaintext
date_sk

date

month

quarter

year

week_of_year

is_weekend
```

---

# DimStatus

```plaintext
status_sk

status_name
```

Examples:

```plaintext
Created

Picked Up

In Transit

Delivered
```

---

# Why Not Store Everything In FactShipment?

Reasons:

---

## Separation Of Responsibilities

Fact Table:

```plaintext
Measurements
```

Dimension Table:

```plaintext
Descriptions
```

---

## Reduced Repetition

Without dimensions:

```plaintext
Acme Retail
Acme Retail
Acme Retail
```

repeated thousands of times.

With dimensions:

Store customer once.

Reference via surrogate key.

---

## Easier SCD Management

Customer changes:

```plaintext
Tier

Region

City
```

can be tracked in dimensions.

---

## Flexible Analytics

Join only required dimensions.

Example:

Revenue by Region:

```plaintext
FactShipment
+
DimLocation
```

No need to involve other dimensions.

---

# SCD Strategy

---

# DimCustomer

Type:

```plaintext
SCD Type 2
```

Reason:

Historical changes matter.

Examples:

```plaintext
Customer Tier

Customer Region

Customer City
```

Business may ask:

```plaintext
Revenue while customer was Gold.
```

---

# DimLocation

Usually:

```plaintext
SCD Type 1
```

Reason:

Changes are often:

```plaintext
Renames

Corrections

Standardization
```

Example:

```plaintext
Bombay
↓
Mumbai
```

Business usually does not care about old name history.

---

# DimProduct

Usually:

```plaintext
SCD Type 2
```

Reason:

Historical product categorization may matter.

Examples:

```plaintext
Category changes

Rebranding

Product hierarchy changes
```

---

# DimStatus

Usually:

```plaintext
SCD Type 1
```

Reason:

Typically contains static definitions.

Examples:

```plaintext
Created

Picked Up

Delivered
```

---

# Event Tables vs SCD

Shipment status changes:

```plaintext
Created
↓
Picked Up
↓
In Transit
↓
Delivered
```

should be modeled as:

```plaintext
Shipment Events
```

not SCD Type 2.

Reason:

The change itself is a business event.

---

# Gold Layer

Purpose:

```plaintext
Business Answers
```

Not raw data.

Not cleaned data.

Precomputed analytics.

---

# Gold KPIs Designed

---

## Total Revenue

```plaintext
gold_total_revenue
```

Metrics:

```plaintext
total_revenue

daily_revenue

monthly_revenue
```

---

## Delayed Shipment %

```plaintext
gold_shipment_performance
```

Metrics:

```plaintext
delayed_percentage

average_delay_days
```

---

## Top Beverage Types

```plaintext
gold_product_performance
```

Metrics:

```plaintext
shipment_count

revenue
```

---

## Revenue By Destination

```plaintext
gold_revenue_by_destination
```

Metrics:

```plaintext
destination

revenue

shipment_count
```

---

## Revenue By Shipment Type

```plaintext
gold_revenue_by_customer_type
```

Metrics:

```plaintext
revenue

shipment_count

average_delivery_days
```

---

# Why Gold Exists

Without Gold:

Every dashboard refresh performs:

```sql
GROUP BY
SUM
AVG
COUNT
```

on large fact tables.

---

With Gold:

Compute once.

Read many times.

Benefits:

```plaintext
Fast

Cheap

Predictable
```

---

# Important Realization

Gold answers:

```plaintext
Known Questions
```

Examples:

```plaintext
Revenue By Region

Top Products

Delayed %
```

---

# Warehouse Answers

```plaintext
Unknown Future Questions
```

Examples:

```plaintext
Revenue by Customer Tier

Revenue by Region

for shipments > 50kg

during Q2

with delay > 3 days
```

No Gold table exists.

Warehouse can answer it.

---

# Warehouse Layer Between Silver And Gold

Important realization:

Real systems often look like:

```plaintext
Bronze
↓
Silver
↓
Warehouse Model
(Facts + Dimensions)
↓
Gold
```

---

# Silver

Represents:

```plaintext
Engineering Truth
```

Contains:

```plaintext
Cleaned

Validated

Deduplicated

Current state
```

---

# Warehouse Model

Represents:

```plaintext
Business Model
```

Contains:

```plaintext
FactShipment

DimCustomer

DimLocation

DimDate

DimProduct

DimStatus
```

Purpose:

Support flexible analytics.

---

# Gold

Represents:

```plaintext
Business Answers
```

Contains:

```plaintext
Precomputed KPIs
```

for dashboards and executives.

---

# End-To-End Architecture

```plaintext
Customer places order
        ↓

Backend APIs
        ↓

PostgreSQL
(Operational System)
        ↓

Ingestion / CDC
        ↓

Bronze
(Raw Data)
        ↓

Silver
(Cleaned Data)

- Deduplication
- Validation
- Delivery Days
- Delayed Days
- Business Flags

        ↓

Warehouse Model

FactShipment

DimCustomer

DimLocation

DimDate

DimStatus

DimProduct

        ↓

Gold KPIs

Revenue By Destination

Top Products

Delayed %

Revenue By Customer Type

Route Performance

        ↓

Dashboard

Power BI

Tableau

CEO Portal

Operations Portal
```

---

# Interview Framework

If asked:

```plaintext
Design a shipment warehouse.
```

Answer:

### Step 1

Define business process.

---

### Step 2

Define grain.

```plaintext
One row = One shipment
```

---

### Step 3

Identify facts.

```plaintext
Cost

Weight

Delivery Days

Delayed Days
```

---

### Step 4

Identify dimensions.

```plaintext
Customer

Location

Date

Product

Status
```

---

### Step 5

Define SCD strategy.

---

### Step 6

Design Gold KPIs.

---

### Step 7

Expose through dashboards.

---

# Biggest Takeaways

Warehouse modeling starts with:

```plaintext
Business Process
```

not tables.

---

Grain is the most important modeling decision.

---

Fact tables store:

```plaintext
Measurements
```

Dimensions store:

```plaintext
Descriptions
```

---

Gold stores:

```plaintext
Known Business Questions
```

Warehouse stores:

```plaintext
Future Business Possibilities
```

---

The complete analytical architecture is:

```plaintext
Bronze
↓
Silver
↓
Warehouse Model
↓
Gold
↓
Dashboards
```

and each layer exists for a different purpose.

---
