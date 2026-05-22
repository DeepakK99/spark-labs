from pyspark.sql import SparkSession
from pyspark.sql.functions import col, broadcast
import time

spark = SparkSession.builder \
    .appName("CacheLab") \
    .getOrCreate()

df = spark.read.csv(
    "../data/raw/shipments.csv",
    header=True,
    inferSchema=True
)

# exercise 1
# processed = (
#     df.filter(
#         col("ShippingCostUSD") > 50
#     )
#     .groupBy("Status")
#     .count()
# )

# print("WITHOUT CACHE")

# start = time.time()
# processed.show()
# print(
#     "Time1:",
#     round(time.time()-start,3)
# )

# start = time.time()
# processed.show()
# print(
#     "Time2:",
#     round(time.time()-start,3)
# )

# processed.cache()

# print("\nWITH CACHE")

# start = time.time()
# processed.show()
# print(
#     "Time3:",
#     round(time.time()-start,3)
# )

# start = time.time()
# processed.show()
# print(
#     "Time4:",
#     round(time.time()-start,3)
# )

# exercise 2
# result = (
#     df.groupBy(
#         "Status"
#     )
#     .count()
# )

# result.explain(True)

# exercise 3
# customer_df = spark.createDataFrame(
#     [
#         (1,"Acme Retail"),
#         (2,"GreenLeaf Stores"),
#         (3,"Urban Cart")
#     ],
#     ["customer_id","customerName"]
# )

# joined = df.join(
#     broadcast(customer_df),
#     "customerName"
# )

# joined.explain(True)

# exercise 4
bad_pipeline = (
    df.distinct()
      .repartition(50)
      .groupBy("Status")
      .count()
      .orderBy("count")
)

bad_pipeline.explain(True)