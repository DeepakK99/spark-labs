from pyspark.sql.functions import (
    avg,
    count,
    sum,
    desc,
    col
)


def run_analytics(df):

    print("\nAverage delivery days by status")

    df.groupBy(
        "Status"
    ).agg(
        avg("delivery_days")
    ).show()


    print("\nShipment count by route")

    df.groupBy(
        "OriginCity",
        "DestinationCity"
    ).count().show()


    print("\nDelayed shipment percentage")

    delayed = (
        df.filter(
            col("delivery_category")
            == "Delayed"
        ).count()
    )

    total = df.count()

    print(
        round(
            (delayed/total)*100,
            2
        ),
        "%"
    )


    print("\nRevenue by destination")

    df.groupBy(
        "DestinationCity"
    ).agg(
        sum("ShippingCostUSD")
    ).show()


    print("\nTop customers")

    df.groupBy(
        "CustomerName"
    ).agg(
        sum("ShippingCostUSD")
        .alias("total_spent")
    ).orderBy(
        desc("total_spent")
    ).show()