from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip
from pyspark.sql.functions import current_timestamp, input_file_name

builder = (
    SparkSession.builder.appName("MedallionLab")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config(
        "spark.sql.catalog.spark_catalog",
        "org.apache.spark.sql.delta.catalog.DeltaCatalog",
    )
)

spark = configure_spark_with_delta_pip(builder).getOrCreate()

# exercise 1
# df = spark.read.csv(
#     "../data/raw/shipments.csv",
#     header=True,
#     inferSchema=True
# )


# bronze_df = (
#     df
#     .withColumn(
#         "ingestion_timestamp",
#         current_timestamp()
#     )
#     .withColumn(
#         "source_file",
#         input_file_name()
#     )
# )

# bronze_df.show(5)

# bronze_df.write \
#     .format("delta") \
#     .mode("overwrite") \
#     .save(
#         "../data/bronze/shipments"
#     )

# exercise 2
# from pyspark.sql.functions import (
#     initcap,
#     datediff,
#     when,
#     col
# )

# bronze_df = spark.read \
#     .format("delta") \
#     .load(
#         "../data/bronze/shipments"
#     )

# silver_df = (
#     bronze_df
#     .dropDuplicates(
#         ["ShipmentID"]
#     )
#     .withColumn(
#         "Status",
#         initcap(
#             col("Status")
#         )
#     )
#     .filter(
#         col("ShipmentID").isNotNull()
#     )
#     .filter(
#         col("ShippingCostUSD") >= 0
#     )
#     .withColumn(
#         "delivery_days",
#         datediff(
#             col("DeliveryDate"),
#             col("ShipDate")
#         )
#     )
#     .withColumn(
#         "high_cost_flag",
#         when(
#             col("ShippingCostUSD") > 1000,
#             True
#         ).otherwise(
#             False
#         )
#     )
# )

# silver_df.show(5)

# silver_df.write \
#     .format("delta") \
#     .mode("overwrite") \
#     .save(
#         "../data/silver/shipments"
#     )

# exercise 2.5
from delta.tables import DeltaTable

silver_table = DeltaTable.forPath(
    spark,
    "data/silver/shipments"
)
updates_data = [
    (
        "SHP1002",
        "Delivered",
        "2026-05-31"
    ),
    (
        "SHP1003",
        "Delivered",
        "2026-05-31"
    ),
    (
        "SHP2001",
        "Pending",
        None
    )
]
from pyspark.sql.types import *

updates_schema = StructType([
    StructField("ShipmentID", StringType()),
    StructField("Status", StringType()),
    StructField("DeliveryDate", StringType())
])
updates_df = spark.createDataFrame(
    updates_data,
    updates_schema
)
(
    silver_table.alias("target")
    .merge(
        updates_df.alias("source"),
        "target.ShipmentID = source.ShipmentID"
    )
    .whenMatchedUpdate(
        set={
            "Status": "source.Status",
            "DeliveryDate": "to_date(source.DeliveryDate)"
        }
    )
    .whenNotMatchedInsert(
        values={
            "ShipmentID": "source.ShipmentID",
            "Status": "source.Status",
            "DeliveryDate": "to_date(source.DeliveryDate)"
        }
    )
    .execute()
)

# exercise 3
# gold - each df should be a table
from pyspark.sql.functions import avg, sum, count, desc, col

silver_df = spark.read.format("delta").load("../data/silver/shipments")

from pyspark.sql.functions import sum

revenue_by_destination = silver_df.groupBy("DestinationCity").agg(
    sum("ShippingCostUSD").alias("total_revenue")
)

revenue_by_destination.show()

avg_delivery_days = silver_df.filter(col("Status") == "Delivered").agg(
    avg("delivery_days").alias("avg_delivery_days")
)

delivered_shipments = silver_df.filter(col("Status") == "Delivered")
delivered_shipments_count = delivered_shipments.count()

delayed_shipments = delivered_shipments.filter(col("delivery_days") > 3)

delayed_shipments_count = delayed_shipments.count()

delayed_shipments_percentage = round(
    (delayed_shipments_count / delivered_shipments_count) * 100, 2
)

print(f"delayed shipments % : {delayed_shipments_percentage}%")
df = spark.createDataFrame(
    [
        (delayed_shipments_percentage,),
    ],
    ["delayed_shipments_percentage"],
)
df.show()

top_customers = (
    silver_df.groupBy("CustomerName")
    .agg(sum("ShippingCostUSD").alias("total_spent"))
    .orderBy(desc("total_spent"))
)

top_customers.show()

routes_performance = (
    silver_df.filter(col("Status") == "Delivered")
    .groupBy(["OriginCity", "DestinationCity"])
    .agg(avg("delivery_days"))
)

routes_performance.show()
