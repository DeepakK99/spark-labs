from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, date_diff

spark = SparkSession.builder.appName("ShipmentProcessing").getOrCreate()

df = spark.read.csv("../data/raw/shipments.csv", 
                    header=True, 
                    inferSchema=True)

# df.show()

# df.printSchema()

# df.describe().show()

# build logical plan

df = df.withColumn("DeliveryDays", date_diff(col("DeliveryDate"), col("ShipDate")))

pipeline_df = df.withColumn("WeightClass", when(col("WeightKg") <= 10, "light")
                            .when(col("WeightKg") <= 20, "medium")
                            .otherwise("heavy"))

result = pipeline_df.groupBy("WeightClass").avg("DeliveryDays")

print("Plan craeted")

print("triggering execution")

# trigger plan

result.show()

print("Complete")

# spark = query optimizer + distributed planner

