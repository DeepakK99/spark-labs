from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("FirstSparkApp").getOrCreate()

print("Spark session created!")

print("Reading shipments csv data..")

df = spark.read.csv("../data/raw/shipments.csv", header=True, inferSchema=True)

df.filter(df.Status == "Pending").show()

df.groupBy("status").count().show()

print(df.rdd.getNumPartitions())

df.explain()
