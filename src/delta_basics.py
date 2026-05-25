from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip

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
delta_df = spark.read.format("delta").load("../data/processed/delta_shipments")

delta_df.show(5)

spark.stop()