import time
from pyspark.sql import SparkSession
from ingestion import read_shipments
from transformations import transform_shipments
from optimization import write_optimized
from analytics import run_analytics


spark = SparkSession.builder \
    .appName("ShipmentPipeline") \
    .getOrCreate()

df = read_shipments(spark)

transformed_df = transform_shipments(df)

transformed_df.cache()
transformed_df.count()

write_optimized(
    transformed_df
)

print(
    "Optimized parquet written"
)

run_analytics(
    transformed_df
)

time.sleep(300)