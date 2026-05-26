from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip

builder = (SparkSession.builder
         .appName("DeltaBasics")
         .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
         .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        )

spark = configure_spark_with_delta_pip(builder).getOrCreate()

print("Spark started successfully")

delta_df = spark.read \
    .format("delta") \
    .load(
        "../data/processed/delta_shipments"
    )

delta_df.printSchema()

# exercise 1
# new_df = spark.createDataFrame(
#     [
#         (
#             2001,
#             "Rajiv",
#             "Bangalore",
#             "Mumbai",
#             "2026-05-25",
#             "2026-05-28",
#             "Delivered",
#             700,
#             "HIGH"
#         )
#     ],
#     [
#         "shipment_id",
#         "customer_name",
#         "origin",
#         "destination",
#         "shipment_date",
#         "delivery_date",
#         "status",
#         "cost",
#         "priority"
#     ]
# )

# new_df.printSchema()

# new_df = (
#     new_df
#     .withColumnRenamed(
#         "shipment_id",
#         "ShipmentID"
#     )
#     .withColumnRenamed(
#         "customer_name",
#         "CustomerName"
#     )
#     .withColumnRenamed(
#         "origin",
#         "OriginCity"
#     )
#     .withColumnRenamed(
#         "destination",
#         "DestinationCity"
#     )
#     .withColumnRenamed(
#         "shipment_date",
#         "ShipDate"
#     )
#     .withColumnRenamed(
#         "delivery_date",
#         "DeliveryDate"
#     )
#     .withColumnRenamed(
#         "cost",
#         "ShippingCostUSD"
#     )
#     .withColumnRenamed(
#         "status",
#         "Status"
#     )
#       .withColumnRenamed(
#         "priority",
#         "Priority"
#     )
# )

# from pyspark.sql.functions import to_date, col

# new_df = (
#     new_df
#     .withColumn(
#         "ShipDate",
#         to_date(col("ShipDate"))
#     )
#     .withColumn(
#         "DeliveryDate",
#         to_date(col("DeliveryDate"))
#     )
#     .withColumn("ShipmentID", col("ShipmentID").cast("string"))
#     .withColumn("ShippingCostUSD", col("ShippingCostUSD").cast("double"))
# )


# new_df.write \
#     .format("delta") \
#       .option(
#             "mergeSchema",
#             "true"
#        ) \
#     .mode("append") \
#     .save(
#         "../data/processed/delta_shipments"
#     )

# exercise 2
delta_df.select("ShipmentID", "Priority").show(1000, truncate=False)