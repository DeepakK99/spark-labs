# Week 4 Day 3

# Star Schema vs Snowflake Schema

---

# Main Learning Goal

Today I learned how warehouse dimensions can be organized.

The key question is not:

```plaintext
Which schema is correct?
```

The real question is:

```plaintext
What tradeoff am I making?
```

Data modeling is largely about tradeoffs.

---

# Quick Recap

From Day 2:

I designed:

```plaintext
FactShipment
```

with dimensions:

```plaintext
DimCustomer
DimLocation
DimDate
DimStatus
```

This naturally forms a Star Schema.

---

# What Is A Star Schema?

Structure:

```plaintext
                 DimCustomer
                      |
                      |
DimDate --- FactShipment --- DimLocation
                      |
                      |
                 DimStatus
```

Looks like a star.

Hence:

```plaintext
Star Schema
```

---

# Characteristics

Fact table sits in the center.

Dimensions surround it.

---

## FactShipment

Contains:

```plaintext
shipment_cost
delivery_days
weight_kg
shipment_count
```

and foreign keys:

```plaintext
customer_id
date_id
location_id
status_id
```

---

## Dimensions

Contain descriptive information.

Examples:

```plaintext
customer_name
customer_type

city
state
country

month
quarter
year
```

---

# Why Analysts Love Star Schema

Simple queries.

Example:

```plaintext
Revenue by Customer Type
```

Requires:

```plaintext
FactShipment
    ↓
DimCustomer
```

Only one join.

Easy to understand.

Easy to maintain.

---

# Example Star Schema

## FactShipment

```plaintext
shipment_id

customer_id

origin_location_id

destination_location_id

date_id

status_id

shipment_cost

delivery_days

weight_kg
```

---

## DimCustomer

```plaintext
customer_id

customer_name

customer_type

city

state

country
```

---

## DimLocation

```plaintext
location_id

city

state

country

region
```

---

## DimDate

```plaintext
date_id

date

month

quarter

year

week_of_year

is_weekend
```

---

## DimStatus

```plaintext
status_id

status_name
```

---

# Important Observation

DimLocation contains repeated values.

Example:

```plaintext
Mumbai
Maharashtra
India
West
```

and

```plaintext
Pune
Maharashtra
India
West
```

Repeated data exists.

This is intentional.

---

# What Is A Snowflake Schema?

Instead of storing everything in one dimension:

```plaintext
DimLocation
```

we normalize the dimension.

Example:

```plaintext
DimCity
    ↓
DimState
    ↓
DimCountry
    ↓
DimRegion
```

This creates a snowflake shape.

Hence:

```plaintext
Snowflake Schema
```

---

# Example Snowflake Design

## FactShipment

```plaintext
shipment_id

customer_id

city_id

date_id

status_id

shipment_cost

delivery_days
```

---

## DimCity

```plaintext
city_id

city_name

state_id
```

---

## DimState

```plaintext
state_id

state_name

country_id
```

---

## DimCountry

```plaintext
country_id

country_name

region_id
```

---

## DimRegion

```plaintext
region_id

region_name
```

---

# Visualization

```plaintext
FactShipment
     ↓
DimCity
     ↓
DimState
     ↓
DimCountry
     ↓
DimRegion
```

---

# Normalization

Goal:

```plaintext
Reduce duplication
```

Example:

Instead of storing:

```plaintext
India
India
India
India
```

many times,

store it once.

Reference it using keys.

---

# Denormalization

Goal:

```plaintext
Reduce joins
```

Store related attributes together.

Accept some duplication.

---

# Star Schema Advantages

## Simpler Queries

Example:

```plaintext
Revenue by Country
```

Requires:

```plaintext
FactShipment
     ↓
DimLocation
```

One join.

---

## Easier For Analysts

Business users can understand it quickly.

---

## Better BI Tool Experience

Works well with:

* Power BI
* Tableau
* Looker

---

## Fewer Joins

Less SQL complexity.

