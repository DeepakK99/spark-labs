import time
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("ParitionLab").getOrCreate()

# df = spark.read.csv("../data/raw/shipments.csv",
#                     header=True,
#                     inferSchema=True)

# excercise 1
# df2 = df.repartition(10)

# print(
#     "After repartition:",
#     df2.rdd.getNumPartitions()
# )

# df3 = df2.coalesce(2)

# print(
#     "After coalesce:",
#     df3.rdd.getNumPartitions()
# )

# excercise 2
# result = (
#     df.groupBy("Status")
#       .count()
# )

# result.show()

# excercise 3
data = (
    [("Delayed",)]*900 +
    [("Delivered",)]*50 +
    [("Returned",)]*50
)

df = spark.createDataFrame(
    data,
    ["status"]
)

df = df.repartition(4)


# data skewness observation
df.groupBy(
    "status"
).count().show()

print(df.rdd.getNumPartitions())
time.sleep(300)