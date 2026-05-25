from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import to_date
from delta import configure_spark_with_delta_pip
from datetime import date

builder = (SparkSession.builder
         .appName("DeltaBasics")
         .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
         .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        )

spark = configure_spark_with_delta_pip(builder).getOrCreate()

print("Spark started successfully")

# exercise 1
# df = spark.read.csv("../data/raw/shipments.csv",
#                     header=True,
#                     inferSchema=True)

# df.write.format("delta").mode("overwrite").save("../data/processed/delta_shipments")

# exercise 2
# delta_df = spark.read.format("delta").load("../data/processed/delta_shipments")

# delta_df.show(5)

# exercise 3 (day 2)
# existing_df = spark.read \
#     .format("delta") \
#     .load("../data/processed/delta_shipments")

# new_data = spark.createDataFrame(
#     [
#         Row(
#             ShipmentID="998",
#             OrderDate=date(2026,5,25),
#             ShipDate=date(2026,5,25),
#             CustomerName="Viral",
#             OriginCity="Bangalore",
#             DestinationCity="Mumbai",
#             Carrier="DHL",
#             TrackingNumber="TR998",
#             WeightKg=5.0,
#             ShippingCostUSD=500.0,
#             Status="Delivered",
#             DeliveryDate=date(2026,5,28)
#         )
#     ]
# )

# new_data.show()

# new_data.write \
#     .format("delta") \
#     .mode("append") \
#     .save(
#         "../data/processed/delta_shipments"
#     )

# exercie 4 (day 2)
# from delta.tables import DeltaTable

# deltaTable = DeltaTable.forPath(spark, "../data/processed/delta_shipments")

# deltaTable.history().show(
#     truncate=False
# )

# exercise 5 (day 2)
old_table = spark.read.format("delta").option("versionAsOf", 0).load("../data/processed/delta_shipments")

print(f"Old table record count: {old_table.count()}")

new_table = spark.read.format("delta").load("../data/processed/delta_shipments")
print(f"New table record count: {new_table.count()}")

spark.stop()