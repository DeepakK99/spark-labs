from pyspark.sql.functions import (
    col,
    datediff,
    when
)


def transform_shipments(df):

    # Remove null shipment IDs
    df = df.filter(
        col("ShipmentID").isNotNull()
    )

    # Remove duplicate shipment IDs
    df = df.dropDuplicates(
        ["ShipmentID"]
    )

    # Create delivery_days
    df = df.withColumn(
        "delivery_days",
        datediff(
            col("DeliveryDate"),
            col("ShipDate")
        )
    )

    # Create delivery category
    df = df.withColumn(
        "delivery_category",
        when(
            col("delivery_days") <= 2,
            "Fast"
        )
        .when(
            col("delivery_days") <= 5,
            "Normal"
        )
        .otherwise(
            "Delayed"
        )
    )

    # High cost shipment flag
    df = df.withColumn(
        "high_cost_flag",
        when(
            col("ShippingCostUSD") > 1000,
            True
        )
        .otherwise(False)
    )

    return df