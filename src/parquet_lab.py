from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder.appName("ParquetLab").getOrCreate()

# exercise 1
# csv_df = spark.read.csv("../data/raw/shipments.csv",
#                     header=True,
#                     inferSchema=True)

# csv_df.write.mode("overwrite").parquet("../data/processed/parquet_shipments")

# exercise 2
# parquet_df = spark.read.parquet("../data/processed/parquet_shipments")

# parquet_df.show()

# parquet_df.printSchema()

# exercise 3
# parquet_df.select("Status").explain(True)

# excercie 4
# csv_df.write.mode("overwrite").partitionBy("Status").parquet("../data/processed/partitioned_shipments")

# excercise 5
partitioned_df = spark.read.parquet("../data/processed/partitioned_shipments")

partitioned_df.filter(col("Status") == "Delivered").explain(True)