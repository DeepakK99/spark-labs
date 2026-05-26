# Week 3 — Day 3
# Schema Enforcement + Schema Evolution + Data Contracts

---

# Main Learning Goal

Schema is not:

```plaintext
Column definitions
```

Schema is:

```plaintext
Contract between systems
```

---

# Schema Drift

Definition:

Unexpected changes in incoming data structure.

Examples:

```plaintext
cost
↓
shipment_cost
```

```plaintext
double
↓
string
```

```plaintext
customer_name removed
```

Problems:

- broken pipelines
- incorrect analytics
- dashboard failures
- bad ML predictions

---

# Schema Enforcement

Delta validates:

```plaintext
Incoming schema
vs
Table schema
```

If mismatch:

```plaintext
Stop write
```

Observed:

```plaintext
DELTA_METADATA_MISMATCH
```

Purpose:

```plaintext
Prevent silent corruption
```

---

# Schema Evolution

Used:

```python
.option(
    "mergeSchema",
    "true"
)
```

Behavior:

```plaintext
Existing schema
+
New columns
↓
Merged schema
```

Example:

```plaintext
Before:

ShipmentID
Status

After:

ShipmentID
Status
Priority
```

Older rows:

```plaintext
Priority=NULL
```

New rows:

```plaintext
Priority=HIGH
```

---

# Important Lesson

Schema evolution:

```plaintext
Adds structure
```

Schema evolution does NOT:

```plaintext
Understand business meaning
```

Example:

```plaintext
ShipmentID
≠
shipment_id
```

Delta creates:

```plaintext
ShipmentID
shipment_id
```

unless standardized manually.

---

# Dangerous Type Changes

Observed:

```plaintext
ShippingCostUSD

double
↓
string
```

Example:

```plaintext
"five hundred"
```

Result:

```plaintext
DELTA_FAILED_TO_MERGE_FIELDS
```

Purpose:

```plaintext
Fail early
instead of
corrupt data
```

---

# Production Pattern

Raw source
↓
Standardize names
↓
Validate types
↓
Schema evolution if approved
↓
Write to Delta

---

# Key Takeaways

- Schema drift is common
- Schema enforcement prevents silent failures
- Schema evolution should be intentional
- mergeSchema is powerful but dangerous if misused
- Data contracts improve reliability
- Delta behaves like a controlled system, not a file folder

---