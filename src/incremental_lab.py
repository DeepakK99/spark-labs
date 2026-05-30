from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip
from delta.tables import DeltaTable

builder = (SparkSession.builder
         .appName("DeltaBasics")
         .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
         .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        )

spark = configure_spark_with_delta_pip(builder).getOrCreate()

print("Spark started successfully")

# exercise 1
# base_df = spark.createDataFrame(
#     [
#         (101, "In Transit"),
#         (102, "Delivered"),
#         (103, "Pending")
#     ],
#     ["shipment_id", "status"]
# )

# base_df.show()

# base_df.write \
#     .format("delta") \
#     .mode("overwrite") \
#     .save(
#         "../data/processed/delta_shipments_incremental"
#     )

# shipment_df = spark.read.format("delta").load("../data/processed/delta_shipments_incremental")

# shipment_df.show()

# updates_df = spark.createDataFrame(
#     [
#         (101, "Delivered"),
#         (999, "In Transit")
#     ],
#     ["shipment_id", "status"]
# )

# updates_df.show()

# updates_df.write \
#     .format("delta") \
#     .mode("append") \
#     .save(
#         "../data/processed/delta_shipments_incremental"
#     )

# spark.read \
#     .format("delta") \
#     .load(
#         "../data/processed/delta_shipments_incremental"
#     ) \
#     .show()

# exercise 2
# delta_table = DeltaTable.forPath(
#     spark,
#     "../data/processed/delta_shipments_incremental"
# )

# delta_table.alias("target") \
#     .merge(
#         updates_df.alias("source"),
#         "target.shipment_id = source.shipment_id"
#     ) \
#     .whenMatchedUpdateAll() \
#     .whenNotMatchedInsertAll() \
#     .execute()

# spark.read \
#     .format("delta") \
#     .load(
#         "../data/processed/delta_shipments_incremental"
#     ) \
#     .orderBy("shipment_id") \
#     .show()

# exercise 3
# cdc_df = spark.createDataFrame(
#     [
#         (101, "Delivered"),
#         (102, "Cancelled")
#     ],
#     ["shipment_id", "status"]
# )

# cdc_df.show()

# use - .whenMatchedUpdate(
#     set={
#         "status": "source.status"
#     }
# )