from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip
from pyspark.sql.functions import (
    current_timestamp,
    input_file_name
)

builder = SparkSession.builder \
    .appName("MedallionLab") \
    .config(
        "spark.sql.extensions",
        "io.delta.sql.DeltaSparkSessionExtension"
    ) \
    .config(
        "spark.sql.catalog.spark_catalog",
        "org.apache.spark.sql.delta.catalog.DeltaCatalog"
    )

spark = configure_spark_with_delta_pip(
    builder
).getOrCreate()

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

# exercise 3
from pyspark.sql.functions import avg, sum, count, round

silver_df = spark.read \
    .format("delta") \
    .load(
        "../data/silver/shipments"
    )

gold_df = (
    silver_df
    .groupBy("Status")
    .agg(
        round(
            avg("delivery_days"),
            2
        ).alias(
            "avg_delivery_days"
        ),
        count("*").alias(
            "shipment_count"
        ),
        round(
            sum("ShippingCostUSD"),
            2
        ).alias(
            "total_revenue"
        )
    )
)

gold_df.show()

gold_df.write \
    .format("delta") \
    .mode("overwrite") \
    .save(
        "../data/gold/shipment_analytics"
    )