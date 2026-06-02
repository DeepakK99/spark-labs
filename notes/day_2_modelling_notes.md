# Week 4 Day 2

# Fact Tables, Dimension Tables, and Grain

---

# Main Learning Goal

Today I learned how analytical data is modeled inside a data warehouse.

The most important realization:

```plaintext
Warehouse modeling starts with the business,
not with tables.
```

Before designing tables, identify:

1. Business process
2. Business event
3. Grain
4. Facts
5. Dimensions

---

# Business Event

A fact table represents a business event.

For the shipment platform:

Business process:

```plaintext
Shipment Delivery
```

Business event:

```plaintext
A shipment occurs
```

Possible events:

* Shipment Created
* Shipment Picked Up
* Shipment Delivered
* Shipment Returned

These events generate measurable business information.

---

# Fact Tables

Definition:

A fact table stores measurable business events.

Contains:

* Measures
* Foreign Keys to dimensions

Examples of measures:

```plaintext
shipment_cost
delivery_days
weight_kg
shipment_count
```

Measures are values that can be:

```plaintext
SUM
AVG
COUNT
MIN
MAX
```

Examples:

```plaintext
ShippingCostUSD
delivery_days
WeightKg
```

---

# Dimension Tables

Definition:

Dimension tables provide descriptive context for facts.

Dimensions answer:

```plaintext
Who?
What?
Where?
When?
```

Examples:

```plaintext
Customer
Location
Date
Shipment Status
```

Dimension values describe facts.

Examples:

```plaintext
CustomerName
City
Country
Status
Month
Quarter
```

---

# Fact vs Dimension Rule

Simple rule:

```plaintext
Measurable
=
Fact
```

```plaintext
Descriptive
=
Dimension
```

Examples:

| Column          | Type      |
| --------------- | --------- |
| ShippingCostUSD | Fact      |
| delivery_days   | Fact      |
| WeightKg        | Fact      |
| CustomerName    | Dimension |
| DestinationCity | Dimension |
| Status          | Dimension |
| OrderDate       | Dimension |

---

# Important Realization

Fact does NOT mean numeric.

Dimension does NOT mean string.

The correct question is:

```plaintext
Is this a measurement
or a description?
```

---

# Grain (Most Important Concept)

Definition:

```plaintext
What does one row represent?
```

Before creating a fact table:

Always define grain.

---

# Shipment Warehouse Grain

FactShipment

Grain:

```plaintext
One row = One Shipment
```

Example:

```plaintext
SHP1001
```

represents exactly one shipment.

---

# Why Grain Matters

A wrong grain causes:

* Incorrect metrics
* Confusing queries
* Duplicate counting
* Broken analytics

Grain must be defined before table design.

---

# FactShipment Design

Grain:

```plaintext
One row per shipment
```

Possible columns:

```plaintext
shipment_id

customer_id

origin_location_id

destination_location_id

shipment_date_id

status_id

shipment_cost

delivery_days

weight_kg

shipment_count
```

Contains:

* Foreign Keys
* Measures

---

# DimCustomer

Purpose:

Store customer descriptions.

Columns:

```plaintext
customer_id

customer_name

customer_type

email

phone

address

city

state

country
```

Contains descriptive customer information.

---

# DimLocation

Purpose:

Store location descriptions.

Columns:

```plaintext
location_id

city

state

country

region
```

Examples:

```plaintext
Mumbai
Maharashtra
India
West
```

---

# Why DimLocation Exists

Without dimension:

```plaintext
Mumbai
Maharashtra
India
West
```

repeated millions of times.

With dimension:

Fact table stores:

```plaintext
location_id
```

Only.

Reduces duplication.

---

# DimDate

One of the most important dimensions.

Possible columns:

```plaintext
date_id

date

day

month

month_name

quarter

year

week_of_year

is_weekend
```

Advanced examples:

```plaintext
fiscal_month

fiscal_quarter

fiscal_year

holiday_flag
```

---

# Why DimDate Exists

Benefits:

## Performance

Avoid repeatedly calculating:

```sql
YEAR(date)
MONTH(date)
QUARTER(date)
```

over millions of rows.

---

## Consistency

Business definitions are centralized.

Everyone uses the same:

* Quarter
* Fiscal Year
* Month

No conflicting report logic.

---

# DimShipmentStatus

Purpose:

Store shipment status information.

Columns:

```plaintext
status_id

status_name
```

Examples:

```plaintext
Delivered

Pending

Cancelled

In Transit
```

---

# Why Not One Giant Table?

Example:

```plaintext
ShipmentID

CustomerName

CustomerAddress

OriginCity

OriginState

DestinationCity

Status

Cost

Weight
...
```

all together.

Problems:

---

## Repetition

Values repeated millions of times.

Example:

```plaintext
Mumbai
Mumbai
Mumbai
Mumbai
...
```

---

## Storage Waste

Large amount of duplicated data.

---

## Update Problems

Example:

```plaintext
Bangalore
```

renamed to:

```plaintext
Bengaluru
```

Without dimensions:

Potentially millions of updates.

With dimensions:

Update one row in DimLocation.

---

## Poor Modeling

The table has no clear purpose.

Fact tables should contain:

```plaintext
Measurements
```

Dimensions should contain:

```plaintext
Descriptions
```

Mixing everything reduces clarity.

---

# Typical Warehouse Queries

Revenue by destination:

```plaintext
FactShipment
    ↓
DimLocation
```

---

Average delivery days by customer type:

```plaintext
FactShipment
    ↓
DimCustomer
```

---

Revenue by quarter:

```plaintext
FactShipment
    ↓
DimDate
```

---

# Warehouse Design Process

Good warehouse design:

1. Define business process
2. Define grain
3. Identify facts
4. Identify dimensions
5. Design query patterns

Not:

```plaintext
Let's create tables first
```

---

# Interview Thinking

If asked:

"Design a shipment analytics warehouse"

A strong answer is:

```plaintext
Step 1:
Define grain

One row = One Shipment

Step 2:
Identify measures

shipment_cost
delivery_days
weight

Step 3:
Identify dimensions

Customer
Location
Date
Status

Step 4:
Design fact table and dimensions
```

---

# Biggest Takeaways

Fact Table:

```plaintext
Stores measurements.
```

Dimension Table:

```plaintext
Stores descriptive context.
```

Grain:

```plaintext
Defines what one row represents.
```

The most important question in warehouse modeling is:

```plaintext
What does one row represent?
```

Everything else follows from that decision.

---