---

# Star Schema Disadvantages

## Data Duplication

Example:

```plaintext
India
India
India
```

appears repeatedly.

---

## Larger Dimensions

More storage required.

---

# Snowflake Schema Advantages

## Reduced Duplication

Reference data stored once.

---

## Better Normalization

Cleaner hierarchy.

Example:

```plaintext
City
↓
State
↓
Country
↓
Region
```

---

## Smaller Dimension Tables

Less repeated data.

---

# Snowflake Schema Disadvantages

## More Joins

Example:

Revenue by Country:

```plaintext
FactShipment
     ↓
DimCity
     ↓
DimState
     ↓
DimCountry
```

Multiple joins.

---

## More Complex Queries

Harder to write.

Harder to maintain.

---

## Harder For Analysts

Business users usually prefer simpler models.

---

# Revenue By Country Example

## Star Schema

```plaintext
FactShipment
     ↓
DimLocation
```

One join.

---

## Snowflake Schema

```plaintext
FactShipment
     ↓
DimCity
     ↓
DimState
     ↓
DimCountry
```

Three joins.

---

# Modern Reality

Modern platforms are very good at joins:

* Snowflake
* Databricks SQL
* BigQuery

The performance gap is smaller than it used to be.

---

# Why Star Schema Still Dominates

The biggest reason today is:

```plaintext
Human productivity
```

not performance.

Storage is cheap.

Analyst time is expensive.

---

# Important Insight

Tradeoff:

## Star Schema

Optimizes for:

```plaintext
Query simplicity
Readability
Ease of use
```

Accepts:

```plaintext
Some duplication
```

---

## Snowflake Schema

Optimizes for:

```plaintext
Storage efficiency
Normalization
Data consistency
```

Accepts:

```plaintext
More joins
More complexity
```

---

# OLTP vs OLAP Connection

## OLTP Systems

Prefer:

```plaintext
Normalization
```

Because they optimize for:

```plaintext
Updates
Consistency
Storage efficiency
```

---

## OLAP Systems

Prefer:

```plaintext
Denormalization
```

Because they optimize for:

```plaintext
Analytics
Read performance
Query simplicity
```

---

# Shipment Analytics Decision

Scenario:

```plaintext
2 billion shipment rows
```

Common queries:

```plaintext
Revenue by Country

Revenue by Region

Revenue by Customer Type

Delayed Shipment %
```

Storage cost is not a concern.

---

Decision:

```plaintext
Star Schema
```

Reason:

Analytics workloads prioritize:

```plaintext
Query simplicity
Analyst productivity
Ease of maintenance
```

More than saving a small amount of dimension storage.

---

# Interview Answer

Question:

Why would you choose Star Schema?

Answer:

Star Schema is generally preferred for analytics because it simplifies query writing, reduces the number of joins, and is easier for analysts and BI tools to use. Although it introduces some duplication in dimensions, modern storage is inexpensive, making the tradeoff worthwhile.

---

# Biggest Takeaways

Star Schema:

```plaintext
Denormalized dimensions
Fewer joins
Simpler analytics
```

---

Snowflake Schema:

```plaintext
Normalized dimensions
More joins
Less duplication
```

---

Important realization:

```plaintext
OLTP prefers normalization.

OLAP often prefers denormalization.
```

---

# What Surprised Me

The most surprising realization was that:

```plaintext
Storage savings
```

is often not the primary concern anymore.

Instead:

```plaintext
Analyst productivity
Query simplicity
Ease of understanding
```

drive many warehouse design decisions.

---

# Week 4 Progress

Day 1:

```plaintext
Why Warehouses Exist
```

---

Day 2:

```plaintext
Fact Tables
Dimensions
Grain
```

---

Day 3:

```plaintext
Star Schema
vs
Snowflake Schema
```

I can now explain:

* Why dimensions exist
* How dimensions are organized
* Why Star Schema is common
* What tradeoffs are involved

and model a warehouse using either approach.

---
